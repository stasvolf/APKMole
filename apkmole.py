#!/usr/bin/env python
try:
	from pyadb import ADB
	import os
	import zipfile
	import time
	import random
	import string
	import tarfile
	import shutil
	from sys import stdin
except ImportError,e:
	print "[f] Required module missing. %s" % e.args[0]
	exit(-1)
	
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
GR = '\033[37m' # gray
C  = '\033[36m' # cyan

			
def analyze(adb):
	try:
		print "\n[*] Applications installed:\n"
		apps=adb.shell_command("pm list packages")
		print C+apps+W
	except:
		print R+"[-] Cant retrieve applications installed.."+W
		exit(-6)
	packageTarget=None
	while (1):
		packageTarget =  raw_input("[#] Enter package name to analyse(q - quit):")
		if (packageTarget is 'q'):
			exit(-7)
		try:
			path2apk = "pm path "+packageTarget
			theApk=adb.shell_command(path2apk)
		except:
			print R+"[-] Failed to resolve APK file"+W
		if ("package:" in theApk):
			apkP=theApk.find("package:")
			apkFile=theApk[apkP+8:]
			print "[*] APK file found: "+apkFile ,
			break
		else:
			print R+"[-] Package not found."+W
	print "[*] Checking root...." ,
	supath = adb.find_binary("su")
	if "not found" not in supath:
		print G+"\t[DONE] - "+supath+W ,
		print W
	else:
		print R+"[-] didn't find su binary.."+W
		exit(-8)
	if os.path.exists("./analyse/"+packageTarget):
		print R+"[-] path exists..aborting."+W
		return
	print "[*] Importing app library.." ,
	tarname = '/sdcard/APKMole_' + ''.join(random.choice(string.letters) for i in xrange(10)) + '.tar'
	print G+"\t[DONE]"+W
	print "[*] Creating remote tar file: "+W+tarname ,
	cmd = supath+" -c 'tar -c /data/data/"+packageTarget+" -f "+tarname+"'"
	adb.shell_command(cmd)
	print G+"\t[DONE]"+W
	print "[*] Retrieving remote file: "+tarname ,
	if not os.path.exists("./analyse/"):
		os.makedirs("./analyse/")
	if not os.path.exists("./analyse/"+packageTarget):
		os.makedirs("./analyse/"+packageTarget)
	adb.get_remote_file(tarname, './analyse/'+packageTarget+'/')
	print G+"\t[DONE]"+W
	print "[*] Removing remote file: "+tarname ,
	cmd = 'su -c \'rm %s\'' % tarname
	adb.shell_command(cmd)
	print G+"\t[DONE]"+W
	print G+"[*] TAR file saved on: ./analyse/"+packageTarget+"/"+packageTarget+W
	print "[*] Extracting content.." , 
	try:
		tarA = tarfile.open("./analyse/"+packageTarget+"/"+tarname[8:])
		for member in tarA.getmembers():
			tarA.extract(member,path="./analyse/"+packageTarget)
		
		print G+"\t[DONE]"+W
	except:
		print R+"\t[FAILED]"+W
	print "[*] looking for interesting files.."
	print "[*] DB files:\n" ,
	for member in tarA.getnames():
		if ".db" in member:
			print "- "+C+member+W
			try:
				if not os.path.exists("./analyse/"+packageTarget+"/interesting_files/db"):
					os.makedirs("./analyse/"+packageTarget+"/interesting_files/db")
				shutil.copy("./analyse/"+packageTarget+"/"+member,"./analyse/"+packageTarget+"/interesting_files/db")
			except:
				print R+"\t[FAILED] - couldn't copy to \"interesting_files\""+W
	print "[*] XML files:\n"	
	for member in tarA.getnames():
		if ".xml" in member:
			print "- "+C+member+W
			try:
				if not os.path.exists("./analyse/"+packageTarget+"/interesting_files/xml"):
					os.makedirs("./analyse/"+packageTarget+"/interesting_files/xml")
				shutil.copy("./analyse/"+packageTarget+"/"+member,"./analyse/"+packageTarget+"/interesting_files/xml")
			except:
				print R+"\t[FAILED] - couldn't copy to \"interesting_files\""+W
	print G+"\n[*] Checkout \"./analyse/"+packageTarget+"/interesting_files\" for more details.."+W
	tarA.close()

def decompile(adb):
	try:
		print "\n[*] Applications installed:\n"
		apps=adb.shell_command("pm list packages")
		print C+apps+W
	except:
		print R+"[-] Cant retrieve applications installed.."+W
		exit(-6)
	packageTarget=None
	while (1):
		packageTarget =  raw_input("[#] Enter package as target(q - quit):")
		if (packageTarget is 'q'):
			exit(-7)
		try:
			path2apk = "pm path "+packageTarget
			theApk=adb.shell_command(path2apk)
		except:
			print R+"[-] Failed to resolve APK file"+W
		if ("package:" in theApk):
			apkP=theApk.find("package:")
			apkFile=theApk[apkP+8:]
			print "[*] APK file found: "+apkFile ,
			break
		else:
			print R+"[-] Package not found."+W
	apkF=apkFile.rstrip('\r\n')
	print "[*] Importing APK file.." ,
	if not os.path.exists("./decompile"):
		os.makedirs("./decompile")
	importCMD="pull "+apkF+" ./decompile"
	pullAPK=importLib=adb.run_cmd(importCMD)
	time.sleep(3) # enough time for apk to download..
	print G+" [DONE]"+W+"\n[*] Extracting to: /decompile/decompile_"+apkF[10:]+".." ,
	if not os.path.exists("./decompile/decompile_"+apkF[10:]):
		os.makedirs("./decompile/decompile_"+apkF[10:])
		try:
			apk=zipfile.ZipFile("./decompile/"+apkF[10:])
			apk.extractall("./decompile/decompile_"+apkF[10:])
			print G+"\t[DONE]"+W
			print G+"1. use dex2jar to decompile classes.dex file."
			print "2. use jd-gui to reflect source.."+W
		except:
			print R+"\t[FAILED (APK not found)]"+W
	else:
		print R+"\n[FAILED (already exists)]"+W
def pull(adb, apkF):
	print "[*] Pulling APK.."
	
def pullApp(apkF):
	print "pilling app"
	

def menu(adb):
	while (1):
		print "\n\n----------------------------------------"
		print "1. Analyze APP internal files(rooted device only)"
		print "2. Pull and prepare for decompilation"
		print "3. Pull APK"
		print "4. Pull application folder"
		option = raw_input("option(q - quit): ")
		if option is '1':
			analyze(adb)
		elif option is '2':
			decompile(adb)
		elif option is '3':
			pull(apkFile)
		elif option is '4':
			pullApp(apkFile)
		elif option is 'q':
			exit(-10)
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
		if error is 2:
			print R+"[-] You haven't enought permissions."+W
			exit(-3)
		print "\t"+G+"[OK]"+W
		dev = 1
		if len(devices) == 0:
			print C+"[-] No devices detected! waiting for devices.."+W
			adb.wait_for_device()
			error,devices = adb.get_devices()
			continue
	# devices...
	i = 0
	for dev in devices:
		print "\t%d: %s" % (i,dev)
		i += 1
	#more that one device..
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
		print R+"\n[-] Error:\t- ADB: %s\t - Python: %s" % (adb.get_error(),e.args)
		exit(-5)
	print "\n[+] Using \"%s\" as target device" % devices[dev]
	menu(adb)
if __name__ == "__main__":
	main()
