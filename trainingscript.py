#WRITTEN BY PAUL KASSOVIC FOR MEDRIO, INC.
#EMAIL: PKASSOVIC@MEDRIO.COM
#FREELY REDISTRIBUTABLE

import requests # easy HTTP requests
import xml.dom.minidom as minidom # beautify XML
import time  # add pauses

# WELCOME
print ("\n", 10 * "-", "Welcome to Medrio\'s API Training Script!", 10 * "-")
time.sleep(1)
print ('\nThis tool will assist you in making export requests from your Medrio study!\n')
print (62 * "-" + "\n")
time.sleep(1)

# DEFINE API KEY
def api_key_menu():
	global api_key
	api_key = input("Please enter your study API key: ")
	print ("" + api_key + "has been saved.")

# DEFINE INSTANCE
def server_menu():
	global server
	server = input("Please enter your study server instance: ")
	print ("" + server + "has been saved.")

# READ XML FILE
def print_payload():
	with open(filename, 'rb') as x:
		checkodm = x.read()
		print (minidom.parseString(checkodm).toprettyxml())

# LOAD XML FILE
def read_payload():
	global uploadfile
	global readfile
	global filename
	global request
	filename = input("Please enter your payload file name and include the .xml extension: ")
	uploadfile = open(filename, 'r')
	readfile = uploadfile.read()
	if "ExportODM" in readfile:
		request = "ExportODM"
		print ("\nI see that you're trying to run an ODM Export...\n")
		print ("Reading ODM XML Payload...\n")
		#print_payload() # show if you want to print payload in CMD window
	else:
		request = "ExportFileConfig"
		print ("\nI see that you're trying to run an ExportFileConfig...")
		print ("Reading File Export Config XML Payload...\n")
		#print_payload()

# MAKE HTTP REQUEST
def httprequest():
	global jobidstring
	headers = {'Content-Type': 'application/xml'}
	getexport = requests.post('https://'+server+'.api.medrio.com/v1/MedrioServiceV1.svc/Studies/'+api_key+'/jobs/'+request+'', data=readfile, headers=headers)
	postexport = getexport.text
	temp = minidom.parseString(postexport)
	#print (temp.toprettyxml()) # PRINT XML CALLBACK
	getmessage = (temp.getElementsByTagName('Message')[0])
	messagestring = getmessage.firstChild.nodeValue
	if messagestring == "Success":
		getjobid = (temp.getElementsByTagName('JobID')[0])
		getstatus = (temp.getElementsByTagName('Status')[0])
		getcode = (temp.getElementsByTagName('Code')[0])
		codestring = getcode.firstChild.nodeValue
		jobidstring = getjobid.firstChild.nodeValue
		statusstring = getstatus.firstChild.nodeValue
		print ("\nRequest: " + statusstring + "" )
		print ("Status: " + codestring + "")
		print ("JobID: " + jobidstring + "\n")
	else:
		print ("\nRequest failed: "+messagestring+'')


def jobrequest():
	global filestring
	print ("\nNow making request to JobID: " + jobidstring + "")
	print (64 * "-")
	print ("FETCHING JOB - THIS MAY TAKE A WHILE DEPENDING ON SIZE OF STUDY")
	print (64 * "-")
	while True:
		getjob = requests.get('https://'+server+'.api.medrio.com/v1/MedrioServiceV1.svc/Studies/'+api_key+'/jobs/'+jobidstring+'')
		getjobtext = getjob.text
		temp2 = minidom.parseString(getjobtext)
		getstatus = (temp2.getElementsByTagName('Status')[0])
		statusstring = getstatus.firstChild.nodeValue
		if statusstring == "Successful":
			break
	print ("File has now successfuly been generated\n")
	getfile = (temp2.getElementsByTagName('File')[0])
	filestring = getfile.firstChild.nodeValue
	
def grabfile():
	filename = input("Please enter an export file name: ")
	print ("\nDownloading file...")
	r = requests.get(filestring, stream=True)
	with open(filename+".zip", "wb") as code:
		code.write(r.content)
	print (40 * "-")
	print ("File successfully downloaded!")
	print (40 * "-")


#SAMPLE SETTINGS
#COMMENT THE NEXT TWO LINES FOR LIVE
api_key = "AUoYe5PfGNPmTqerFEti"
server = "na4"

#api_key_menu()
#server_menu()
read_payload()
httprequest()
jobrequest()
grabfile()