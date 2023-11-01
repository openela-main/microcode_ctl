#! /bin/bash -efu

# Generator of RPM "Provides:" tags for Intel microcode files.
#
# SPDX-License-Identifier: CC0-1.0

IFS=$'\n'
UPDATED="intel-beta"
CODENAMES="codenames"

if [ "$#" -ge 1 ]; then
	CODENAMES="$1"
	shift
fi

# Match only FF-MM-SS ucode files under intel-ucode/intel-ucode-with-caveats
# directories.
for f in $(grep -E '/intel-ucode.*/[0-9a-f][0-9a-f]-[0-9a-f][0-9a-f]-[0-9a-f][0-9a-f]$'); do
	ucode=$(basename "$f")
	ucode_caveat="$(basename "$(dirname "$(dirname "$f")")")"
	ucode_fname="$ucode_caveat/$ucode"
	file_sz="$(stat -c "%s" "$f")"
	skip=0
	ext_hdr=0
	ext_sig_cnt=0
	ext_sig_pos=0
	next_skip=0

	# Microcode header format description:
	# https://gitlab.com/iucode-tool/iucode-tool/blob/master/intel_microcode.c
	while :; do
		[ "$skip" -lt "$file_sz" ] || break

		# Do we parse ext_sig table or another microcode header?
		if [ 0 != "$next_skip" ]; then
			# Check whether we should abort ext_sig table parsing
			[ \( "${skip}" -lt "${next_skip}" \) -a \
			  \( "${ext_sig_pos}" -lt "${ext_sig_cnt}" \) ] || {
				skip="${next_skip}"
				next_skip=0
				continue
			}

			# ext_sig, 12 bytes in size
			IFS=' ' read cpuid pf_mask <<- EOF
			$(hexdump -s "$skip" -n 8 \
				-e '"" 1/4 "%08x " 1/4 "%u" "\n"' "$f")
			EOF

			skip="$((skip + 12))"
			ext_sig_pos="$((ext_sig_pos + 1))"
		else
			# Microcode header, 48 bytes, last 3 fields reserved
			IFS=' ' read hdrver rev \
			       date_y date_d date_m \
			       cpuid cksum ldrver \
			       pf_mask datasz totalsz <<- EOF
			$(hexdump -s "$skip" -n 36 \
				-e '"" 1/4 "%u " 1/4 "%#x " \
			               1/2 "%04x " 1/1 "%02x " 1/1 "%02x " \
				       1/4 "%08x " 1/4 "%x " 1/4 "%#x " \
				       1/4 "%u " 1/4 "%u " 1/4 "%u" "\n"' "$f")
			EOF

			[ 0 != "$datasz" ] || datasz=2000
			[ 0 != "$totalsz" ] || totalsz=2048

			# TODO: add some sanity/safety checks here.  As of now,
			#       there's a (pretty fragile) assumption that all
			#       the matched files are valid Intel microcode
			#       files in the expected format.

			# ext_sig table is after the microcode payload,
			# check for its presence
			if [ 48 -lt "$((totalsz - datasz))" ]; then
				next_skip="$((skip + totalsz))"
				skip="$((skip + datasz + 48))"
				ext_sig_pos=0

				# ext_sig table header, 20 bytes in size,
				# last 3 fields are reserved.
				IFS=' ' read ext_sig_cnt  <<- EOF
				$(hexdump -s "$skip" -n 4 \
					-e '"" 1/4 "%u" "\n"' "$f")
				EOF

				skip="$((skip + 20))"
			else
				skip="$((skip + totalsz))"
				next_skip=0
			fi
		fi

		#[ -n "$rev" ] || continue

		# Basic "Provides:" tag. Everything else is bells and whistles.
		# It's possible that microcode files for different platform_id's
		# and the same CPUID have the same version, that's why "sort -u"
		# in the end.
		printf "firmware(intel-ucode/%s) = %s\n" "$ucode" "$rev"

		# Generate extended "Provides:" tags with additional
		# information, which allow more precise matching.
		printf "iucode_date(fname:%s;cpuid:%s;pf_mask:0x%x) = %s.%s.%s\n" \
			"$ucode_fname" "$cpuid" "$pf_mask" "$date_y" "$date_m" "$date_d"
		printf "iucode_rev(fname:%s;cpuid:%s;pf_mask:0x%x) = %s\n" \
			"$ucode_fname" "$cpuid" "$pf_mask" "$rev"

		# Generate tags for each possible platform_id
		_pf=1
		_pf_mask="$pf_mask"
		while [ 0 -lt "$_pf_mask" ]; do
			[ 1 -ne "$((_pf_mask % 2))" ] || \
				# We try to provide a more specific firmware()
				# dependency here.  It has incorrect file name,
				# but allows constructing a required RPM
				# capability name by (directly) using
				# the contents of /proc/cpuinfo and
				# /sys/devices/system/cpu/cpu*/microcode/processor_flags
				# (except for a Deschutes CPU with sig 0x1632)
				printf "iucode_rev(fname:%s;platform_id:0x%x) = %s\n" \
					"$ucode_fname" "$_pf" "$rev"

			_pf_mask=$((_pf_mask / 2))
			_pf=$((_pf * 2))
		done

		# Generate tags with codename information, in case
		# it is available
		if [ -e "$CODENAMES" ]; then
			cpuid_up="$(echo "$cpuid" | tr 'a-z' 'A-Z')"
			cpuid_short="$(printf "%x" "0x$cpuid")"
			(grep '	'"$cpuid_up"'	' "$CODENAMES" || :; grep ';'"$cpuid_short"';' "$CODENAMES" || :) \
			| while IFS=$';\t' read segm int_fname codename stepping candidate_pf cpuid_cn cname variants rest; do
				[ "x${segm###}" = "x$segm" ] || continue
				[ -n "${segm}" ] || continue
				codename=$(echo "$codename" | tr ' (),' '_[];')
				candidate_pf=$(printf "%u" "0x${candidate_pf}")
				(IFS=','; for s in $stepping; do
					[ \( 0 -ne "$pf_mask" \) -a \
					  \( 0 -eq "$((candidate_pf & pf_mask))" \) ] || { \
						printf "iucode_rev(fname:%s;cpuid:%s;pf_mask:0x%x;segment:\"%s\";codename:\"%s\";stepping:\"%s\";pf_model:0x%x) = %s\n" \
							"$ucode_fname" "$cpuid" "$pf_mask" \
							"$segm" "$codename" "$s" "$candidate_pf" \
							"$rev";
						printf "iucode_date(fname:%s;cpuid:%s;pf_mask:0x%x;segment:\"%s\";codename:\"%s\";stepping:\"%s\";pf_model:0x%x) = %s.%s.%s\n" \
							"$ucode_fname" "$cpuid" "$pf_mask" \
							"$segm" "$codename" "$s" "$candidate_pf" \
							"$date_y" "$date_m" "$date_d";
						if [ "$cpuid_short" = "$cpuid_cn" -a -n "$variants" ]; then
							(IFS=','; for v in $variants; do
								v=$(echo "$v" | tr ' (),' '_[];')
								printf "iucode_rev(fname:%s;cpuid:%s;pf_mask:0x%x;segment:\"%s\";codename:\"%s_%s\";stepping:\"%s\";pf_model:0x%x) = %s\n" \
									"$ucode_fname" "$cpuid" "$pf_mask" \
									"$segm" "$codename" "$v" "$s" "$candidate_pf" \
									"$rev";
								printf "iucode_date(fname:%s;cpuid:%s;pf_mask:0x%x;segment:\"%s\";codename:\"%s_%s\";stepping:\"%s\";pf_model:0x%x) = %s.%s.%s\n" \
									"$ucode_fname" "$cpuid" "$pf_mask" \
									"$segm" "$codename" "$v" "$s" "$candidate_pf" \
									"$date_y" "$date_m" "$date_d";
							done)
						fi
					  }
				done)
			done
		fi

		# Kludge squared: generate additional "Provides:" tags
		# for the files in the overrides tarball (that a placed
		# in a separate caveat with a specific name)
		[ "x${ucode_caveat}" != "x${UPDATED}" ] || {
			printf "firmware_updated(intel-ucode/%s) = %s\n" \
				"$ucode" "$rev";
		}
	done
done | sort -u
