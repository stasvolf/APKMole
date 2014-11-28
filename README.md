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

libraries:
	from pyadb import ADB
	import os
	import zipfile
	import time
	import random
	import string
	import tarfile
	import shutil
	from sys import stdin
	
pyadb: https://github.com/sch3m4/pyadb

next version TODO's:

1. Minimalism in Code
2. More analysis operations.
