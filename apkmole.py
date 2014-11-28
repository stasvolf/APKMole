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
C  = '\033[36m' # cyan

def analyseManifest(adb): #analyse Manifest file and invoke activities
	decompiledExists=0
	if not os.path.exists("./decompile"):
		print R+"[-] Didn't found ./dicompile folder.\nuse option 2 - decompile first"+W
		return
	print "[*] Application ready for analysis:" 
	decompiled=os.listdir("./decompile") 
	for filename in decompiled:
		if "decompile_" in filename:
			decompiledExists=1
			print C+filename[10:]+W
	if decompiledExists==0:
		print R+"\t[NONE]"+W
		return
	while(1):
		toAnalyse = raw_input("Enter package to analyse(q - quit):")
		if toAnalyse is 'q':
			return
		if "decompile_"+toAnalyse not in decompiled:
			continue
		else:
			break
	print "[*] Opening Manifest file.." ,
	try:
		mani = open("./decompile/decompile_"+toAnalyse+"/AndroidManifest.xml","r")
		print G+"\t[DONE]"+W
	except:
		print R+"\t[FAILED]"+W
	maniLines = mani.readlines()
	print "[*] Activities available:"
	for activity in maniLines:
		if "<activity" in activity:
			activitySplitted=activity.split(' ')
			for element in activitySplitted:
				if "name=" in element:
					element=element[:element.rindex(".")] + "/" + element[element.rindex("."):]
					print C+element[14:].strip("\"").strip("\">").strip("\"/>\n")+W
	while (1):
		activityChosen = raw_input("[#]Choose an activity to invoke(ex : com.whatsapp/.Main , q -quit):")
		if activityChosen is 'q':
			return
		print "[*] Invoking "+activityChosen+" activity.."
		actExe = adb.shell_command("su -c 'am start -n "+activityChosen+"'") #remove " su -c ' " to run as regular user
		if "Error" in actExe:
			print actExe[actExe.rfind("Error"):]
			
def bypass(adb): #unlock device authentication
	print "[*] Checking root...." ,
	supath = adb.find_binary("su")
	if "not found" not in supath:
		print G+"\t[DONE] - "+supath+W ,
		print W
	else:
		print R+"[-] didn't find su binary.."+W
		exit(-8)
	agree= raw_input("[*] type : \"on my own risk\" to continue, or anything else to quit\n")
	if agree == "on my own risk":
		removeKey  = supath+" -c 'rm /data/system/*.key'"
		print "[*] Removing key files..." ,
		print adb.shell_command(removeKey)
		try:
			adb.shell_command(removeKey)
			print G+"\t[DONE] - reboot..."+W
		except:
			print "\t[FAILED]"
	else:
		return
		

def appPrint(adb): # print device applications and resolve apk
	try:
		print "\n[*] Applications installed:\n"
		apps=adb.shell_command("pm list packages")
		print C+apps+W
	except:
		print R+"[-] Cant retrieve applications installed.."+W
		exit(-6)
	packageTarget=None
	while (1):
		packageTarget =  raw_input("[#] Enter package name to analyse(ex: com.whatsapp, q - quit):")
		if packageTarget is 'q':
			exit(-1)
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
	return (packageTarget,apkFile)

def meminfo(adb): # print meminfo
	packageTarget,apkFile=appPrint(adb)
	cmd = "dumpsys meminfo "+packageTarget
	print adb.shell_command(cmd)
	
	
def analyse(adb): #pull and analyse application folder from device
	packageTarget,apkFile=appPrint(adb)
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
	try:
		adb.shell_command(cmd)
		print G+"\t[DONE]"+W
	except:
		print R+"\t[FAILED] - can't create remote tar."+W
	print "[*] Retrieving remote file: "+tarname ,
	try:
		if not os.path.exists("./analyse/"):
			os.makedirs("./analyse/")
		if not os.path.exists("./analyse/"+packageTarget):
			os.makedirs("./analyse/"+packageTarget)
		adb.get_remote_file(tarname, './analyse/'+packageTarget+'/')
		print G+"\t[DONE]"+W
	except:
		print R+"\t[FAILED] - can't create directory."+W
		return
	print "[*] Removing remote file: "+tarname ,
	cmd = 'su -c \'rm %s\'' % tarname
	try:
		adb.shell_command(cmd)
		print G+"\t[DONE]"+W
	except:
		print R+"\t[FAILED] - can't remove remote tar."+W
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
				print R+"\t[FAILED] - copy to \"interesting_files\""+W
	print "[*] XML files:\n"	
	for member in tarA.getnames():
		if ".xml" in member:
			print "- "+C+member+W
			try:
				if not os.path.exists("./analyse/"+packageTarget+"/interesting_files/xml"):
					os.makedirs("./analyse/"+packageTarget+"/interesting_files/xml")
				shutil.copy("./analyse/"+packageTarget+"/"+member,"./analyse/"+packageTarget+"/interesting_files/xml")
			except:
				print R+"\t[FAILED] - copy to \"interesting_files\""+W
	print G+"\n[*] Checkout \"./analyse/"+packageTarget+"/interesting_files\" for more details.."+W
	tarA.close()

def decompileAPK(adb,APKTOOL): #pull and decomile apk file from device
	packageTarget,apkFile = appPrint(adb)
	apkF=apkFile.rstrip('\r\n')
	print "[*] Importing APK file.." ,
	try:
		if not os.path.exists("./decompile"):
			os.makedirs("./decompile")
	except:
		print R+"\t[FAILED] - can't create directory."+W
	importCMD="pull "+apkF+" ./decompile"
	try:
		pullAPK=adb.run_cmd(importCMD)
	except:
		print R+"\t[FAILED] - can't pull APK"+W
		return
	time.sleep(3) # enough time for apk to download..
	print G+"\t[DONE]"+W
	print "[*] all operations saved on ./decompile/decompile_"+apkF[10:-4] ,
	if not os.path.exists("./decompile/decompile_"+apkF[10:-4]):
		os.makedirs("./decompile/decompile_"+apkF[10:-4])
		try:
			exeCMD="java -jar "+APKTOOL+" decode ./decompile/"+apkF[10:]+" -f -o ./decompile/decompile_"+apkF[10:-4]
			os.system(exeCMD)
		except:
			print R+"\t[FAILED]"+W
	else:
		print R+"\n[-]FAILED (path already exists)"+W
	

def menu(adb,APKTOOL): #menu handeling
	while (1):
		print "\n\n----------------------------------------"
		print "1. Analyse APP internal files and look for interesting files(rooted device)"
		print "2. Pull and decompile APK application files"
		print "3. Analyse decompiled Manifest and invoke activities(rooted device)"
		print "4. Dump meminfo of an application"
		print "5. Bypass device authentication(password,pattern...)"
		option = raw_input("option(q - quit): ")
		if option is '1':
			analyse(adb)
		elif option is '2':
			decompileAPK(adb,APKTOOL)
		elif option is '3':
			analyseManifest(adb)
		elif option is '4':
			meminfo(adb)
		elif option is '5':
			bypass(adb)
		elif option is 'q':
			exit(-10)
		else:
			print "[-] Invalid option"
			
				
		
def main():
	APKTOOL = "/home/stas/Downloads/apktool_2.0.0rc3.jar"  # APKTOOL Directory
	ADBTOOL = "/usr/bin/adb" # ADB Directory
	print "#################################################################################"
	print "#                                APKmole V1.0                                   #"
	print "# ADB & APKTool wrapper for application analysis located on an android device   #"
	print "# Author: Stas Volfus                                                           #"
	print "# the author isn't responsible for any damage caused by using this tool         #"                                                                              #"
	print "#################################################################################"
	print "\nADB Path: "+ADBTOOL
	print "APKtool Path: "+APKTOOL    
	print "\n\n[*] Setting up ADB.."
	adb = ADB()
	adb.set_adb_path(ADBTOOL) 	# path to adb..
	print "[*] Checking APKTool path.." ,
	if os.path.isfile(APKTOOL) is False:
		print R+"\t[FAILED] - path not found."+W
		exit(-1)
	print G+"\t[OK]"+W
	print "[*] Checking ADB path.." ,
	if adb.check_path() is False:
		print "\t"+R+"\t[FAILED] - ADB path doesn't exists..\n"+W
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
	#more than one device..
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
	menu(adb,APKTOOL)
if __name__ == "__main__":
	main()
