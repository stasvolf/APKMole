#!/usr/bin/env python
try:
	from pyadb import ADB
	import os
	import zipfile
	import time
	
except ImportError,e:
	print "[f] Required module missing. %s" % e.args[0]
	exit(-1)
	
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
GR = '\033[37m' # gray
C  = '\033[36m' # cyan


	
def analyze(adb, packageTarget):
	print "[*] Importing app library.."
	print "soon...."
def decompile(adb,apkF):
	apkF=apkF.rstrip('\r\n')
	print "[*] Importing APK file.." ,
	if not os.path.exists("./decompile"):
		os.makedirs("./decompile")
	importCMD="pull "+apkF+" ./decompile"
	pullAPK=importLib=adb.run_cmd(importCMD)
	time.sleep(2)
	print G+" [DONE]"+W+"\n[*] Extracting to: /decompile/decompile_"+apkF[10:]+".." ,
	if not os.path.exists("./decompile/decompile_"+apkF[10:]):
		os.makedirs("./decompile/decompile_"+apkF[10:])
		try:
			apk=zipfile.ZipFile("./decompile/"+apkF[10:])
			apk.extractall("./decompile/decompile_"+apkF[10:])
			print G+"\t[DONE]"+W
			print R+"1. use dex2jar to decompile classes.dex file."
			print "2. use jd-gui to reflect source.."+W
		except:
			print R+"\t[FAILED (APK not found)]"+W
	else:
		print R+"[FAILED (already exists)]"+W
def pull(adb, apkF):
	print "[*] Pulling APK.."
	
def pullApp(apkF):
	print "pilling app"
	

def getApps(adb):
	try:
		print "\n[*] Applications installed:\n"
		apps=adb.shell_command("pm list packages")
		print C+apps+W
	except:
		print R+"[-] Cant retrieve applications installed.."+W
		exit(-6)
	packageTarget=None
	while (1):
		packageTarget =  raw_input("[#] Enter package name to target(q - quit):")
		try:
			path2apk = "pm path "+packageTarget
			theApk=adb.shell_command(path2apk)
		except:
			print R+"[-] Failed to resolve APK file"+W
		if ("package:" in theApk):
			apkP=theApk.find("package:")
			apkFile=theApk[apkP+8:]
			print G+"[*] APK file found: "+apkFile+W
			break
		else:
			print R+"[-] Package not found."+W
		if (packageTarget is'q'):
			exit(-7)
	print "\n----------------------------------------"
	print "1. Analyze internal files"
	print "2. Pull and prepare for decompilation"
	print "3. Pull APK"
	print "4. Pull application folder"
	option = raw_input("option: ")
	if option is '1':
		analyze(adb,packageTarget)
	elif option is '2':
		decompile(adb,apkFile)
	elif option is '3':
		pull(apkFile)
	elif option is '4':
		pullApp(apkFile)
	else:
		print "[-] Invalid option"
			
				
		
def main():
	print "############################################################"
	print "#APKmole - Analyze application on yor android device       #"
        print "#                                                          #"                 
        print "#                                                          #"
        print "#                                                          #"                 
        print "############################################################"
	print "\n\n[*] Setting up ADB.."
	adb = ADB()
	#adb.set_adb_path('~/android-sdk-linux/platform-tools/adb')
	adb.set_adb_path('/usr/bin/adb') 	# path to adb..
	print "[*] Checking ADB path.." ,
	if adb.check_path() is False:
		print "\t"+R+"[FAILED - ADB path doesn't exists..]\n"+W
		exit(-2)
	print "\t"+G+"[OK]"+W
	print "[*] Restarting ADB server.." ,
	adb.restart_server()
	if adb.lastFailed():
		print "\t"+R+"[ERROR]"+W
		exit(-3)
	print "\t"+G+"[OK]"+W
	dev = 0
	while dev is 0:
		print "[*] Detecting devices..." ,
		error,devices = adb.get_devices()
		if error is 1:
			# no devices connected
			print "[-] No devices connected"
			print "[*] Waiting for devices..." ,
			adb.wait_for_device()
			continue
		elif error is 2:
			print "[-] You haven't enought permissions."
			exit(-3)
		print "\t"+G+"[OK]"+W
		dev = 1
	# this should never be reached
	if len(devices) == 0:
		print R+"[-] No devices detected!"
		exit(-4)
	# show detected devices
	i = 0
	for dev in devices:
		print "\t%d: %s" % (i,dev)
		i += 1
	# if there are more than one devices, ask to the user to choose one of them
	if i > 1:
		dev = i + 1
		while dev < 0 or dev > int(i - 1):
			print "\n[+] Select target device [0-%d]: " % int(i - 1) ,
			dev = int(stdin.readline())
	else:
		dev = 0
	try:
		adb.set_target_device(devices[dev])
	except Exception,e:
		print "\n[!] Error:\t- ADB: %s\t - Python: %s" % (adb.get_error(),e.args)
		exit(-5)
	print "\n[+] Using \"%s\" as target device" % devices[dev]
	getApps(adb)
if __name__ == "__main__":
	main()
