APKMole V1.0
============

ADB &amp; APKTool wrapper for application analysis located on an android device.
this tool automates interaction with your device using ADB and APKTool.

following operations supported on this version:

1. Analyse APP internal files and look for interesting files -
connecting to your device, imports all application files and looking for interesting files( for now only "db" and "xml").
all application's ever analysed stored on "./analyse" directory.
*requires rooted device.

2. Pull and decompile APK application files -
connecting to your device, imports APK file, decompiles the file using APKTool and saves the results on "./decompile" directory.

3. Analyse decompiled Manifest and invoke activities(rooted device) -
explores "./decompile" directory for decompiled applications and analysing Manifest file for activities to invoke.

4. Dump meminfo of an application -
displays meminfo of a specific application.

5. Bypass device authentication(password,pattern...) -
removes all *.key files from /data/system directory to bypass device authentication.


INSTALLATION
============
*******CHANGE ADB and APKTool VARIABLES*******

APKTool path - change APKTool path:(line 253)

	APKTOOL = "/home/example/Downloads/apktool_2.0.0rc3.jar"  # APKTOOL Directory
	
ADB path - change ADB path:(line 254)

	ADBTOOL = "/usr/bin/adb" # ADB Directory

	
	
*******DEPENDENCIES*******

1.libraries:

	pyadb
	os
	zipfile
	time
	random
	string
	tarfile
	shutil
	sys

*pyadb: https://github.com/sch3m4/pyadb

2.APKTool,ADB

*******next version TODO's*******

1. Minimalism in Code
2. More analysis operations.
