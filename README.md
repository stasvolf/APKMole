APKMole V1.0
============

ADB &amp; APKTool wrapper for application analysis located on an android device.
this tool automates interaction with your device using ADB and APKTool.

following operations supported on this version:

1.<b> Analyse APP internal files and look for interesting files </b>-<br>
connecting to your device, imports all application files and looking for interesting files( for now only "db" and "xml").
all application's ever analysed stored on "./analyse" directory.
*requires rooted device.

2. <b>Pull and decompile APK application files </b>-<br>
connecting to your device, imports APK file, decompiles the file using APKTool and saves the results on "./decompile" directory.

3. <b>Analyse decompiled Manifest and invoke activities(rooted device) </b>-<br>
explores "./decompile" directory for decompiled applications and analysing Manifest file for activities to invoke.

4. <b>Analyse decompiled Manifest file </b>-<br> analyse Manifest of decompiled application map all activities and providers.

5.<b> Dump meminfo of an application </b>-<br>
displays meminfo of a specific application.

6. <b>Bypass device authentication(password,pattern...) </b>-<br>
removes all *.key files from /data/system directory to bypass device authentication.


<h3>INSTALLATION</h3>

*******CHANGE ADB and APKTool VARIABLES*******

APKTool path - change APKTool path:(line 253)

	APKTOOL = "/home/example/Downloads/apktool_2.0.0rc3.jar"  # APKTOOL Directory
	
ADB path - change ADB path:(line 254)

	ADBTOOL = "/usr/bin/adb" # ADB Directory

	
	
<h3>DEPENDENCIES</h3>

1.libraries:

	pyadb
	os
	zipfile
	time
	random
	string
	tarfile
	shutil
	xml
	sys

*pyadb: https://github.com/sch3m4/pyadb

2.APKTool,ADB

<h3>USAGE<h3>
1. Enable ADB on device.<br>
2. Connect device and run:
python apkmole.py


