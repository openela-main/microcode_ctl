#! /usr/bin/python
# SPDX-License-Identifier: CC0-1.0

import argparse
import errno
import fnmatch
import io
import itertools
import os
import re
import shutil
import struct
import sys
import tarfile
import tempfile
from subprocess import PIPE, Popen, STDOUT

# Python 3 shims
try:
    from functools import reduce
except:
    pass
try:
    from itertools import zip_longest as izip_longest
except:
    from itertools import izip_longest

# revs:
# [ { "path", "cpuid", "pf", "rev", "date" } ]

# artifacts:
#  * content summary (per-file)
#   * overlay summary (per-fms/pf)
#  * changelog (per-file?)
#  * discrepancies (per-fms/pf)

log_level = 0
print_date = False
file_glob = ["*??-??-??", "*microcode*.dat"]


def log_status(msg, level=0):
    global log_level

    if log_level >= level:
        sys.stderr.write(msg + "\n")


def log_info(msg, level=2):
    global log_level

    if log_level >= level:
        sys.stderr.write("INFO: " + msg + "\n")


def log_warn(msg, level=1):
    global log_level

    if log_level >= level:
        sys.stderr.write("WARNING: " + msg + "\n")


def log_error(msg, level=-1):
    global log_level

    if log_level >= level:
        sys.stderr.write("ERROR: " + msg + "\n")


def remove_prefix(text, prefix):
    if isinstance(prefix, str):
        prefix = [prefix, ]

    for p in prefix:
        pfx = p if p.endswith(os.sep) else p + os.sep
        if text.startswith(pfx):
            return text[len(pfx):]

    return text


def file_walk(args, yield_dirs=False):
    for content in args:
        if os.path.isdir(content):
            if yield_dirs:
                yield ("", content)
            for root, dirs, files in os.walk(content):
                if yield_dirs:
                    for f in dirs:
                        p = os.path.join(root, f)
                        yield (remove_prefix(p, content), p)
                for f in files:
                    p = os.path.join(root, f)
                    yield (remove_prefix(p, content), p)
        elif os.path.exists(content):
            yield ("", content)
        else:
            raise IOError(errno.ENOENT, os.strerror(errno.ENOENT), content)


def cpuid_fname(c):
    # Note that the Extended Family is summed up with the Family,
    # while the Extended Model is concatenated with the Model.
    return "%02x-%02x-%02x" % (
        ((c >> 20) & 0xff) + ((c >> 8) & 0xf),
        ((c >> 12) & 0xf0) + ((c >> 4) & 0xf),
        c & 0xf)


def read_revs_dir(path, args, src=None, ret=None):
    if ret is None:
        ret = []

    ucode_re = re.compile('[0-9a-f]{2}-[0-9a-f]{2}-0[0-9a-f]$')
    ucode_dat_re = re.compile('microcode.*\.dat$')

    for rp, ap in file_walk([path, ]):
        rp_fname = os.path.basename(rp)
        if not ucode_re.match(rp_fname) and not ucode_dat_re.match(rp_fname):
            continue

        # Text-based format
        data = None
        if ucode_dat_re.match(rp_fname):
            data = io.BytesIO()
            with open(ap, "r") as f:
                for line in f:
                    if line.startswith("/"):
                        continue
                    vals = line.split(",")
                    for val in vals:
                        val = val.strip()
                        if not val:
                            continue
                        data.write(struct.pack("<I", int(val, 16)))
            sz = data.seek(0, os.SEEK_CUR)
            data.seek(0, os.SEEK_SET)
        else:
            sz = os.stat(ap).st_size

        try:
            with data or open(ap, "rb") as f:
                log_info("Processing %s" % ap)
                offs = 0
                while offs < sz:
                    f.seek(offs, os.SEEK_SET)
                    hdr = struct.unpack("IiIIIIIIIIII", f.read(48))
                    ret.append({"path": rp, "src": src or path,
                                "cpuid": hdr[3], "pf": hdr[6], "rev": hdr[1],
                                "date": hdr[2], "offs": offs, "cksum": hdr[4],
                                "data_size": hdr[7], "total_size": hdr[8]})

                    if hdr[8] and hdr[8] - hdr[7] > 48:
                        f.seek(hdr[7], os.SEEK_CUR)
                        ext_tbl = struct.unpack("IIIII", f.read(20))
                        log_status("Found %u extended signatures for %s:%#x" %
                                   (ext_tbl[0], rp, offs), level=1)

                        cur_offs = offs + hdr[7] + 48 + 20
                        ext_sig_cnt = 0
                        while cur_offs < offs + hdr[8] \
                                and ext_sig_cnt <= ext_tbl[0]:
                            ext_sig = struct.unpack("III", f.read(12))
                            ignore = args.ignore_ext_dups and \
                                (ext_sig[0] == hdr[3])
                            if not ignore:
                                ret.append({"path": rp, "src": src or path,
                                            "cpuid": ext_sig[0],
                                            "pf": ext_sig[1],
                                            "rev": hdr[1], "date": hdr[2],
                                            "offs": offs, "ext_offs": cur_offs,
                                            "cksum": hdr[4],
                                            "ext_cksum": ext_sig[2],
                                            "data_size": hdr[7],
                                            "total_size": hdr[8]})
                            log_status(("Got ext sig %#x/%#x for " +
                                        "%s:%#x:%#x/%#x%s") %
                                       (ext_sig[0], ext_sig[1],
                                        rp, offs, hdr[3], hdr[6],
                                        " (ignored)" if ignore else ""),
                                       level=2)

                            cur_offs += 12
                            ext_sig_cnt += 1

                    offs += hdr[8] or 2048
        except Exception as e:
            log_error("a problem occurred while processing %s: %s" % (ap, e),
                      level=1)

    return ret


def read_revs_rpm(path, args, ret=None):
    if ret is None:
        ret = []

    dir_tmp = tempfile.mkdtemp()

    log_status("Trying to extract files from RPM \"%s\"..." % path,
               level=1)

    rpm2cpio = Popen(args=["rpm2cpio", path], stdout=PIPE, stderr=PIPE,
                     close_fds=True)
    cpio = Popen(args=["cpio", "-idmv"] + file_glob,
                 cwd=dir_tmp, stdin=rpm2cpio.stdout,
                 stdout=PIPE, stderr=STDOUT)
    out, cpio_stderr = cpio.communicate()
    rpm2cpio_out, rpm2cpio_err = rpm2cpio.communicate()

    rpm2cpio_ret = rpm2cpio.returncode
    cpio_ret = cpio.returncode

    log_info("rpm2cpio exit code: %d, cpio exit code: %d" %
             (rpm2cpio_ret, cpio_ret))
    if rpm2cpio_err:
        log_info("rpm2cpio stderr:\n%s" % rpm2cpio_err, level=3)
    if out:
        log_info("cpio output:\n%s" % out, level=3)
    if cpio_stderr:
        log_info("cpio stderr:\n%s" % cpio_stderr, level=3)

    if rpm2cpio_ret == 0 and cpio_ret == 0:
        ret = read_revs_dir(dir_tmp, args, path)

    shutil.rmtree(dir_tmp)

    return ret


def read_revs_tar(path, args, ret=None):
    if ret is None:
        ret = []

    dir_tmp = tempfile.mkdtemp()

    log_status("Trying to extract files from tarball \"%s\"..." % path,
               level=1)

    try:
        with tarfile.open(path, "r:*") as tar:
            for ti in tar:
                if any(fnmatch.fnmatchcase(ti.name, p) for p in file_glob):
                    d = os.path.normpath(os.path.join("/",
                                         os.path.dirname(ti.name)))
                    # For now, strip exactl one level
                    d = os.path.join(*(d.split(os.path.sep)[2:]))
                    n = os.path.join(d, os.path.basename(ti.name))

                    if not os.path.exists(d):
                        os.makedirs(d)
                    t = tar.extractfile(ti)
                    with open(n, "wb") as f:
                        shutil.copyfileobj(t, f)
                    t.close()

        ret = read_revs_dir(dir_tmp, args, path)
    except Exception as err:
        log_error("Error while reading \"%s\" as a tarball: \"%s\"" %
                  (path, str(err)))

    shutil.rmtree(dir_tmp)

    return ret


def read_revs(path, args, ret=None):
    if ret is None:
        ret = []
    if os.path.isdir(path):
        return read_revs_dir(path, args, ret)
    elif tarfile.is_tarfile(path):
        return read_revs_tar(path, args, ret)
    else:
        return read_revs_rpm(path, args, ret)


def gen_mc_map(mc_data, merge=False, merge_path=False):
    """
    Converts an array of microcode file information to a map with path/sig/pf
    as a key.

    merge: whether to leave only the newest mc variant in the map or leave all
           possible variants.
    """
    res = dict()

    for mc in mc_data:
        key = (None if merge_path else mc["path"], mc["cpuid"], mc["pf"])

        if key not in res:
            res[key] = dict()

        cpuid = mc["cpuid"]
        cur_pf = mc["pf"]
        pid = 1
        while cur_pf > 0:
            if cur_pf & 1 and not (merge and pid in res[key]
                                   and res[key][pid]["rev"][0] >= mc["rev"]):
                if pid not in res[cpuid] or merge:
                    res[cpuid][pid] = []
                res[cpuid][pid].append(mc)

            cur_pf = cur_pf / 2
            pid = pid * 2

    return res


def gen_fn_map(mc_data, merge=False, merge_path=False):
    res = dict()

    for mc in mc_data:
        key = (None if merge_path else mc["path"], mc["cpuid"], mc["pf"])
        if key in res:
            log_warn("Duplicate path/cpuid/pf: %s/%#x/%#x" % key)
        else:
            res[key] = []
        if merge and len(res[key]):
            if mc["rev"] > res[key][0]["rev"]:
                res[key][0] = mc
        else:
            res[key].append(mc)

    return res


def revcmp(a, b):
    return b["rev"] - a["rev"]


class ChangeLogEntry:
    ADDED = 0
    REMOVED = 1
    UPDATED = 2
    DOWNGRADED = 3
    OTHER = 4


def mc_stripped_path(mc):
    paths = ("usr/share/microcode_ctl/ucode_with_caveats/intel",
             "usr/share/microcode_ctl/ucode_with_caveats",
             "usr/share/microcode_ctl",
             "lib/firmware",
             "etc/firmware",
             )

    return remove_prefix(mc["path"], paths)


class mcnm:
    MCNM_ABBREV = 0
    MCNM_FAMILIES = 1
    MCNM_MODELS = 2
    MCNM_FAMILIES_MODELS = 3
    MCNM_CODENAME = 4


def get_mc_cnames(mc, cmap, mode=mcnm.MCNM_ABBREV, stringify=True,
                  segment=False):
    if not isinstance(mc, dict):
        mc = mc_from_mc_key(mc)
    sig = mc["cpuid"]
    pf = mc["pf"]
    res = []

    if not cmap:
        return None
    if sig not in cmap:
        log_info("No codename information for sig %#x" % sig)
        return None

    cnames = cmap[sig]

    if mode in (mcnm.MCNM_FAMILIES, mcnm.MCNM_MODELS,
                mcnm.MCNM_FAMILIES_MODELS):
        for c in cnames:
            if not (pf & c["pf_mask"]):
                continue
            for m, f in ((mcnm.MCNM_FAMILIES, "families"),
                         (mcnm.MCNM_MODELS, "models")):
                if m & mode == 0:
                    continue
                if f not in c or not c[f]:
                    log_info("No %s for sig %#x in %r" % (f, sig, c))
                    continue

                res.append(c[f])

        return ", ".join(res) or None

    steppings = dict()
    suffices = dict()
    for c in cnames:
        if pf and not (pf & c["pf_mask"]):
            continue

        if mode == mcnm.MCNM_ABBREV and "abbrev" in c and c["abbrev"]:
            cname = c["abbrev"]
        else:
            cname = c["codename"]

        if segment:
            cname = c["segment"] + " " + cname

        if cname not in suffices:
            suffices[cname] = set()
        if "variant" in c and c["variant"]:
            suffices[cname] |= set(c["variant"])

        if cname not in steppings:
            steppings[cname] = set()
        if c["stepping"]:
            steppings[cname] |= set(c["stepping"])

    for cname in sorted(steppings.keys()):
        cname_res = [cname]
        if len(suffices[cname]):
            cname_res[0] += "-" + "/".join(sorted(suffices[cname]))
        if len(steppings[cname]):
            cname_res.append("/".join(sorted(steppings[cname])))
        res.append(" ".join(cname_res) if stringify else cname_res)

    return (", ".join(res) or None) if stringify else res


def mc_from_mc_key(k):
    return dict(zip(("path", "cpuid", "pf"), k))


def mc_path(mc, pf_sfx=True, midword=None, cmap=None, cname_segment=False):
    if not isinstance(mc, dict):
        mc = mc_from_mc_key(mc)
    path = mc_stripped_path(mc) if mc["path"] is not None else None
    cpuid_fn = cpuid_fname(mc["cpuid"])
    fname = os.path.basename(mc["path"] or cpuid_fn)
    midword = "" if midword is None else " " + midword
    cname = get_mc_cnames(mc, cmap, segment=cname_segment)
    cname_str = " (" + cname + ")" if cname else ""

    if pf_sfx:
        sfx = "/0x%02x" % mc["pf"]
    else:
        sfx = ""

    if not path or path == os.path.join("intel-ucode", cpuid_fn):
        return "%s%s%s%s" % (fname, sfx, cname_str, midword)
    else:
        return "%s%s%s%s (in %s)" % (cpuid_fn, sfx, cname_str, midword, path)


def gen_changelog_file(old, new):
    pass


def mc_cmp(old_mc, new_mc):
    res = []

    old_mc_revs = [x["rev"] for x in old_mc]
    new_mc_revs = [x["rev"] for x in new_mc]
    common = set(old_mc_revs) & set(new_mc_revs)
    old_rev_list = [x for x in sorted(old_mc_revs) if x not in common]
    new_rev_list = [x for x in sorted(new_mc_revs) if x not in common]

    if len(old_rev_list) != 1 or len(new_rev_list) != 1:
        for i in new_mc:
            if i["rev"] in new_rev_list:
                res.append((ChangeLogEntry.ADDED, None, i))
        for i in old_mc:
            if i["rev"] in old_rev_list:
                res.append((ChangeLogEntry.REMOVED, i, None))
    else:
        for old in old_mc:
            if old["rev"] == old_rev_list[0]:
                break
        for new in new_mc:
            if new["rev"] == new_rev_list[0]:
                break
        if new["rev"] > old["rev"]:
            res.append((ChangeLogEntry.UPDATED, old, new))
        elif new["rev"] < old["rev"]:
            res.append((ChangeLogEntry.DOWNGRADED, old, new))

    return res


def gen_changelog(old, new):
    res = []

    old_map = gen_fn_map(old)
    new_map = gen_fn_map(new)

    old_files = set(old_map.keys())
    new_files = set(new_map.keys())

    both = old_files & new_files
    added = new_files - old_files
    removed = old_files - new_files

    for f in sorted(added):
        p = mc_path(new_map[f][0])
        for old_f in sorted(removed):
            old_p = mc_path(old_map[old_f][0])
            if p == old_p and f[1] == old_f[1] and f[2] == old_f[2]:
                log_info("Matched %s (%s and %s)" %
                         (p, old_map[old_f][0]["path"], new_map[f][0]["path"]))
                added.remove(f)
                removed.remove(old_f)

                res += mc_cmp(old_map[old_f], new_map[f])

    for f in sorted(added):
        for i in new_map[f]:
            res.append((ChangeLogEntry.ADDED, None, i))
    for f in sorted(removed):
        for i in old_map[f]:
            res.append((ChangeLogEntry.REMOVED, i, None))
    for f in sorted(both):
        res += mc_cmp(old_map[f], new_map[f])

    return res


def mc_date(mc):
    if isinstance(mc, dict):
        mc = mc["date"]
    return "%04x-%02x-%02x" % (mc & 0xffff, mc >> 24, (mc >> 16) & 0xff)


def mc_rev(mc, date=None):
    '''
    While revision is signed for comparison purposes, historically
    it is printed as unsigned,  Oh well.
    '''
    global print_date

    if mc["rev"] < 0:
        rev = 2**32 + mc["rev"]
    else:
        rev = mc["rev"]

    if date if date is not None else print_date:
        return "%#x (%s)" % (rev, mc_date(mc))
    else:
        return "%#x" % rev


def print_changelog_rpm(clog, cmap, args):
    for e, old, new in clog:
        mc_str = mc_path(new if e == ChangeLogEntry.ADDED else old,
                         midword="microcode",
                         cmap=cmap, cname_segment=args.segment)

        if e == ChangeLogEntry.ADDED:
            print("Addition of %s at revision %s" % (mc_str, mc_rev(new)))
        elif e == ChangeLogEntry.REMOVED:
            print("Removal of %s at revision %s" % (mc_str, mc_rev(old)))
        elif e == ChangeLogEntry.UPDATED:
            print("Update of %s from revision %s up to %s" %
                  (mc_str, mc_rev(old), mc_rev(new)))
        elif e == ChangeLogEntry.DOWNGRADED:
                print("Downgrade of %s from revision %s down to %s" %
                      (mc_str, mc_rev(old), mc_rev(new)))
        elif e == ChangeLogEntry.OTHER:
            print("Other change in %s:" % old["path"])
            print("  old: %#x/%#x: rev %s (offs %#x)" %
                  (old["cpuid"], old["pf"], mc_rev(old), old["offs"]))
            print("  new: %#x/%#x: rev %s (offs %#x)" %
                  (new["cpuid"], new["pf"], mc_rev(new), new["offs"]))


def print_changelog_intel(clog, cmap, args):
    def clog_sort_key(x):
        res = str(x[0])

        if x[0] != ChangeLogEntry.ADDED:
            res += "%08x%02x" % (x[1]["cpuid"], x[1]["pf"])
        else:
            res += "0" * 10

        if x[0] != ChangeLogEntry.REMOVED:
            res += "%08x%02x" % (x[2]["cpuid"], x[2]["pf"])
        else:
            res += "0" * 10

        return res

    sorted_clog = sorted(clog, key=clog_sort_key)
    sections = (("New Platforms",     (ChangeLogEntry.ADDED, )),
                ("Updated Platforms", (ChangeLogEntry.UPDATED,
                                       ChangeLogEntry.DOWNGRADED)),
                ("Removed Platforms", (ChangeLogEntry.REMOVED, )))

    def print_line(e, old, new, types):
        if e not in types:
            return

        if not print_line.hdr:
            print("""
| Processor      | Stepping | F-M-S/PI    | Old Ver  | New Ver  | Products
|:---------------|:---------|:------------|:---------|:---------|:---------""")
            print_line.hdr = True

        mc = new if e == ChangeLogEntry.ADDED else old
        cnames = get_mc_cnames(mc, cmap, stringify=False,
                               segment=args.segment) or (("???", ""), )
        for cn in cnames:
            cname = cn[0]
            stepping = cn[1] if len(cn) > 1 else ""
        print("| %-14s | %-8s | %8s/%02x | %8s | %8s | %s" %
              (cname,
               stepping,
               cpuid_fname(mc["cpuid"]), mc["pf"],
               ("%08x" % old["rev"]) if e != ChangeLogEntry.ADDED else "",
               ("%08x" % new["rev"]) if e != ChangeLogEntry.REMOVED else "",
               get_mc_cnames(mc, cmap, mode=mcnm.MCNM_FAMILIES,
                             segment=args.segment) or ""))

    for h, types in sections:
        print("\n### %s" % h)
        print_line.hdr = False
        for e, old, new in sorted_clog:
            print_line(e, old, new, types)


def print_changelog(clog, cmap, args):
    if args.format == "rpm":
        print_changelog_rpm(clog, cmap, args)
    elif args.format == "intel":
        print_changelog_intel(clog, cmap, args)
    else:
        log_error(("unknown changelog format: \"%s\". " +
                   "Supported formats are: rpm, intel.") % args.format)


class TableStyles:
    TS_CSV = 0
    TS_FANCY = 1


def print_line(line, column_sz):
    print(" | ".join([str(x).ljust(column_sz[i])
                      for i, x in zip(itertools.count(),
                                      itertools.chain(line,
                                      [""] * (len(column_sz) -
                                              len(line))))]).rstrip())


def print_table(items, header=[], style=TableStyles.TS_CSV):
    if style == TableStyles.TS_CSV:
        for i in items:
            print(";".join(i))
    elif style == TableStyles.TS_FANCY:
        column_sz = list(reduce(lambda x, y:
                                map(max, izip_longest(x, y, fillvalue=0)),
                                [[len(x) for x in i]
                                 for i in itertools.chain(header, items)]))
        for i in header:
            print_line(i, column_sz)
        if header:
            print("-+-".join(["-" * x for x in column_sz]))
        for i in items:
            print_line(i, column_sz)


def print_summary(revs, cmap, args):
    m = gen_fn_map(revs)
    cnames_mode = mcnm.MCNM_ABBREV if args.abbrev else mcnm.MCNM_CODENAME

    header = []
    if args.header:
        header.append(["Path", "Offset", "Ext. Offset", "Data Size",
                       "Total Size", "CPUID", "Platform ID Mask", "Revision",
                       "Date", "Checksum", "Codenames"] +
                      (["Models"] if args.models else []))
    tbl = []
    for k in sorted(m.keys()):
        for mc in m[k]:
            tbl.append([mc_stripped_path(mc),
                        "0x%x" % mc["offs"],
                        "0x%x" % mc["ext_offs"] if "ext_offs" in mc else "-",
                        "0x%05x" % mc["data_size"],
                        "0x%05x" % mc["total_size"],
                        "0x%05x" % mc["cpuid"],
                        "0x%02x" % mc["pf"],
                        mc_rev(mc, date=False),
                        mc_date(mc),
                        "0x%08x" % (mc["ext_cksum"]
                                    if "ext_cksum" in mc else mc["cksum"]),
                        get_mc_cnames(mc, cmap, cnames_mode,
                                      segment=args.segment) or ""] +
                       ([get_mc_cnames(mc, cmap,
                                       mcnm.MCNM_FAMILIES_MODELS,
                                       segment=args.segment)]
                        if args.models else []))

    print_table(tbl, header, style=TableStyles.TS_FANCY)


def read_codenames_file(path):
    '''
    Supports two formats: new and old
     * old: tab-separated. Field order:
       Segment, (unused), Codename, (dash-separated) Stepping,
       Platform ID mask, CPUID, (unused) Update link, (unused) Specs link
     * new: semicolon-separated; support comments.  Distinguished
       by the first line that starts with octothorp.  Field order:
       Segment, Unused, Codename, Stepping, Platform ID mask, CPUID,
       Abbreviation, Variant(s), Families, Models
    '''
    old_fields = ["segment", "_", "codename", "stepping", "pf_mask", "sig",
                  "_update", "_specs"]
    new_fields = ["segment", "_", "codename", "stepping", "pf_mask", "sig",
                  "abbrev", "variant", "families", "models"]
    new_fmt = False
    field_names = old_fields

    res = dict()

    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue
                if line[0] == '#':
                    new_fmt = True
                    field_names = new_fields
                    continue

                fields = line.split(";" if new_fmt else "\t",
                                    1 + len(field_names))
                fields = dict(zip(field_names, fields))
                if "sig" not in fields:
                    log_warn("Skipping %r (from \"%s\")" % (fields, line))
                    continue

                sig = fields["sig"] = int(fields["sig"], 16)
                fields["pf_mask"] = int(fields["pf_mask"], 16)
                fields["stepping"] = fields["stepping"].split(",")
                if "variant" in fields:
                    if fields["variant"]:
                        fields["variant"] = fields["variant"].split(",")
                    else:
                        fields["variant"] = []

                if sig not in res:
                    res[sig] = list()
                res[sig].append(fields)
    except Exception as e:
        log_error("a problem occurred while reading code names: %s" % e)

    return res


def print_discrepancies(rev_map, deps, cmap, args):
    """
    rev_map: dict "name": revs
    deps: list of tuples (name, parent/None)
    """
    sigs = set()

    for p, r in rev_map.items():
        sigs |= set(r.keys())

    if args.header:
        header1 = ["sig"]
        if args.print_vs:
            header2 = [""]
        for p, n, d in deps:
            header1.append(n)
            if args.print_vs:
                add = ""
                if d:
                    for pd, nd, dd in deps:
                        if pd == d:
                            add = "(vs. %s)" % nd
                            break
                header2.append(add)
        if args.models:
            header1.append("Model names")
            if args.print_vs:
                header2.append("")
    header = [header1] + ([header2] if args.print_vs else [])

    tbl = []
    for s in sorted(sigs):
        out = [mc_path(s)]
        print_out = not args.print_filter
        print_date = args.min_date is None

        for p, n, d in deps:
            cur = dict([(x["rev"], x) for x in rev_map[p][s]]) \
                  if s in rev_map[p] else []
            v = "/".join([mc_rev(y) for x, y in sorted(cur.items())]) \
                if cur else "-"
            if d is not None:
                prev = [x["rev"] for x in rev_map[d][s]] if s in rev_map[d] \
                        else []
                if [x for x in cur if x not in prev]:
                    v += " (*)"
                    print_out = True
            if args.min_date is not None and s in rev_map[p]:
                for x in rev_map[p][s]:
                    print_date |= mc_date(x) > args.min_date
            out.append(v)

        if print_out and print_date:
            if args.models:
                out.append(get_mc_cnames(s, cmap, segment=args.segment) or "")
            tbl.append(out)

    print_table(tbl, header, style=TableStyles.TS_FANCY)


def cmd_summary(args):
    revs = []
    for p in args.filelist:
        revs = read_revs(p, args, ret=revs)

    codenames_map = read_codenames_file(args.codenames)

    print_summary(revs, codenames_map, args)

    return 0


def cmd_changelog(args):
    codenames_map = read_codenames_file(args.codenames)
    base_path = args.filelist[0]
    upd_path = args.filelist[1]

    base = read_revs(base_path, args)
    upd = read_revs(upd_path, args)

    print_changelog(gen_changelog(base, upd), codenames_map, args)

    return 0


def cmd_discrepancies(args):
    """
    filenames:
     * "<" prefix (possibly multiple times) to refer to a previous entry
       to compare against
     * "[name]" prefix is a name reference
    """
    codenames_map = read_codenames_file(args.codenames)
    rev_map = dict()
    deps = list()
    cur = -1

    for path in args.filelist:
        orig_path = path
        name = None
        cur += 1
        dep = None
        while True:
            if path[0] == '<':
                path = path[1:]
                dep = cur - 1 if dep is None else dep - 1
            elif path[0] == '[' and path.find(']') > 0:
                pos = path.find(']')
                name = path[1:pos]
                path = path[pos + 1:]
            else:
                break
        if name is None:
            name = path
        if dep is not None and dep < 0:
            log_error("Incorrect dep reference for '%s' (points to index %d)" %
                      (orig_path, dep))
            return 1
        deps.append((path, name, deps[dep][0] if dep is not None else None))
        rev_map[path] = gen_fn_map(read_revs(path, args), merge=args.merge,
                                   merge_path=True)

    print_discrepancies(rev_map, deps, codenames_map, args)

    return 0


def parse_cli():
    root_parser = argparse.ArgumentParser(prog="gen_updates",
                                          description="Intel CPU Microcode " +
                                          "parser")
    root_parser.add_argument("-C", "--codenames", default='codenames',
                             help="Code names file")
    root_parser.add_argument("-v", "--verbose", action="count", default=0,
                             help="Increase output verbosity")
    root_parser.add_argument("-E", "--no-ignore-ext-duplicates",
                             action="store_const", dest="ignore_ext_dups",
                             default=False, const=False,
                             help="Do not ignore duplicates of the main " +
                                  "signature in the extended signature header")
    root_parser.add_argument("-e", "--ignore-ext-duplicates",
                             action="store_const", dest="ignore_ext_dups",
                             const=True,
                             help="Ignore duplicates of the main signature " +
                                   "in the extended signature header")
    root_parser.add_argument("-t", "--print-segment", action="store_const",
                             dest="segment", const=True,
                             help="Print model segment")
    root_parser.add_argument("-T", "--no-print-segment", action="store_const",
                             dest="segment", const=False, default=False,
                             help="Do not print model segment")

    cmdparsers = root_parser.add_subparsers(title="Commands",
                                            help="main gen_updates commands")

    parser_s = cmdparsers.add_parser("summary",
                                     help="Generate microcode summary")
    parser_s.add_argument("-a", "--abbreviate", action="store_const",
                          dest="abbrev", const=True, default=True,
                          help="Abbreviate code names")
    parser_s.add_argument("-A", "--no-abbreviate", action="store_const",
                          dest="abbrev", const=False,
                          help="Do not abbreviate code names")
    parser_s.add_argument("-m", "--print-models", action="store_const",
                          dest="models", const=True, default=False,
                          help="Print models")
    parser_s.add_argument("-M", "--no-print-models",
                          action="store_const", dest="models",
                          const=False, help="Do not print models")
    parser_s.add_argument("-H", "--no-print-header",
                          action="store_const", dest="header",
                          const=False, default=True,
                          help="Do not print hader")
    parser_s.add_argument("filelist", nargs="*", default=[],
                          help="List or RPMs/directories to process")
    parser_s.set_defaults(func=cmd_summary)

    parser_c = cmdparsers.add_parser("changelog",
                                     help="Generate changelog")
    parser_c.add_argument("-F", "--format", choices=["rpm", "intel"],
                          default="rpm", help="Changelog format")
    parser_c.add_argument("filelist", nargs=2,
                          help="RPMs/directories to compare")
    parser_c.set_defaults(func=cmd_changelog)

    parser_d = cmdparsers.add_parser("discrepancies",
                                     help="Generate discrepancies")
    parser_d.add_argument("-s", "--merge-revs", action="store_const",
                          dest="merge", const=True, default=False,
                          help="Merge revisions that come" +
                               " from different files")
    parser_d.add_argument("-S", "--no-merge-revs", action="store_const",
                          dest="merge", const=False,
                          help="Do not Merge revisions that come" +
                               " from different files")
    parser_d.add_argument("-v", "--print-vs", action="store_const",
                          dest="print_vs", const=True, default=False,
                          help="Print base version ")
    parser_d.add_argument("-V", "--no-print-vs", action="store_const",
                          dest="print_vs", const=False,
                          help="Do not Merge revisions that come" +
                               " from different files")
    parser_d.add_argument("-m", "--print-models", action="store_const",
                          dest="models", const=True, default=True,
                          help="Print model names")
    parser_d.add_argument("-M", "--no-print-models", action="store_const",
                          dest="models", const=False,
                          help="Do not print model names")
    parser_d.add_argument("-H", "--no-print-header", action="store_const",
                          dest="header", const=False, default=True,
                          help="Do not print hader")
    parser_d.add_argument("-a", "--print-all-files", action="store_const",
                          dest="print_filter", const=False, default=True,
                          help="Print all files")
    parser_d.add_argument("-c", "--print-changed-files", action="store_const",
                          dest="print_filter", const=True,
                          help="Print only changed files")
    parser_d.add_argument("-d", "--min-date", action="store",
                          help="Minimum date filter")
    parser_d.add_argument("filelist", nargs='*',
                          help="RPMs/directories to compare")
    parser_d.set_defaults(func=cmd_discrepancies)

    args = root_parser.parse_args()
    if not hasattr(args, "func"):
        root_parser.print_help()
        return None

    global log_level
    log_level = args.verbose

    return args


def main():
    args = parse_cli()
    if args is None:
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
