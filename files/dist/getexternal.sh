#! /bin/bash
# vim: set tabstop=4 shiftwidth=4 noexpandtab filetype=sh:

if ! hash wget; then
	echo "wget is not installed. On a Mac, install it with MacPorts or Homebrew."
fi

echo "Downloading items..."

mkdir -p files/external/source
wget -O files/external/source/ciopfs-0.4.tar.gz http://www.brain-dump.org/projects/ciopfs/ciopfs-0.4.tar.gz
wget -O files/external/source/macipgw.zip https://github.com/zero2sixd/macipgw/archive/2a5f6a7521a627e46b18468d44f4306fb0a7b7ab.zip
wget -O files/external/source/netatalk-2.2.4.tar.gz http://downloads.sourceforge.net/project/netatalk/netatalk/2.2.4/netatalk-2.2.4.tar.gz
wget -O files/external/source/nulib2-3.1.0a2.zip https://github.com/fadden/nulib2/archive/20fe7efb4d37fedf807416c16d74d51d893ea48a.zip
wget -O files/external/source/unar-1.8.1.zip https://github.com/incbee/Unarchiver/archive/unar-1.8.1.zip

mkdir -p files/external/appleii
wget --max-redirect 0 -O files/external/appleii/Apple_II_System_Disk_3.2.sea.bin http://download.info.apple.com/Apple_Support_Area/Apple_Software_Updates/English-North_American/Apple_II/Apple_II_Supplemental/Apple_II_System_Disk_3.2.sea.bin
wget -O files/external/appleii/Asimov.shk http://www.ninjaforce.com/downloads/Asimov.shk
wget -O files/external/appleii/MOUNTIT.SHK http://www.brutaldeluxe.fr/products/apple2gs/MOUNTIT.SHK
wget -O files/external/appleii/Marinetti3.0b8.po http://www.a2retrosystems.com/downloads/Marinetti3.0b8.po
wget -O files/external/appleii/PPPX.1.3d4.SHK http://www.apple2.org/marinetti/PPPX.1.3d4.SHK
wget -O files/external/appleii/dsk2file.shk http://www.dwheeler.com/6502/oneelkruns/dsk2file.zip
wget -O files/external/appleii/gshk11.sea http://www.nulib.com/library/gshk11.sea
wget -O files/external/appleii/shrinkit.sdk http://www.nulib.com/library/shrinkit.sdk
wget -O files/external/appleii/spectrum_gold_2mg.zip http://www.speccie.co.uk/speccie/software/spectrum_gold_2mg.zip
wget -O files/external/appleii/uthernet2ll.bxy http://www.speccie.co.uk/speccie/software/uthernet2ll.bxy
wget -O files/external/appleii/uthernetll.bxy http://www.speccie.co.uk/speccie/software/uthernetll.bxy

unset safeUrl samUrl snapUrl safeVer samVer snapVer
html=$(wget -qO- http://speccie.co.uk/speccie/Site/Download_Centre_files/widget1_markup.html)
safeUrl=$(echo "$html" | grep -i 'safe2.*bxy' | tr '<>' '\n' | grep href | cut -d '=' -f 2 | tr -d '"')
samUrl=$(echo "$html" | grep -i 'sam2.*bxy' | tr '<>' '\n' | grep href | cut -d '=' -f 2 | tr -d '"')
snapUrl=$(echo "$html" | grep -i 'snap.*bxy' | tr '<>' '\n' | grep href | cut -d '=' -f 2 | tr -d '"')
wget -O files/external/appleii/safe2.bxy "$safeUrl"
wget -O files/external/appleii/sam2.bxy "$samUrl"
wget -O files/external/appleii/snap.bxy "$snapUrl"

for gsosInstall in {1..3}; do
	activeDisk=0
	mkdir -p files/external/appleii/gsos60${gsosInstall}

	diskNames=( Install System.Disk SystemTools1 SystemTools2 Fonts synthLAB )
	if (( $gsosInstall == 1 )); then
		gsosURL="http://download.info.apple.com/Apple_Support_Area/Apple_Software_Updates/English-North_American/Apple_II/Apple_IIGS_System_6.0.1/"
		wget --max-redirect 0 -O files/external/appleii/gsos601/Disk_7_of_7-Apple_II_Setup.sea.bin http://download.info.apple.com/Apple_Support_Area/Apple_Software_Updates/English-North_American/Apple_II/Apple_IIGS_System_6.0.1/Disk_7_of_7-Apple_II_Setup.sea.bin
	elif (( $gsosInstall == 2 )); then
		gsosURL="http://mirrors.apple2.org.za/Apple%20II%20Documentation%20Project/Software/Operating%20Systems/Apple%20IIGS%20System/Disk%20Images/"
		diskNames=( Install System.Disk SystemTools1 SystemTools2 SystemTools3 Fonts1 Fonts2 synthLAB )
		diskWebNames=( Install System%20disk System%20tools%201 System%20tools%202 System%20tools%203 Fonts%201 Fonts%202 Synthlab )
	elif (( $gsosInstall == 3 )); then
		gsosURL="ftp://ftp.apple.asimov.net/pub/apple_II/images/gs/os/gsos/Apple_IIGS_System_6.0.3/"
	fi

	for diskname in ${diskNames[@]}; do
		outfile="files/external/appleii/gsos60${gsosInstall}/$diskname.po"
		(( activeDisk++ ))
		if (( $gsosInstall == 1 )); then
			wget --max-redirect 0 -O files/external/appleii/gsos601/"Disk_${activeDisk}_of_7-${diskname}.sea.bin" "${gsosURL}Disk_${activeDisk}_of_7-${diskname}.sea.bin"
		elif (( $gsosInstall == 2 )); then
			wget -O $outfile "$gsosURL/IIGS%20System%206.0.2%20-%20Disk%20${activeDisk}%20${diskWebNames[$activeDisk-1]}.po"
		elif (( $gsosInstall == 3 )); then
			wget -O $outfile "$gsosURL/$diskname.po"
		fi
	done
done
