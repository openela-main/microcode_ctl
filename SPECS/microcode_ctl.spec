%define intel_ucode_version 20231009
%global debug_package %{nil}

%define caveat_dir %{_datarootdir}/microcode_ctl/ucode_with_caveats
%define microcode_ctl_libexec %{_libexecdir}/microcode_ctl

%define update_ucode %{microcode_ctl_libexec}/update_ucode
%define check_caveats %{microcode_ctl_libexec}/check_caveats
%define reload_microcode %{microcode_ctl_libexec}/reload_microcode

%define dracutlibdir %{_prefix}/lib/dracut

Summary:        CPU microcode updates for Intel x86 processors
Name:           microcode_ctl
Version:        20230808
Release:        2.%{intel_ucode_version}.1%{?dist}
Epoch:          4
License:        CC0 and Redistributable, no modification permitted
URL:            https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files
#Source0:        https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/archive/microcode-%{intel_ucode_version}.tar.gz
Source0:        microcode-%{intel_ucode_version}.tar.gz

# (Pre-MDS) revision 0x714 of 06-2d-07 microcode
Source2:        https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/raw/microcode-20190514/intel-ucode/06-2d-07

# (Pre-20191112) revision 0x2000064 of 06-55-04 microcode
Source3:        https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/raw/microcode-20190918/intel-ucode/06-55-04

# (Pre-20200609) revision 0xd6 of 06-4e-03/06-5e-03 microcode
Source4:        https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/raw/microcode-20200520/intel-ucode/06-4e-03
Source5:        https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/raw/microcode-20200520/intel-ucode/06-5e-03

# microcode-20190918 release,containing revision 0xb4/0xb8 of 06-[89]e-0X microcode
Source6:        https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/archive/microcode-20190918.tar.gz
# microcode-20191115 release,containing revision 0xca of 06-[89]e-0X microcode
Source7:        https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/archive/microcode-20191115.tar.gz


# systemd unit
Source10:       microcode.service

# dracut-related stuff
Source20:       01-microcode.conf
Source21:       99-microcode-override.conf
Source22:       dracut_99microcode_ctl-fw_dir_override_module_init.sh

# libexec
Source30:       update_ucode
Source31:       check_caveats
Source32:       reload_microcode

# docs
Source41:       README.caveats
Source42:       README

## Caveats
# BDW EP/EX
# https://bugzilla.redhat.com/show_bug.cgi?id=1622180
# https://bugzilla.redhat.com/show_bug.cgi?id=1623630
# https://bugzilla.redhat.com/show_bug.cgi?id=1646383
Source100:      06-4f-01_readme
Source101:      06-4f-01_config
Source102:      06-4f-01_disclaimer

# Unsafe early MC update inside VM:
# https://bugzilla.redhat.com/show_bug.cgi?id=1596627
Source110:      intel_readme
Source111:      intel_config
Source112:      intel_disclaimer

# SNB-EP (CPUID 0x206d7) post-MDS hangs
# https://bugzilla.redhat.com/show_bug.cgi?id=1758382
# https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/issues/15
Source120:      06-2d-07_readme
Source121:      06-2d-07_config
Source122:      06-2d-07_disclaimer

# SKL-SP/W/X (CPUID 0x50654) post-20191112 hangs
# https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/issues/21
Source130:      06-55-04_readme
Source131:      06-55-04_config
Source132:      06-55-04_disclaimer

# SKL-U/Y (CPUID 0x406e3) post-20200609 hangs
# https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/issues/31
Source140:      06-4e-03_readme
Source141:      06-4e-03_config
Source142:      06-4e-03_disclaimer

# SKL-H/S/Xeon E3 v5 (CPUID 0x506e3) post-20200609 possible hangs
# https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/issues/31#issuecomment-644885826
Source150:      06-5e-03_readme
Source151:      06-5e-03_config
Source152:      06-5e-03_disclaimer

# Dell 06-[89]e-0x hangs - intermediate 0xca microcode revision
# https://bugzilla.redhat.com/show_bug.cgi?id=1807960
# https://bugzilla.redhat.com/show_bug.cgi?id=1846097
# https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/issues/23
# https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/issues/24
# https://bugs.launchpad.net/ubuntu/+source/intel-microcode/+bug/1862751
Source160:      06-8e-9e-0x-0xca_readme
Source161:      06-8e-9e-0x-0xca_config
Source162:      06-8e-9e-0x-0xca_disclaimer

# Dell 06-[89]e-0x hangs - latest microcode revision
# https://bugzilla.redhat.com/show_bug.cgi?id=1807960
# https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/issues/33
# https://bugs.debian.org/962757
# https://bugs.launchpad.net/ubuntu/+source/intel-microcode/+bug/1882943
Source170:      06-8e-9e-0x-dell_readme
Source171:      06-8e-9e-0x-dell_config
Source172:      06-8e-9e-0x-dell_disclaimer

# TGL-UP3/UP4 (CPUID 06-8c-01) hangs
# https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/issues/44
Source180:      06-8c-01_readme
Source181:      06-8c-01_config
Source182:      06-8c-01_disclaimer

# "Provides:" RPM tags generator
Source1000:     gen_provides.sh
Source1001:     codenames.list
Source1002:     gen_updates2.py

Patch0001: 0001-releasenote.md-eliminate-usage-of-U-0080.patch
Patch0002: 0002-releasenote.md-eliminate-most-of-the-trailing-whites.patch
Patch0003: 0003-releasenote.md-remove-excess-Release-Notes-headers.patch
Patch0004: 0004-releasenote.md-sort-the-entries-of-the-20230808-rele.patch
Patch0005: 0005-releasenote.md-fix-incorrect-platform-mask-for-RPL-H.patch
Patch0006: 0006-releasenote.md-fix-stepping-for-RPL-S.patch
Patch0007: 0007-releasenote.md-add-missing-06-ba-03-e0-to-the-new-mi.patch
Patch0008: 0008-releasenote.md-remove-the-duplicating-06-9e-0c-22-re.patch
Patch0009: 0009-releasenote.md-fix-old-revisions-for-06-8e-09-10-and.patch
Patch0010: 0010-releasenote.md-add-old-revisions-for-06-be-00-11-06-.patch
Patch0011: 0011-releasenote.md-add-stub-release-notes-for-microcode-.patch

ExclusiveArch:  %{ix86} x86_64
BuildRequires:  systemd-units
# hexdump is used in gen_provides.sh
BuildRequires:  coreutils util-linux
Requires:       coreutils
Requires(post): systemd coreutils
Requires(preun): systemd coreutils
Requires(postun): systemd coreutils
Requires(posttrans): dracut coreutils

%global _use_internal_dependency_generator 0
%define __find_provides "%{SOURCE1000}" "%{SOURCE1001}"

%description
This package provides microcode update files for Intel x86 and x86_64 CPUs.

The microcode update is volatile and needs to be uploaded on each system
boot i.e. it isn't stored on a CPU permanently; reboot and it reverts
back to the old microcode.

Package name "microcode_ctl" is historical, as the binary with the same name
is no longer used for microcode upload and, as a result, no longer provided.

%prep
%setup -n "Intel-Linux-Processor-Microcode-Data-Files-microcode-%{intel_ucode_version}"

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1

%build
# remove bogus *_DUPLICATE files with older microcode revisions
rm -vf intel-ucode/??-??-??_DUPLICATE

# replacing SNB-EP (CPUID 0x206d7) microcode with pre-MDS version
mv intel-ucode/06-2d-07 intel-ucode-with-caveats/
cp "%{SOURCE2}" intel-ucode/

# replacing SKL-SP/W/X (CPUID 0x50654) microcode with pre-20191112 version
mv intel-ucode/06-55-04 intel-ucode-with-caveats/
cp "%{SOURCE3}" intel-ucode/

# replacing SKL-U/Y (CPUID 0x4063e) microcode with pre-20200609 version
mv intel-ucode/06-4e-03 intel-ucode-with-caveats/
cp "%{SOURCE4}" intel-ucode/

# replacing SKL-H/S/Xeon E3 v5 (CPUID 0x5063e) microcode with pre-20200609 version
mv intel-ucode/06-5e-03 intel-ucode-with-caveats/
cp "%{SOURCE5}" intel-ucode/

# Replacing the latest 06-[89]e-0x caveat with pre-20191112 version
mv intel-ucode/06-[89]e-0* intel-ucode-with-caveats/
tar xvvf "%{SOURCE6}" --wildcards --strip-components=1 \
	'*/intel-ucode/06-[89]e-0*'

# Unpacking intermediate 06-[89]e-0x microcode revision 0xca (from microcode-20191115)
mkdir -p intel-ucode-0xca
pushd intel-ucode-0xca
tar xvvf "%{SOURCE7}" --wildcards --strip-components=2 \
	'*/intel-ucode/06-[89]e-0*'
popd

# Moving 06-8c-01 microcode to intel-ucode-with-caveats
mv intel-ucode/06-8c-01 intel-ucode-with-caveats/

:

%install
install -m 755 -d \
	"%{buildroot}/%{_datarootdir}/microcode_ctl/intel-ucode" \
	"%{buildroot}/%{caveat_dir}/" \
	"%{buildroot}/etc/microcode_ctl/ucode_with_caveats/"

# systemd unit
install -m 755 -d "%{buildroot}/%{_unitdir}"
install -m 644 "%{SOURCE10}" -t "%{buildroot}/%{_unitdir}/"

# dracut
%define dracut_mod_dir "%{buildroot}/%{dracutlibdir}/modules.d/99microcode_ctl-fw_dir_override"
install -m 755 -d \
	"%{dracut_mod_dir}" \
	"%{buildroot}/%{dracutlibdir}/dracut.conf.d/"
install -m 644 "%{SOURCE20}" "%{SOURCE21}" \
	-t "%{buildroot}/%{dracutlibdir}/dracut.conf.d/"
install -m 755 "%{SOURCE22}" "%{dracut_mod_dir}/module-setup.sh"

# Internal helper scripts
install -m 755 -d "%{buildroot}/%{microcode_ctl_libexec}"
install "%{SOURCE30}" "%{SOURCE31}" "%{SOURCE32}" \
	-m 755 -t "%{buildroot}/%{microcode_ctl_libexec}"


## Documentation
install -m 755 -d "%{buildroot}/%{_pkgdocdir}/caveats"

# caveats readme
install "%{SOURCE41}"  "%{SOURCE42}" \
	-m 644 -t "%{buildroot}/%{_pkgdocdir}/"

# Provide Intel microcode license, as it requires so
install -m 644 license \
	"%{buildroot}/%{_pkgdocdir}/LICENSE.intel-ucode"

# Provide release notes, README and security for Intel microcode
install -m 644 README.md \
	"%{buildroot}/%{_pkgdocdir}/README.intel-ucode"
install -m 644 security.md \
	"%{buildroot}/%{_pkgdocdir}/SECURITY.intel-ucode"
install -m 644 releasenote.md \
	"%{buildroot}/%{_pkgdocdir}/RELEASE_NOTES.intel-ucode"

# caveats
install -m 644 "%{SOURCE100}" "%{SOURCE110}" "%{SOURCE120}" "%{SOURCE130}" \
	       "%{SOURCE140}" "%{SOURCE150}" "%{SOURCE160}" "%{SOURCE170}" \
	       "%{SOURCE180}" \
	-t "%{buildroot}/%{_pkgdocdir}/caveats/"


## Caveat data

# BDW caveat
%define bdw_inst_dir %{buildroot}/%{caveat_dir}/intel-06-4f-01/
install -m 755 -d "%{bdw_inst_dir}/intel-ucode"
install -m 644 intel-ucode-with-caveats/06-4f-01 -t "%{bdw_inst_dir}/intel-ucode/"
install -m 644 "%{SOURCE100}" "%{bdw_inst_dir}/readme"
install -m 644 "%{SOURCE101}" "%{bdw_inst_dir}/config"
install -m 644 "%{SOURCE102}" "%{bdw_inst_dir}/disclaimer"

# Early update caveat
%define intel_inst_dir %{buildroot}/%{caveat_dir}/intel/
install -m 755 -d "%{intel_inst_dir}/intel-ucode"
install -m 644 intel-ucode/* -t "%{intel_inst_dir}/intel-ucode/"
install -m 644 "%{SOURCE110}" "%{intel_inst_dir}/readme"
install -m 644 "%{SOURCE111}" "%{intel_inst_dir}/config"
install -m 644 "%{SOURCE112}" "%{intel_inst_dir}/disclaimer"

# SNB caveat
%define snb_inst_dir %{buildroot}/%{caveat_dir}/intel-06-2d-07/
install -m 755 -d "%{snb_inst_dir}/intel-ucode"
install -m 644 intel-ucode-with-caveats/06-2d-07 -t "%{snb_inst_dir}/intel-ucode/"
install -m 644 "%{SOURCE120}" "%{snb_inst_dir}/readme"
install -m 644 "%{SOURCE121}" "%{snb_inst_dir}/config"
install -m 644 "%{SOURCE122}" "%{snb_inst_dir}/disclaimer"

# SKL-SP caveat
%define skl_sp_inst_dir %{buildroot}/%{caveat_dir}/intel-06-55-04/
install -m 755 -d "%{skl_sp_inst_dir}/intel-ucode"
install -m 644 intel-ucode-with-caveats/06-55-04 -t "%{skl_sp_inst_dir}/intel-ucode/"
install -m 644 "%{SOURCE130}" "%{skl_sp_inst_dir}/readme"
install -m 644 "%{SOURCE131}" "%{skl_sp_inst_dir}/config"
install -m 644 "%{SOURCE132}" "%{skl_sp_inst_dir}/disclaimer"

# SKL-U/Y caveat
%define skl_uy_inst_dir %{buildroot}/%{caveat_dir}/intel-06-4e-03/
install -m 755 -d "%{skl_uy_inst_dir}/intel-ucode"
install -m 644 intel-ucode-with-caveats/06-4e-03 -t "%{skl_uy_inst_dir}/intel-ucode/"
install -m 644 "%{SOURCE140}" "%{skl_uy_inst_dir}/readme"
install -m 644 "%{SOURCE141}" "%{skl_uy_inst_dir}/config"
install -m 644 "%{SOURCE142}" "%{skl_uy_inst_dir}/disclaimer"

# SKL-H/S/Xeoon E3 v5 caveat
%define skl_hs_inst_dir %{buildroot}/%{caveat_dir}/intel-06-5e-03/
install -m 755 -d "%{skl_hs_inst_dir}/intel-ucode"
install -m 644 intel-ucode-with-caveats/06-5e-03 -t "%{skl_hs_inst_dir}/intel-ucode/"
install -m 644 "%{SOURCE150}" "%{skl_hs_inst_dir}/readme"
install -m 644 "%{SOURCE151}" "%{skl_hs_inst_dir}/config"
install -m 644 "%{SOURCE152}" "%{skl_hs_inst_dir}/disclaimer"

# Dell 06-[89]e-0x 0xca caveat
%define dell_0xca_inst_dir %{buildroot}/%{caveat_dir}/intel-06-8e-9e-0x-0xca/
install -m 755 -d "%{dell_0xca_inst_dir}/intel-ucode"
install -m 644 intel-ucode-0xca/06-[89]e-0? -t "%{dell_0xca_inst_dir}/intel-ucode/"
install -m 644 "%{SOURCE160}" "%{dell_0xca_inst_dir}/readme"
install -m 644 "%{SOURCE161}" "%{dell_0xca_inst_dir}/config"
install -m 644 "%{SOURCE162}" "%{dell_0xca_inst_dir}/disclaimer"

# Dell 06-[89]e-0x latest caveat
%define dell_latest_inst_dir %{buildroot}/%{caveat_dir}/intel-06-8e-9e-0x-dell/
install -m 755 -d "%{dell_latest_inst_dir}/intel-ucode"
install -m 644 intel-ucode-with-caveats/06-[89]e-0? -t "%{dell_latest_inst_dir}/intel-ucode/"
install -m 644 "%{SOURCE170}" "%{dell_latest_inst_dir}/readme"
install -m 644 "%{SOURCE171}" "%{dell_latest_inst_dir}/config"
install -m 644 "%{SOURCE172}" "%{dell_latest_inst_dir}/disclaimer"

# TGL caveat
%define tgl_inst_dir %{buildroot}/%{caveat_dir}/intel-06-8c-01/
install -m 755 -d "%{tgl_inst_dir}/intel-ucode"
install -m 644 intel-ucode-with-caveats/06-8c-01 -t "%{tgl_inst_dir}/intel-ucode/"
install -m 644 "%{SOURCE180}" "%{tgl_inst_dir}/readme"
install -m 644 "%{SOURCE181}" "%{tgl_inst_dir}/config"
install -m 644 "%{SOURCE182}" "%{tgl_inst_dir}/disclaimer"

# SUMMARY.intel-ucode generation
# It is to be done only after file population, so, it is here,
# at the end of the install stage
/usr/libexec/platform-python "%{SOURCE1002}" -C "%{SOURCE1001}" \
	summary -A "%{buildroot}" \
	> "%{buildroot}/%{_pkgdocdir}/SUMMARY.intel-ucode"


%post
%systemd_post microcode.service
%{update_ucode}
%{reload_microcode}

# send the message to syslog, so it gets recorded on /var/log
if [ -e /usr/bin/logger ]; then
	%{check_caveats} -m -d | /usr/bin/logger -p syslog.warning -t DISCLAIMER
fi
# also paste it over dmesg (some customers drop dmesg messages while
# others keep them into /var/log for the later case, we'll have the
# disclaimer recorded twice into system logs.
%{check_caveats} -m -d > /dev/kmsg

exit 0

%posttrans
# We only want to regenerate the initramfs for a fully booted
# system; if this package happened to e.g. be pulled in as a build
# dependency, it is pointless at best to regenerate the initramfs,
# and also does not work with rpm-ostree:
# https://bugzilla.redhat.com/show_bug.cgi?id=1199582
# https://bugzilla.redhat.com/show_bug.cgi?id=1530400
[ -d /run/systemd/system ] || exit 0

# We can't simply update all initramfs images, since "dracut --regenerate-all"
# generates initramfs even for removed kernels and if dracut generates botched
# initramfs image, that results in unbootable system, even with older kernels
# that can't be used as a fallback:
# https://bugzilla.redhat.com/show_bug.cgi?id=1420180
# https://access.redhat.com/support/cases/#/case/01779274
# https://access.redhat.com/support/cases/#/case/01814106
#
# ...and we can't simply limit ourselves to updating only the currently
# running kernel, as this doesn't work well with cases where kernel
# is installed before the updated microcode, or in the same transaction.
# And we can't rely on late update either, due to issues like this:
# https://bugzilla.redhat.com/show_bug.cgi?id=1710445
#
# ...and there are also issues with setups with increased "installonly_limit"
# in /etc/yum.conf, which could lead to unacceptably long package installation
# times.
#
# So, in the end, we try to grab no more than 2 most recently installed kernels
# that are installed after the currently running one (with the currently running
# kernel that makes up to 3 in total, the default "installonly_limit" value)
# as a kernel package selection heuristic that tries to accomodate both the need
# to put the latest microcode in freshly installed kernels and also addresses
# existing concerns.
#
# For RPM selection, kernel flavours (like "debug" or "kdump" or "zfcp",
# with only the former being relevant to x86 architecture) are a part or RPM
# name; it's also a part of uname, with different separator used in RHEL 6/7
# and RHEL 8.  RT kernel, however, is special, as "rt" is another part
# of RPM name and it has its own versioning scheme both in NVR and uname.
# And there's the kernel package split in RHEL 8, so one should look for *-core
# and not the main package.
pkgs="kernel-core kernel-debug-core kernel-rt-core kernel-rt-debug-core"
qf='%%{NAME} %%{VERSION}-%%{RELEASE}.%%{ARCH} %%{installtime}\n'
: "${MICROCODE_RPM_KVER_LIMIT=2}"

rpm -qa --qf "${qf}" ${pkgs} | sort -r -n -k'3,3' | {
	kver_cnt=0
	processed=""
	skipped=""
	skip=0

	while read -r pkgname vra install_ts; do
		flavour=''

		# For x86, only "debug" flavour exists in RHEL 8
		[ "x${pkgname%*-debug-core}" = "x${pkgname}" ] \
			|| flavour='+debug'

		kver_cnt="$((kver_cnt + 1))"
		kver_uname="${vra}${flavour}"

		# Also check that the kernel is actually installed:
		# https://bugzilla.redhat.com/show_bug.cgi?id=1591664
		# We use the presence of symvers file as an indicator, the check
		# similar to what weak-modules script does.
		#
		# Now that /boot/symvers-KVER.gz population is now relies
		# on some shell scripts that are triggered by other shell
		# scripts (kernel-install, which is a part of systemd) that
		# called by RPM scripts, and systemd is not inclined to fix
		# https://bugzilla.redhat.com/show_bug.cgi?id=1609698
		# https://bugzilla.redhat.com/show_bug.cgi?id=1609696
		# So, we check for symvers file inside /lib/modules.
		#
		# XXX: Not sure if this check is still needed, since we now
		# iterate over the rpm output.
		[ -e "/lib/modules/${kver_uname}/symvers.gz" ] || continue
		# Check that modules.dep for the kernel is present as well,
		# otherwise dracut complains with "/lib/modules/.../modules.dep
		# is missing. Did you run depmod?".
		[ -e "/lib/modules/${kver_uname}/modules.dep" ] || continue

		# We update the kernels with the same uname as the running kernel
		# regardless of the selected limit
		if [ "x$(uname -r)" = "x${kver_uname}" \
		     -o \( "${kver_cnt}" -le "${MICROCODE_RPM_KVER_LIMIT}" \
		           -a "${skip}" = 0 \) ]
		then
			dracut -f --kver "${kver_uname}"

			processed="${processed} ${pkgname}-${vra}"
		else
			skipped="${skipped} ${pkgname}-${vra}"
		fi

		# The packages are processed until a package with the same uname
		# as the running kernel is hit (since they are sorted
		# in the descending installation time stamp older).
		[ "x$(uname -r)" != "x${kver_uname}" ] || skip=1
	done

	if [ -n "${skipped}" ]; then
		skip_msg="<4>After installation of a new version of microcode_ctl package,
initramfs hasn't been re-generated for all the installed kernel packages.
The following kernel packages have been skipped:${skipped}.
Please re-generate initramfs manually for these kernel packages with the
\"dracut -f --kver KERNEL_VERSION\" command in order to get the latest
Intel CPU microcode included into early initramfs image for it, if needed."

		if [ -e /usr/bin/logger ]; then
			echo "${skip_msg}" |
				/usr/bin/logger -p syslog.warning -t microcode_ctl
		fi

		if [ -e /dev/kmsg ]; then
			echo "${skip_msg}" > /dev/kmsg
		fi
	fi
}

exit 0

%global rpm_state_dir %{_localstatedir}/lib/rpm-state


%preun
%systemd_preun microcode.service

# Storing ucode list before uninstall
ls /usr/share/microcode_ctl/intel-ucode |
	sort > "%{rpm_state_dir}/microcode_ctl_un_intel-ucode"
ls /usr/share/microcode_ctl/ucode_with_caveats |
	sort > "%{rpm_state_dir}/microcode_ctl_un_ucode_caveats"
%{update_ucode} --action list --skip-common |
	sort > "%{rpm_state_dir}/microcode_ctl_un_file_list"

%postun
%systemd_postun microcode.service

ls /usr/share/microcode_ctl/intel-ucode 2> /dev/null |
	sort > "%{rpm_state_dir}/microcode_ctl_un_intel-ucode_after"
comm -23 \
	"%{rpm_state_dir}/microcode_ctl_un_intel-ucode" \
	"%{rpm_state_dir}/microcode_ctl_un_intel-ucode_after" \
	> "%{rpm_state_dir}/microcode_ctl_un_intel-ucode_diff"

if [ -e "%{update_ucode}" ]; then
	ls /usr/share/microcode_ctl/ucode_with_caveats 2> /dev/null |
		sort > "%{rpm_state_dir}/microcode_ctl_un_ucode_caveats_after"

	comm -23 \
		"%{rpm_state_dir}/microcode_ctl_un_ucode_caveats" \
		"%{rpm_state_dir}/microcode_ctl_un_ucode_caveats_after" \
		> "%{rpm_state_dir}/microcode_ctl_un_ucode_caveats_diff"

	%{update_ucode} --action remove --cleanup \
		"%{rpm_state_dir}/microcode_ctl_un_intel-ucode_diff" \
		"%{rpm_state_dir}/microcode_ctl_un_ucode_caveats_diff" || :

	rm -f "%{rpm_state_dir}/microcode_ctl_un_ucode_caveats_after"
	rm -f "%{rpm_state_dir}/microcode_ctl_un_ucode_caveats_diff"
else
	while read -r f; do
		[ -L "/lib/firmware/intel-ucode/$f" ] || continue
		rm -f "/lib/firmware/intel-ucode/$f"
	done < "%{rpm_state_dir}/microcode_ctl_un_intel-ucode_diff"

	rmdir "/lib/firmware/intel-ucode" 2>/dev/null || :

	# We presume that if we don't have update_ucode script, we can remove
	# all the caveats-related files.
	while read -r f; do
		if [ -L "$f" ] || [ "${f%%readme-*}" != "$f" ]; then
			rm -f "$f"
			rmdir -p $(dirname "$f") 2>/dev/null || :
		fi
	done < "%{rpm_state_dir}/microcode_ctl_un_file_list"
fi

rm -f "%{rpm_state_dir}/microcode_ctl_un_intel-ucode"
rm -f "%{rpm_state_dir}/microcode_ctl_un_intel-ucode_after"
rm -f "%{rpm_state_dir}/microcode_ctl_un_intel-ucode_diff"

rm -f "%{rpm_state_dir}/microcode_ctl_un_ucode_caveats"

rm -f "%{rpm_state_dir}/microcode_ctl_un_file_list"

exit 0


%triggerin -- kernel-core, kernel-debug-core, kernel-rt-core, kernel-rt-debug-core
%{update_ucode}

%triggerpostun -- kernel-core, kernel-debug-core, kernel-rt-core, kernel-rt-debug-core
%{update_ucode}


%clean
rm -rf %{buildroot}


%files
%ghost %attr(0755, root, root) /lib/firmware/intel-ucode
%{microcode_ctl_libexec}
/usr/share/microcode_ctl
/etc/microcode_ctl
%{dracutlibdir}/modules.d/*
%config(noreplace) %{dracutlibdir}/dracut.conf.d/*
%{_unitdir}/microcode.service
%doc %{_pkgdocdir}


%changelog
* Wed Nov 01 2023 Eugene Syromiatnikov <esyr@redhat.com> - 4:20230808-2.20231009.1
- Update Intel CPU microcode to microcode-20231009 release, addresses
  CVE-2023-23583 (RHEL-3684):
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode (in
    intel-06-8c-01/intel-ucode/06-8c-01) from revision 0xac up to 0xb4;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd0003a5
    up to 0xd0003b9;
  - Update of 06-6c-01/0x10 (ICL-D B0) microcode from revision 0x1000230
    up to 0x1000268;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xbc
    up to 0xc2;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x2c up
    to 0x34;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x46 up
    to 0x4e;
  - Update of 06-8f-04/0x10 microcode from revision 0x2c000271 up to
    0x2c000290;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode from revision
    0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-04) from revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-04) from
    revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-05) from
    revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode from revision
    0x2c000271 up to 0x2c000290;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode from revision 0x2b0004b1
    up to 0x2b0004d0;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-05) from
    revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-06) from
    revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-06/0x10 microcode from revision 0x2c000271 up to
    0x2c000290;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode from revision 0x2b0004b1
    up to 0x2b0004d0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode from revision
    0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-08) from
    revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-08) from
    revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode from revision
    0x2c000271 up to 0x2c000290;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode from revision
    0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode from revision
    0x2e up to 0x32;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) from revision 0x2e up to 0x32;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x2e up to 0x32;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x2e up to 0x32;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x2e up to 0x32;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode from revision 0x2e
    up to 0x32;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x2e up to 0x32;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x2e up to 0x32;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode from revision
    0x42c up to 0x430;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) from revision 0x42c up to 0x430;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) from revision 0x42c up to 0x430;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode from revision 0x42c
    up to 0x430;
  - Update of 06-9a-04/0x40 (AZB A0) microcode from revision 0x4 up
    to 0x5;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x59 up
    to 0x5d;
  - Update of 06-b7-01/0x32 (RPL-S B0) microcode from revision 0x119 up
    to 0x11d;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode from revision
    0x4119 up to 0x411c;
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode (in
    intel-ucode/06-ba-02) from revision 0x4119 up to 0x411c;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode (in
    intel-ucode/06-ba-03) from revision 0x4119 up to 0x411c;
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode from revision 0x4119
    up to 0x411c;
  - Update of 06-be-00/0x11 (ADL-N A0) microcode from revision 0x11 up
    to 0x12;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-02) from revision 0x2e up to 0x32;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) from revision 0x2e up to 0x32;
  - Update of 06-bf-02/0x07 (ADL C0) microcode from revision 0x2e up
    to 0x32;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-bf-02)
    from revision 0x2e up to 0x32;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-05) from revision 0x2e up to 0x32;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) from revision 0x2e up to 0x32;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-bf-05)
    from revision 0x2e up to 0x32;
  - Update of 06-bf-05/0x07 (ADL C0) microcode from revision 0x2e up
    to 0x32.

* Tue Aug 22 2023 Eugene Syromiatnikov <esyr@redhat.com> - 4:20230808-2
- Add support for the new, more correct, variant of dracut's default
  $fw_dir path in dracut_99microcode_ctl-fw_dir_override_module_init.sh.

* Thu Aug 10 2023 Eugene Syromiatnikov <esyr@redhat.com> - 4:20230808-1
- Update Intel CPU microcode to microcode-20230808 release, addresses
  CVE-2022-40982, CVE-2022-41804, CVE-2023-23908 (#2213125, #2223993, #2230678,
  #2230690):
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode (in
    intel-06-55-04/intel-ucode/06-55-04) from revision 0x2006f05 up
    to 0x2007006;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode (in
    intel-06-8c-01/intel-ucode/06-8c-01) from revision 0xaa up to 0xac;
  - Update of 06-8e-09/0xc0 (KBL-U/U 2+3e/Y H0/J1) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-09) from revision 0xf2 up
    to 0xf4;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-09) from revision 0xf2 up
    to 0xf4;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0a) from revision 0xf2 up
    to 0xf4;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0b) from revision 0xf2 up
    to 0xf4;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode (in intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0c) from
    revision 0xf6 up to 0xf8;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-09) from revision 0xf2 up
    to 0xf4;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0a) from revision 0xf2 up
    to 0xf4;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0b) from revision 0xf2 up
    to 0xf4;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0c) from revision 0xf2 up
    to 0xf4;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0d) from revision 0xf8 up
    to 0xfa;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x1000171
    up to 0x1000181;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4003501
    up to 0x4003604;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003501 up to 0x5003604;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x7002601
    up to 0x7002703;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd000390
    up to 0xd0003a5;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xba
    up to 0xbc;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x2a up
    to 0x2c;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x44 up
    to 0x46;
  - Update of 06-8f-04/0x10 microcode from revision 0x2c0001d1 up to
    0x2c000271;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode from revision
    0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-04) from revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-04) from
    revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-05) from
    revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode from revision
    0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode from revision 0x2b000461
    up to 0x2b0004b1;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-05) from
    revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-06) from
    revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-06/0x10 microcode from revision 0x2c0001d1 up to
    0x2c000271;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode from revision 0x2b000461
    up to 0x2b0004b1;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode from revision
    0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-08) from
    revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-08) from
    revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode from revision
    0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode from revision
    0x2b000461 up to 0x2b0004b1;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode from revision
    0x2c up to 0x2e;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) from revision 0x2c up to 0x2e;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x2c up to 0x2e;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x2c up to 0x2e;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x2c up to 0x2e;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode from revision 0x2c
    up to 0x2e;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x2c up to 0x2e;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x2c up to 0x2e;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode from revision
    0x42a up to 0x42c;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) from revision 0x42a up to 0x42c;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) from revision 0x42a up to 0x42c;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode from revision 0x42a
    up to 0x42c;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xf6 up
    to 0xf8;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xf6
    up to 0xf8;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xf6
    up to 0xf8;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xf6
    up to 0xf8;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K1) microcode from revision
    0xf6 up to 0xf8;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x58 up
    to 0x59;
  - Update of 06-b7-01/0x32 (RPL-S B0) microcode from revision 0x113 up
    to 0x119;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-02) from revision 0x2c up to 0x2e;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) from revision 0x2c up to 0x2e;
  - Update of 06-bf-02/0x07 (ADL C0) microcode from revision 0x2c up
    to 0x2e;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-bf-02)
    from revision 0x2c up to 0x2e;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-05) from revision 0x2c up to 0x2e;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) from revision 0x2c up to 0x2e;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-bf-05)
    from revision 0x2c up to 0x2e;
  - Update of 06-bf-05/0x07 (ADL C0) microcode from revision 0x2c up
    to 0x2e;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode from revision
    0x4112 up to 0x4119 (old pf 0xc0);
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode (in
    intel-ucode/06-ba-02) from revision 0x4112 up to 0x4119 (old pf 0xc0);
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode (in
    intel-ucode/06-ba-03) from revision 0x4112 up to 0x4119 (old pf 0xc0);
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode from revision 0x4112
    up to 0x4119 (old pf 0xc0);
  - Update of 06-be-00/0x11 (ADL-N A0) microcode from revision 0x10 up
    to 0x11 (old pf 0x1).

* Mon Aug 07 2023 Eugene Syromiatnikov <esyr@redhat.com> - 4:20230516-1
- Update Intel CPU microcode to microcode-20230516 release (#2213125):
  - Addition of 06-be-00/0x01 (ADL-N A0) microcode at revision 0x10;
  - Addition of 06-9a-04/0x40 (AZB A0) microcode at revision 0x4;
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode (in
    intel-06-55-04/intel-ucode/06-55-04) from revision 0x2006e05 up
    to 0x2006f05;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode (in
    intel-06-8c-01/intel-ucode/06-8c-01) from revision 0xa6 up to 0xaa;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-09) from revision 0xf0 up
    to 0xf2;
  - Update of 06-8e-09/0xc0 (KBL-U/U 2+3e/Y H0/J1) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-09) from revision 0xf0 up
    to 0xf2;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0a) from revision 0xf0 up
    to 0xf2;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0b) from revision 0xf0 up
    to 0xf2;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode (in intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0c) from
    revision 0xf4 up to 0xf6;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-09) from revision 0xf0 up
    to 0xf2;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0a) from revision 0xf0 up
    to 0xf2;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0b) from revision 0xf0 up
    to 0xf2;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0c) from revision 0xf0 up
    to 0xf2;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0d) from revision 0xf4 up
    to 0xf8;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x1000161
    up to 0x1000171;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4003303
    up to 0x4003501;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003303 up to 0x5003501;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x7002503
    up to 0x7002601;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd000389
    up to 0xd000390;
  - Update of 06-6c-01/0x10 (ICL-D B0) microcode from revision 0x1000211
    up to 0x1000230;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xb8
    up to 0xba;
  - Update of 06-8a-01/0x10 (LKF B2/B3) microcode from revision 0x32 up
    to 0x33;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x28 up
    to 0x2a;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x42 up
    to 0x44;
  - Update of 06-8f-04/0x10 microcode from revision 0x2c000170 up to
    0x2c0001d1;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode from revision
    0x2b000181 up to 0x2b000461;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-04) from revision 0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-04) from
    revision 0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-05) from
    revision 0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode from revision
    0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode from revision 0x2b000181
    up to 0x2b000461;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-05) from
    revision 0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-06) from
    revision 0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-06/0x10 microcode from revision 0x2c000170 up to
    0x2c0001d1;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode from revision 0x2b000181
    up to 0x2b000461;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode from revision
    0x2b000181 up to 0x2b000461;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-08) from
    revision 0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-08) from
    revision 0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b000181 up to 0x2b000461;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode from revision
    0x2c000170 up to 0x2c0001d1;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode from revision
    0x2b000181 up to 0x2b000461;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode from revision
    0x429 up to 0x42a;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) from revision 0x429 up to 0x42a;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) from revision 0x429 up to 0x42a;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode from revision 0x429
    up to 0x42a;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xf4 up
    to 0xf6;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xf4
    up to 0xf6;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xf4
    up to 0xf6;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xf4
    up to 0xf6;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K1) microcode from revision
    0xf4 up to 0xf6;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x57 up
    to 0x58;
  - Update of 06-b7-01/0x32 (RPL-S B0) microcode from revision 0x112 up
    to 0x113;
  - Update of 06-ba-02/0xc0 (RPL-H 6+8/P 6+8 J0) microcode from revision
    0x410e up to 0x4112;
  - Update of 06-ba-03/0xc0 (RPL-U 2+8 Q0) microcode (in
    intel-ucode/06-ba-02) from revision 0x410e up to 0x4112;
  - Update of 06-ba-02/0xc0 (RPL-H 6+8/P 6+8 J0) microcode (in
    intel-ucode/06-ba-03) from revision 0x410e up to 0x4112;
  - Update of 06-ba-03/0xc0 (RPL-U 2+8 Q0) microcode from revision 0x410e
    up to 0x4112.

* Tue Aug 01 2023 Eugene Syromiatnikov <esyr@redhat.com> - 4:20230214-4
- Avoid spurious find failures due to calls on directories that may not exist
  (#2231065).

* Wed Jun 28 2023 Eugene Syromiatnikov <esyr@redhat.com> - 4:20230214-3
- Force locale to C in check_caveats, reload_microcode, and update_ucode
  (#2218096).

* Tue Jun 06 2023 Eugene Syromiatnikov <esyr@redhat.com> - 4:20230214-2
- Cleanup the dangling symlinks in update_ucode (#2135376).

* Wed Feb 15 2023 Eugene Syromiatnikov <esyr@redhat.com> - 4:20230214-1
- Update Intel CPU microcode to microcode-20230214 release, addresses
  CVE-2022-21216, CVE-2022-33196, CVE-2022-33972, CVE-2022-38090 (#2171234,
  #2171259):
  - Addition of 06-6c-01/0x10 (ICL-D B0) microcode at revision 0x1000211;
  - Addition of 06-8f-04/0x87 (SPR-SP E0/S1) microcode at revision
    0x2b000181;
  - Addition of 06-8f-04/0x10 microcode at revision 0x2c000170;
  - Addition of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-04) at revision 0x2b000181;
  - Addition of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-04) at revision 0x2c000170;
  - Addition of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-04) at revision 0x2b000181;
  - Addition of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-04) at
    revision 0x2c000170;
  - Addition of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-04) at revision 0x2b000181;
  - Addition of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-04) at revision 0x2b000181;
  - Addition of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-04) at revision 0x2c000170;
  - Addition of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-05) at revision 0x2b000181;
  - Addition of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-05) at
    revision 0x2c000170;
  - Addition of 06-8f-05/0x87 (SPR-SP E2) microcode at revision
    0x2b000181;
  - Addition of 06-8f-05/0x10 (SPR-HBM B1) microcode at revision
    0x2c000170;
  - Addition of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-05) at revision 0x2b000181;
  - Addition of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-05) at
    revision 0x2c000170;
  - Addition of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-05) at revision 0x2b000181;
  - Addition of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-05) at revision 0x2b000181;
  - Addition of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-05) at revision 0x2c000170;
  - Addition of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-06) at revision 0x2b000181;
  - Addition of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-06) at
    revision 0x2c000170;
  - Addition of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-06) at revision 0x2b000181;
  - Addition of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-06) at revision 0x2c000170;
  - Addition of 06-8f-06/0x87 (SPR-SP E3) microcode at revision
    0x2b000181;
  - Addition of 06-8f-06/0x10 microcode at revision 0x2c000170;
  - Addition of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-06) at revision 0x2b000181;
  - Addition of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-06) at revision 0x2b000181;
  - Addition of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-06) at revision 0x2c000170;
  - Addition of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-07) at revision 0x2b000181;
  - Addition of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-07) at revision 0x2b000181;
  - Addition of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-07) at revision 0x2b000181;
  - Addition of 06-8f-07/0x87 (SPR-SP E4/S2) microcode at revision
    0x2b000181;
  - Addition of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-07) at revision 0x2b000181;
  - Addition of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-08) at revision 0x2b000181;
  - Addition of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-08) at
    revision 0x2c000170;
  - Addition of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-08) at revision 0x2b000181;
  - Addition of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-08) at revision 0x2c000170;
  - Addition of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-08) at revision 0x2b000181;
  - Addition of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-08) at
    revision 0x2c000170;
  - Addition of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-08) at revision 0x2b000181;
  - Addition of 06-8f-08/0x87 (SPR-SP E5/S3) microcode at revision
    0x2b000181;
  - Addition of 06-8f-08/0x10 (SPR-HBM B3) microcode at revision
    0x2c000170;
  - Addition of 06-b7-01/0x32 (RPL-S S0) microcode at revision 0x112;
  - Addition of 06-ba-02/0xc0 microcode at revision 0x410e;
  - Addition of 06-ba-03/0xc0 microcode (in intel-ucode/06-ba-02) at
    revision 0x410e;
  - Addition of 06-ba-02/0xc0 microcode (in intel-ucode/06-ba-03) at
    revision 0x410e;
  - Addition of 06-ba-03/0xc0 microcode at revision 0x410e;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode (in
    intel-06-8c-01/intel-ucode/06-8c-01) from revision 0xa4 up to 0xa6;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode (in intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0c) from
    revision 0xf0 up to 0xf4;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0d) from revision 0xf0 up
    to 0xf4;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x100015e
    up to 0x1000161;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4003302
    up to 0x4003303;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003302 up to 0x5003303;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x7002501
    up to 0x7002503;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd000375
    up to 0xd000389;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x3c up
    to 0x3e;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x20 up
    to 0x22;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xb2
    up to 0xb8;
  - Update of 06-8a-01/0x10 (LKF B2/B3) microcode from revision 0x31 up
    to 0x32;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x40 up
    to 0x42;
  - Update of 06-96-01/0x01 (EHL B1) microcode from revision 0x16 up
    to 0x17;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode from revision
    0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode from revision 0x22
    up to 0x2c (old pf 0x3);
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode from revision
    0x421 up to 0x429;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) from revision 0x421 up to 0x429;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) from revision 0x421 up to 0x429;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode from revision 0x421
    up to 0x429;
  - Update of 06-9c-00/0x01 (JSL A0/A1) microcode from revision 0x24000023
    up to 0x24000024;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xf0 up
    to 0xf4;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xf0
    up to 0xf4;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xf0
    up to 0xf4;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xf0
    up to 0xf4;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K1) microcode from revision
    0xf0 up to 0xf4;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x54 up
    to 0x57;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-02) from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-bf-02/0x07 (ADL C0) microcode from revision 0x22 up to
    0x2c (old pf 0x3);
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-bf-02)
    from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-05) from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-bf-05)
    from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-bf-05/0x07 (ADL C0) microcode from revision 0x22 up to
    0x2c (old pf 0x3).

* Tue Oct 25 2022 Eugene Syromiatnikov <esyr@redhat.com> - 4:20220809-2
- Change the logger severity level to warning to align with the kmsg one
  (#2136224).

* Tue Aug 09 2022 Eugene Syromiatnikov <esyr@redhat.com> - 4:20220809-1
- Update Intel CPU microcode to microcode-20220510 release, addresses
  CVE-2022-21233 (#2115667):
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode (in
    intel-06-55-04/intel-ucode/06-55-04) from revision 0x2006d05 up
    to 0x2006e05;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x100015d
    up to 0x100015e;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd000363
    up to 0xd000375;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x3a up
    to 0x3c;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x1e up
    to 0x20;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xb0
    up to 0xb2;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x26 up
    to 0x28;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x3e up
    to 0x40;
  - Update of 06-97-02/0x03 (ADL-HX/S 8+8 C0) microcode from revision
    0x1f up to 0x22;
  - Update of 06-97-05/0x03 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) from revision 0x1f up to 0x22;
  - Update of 06-bf-02/0x03 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x1f up to 0x22;
  - Update of 06-bf-05/0x03 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x1f up to 0x22;
  - Update of 06-97-02/0x03 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x1f up to 0x22;
  - Update of 06-97-05/0x03 (ADL-S 6+0 K0) microcode from revision 0x1f
    up to 0x22;
  - Update of 06-bf-02/0x03 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x1f up to 0x22;
  - Update of 06-bf-05/0x03 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x1f up to 0x22;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode from revision
    0x41c up to 0x421;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) from revision 0x41c up to 0x421;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) from revision 0x41c up to 0x421;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode from revision 0x41c
    up to 0x421;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x53 up
    to 0x54;
  - Update of 06-97-02/0x03 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-02) from revision 0x1f up to 0x22;
  - Update of 06-97-05/0x03 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) from revision 0x1f up to 0x22;
  - Update of 06-bf-02/0x03 (ADL C0) microcode from revision 0x1f up
    to 0x22;
  - Update of 06-bf-05/0x03 (ADL C0) microcode (in intel-ucode/06-bf-02)
    from revision 0x1f up to 0x22;
  - Update of 06-97-02/0x03 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-05) from revision 0x1f up to 0x22;
  - Update of 06-97-05/0x03 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) from revision 0x1f up to 0x22;
  - Update of 06-bf-02/0x03 (ADL C0) microcode (in intel-ucode/06-bf-05)
    from revision 0x1f up to 0x22;
  - Update of 06-bf-05/0x03 (ADL C0) microcode from revision 0x1f up
    to 0x22.

* Tue May 10 2022 Eugene Syromiatnikov <esyr@redhat.com> - 4:20220510-1
- Update Intel CPU microcode to microcode-20220510 release, addresses
  CVE-2022-0005, CVE-2022-21131, CVE-2022-21136, CVE-2022-21151 (#2086743):
  - Addition of 06-97-02/0x03 (ADL-HX C0) microcode at revision 0x1f;
  - Addition of 06-97-05/0x03 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) at revision 0x1f;
  - Addition of 06-bf-02/0x03 (ADL C0) microcode (in intel-ucode/06-97-02)
    at revision 0x1f;
  - Addition of 06-bf-05/0x03 (ADL C0) microcode (in intel-ucode/06-97-02)
    at revision 0x1f;
  - Addition of 06-97-02/0x03 (ADL-HX C0) microcode (in
    intel-ucode/06-97-05) at revision 0x1f;
  - Addition of 06-97-05/0x03 (ADL-S 6+0 K0) microcode at revision 0x1f;
  - Addition of 06-bf-02/0x03 (ADL C0) microcode (in intel-ucode/06-97-05)
    at revision 0x1f;
  - Addition of 06-bf-05/0x03 (ADL C0) microcode (in intel-ucode/06-97-05)
    at revision 0x1f;
  - Addition of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode at
    revision 0x41c;
  - Addition of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) at revision 0x41c;
  - Addition of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) at revision 0x41c;
  - Addition of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode at revision 0x41c;
  - Addition of 06-97-02/0x03 (ADL-HX C0) microcode (in
    intel-ucode/06-bf-02) at revision 0x1f;
  - Addition of 06-97-05/0x03 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) at revision 0x1f;
  - Addition of 06-bf-02/0x03 (ADL C0) microcode at revision 0x1f;
  - Addition of 06-bf-05/0x03 (ADL C0) microcode (in intel-ucode/06-bf-02)
    at revision 0x1f;
  - Addition of 06-97-02/0x03 (ADL-HX C0) microcode (in
    intel-ucode/06-bf-05) at revision 0x1f;
  - Addition of 06-97-05/0x03 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) at revision 0x1f;
  - Addition of 06-bf-02/0x03 (ADL C0) microcode (in intel-ucode/06-bf-05)
    at revision 0x1f;
  - Addition of 06-bf-05/0x03 (ADL C0) microcode at revision 0x1f;
  - Update of 06-4e-03/0xc0 (SKL-U/U 2+3e/Y D0/K1) microcode (in
    intel-06-4e-03/intel-ucode/06-4e-03) from revision 0xec up to 0xf0;
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode (in
    intel-06-55-04/intel-ucode/06-55-04) from revision 0x2006c0a up
    to 0x2006d05;
  - Update of 06-5e-03/0x36 (SKL-H/S/Xeon E3 N0/R0/S0) microcode (in
    intel-06-5e-03/intel-ucode/06-5e-03) from revision 0xec up to 0xf0;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode (in
    intel-06-8c-01/intel-ucode/06-8c-01) from revision 0x9a up to 0xa4;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-09) from revision 0xec up
    to 0xf0;
  - Update of 06-8e-09/0xc0 (KBL-U/U 2+3e/Y H0/J1) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-09) from revision 0xec up
    to 0xf0;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0a) from revision 0xec up
    to 0xf0;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0b) from revision 0xec up
    to 0xf0;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode (in intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0c) from
    revision 0xec up to 0xf0;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-09) from revision 0xec up
    to 0xf0;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0a) from revision 0xec up
    to 0xf0;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0b) from revision 0xec up
    to 0xf0;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0c) from revision 0xec up
    to 0xf0;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0d) from revision 0xec up
    to 0xf0;
  - Update of 06-37-09/0x0f (VLV D0) microcode from revision 0x90c up
    to 0x90d;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x100015c
    up to 0x100015d;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x400320a
    up to 0x4003302;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x500320a up to 0x5003302;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x7002402
    up to 0x7002501;
  - Update of 06-5c-09/0x03 (APL D0) microcode from revision 0x46 up
    to 0x48;
  - Update of 06-5c-0a/0x03 (APL B1/F1) microcode from revision 0x24 up
    to 0x28;
  - Update of 06-5f-01/0x01 (DNV B0) microcode from revision 0x36 up
    to 0x38;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd000331
    up to 0xd000363;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x38 up
    to 0x3a;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x1c up
    to 0x1e;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xa8
    up to 0xb0;
  - Update of 06-8a-01/0x10 (LKF B2/B3) microcode from revision 0x2d up
    to 0x31;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x22 up
    to 0x26;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x3c up
    to 0x3e;
  - Update of 06-96-01/0x01 (EHL B1) microcode from revision 0x15 up
    to 0x16;
  - Update of 06-9c-00/0x01 (JSL A0/A1) microcode from revision 0x2400001f
    up to 0x24000023;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xec up
    to 0xf0;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xec
    up to 0xf0;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xee
    up to 0xf0;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xea
    up to 0xf0;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K1) microcode from revision
    0xec up to 0xf0;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x50 up
    to 0x53.

* Thu Feb 10 2022 Eugene Syromiatnikov <esyr@redhat.com> - 4:20220207-1
- Update Intel CPU microcode to microcode-20220207 release:
  - Fixes in releasenote.md file.

* Mon Feb 07 2022 Eugene Syromiatnikov <esyr@redhat.com> - 4:20220204-1
- Update Intel CPU microcode to microcode-20220204 release, addresses
  CVE-2021-0127, CVE-2021-0145, and CVE-2021-33120 (#1971906, #2049543,
  #2049554, #2049571):
  - Removal of 06-86-04/0x01 (SNR B0) microcode at revision 0xb00000f;
  - Removal of 06-86-05/0x01 (SNR B1) microcode (in intel-ucode/06-86-04)
    at revision 0xb00000f;
  - Removal of 06-86-04/0x01 (SNR B0) microcode (in intel-ucode/06-86-05)
    at revision 0xb00000f;
  - Removal of 06-86-05/0x01 (SNR B1) microcode at revision 0xb00000f;
  - Update of 06-4e-03/0xc0 (SKL-U/U 2+3e/Y D0/K1) microcode (in
    intel-06-4e-03/intel-ucode/06-4e-03) from revision 0xea up to 0xec;
  - Update of 06-4f-01/0xef (BDX-E/EP/EX/ML B0/M0/R0) microcode (in
    intel-06-4f-01/intel-ucode/06-4f-01) from revision 0xb00003e up
    to 0xb000040;
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode (in
    intel-06-55-04/intel-ucode/06-55-04) from revision 0x2006b06 up
    to 0x2006c0a;
  - Update of 06-5e-03/0x36 (SKL-H/S/Xeon E3 N0/R0/S0) microcode (in
    intel-06-5e-03/intel-ucode/06-5e-03) from revision 0xea up to 0xec;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode (in
    intel-06-8c-01/intel-ucode/06-8c-01) from revision 0x88 up to 0x9a;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-09) from revision 0xea up
    to 0xec;
  - Update of 06-8e-09/0xc0 (KBL-U/U 2+3e/Y H0/J1) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-09) from revision 0xea up
    to 0xec;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0a) from revision 0xea up
    to 0xec;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0b) from revision 0xea up
    to 0xec;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode (in intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0c) from
    revision 0xea up to 0xec;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-09) from revision 0xea up
    to 0xec;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0a) from revision 0xea up
    to 0xec;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0b) from revision 0xea up
    to 0xec;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0c) from revision 0xea up
    to 0xec;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0d) from revision 0xea up
    to 0xec;
  - Update of 06-3f-02/0x6f (HSX-E/EN/EP/EP 4S C0/C1/M1/R2) microcode
    from revision 0x46 up to 0x49;
  - Update of 06-3f-04/0x80 (HSX-EX E0) microcode from revision 0x19 up
    to 0x1a;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x100015b
    up to 0x100015c;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4003102
    up to 0x400320a;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003102 up to 0x500320a;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x7002302
    up to 0x7002402;
  - Update of 06-56-03/0x10 (BDX-DE V2/V3) microcode from revision
    0x700001b up to 0x700001c;
  - Update of 06-56-04/0x10 (BDX-DE Y0) microcode from revision 0xf000019
    up to 0xf00001a;
  - Update of 06-56-05/0x10 (BDX-NS A0/A1, HWL A1) microcode from revision
    0xe000012 up to 0xe000014;
  - Update of 06-5c-09/0x03 (APL D0) microcode from revision 0x44 up
    to 0x46;
  - Update of 06-5c-0a/0x03 (APL B1/F1) microcode from revision 0x20 up
    to 0x24;
  - Update of 06-5f-01/0x01 (DNV B0) microcode from revision 0x34 up
    to 0x36;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd0002a0
    up to 0xd000331;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x36 up
    to 0x38;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x1a up
    to 0x1c;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xa6
    up to 0xa8;
  - Update of 06-8a-01/0x10 (LKF B2/B3) microcode from revision 0x2a up
    to 0x2d;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x16 up
    to 0x22;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x2c up
    to 0x3c;
  - Update of 06-96-01/0x01 (EHL B1) microcode from revision 0x11 up
    to 0x15;
  - Update of 06-9c-00/0x01 (JSL A0/A1) microcode from revision 0x1d up
    to 0x2400001f;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xea up
    to 0xec;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xea
    up to 0xec;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xec
    up to 0xee;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xe8
    up to 0xea;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K1) microcode from revision
    0xea up to 0xec;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x40 up
    to 0x50.

* Mon Jul 05 2021 Eugene Syromiatnikov <esyr@redhat.com> - 4:20210608-1
- Update Intel CPU microcode to microcode-20210608 release (#1921773):
  - Fixes in releasenote.md file.

* Mon Jun 14 2021 Eugene Syromiatnikov <esyr@redhat.com> - 4:20210525-2
- Make intel-06-2d-07, intel-06-4e-03, intel-06-4f-01, intel-06-55-04,
  intel-06-5e-03, intel-06-8c-01, intel-06-8e-9e-0x-0xca,
  and intel-06-8e-9e-0x-dell caveats dependent on intel caveat.
- Enable 06-8c-01 microcode update by default (#1970611).
- Enable 06-5e-03 microcode update by default (#1897673).

* Thu May 27 2021 Eugene Syromiatnikov <esyr@redhat.com> - 4:20210525-1
- Update Intel CPU microcode to microcode-20210525 release, addresses
  CVE-2020-24489, CVE-2020-24511, CVE-2020-24512, and CVE-2020-24513
  (#1962664, #1962714, #1962734, #1962680):
  - Addition of 06-55-05/0xb7 (CLX-SP A0) microcode at revision 0x3000010;
  - Addition of 06-6a-05/0x87 (ICX-SP C0) microcode at revision 0xc0002f0;
  - Addition of 06-6a-06/0x87 (ICX-SP D0) microcode at revision 0xd0002a0;
  - Addition of 06-86-04/0x01 (SNR B0) microcode at revision 0xb00000f;
  - Addition of 06-86-05/0x01 (SNR B1) microcode (in intel-ucode/06-86-04)
    at revision 0xb00000f;
  - Addition of 06-86-04/0x01 (SNR B0) microcode (in intel-ucode/06-86-05)
    at revision 0xb00000f;
  - Addition of 06-86-05/0x01 (SNR B1) microcode at revision 0xb00000f;
  - Addition of 06-8c-02/0xc2 (TGL-R C0) microcode at revision 0x16;
  - Addition of 06-8d-01/0xc2 (TGL-H R0) microcode at revision 0x2c;
  - Addition of 06-96-01/0x01 (EHL B1) microcode at revision 0x11;
  - Addition of 06-9c-00/0x01 (JSL A0/A1) microcode at revision 0x1d;
  - Addition of 06-a7-01/0x02 (RKL-S B0) microcode at revision 0x40;
  - Update of 06-4e-03/0xc0 (SKL-U/U 2+3e/Y D0/K1) microcode (in
    intel-06-4e-03/intel-ucode/06-4e-03) from revision 0xe2 up to 0xea;
  - Update of 06-4f-01/0xef (BDX-E/EP/EX/ML B0/M0/R0) microcode (in
    intel-06-4f-01/intel-ucode/06-4f-01) from revision 0xb000038 up
    to 0xb00003e;
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode (in
    intel-06-55-04/intel-ucode/06-55-04) from revision 0x2006a0a up
    to 0x2006b06;
  - Update of 06-5e-03/0x36 (SKL-H/S/Xeon E3 N0/R0/S0) microcode (in
    intel-06-5e-03/intel-ucode/06-5e-03) from revision 0xe2 up to 0xea;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode (in
    intel-06-8c-01/intel-ucode/06-8c-01) from revision 0x68 up to 0x88;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-09) from revision 0xde up
    to 0xea;
  - Update of 06-8e-09/0xc0 (KBL-U/U 2+3e/Y H0/J1) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-09) from revision 0xde up
    to 0xea;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0a) from revision 0xe0 up
    to 0xea;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0b) from revision 0xde up
    to 0xea;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode (in intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0c) from
    revision 0xde up to 0xea;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-09) from revision 0xde up
    to 0xea;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0a) from revision 0xde up
    to 0xea;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0b) from revision 0xde up
    to 0xea;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0c) from revision 0xde up
    to 0xea;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0d) from revision 0xde up
    to 0xea;
  - Update of 06-3f-02/0x6f (HSX-E/EN/EP/EP 4S C0/C1/M1/R2) microcode
    from revision 0x44 up to 0x46;
  - Update of 06-3f-04/0x80 (HSX-EX E0) microcode from revision 0x16 up
    to 0x19;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x1000159
    up to 0x100015b;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4003006
    up to 0x4003102;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003006 up to 0x5003102;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x700001e
    up to 0x7002302;
  - Update of 06-56-03/0x10 (BDX-DE V2/V3) microcode from revision
    0x7000019 up to 0x700001b;
  - Update of 06-56-04/0x10 (BDX-DE Y0) microcode from revision 0xf000017
    up to 0xf000019;
  - Update of 06-56-05/0x10 (BDX-NS A0/A1, HWL A1) microcode from revision
    0xe00000f up to 0xe000012;
  - Update of 06-5c-09/0x03 (APL D0) microcode from revision 0x40 up
    to 0x44;
  - Update of 06-5c-0a/0x03 (APL B1/F1) microcode from revision 0x1e up
    to 0x20;
  - Update of 06-5f-01/0x01 (DNV B0) microcode from revision 0x2e up
    to 0x34;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x34 up
    to 0x36;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x18 up
    to 0x1a;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xa0
    up to 0xa6;
  - Update of 06-8a-01/0x10 (LKF B2/B3) microcode from revision 0x28 up
    to 0x2a;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xe0 up
    to 0xea;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xe0
    up to 0xea;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xe0
    up to 0xec;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xe0
    up to 0xe8;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K0) microcode from revision
    0xe0 up to 0xea.

* Wed Feb 17 2021 Eugene Syromiatnikov <esyr@redhat.com> - 4:20210216-1
- Update Intel CPU microcode to microcode-20210216 release (#1902884):
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode (in
    intel-06-55-04/intel-ucode/06-55-04) from revision 0x2006a08 up
    to 0x2006a0a;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4003003
    up to 0x4003006;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003003 up to 0x5003006.

* Wed Feb 17 2021 Eugene Syromiatnikov <esyr@redhat.com> - 4:20201112-3
- Remove 06-55-04/06-55-06/06-55-07 (SKX-SP/CLX-SP) microcode-20201110 caveats.

* Tue Dec 01 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20201112-2
- Do not use "grep -q" in a pipe in check_caveats (#1902021).
- Add 06-55-04/06-55-06/06-55-07 (SKX-SP/CLX-SP) microcode-20201110 caveats
  (#1902884).

* Fri Nov 13 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20201112-1
- Update Intel CPU microcode to microcode-20201112 release (#1896912):
  - Addition of 06-8a-01/0x10 (LKF B2/B3) microcode at revision 0x28;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x32 up
    to 0x34;
  - Updated releasenote file.

* Fri Nov 13 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20201027-2
- Disable 06-8c-01 (TGL-UP3/UP4 B1) microcode update by default (#1897534).

* Thu Oct 29 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20201027-1
- Update Intel CPU microcode to microcode-20201027 release, addresses
  CVE-2020-8694, CVE-2020-8695, CVE-2020-8696, CVE-2020-8698
  (#1893266, #1893254, #1893234):
  - Addition of 06-55-0b/0xbf (CPX-SP A1) microcode at revision 0x700001e;
  - Addition of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode at revision 0x68;
  - Addition of 06-a5-02/0x20 (CML-H R1) microcode at revision 0xe0;
  - Addition of 06-a5-03/0x22 (CML-S 6+2 G1) microcode at revision 0xe0;
  - Addition of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode at revision 0xe0;
  - Addition of 06-a6-01/0x80 (CML-U 6+2 v2 K0) microcode at revision
    0xe0;
  - Update of 06-4e-03/0xc0 (SKL-U/U 2+3e/Y D0/K1) microcode (in
    intel-06-4e-03/intel-ucode/06-4e-03) from revision 0xdc up to 0xe2;
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode (in
    intel-06-55-04/intel-ucode/06-55-04) from revision 0x2006906 up
    to 0x2006a08;
  - Update of 06-5e-03/0x36 (SKL-H/S/Xeon E3 N0/R0/S0) microcode (in
    intel-06-5e-03/intel-ucode/06-5e-03) from revision 0xdc up to 0xe2;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-09) from revision 0xd6 up
    to 0xde;
  - Update of 06-8e-09/0xc0 (KBL-U/U 2+3e/Y H0/J1) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-09) from revision 0xd6 up
    to 0xde;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0a) from revision 0xd6 up
    to 0xe0;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0b) from revision 0xd6 up
    to 0xde;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode (in intel-06-8e-9e-0x-dell/intel-ucode/06-8e-0c) from
    revision 0xd6 up to 0xde;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-09) from revision 0xd6 up
    to 0xde;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0a) from revision 0xd6 up
    to 0xde;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0b) from revision 0xd6 up
    to 0xde;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0c) from revision 0xd6 up
    to 0xde;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode (in
    intel-06-8e-9e-0x-dell/intel-ucode/06-9e-0d) from revision 0xd6 up
    to 0xde;
  - Update of 06-3f-02/0x6f (HSX-E/EN/EP/EP 4S C0/C1/M1/R2) microcode
    from revision 0x43 up to 0x44;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x1000157
    up to 0x1000159;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4002f01
    up to 0x4003003;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5002f01 up to 0x5003003;
  - Update of 06-5c-09/0x03 (APL D0) microcode from revision 0x38 up
    to 0x40;
  - Update of 06-5c-0a/0x03 (APL B1/F1) microcode from revision 0x16 up
    to 0x1e;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x16 up
    to 0x18;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0x78
    up to 0xa0;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xca
    up to 0xe0.

* Fri Aug 21 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20200609-3
- Add README file to the documentation directory.
- Add publicly-sourced codenames list to supply to gen_provides.sh; update
  the latter to handle the somewhat different format.
- Add SUMMARY.intel-ucode file containing metadata information from
  the microcode file headers.

* Mon Jun 22 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20200609-2
- Blacklist latest microcode revision for 06-[89]e-0x CPUs (AML-Y,
  CFL-H/S/U/Xeon E, CML-Y, KBL-G/H/S/X/U/Y/Xeon E3 v6, WHL-U) on Dell systems,
  use revision 0xae/0xb4/0xb8 by default, provide the latest revision
  and intermediate revision 0xca in caveats (#1807960, #1846097).

* Mon Jun 15 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20200609-1
- Update Intel CPU microcode to microcode-20200609 release (#1845967):
  - Fixed a typo in the release note file.

* Mon Jun 15 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20200602-5
- Enable 06-2d-07 (SNB-E/EN/EP) caveat by default.

* Mon Jun 15 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20200602-4
- Enable 06-55-04 (SKL-X/W) caveat by default.

* Sun Jun 14 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20200602-3
- Do not update 06-4e-03 (SKL-U/Y) and 06-5e-03 (SKL-H/S/Xeon E3 v5) to revision
  0xdc, use 0xd6 by default (#1846119).

* Thu Jun 04 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20200602-2
- Avoid temporary file creation, used for here-documents in check_caveats
  (#1839163).

* Wed Jun 03 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20200602-1
- Update Intel CPU microcode to microcode-20200602 release, addresses
  CVE-2020-0543, CVE-2020-0548, CVE-2020-0549 (#1795354, #1795356, #1827184):
  - Update of 06-3c-03/0x32 (HSW C0) microcode from revision 0x27 up to 0x28;
  - Update of 06-3d-04/0xc0 (BDW-U/Y E0/F0) microcode from revision 0x2e
    up to 0x2f;
  - Update of 06-45-01/0x72 (HSW-U C0/D0) microcode from revision 0x25
    up to 0x26;
  - Update of 06-46-01/0x32 (HSW-H C0) microcode from revision 0x1b up to 0x1c;
  - Update of 06-47-01/0x22 (BDW-H/Xeon E3 E0/G0) microcode from revision 0x21
    up to 0x22;
  - Update of 06-4e-03/0xc0 (SKL-U/Y D0) microcode from revision 0xd6
    up to 0xdc;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x1000151
    up to 0x1000157;
  - Update of 06-55-04/0xb7 (SKX-SP H0/M0/U0, SKX-D M1) microcode
    (in intel-06-55-04/intel-ucode/06-55-04) from revision 0x2000065
    up to 0x2006906;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x400002c
    up to 0x4002f01;
  - Update of 06-55-07/0xbf (CLX-SP B1) microcode from revision 0x500002c
    up to 0x5002f01;
  - Update of 06-5e-03/0x36 (SKL-H/S R0/N0) microcode from revision 0xd6
    up to 0xdc;
  - Update of 06-8e-09/0x10 (AML-Y22 H0) microcode from revision 0xca
    up to 0xd6;
  - Update of 06-8e-09/0xc0 (KBL-U/Y H0) microcode from revision 0xca
    up to 0xd6;
  - Update of 06-8e-0a/0xc0 (CFL-U43e D0) microcode from revision 0xca
    up to 0xd6;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode from revision 0xca
    up to 0xd6;
  - Update of 06-8e-0c/0x94 (AML-Y42 V0, CML-Y42 V0, WHL-U V0) microcode
    from revision 0xca up to 0xd6;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode from revision
    0xca up to 0xd6;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E3 U0) microcode from revision 0xca
    up to 0xd6;
  - Update of 06-9e-0b/0x02 (CFL-S B0) microcode from revision 0xca up to 0xd6;
  - Update of 06-9e-0c/0x22 (CFL-H/S P0) microcode from revision 0xca
    up to 0xd6;
  - Update of 06-9e-0d/0x22 (CFL-H R0) microcode from revision 0xca up to 0xd6.

* Fri May 22 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20200520-1
- Update Intel CPU microcode to microcode-20200520 release (#1783103):
  - Update of 06-2d-06/0x6d (SNB-E/EN/EP C1/M0) microcode from revision 0x61f
    up to 0x621;
  - Update of 06-2d-07/0x6d (SNB-E/EN/EP C2/M1) microcode from revision 0x718
    up to 0x71a.

* Tue May 12 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20200508-1
- Update Intel CPU microcode to microcode-20200508 release (#1783103):
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0x46
    up to 0x78.
- Change the URL to point to the GitHub repository since the microcode download
  section at Intel Download Center does not exist anymore.

* Thu May 07 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20191115-6
- Narrow down SKL-SP/W/X blacklist to exclude Server/FPGA/Fabric segment
  models (#1833036).

* Wed Apr 29 2020 Eugene Syromiatnikov <esyr@redhat.com> - 4:20191115-5
- Re-generate initramfs not only for the currently running kernel,
  but for several recently installed kernels as well (#1773338).

* Mon Dec 09 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20191115-4
- Avoid find being SIGPIPE'd on early "grep -q" exit in the dracut script
  (#1781365).

* Mon Dec 02 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20191115-3
- Update stale posttrans dependency, add triggers for proper handling
  of the debug kernel flavour along with kernel-rt (#1766178).

* Mon Nov 18 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20191115-2
- Do not update 06-55-04 (SKL-SP/W/X) to revision 0x2000065, use 0x2000064
  by default (#1774322).

* Sat Nov 16 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20191115-1
- Update Intel CPU microcode to microcode-20191115 release:
  - Update of 06-4e-03/0xc0 (SKL-U/Y D0) from revision 0xd4 up to 0xd6;
  - Update of 06-5e-03/0x36 (SKL-H/S/Xeon E3 R0/N0) from revision 0xd4
    up to 0xd6;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) from revision 0xc6 up to 0xca;
  - Update of 06-8e-09/0xc0 (KBL-U/Y H0) from revision 0xc6 up to 0xca;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0) from revision 0xc6 up to 0xca;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) from revision 0xc6 up to 0xca;
  - Update of 06-8e-0c/0x94 (AML-Y V0, CML-U 4+2 V0, WHL-U V0) from revision
    0xc6 up to 0xca;
  - Update of 06-9e-09/0x2a (KBL-G/X H0, KBL-H/S/Xeon E3 B0) from revision 0xc6
    up to 0xca;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) from revision 0xc6 up to 0xca;
  - Update of 06-9e-0b/0x02 (CFL-S B0) from revision 0xc6 up to 0xca;
  - Update of 06-9e-0c/0x22 (CFL-S/Xeon E P0) from revision 0xc6 up to 0xca;
  - Update of 06-9e-0d/0x22 (CFL-H/S R0) from revision 0xc6 up to 0xca;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) from revision 0xc6 up to 0xca.

* Fri Nov 15 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20191113-1
- Update Intel CPU microcode to microcode-20191113 release:
  - Update of 06-9e-0c (CFL-H/S P0) microcode from revision 0xae up to 0xc6.
- Drop 0001-releasenote-changes-summary-fixes.patch.

* Tue Nov 12 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20191112-2
- Package the publicy available microcode-20191112 release (#1755027):
  - Addition of 06-4d-08/0x1 (AVN B0/C0) microcode at revision 0x12d;
  - Addition of 06-55-06/0xbf (CSL-SP B0) microcode at revision 0x400002c;
  - Addition of 06-7a-08/0x1 (GLK R0) microcode at revision 0x16;
  - Update of 06-55-03/0x97 (SKL-SP B1) microcode from revision 0x1000150
    up to 0x1000151;
  - Update of 06-55-04/0xb7 (SKL-SP H0/M0/U0, SKL-D M1) microcode from revision
    0x2000064 up to 0x2000065;
  - Update of 06-55-07/0xbf (CSL-SP B1) microcode from revision 0x500002b
    up to 0x500002c;
  - Update of 06-7a-01/0x1 (GLK B0) microcode from revision 0x2e up to 0x32;
- Include 06-9e-0c (CFL-H/S P0) microcode from the microcode-20190918 release.
- Correct the releasenote file (0001-releasenote-changes-summary-fixes.patch).
- Update README.caveats with the link to the new Knowledge Base article.

* Thu Nov 07 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20191112-1
- Intel CPU microcode update to 20191112, addresses CVE-2017-5715,
  CVE-2019-0117, CVE-2019-11135, CVE-2019-11139 (#1755019, #1764060, #1764073,
  #1764952, #1764972, #1765000, #1765404, #1765416, #1766444, #1766873):
  - Addition of 06-a6-00/0x80 (CML-U 6+2 A0) microcode at revision 0xc6;
  - Addition of 06-66-03/0x80 (CNL-U D0) microcode at revision 0x2a;
  - Addition of 06-55-03/0x97 (SKL-SP B1) microcode at revision 0x1000150;
  - Addition of 06-7e-05/0x80 (ICL-U/Y D1) microcode at revision 0x46;
  - Update of 06-4e-03/0xc0 (SKL-U/Y D0) microcode from revision 0xcc to 0xd4;
  - Update of 06-5e-03/0x36 (SKL-H/S/Xeon E3 R0/N0) microcode from revision 0xcc
    to 0xd4
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode from revision 0xb4 to 0xc6;
  - Update of 06-8e-09/0xc0 (KBL-U/Y H0) microcode from revision 0xb4 to 0xc6;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0) microcode from revision 0xb4
    to 0xc6;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode from revision 0xb8 to 0xc6;
  - Update of 06-8e-0c/0x94 (AML-Y V0) microcode from revision 0xb8 to 0xc6;
  - Update of 06-8e-0c/0x94 (CML-U 4+2 V0) microcode from revision 0xb8 to 0xc6;
  - Update of 06-8e-0c/0x94 (WHL-U V0) microcode from revision 0xb8 to 0xc6;
  - Update of 06-9e-09/0x2a (KBL-G/X H0) microcode from revision 0xb4 to 0xc6;
  - Update of 06-9e-09/0x2a (KBL-H/S/Xeon E3 B0) microcode from revision 0xb4
    to 0xc6;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode from revision 0xb4
    to 0xc6;
  - Update of 06-9e-0b/0x02 (CFL-S B0) microcode from revision 0xb4 to 0xc6;
  - Update of 06-9e-0d/0x22 (CFL-H R0) microcode from revision 0xb8 to 0xc6.

* Thu Oct 10 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20190918-3
- Rework dracut hook to address dracut's early initramfs generation
  behaviour (#1760508).

* Sun Oct 06 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20190918-2
- Do not update 06-2d-07 (SNB-E/EN/EP) to revision 0x718, use 0x714
  by default.

* Thu Sep 19 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20190918-1
- Intel CPU microcode update to 20190918 (#1753544).
- Add new disclaimer, generated based on relevant caveats.

* Wed Jun 19 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20190618-1
- Intel CPU microcode update to 20190618 (#1717240).

* Sun Jun 02 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20190514a-2
- Remove disclaimer, as it is not as important now to justify kmsg/log
  pollution; its contents are partially adopted in README.caveats.

* Mon May 20 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20190514a-1
- Intel CPU microcode update to 20190514a (#1711940).

* Thu May 09 2019 Eugene Syromiatnikov <esyr@redhat.com> - 4:20190507-1
- Intel CPU microcode update to 20190507 (#1697901).

* Mon Apr 15 2019 Eugene Syromiatnikov <esyr@redhat.com> 4:20190312-1
- Intel CPU microcode update to 20190312 (#1660320).
- Add "Provides:" tags generation.

* Tue Nov 06 2018 Eugene Syromiatnikov <esyr@redhat.com> 4:20180807a-2
- Do not exit with error in %postin if disclaimer printing returned an error
  (#1647083).

* Wed Oct 17 2018 Eugene Syromiatnikov <esyr@redhat.com> 4:20180807a-1
- Use the tar ball distributed by Intel directly, sync up with RHEL 7.6.

* Fri Aug 24 2018 Eugene Syromiatnikov <esyr@redhat.com> 3:2.1-27
- Bump epoch in order to ensure upgrade from RHEL 7 (#1622131).

* Mon Aug 13 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-26
- Update to upstream 2.1-19. 20180807

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-24
- Update to upstream 2.1-18. 20180703

* Wed May 16 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-23
- Update to upstream 2.1-17. 20180425

* Thu Mar 15 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-22
- Update to upstream 2.1-16. 20180312

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-20
- Update to upstream 2.1-15. 20180108

* Tue Nov 21 2017 Anton Arapov <aarapov@redhat.com> 2:2.1-19
- Update to upstream 2.1-14. 20171117

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Anton Arapov <aarapov@redhat.com> 2:2.1-16
- Update to upstream 2.1-13. 20170707

* Tue May 23 2017 Anton Arapov <aarapov@redhat.com> 2:2.1-15
- Update to upstream 2.1-12. 20170511

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-14.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 02 2016 Anton Arapov <arapov@gmail.com> 2.1-13.1
- Update to upstream 2.1-11. 20161104

* Thu Jul 21 2016 Anton Arapov <arapov@gmail.com> 2.1-13
- Update to upstream 2.1-10. 20160714
- Fixes rhbz#1353103

* Fri Jun 24 2016 Anton Arapov <arapov@gmail.com> 2.1-12
- Update to upstream 2.1-9. 20160607

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Anton Arapov <arapov@gmail.com> 2.1-10
- Update to upstream 2.1-8. 20151106

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.1-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 03 2015 Anton Arapov <arapov@gmail.com> 2.1-8.1
- Update to upstream 2.1-7. 20150121

* Sun Sep 21 2014 Anton Arapov <arapov@gmail.com> 2.1-8
- Update to upstream 2.1-6. 20140913

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 08 2014 Anton Arapov <anton@descope.org> 2.1-6
- Update to upstream 2.1-5. 20140624

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Anton Arapov <anton@redhat.com> 2.1-4
- Update to upstream 2.1-4.

* Fri Jan 24 2014 Anton Arapov <anton@redhat.com> 2.1-3
- Update to upstream 2.1-3.

* Mon Sep 09 2013 Anton Arapov <anton@redhat.com> 2.1-2
- Update to upstream 2.1-2.

* Wed Aug 14 2013 Anton Arapov <anton@redhat.com> 2.1-1
- Update to upstream 2.1-1.

* Sat Jul 27 2013 Anton Arapov <anton@redhat.com> 2.1-0
- Update to upstream 2.1. AMD microcode has been removed, find it in linux-firmware.

* Wed Apr 03 2013 Anton Arapov <anton@redhat.com> 2.0-3.1
- Update to upstream 2.0-3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Anton Arapov <anton@redhat.com> 2.0-2
- Update to upstream 2.0-2

* Tue Oct 02 2012 Anton Arapov <anton@redhat.com> 2.0-1
- Update to upstream 2.0-1

* Mon Aug 06 2012 Anton Arapov <anton@redhat.com> 2.0
- Update to upstream 2.0

* Wed Jul 25 2012 Anton Arapov <anton@redhat.com> 1.18-1
- Update to upstream 1.18

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Anton Arapov <anton@redhat.com> 1.17-25
- Update to microcode-20120606.dat

* Tue Feb 07 2012 Anton Arapov <anton@redhat.com> 1.17-24
- Update to amd-ucode-2012-01-17.tar

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Anton Arapov <anton@redhat.com> 1.17-21
- Fix a segfault that may be triggered by very long parameter [#768803]

* Tue Dec 13 2011 Anton Arapov <anton@redhat.com> 1.17-20
- Update to microcode-20111110.dat

* Tue Sep 27 2011 Anton Arapov <anton@redhat.com> 1.17-19
- Update to microcode-20110915.dat

* Thu Aug 04 2011 Anton Arapov <anton@redhat.com> 1.17-18
- Ship splitted microcode for Intel CPUs [#690930]
- Include tool for splitting microcode for Intl CPUs (Kay Sievers )

* Thu Jun 30 2011 Anton Arapov <anton@redhat.com> 1.17-17
- Fix udev rules (Dave Jones ) [#690930]

* Thu May 12 2011 Anton Arapov <anton@redhat.com> 1.17-14
- Update to microcode-20110428.dat

* Thu Mar 24 2011 Anton Arapov <anton@redhat.com> 1.17-13
- fix memory leak.

* Mon Mar 07 2011 Anton Arapov <anton@redhat.com> 1.17-12
- Update to amd-ucode-2011-01-11.tar

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Anton Arapov <anton@redhat.com> 1.17-10
- manpage fix (John Bradshaw ) [#670879]

* Wed Jan 05 2011 Anton Arapov <anton@redhat.com> 1.17-9
- Update to microcode-20101123.dat

* Mon Nov 01 2010 Anton Arapov <anton@redhat.com> 1.17-8
- Update to microcode-20100914.dat

* Wed Sep 29 2010 jkeating - 1:1.17-7
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Anton Arapov <anton@redhat.com> 1.17-6
- Update to microcode-20100826.dat

* Tue Sep 07 2010 Toshio Kuratomi <toshio@fedoraproject.org> 1.17-5
- Fix license tag: bz#450491

* Fri Aug 27 2010 Dave Jones <davej@redhat.com> 1.17-4
- Update to microcode-20100826.dat

* Tue Mar 23 2010 Anton Arapov <anton@redhat.com> 1.17-3
- Fix the udev rules (Harald Hoyer )

* Mon Mar 22 2010 Anton Arapov <anton@redhat.com> 1.17-2
- Make microcode_ctl event driven (Bill Nottingham ) [#479898]

* Thu Feb 11 2010 Dave Jones <davej@redhat.com> 1.17-1.58
- Update to microcode-20100209.dat

* Fri Dec 04 2009 Kyle McMartin <kyle@redhat.com> 1.17-1.57
- Fix duplicate message pointed out by Edward Sheldrake.

* Wed Dec 02 2009 Kyle McMartin <kyle@redhat.com> 1.17-1.56
- Add AMD x86/x86-64 microcode. (Dated: 2009-10-09)
  Doesn't need microcode_ctl modifications as it's loaded by
  request_firmware() like any other sensible driver.
- Eventually, this AMD firmware can probably live inside
  kernel-firmware once it is split out.

* Wed Sep 30 2009 Dave Jones <davej@redhat.com>
- Update to microcode-20090927.dat

* Fri Sep 11 2009 Dave Jones <davej@redhat.com>
- Remove some unnecessary code from the init script.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-1.52.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 25 2009 Dave Jones <davej@redhat.com>
- Shorten sleep time during init.
  This really needs to be replaced with proper udev hooks, but this is
  a quick interim fix.

* Wed Jun 03 2009 Kyle McMartin <kyle@redhat.com> 1:1.17-1.50
- Change ExclusiveArch to i586 instead of i386. Resolves rhbz#497711.

* Wed May 13 2009 Dave Jones <davej@redhat.com>
- update to microcode 20090330

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-1.46.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Dave Jones <davej@redhat.com>
- update to microcode 20080910

* Tue Apr 01 2008 Jarod Wilson <jwilson@redhat.com>
- Update to microcode 20080401

* Sat Mar 29 2008 Dave Jones <davej@redhat.com>
- Update to microcode 20080220
- Fix rpmlint warnings in specfile.

* Mon Mar 17 2008 Dave Jones <davej@redhat.com>
- specfile cleanups.

* Fri Feb 22 2008 Jarod Wilson <jwilson@redhat.com>
- Use /lib/firmware instead of /etc/firmware

* Wed Feb 13 2008 Jarod Wilson <jwilson@redhat.com>
- Fix permissions on microcode.dat

* Thu Feb 07 2008 Jarod Wilson <jwilson@redhat.com>
- Spec cleanup and macro standardization.
- Update license
- Update microcode data file to 20080131 revision.

* Mon Jul  2 2007 Dave Jones <davej@redhat.com>
- Update to upstream 1.17

* Thu Oct 12 2006 Jon Masters <jcm@redhat.com>
- BZ209455 fixes.

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Fri Jun 16 2006 Bill Nottingham <notting@redhat.com>
- remove kudzu requirement
- add prereq for coreutils, awk, grep

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Fri Jan 27 2006 Dave Jones <davej@redhat.com>
- Update to upstream 1.13

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Dave Jones <davej@redhat.com>
- initscript tweaks.

* Tue Sep 13 2005 Dave Jones <davej@redhat.com>
- Update to upstream 1.12

* Wed Aug 17 2005 Dave Jones <davej@redhat.com>
- Check for device node *after* loading the module. (#157672)

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Thu Feb 17 2005 Dave Jones <davej@redhat.com>
- s/Serial/Epoch/

* Tue Jan 25 2005 Dave Jones <davej@redhat.com>
- Drop the node creation/deletion change from previous release.
  It'll cause grief with selinux, and was a hack to get around
  a udev shortcoming that should be fixed properly.

* Fri Jan 21 2005 Dave Jones <davej@redhat.com>
- Create/remove the /dev/cpu/microcode dev node as needed.
- Use correct path again for the microcode.dat.
- Remove some no longer needed tests in the init script.

* Fri Jan 14 2005 Dave Jones <davej@redhat.com>
- Only enable microcode_ctl service if the CPU is capable.
- Prevent microcode_ctl getting restarted multiple times on initlevel change (#141581)
- Make restart/reload work properly
- Do nothing if not started by root.

* Wed Jan 12 2005 Dave Jones <davej@redhat.com>
- Adjust dev node location. (#144963)

* Tue Jan 11 2005 Dave Jones <davej@redhat.com>
- Load/Remove microcode module in initscript.

* Mon Jan 10 2005 Dave Jones <davej@redhat.com>
- Update to upstream 1.11 release.

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, based upon kernel-utils.

