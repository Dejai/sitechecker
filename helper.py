import re
from datetime import datetime
import smtplib
from email.message import EmailMessage
import getpass

# Clean a string
def __cleanString(value):
	return value.strip().replace("\t", "").replace("\n","")

# Send out the email
def __sendEmail(toEmail, msg, credentials):
	# Set the credentials
	fromEmail = credentials["email"]
	password = credentials["password"]

	# Print loggin
	print("Attempting to send message to %s" % (toEmail))
	print(credentials)

	# Setup email SMTP
	server=smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromEmail, password)
	# server.login("dancinglion.dev@gmail.com", "MoreThanA$nack@24")
	email_content =format("From %s To %s Subject Site Checker Notification \n %s" % (fromEmail, toEmail, msg))
	# email_content = "From dancinglion.dev@gmail.com To " + toEmail + " Subject Site Checker Notification \n" + msg
	server.sendmail("dancinglion.dev@gmail.com", toEmail, msg)
	# server.sendmail(fromEmail, toEmail, email_content)
	server.quit()


#---------------------------------------------------------------------------------------------------------

# Check if the given value is in the site output
def checkAvailability(tempFile, checkValue):
	available = False
	file = open(tempFile, "r+")
	for line in file:
		edited = re.sub(r'\"', '', line)
		available = checkValue in line
		if available:
			break
	file.close()
	# Return if it is available
	return available

# Take in user input for credentials
def getCredentials(emailAddress):
	# email = input("Enter email address to send notifications from: ")
	promptMessage = format("Enter password for %s (it wont't show as you type): " % (emailAddress))
	password = getpass.getpass(prompt=promptMessage)

	credentials = {
		"email": emailAddress,
		"password": password
	}

	return credentials

# Default function when exiting
def exiting(msg):
	print(msg)
	print("Goodbye")

# Takes a comma-separated list of people and sends them an 
def notifyPeople(creds, people, msg):
	splits = people.split(",")
	for person in splits:
		email = __cleanString(person)
		# __sendEmail(email, msg, creds)
		print(msg)

# Get the details from an Input file
def getInputFileDetails(fileName):

	# Set file path and output path
	filePath = "./data/inputs/" + fileName
	logPath = "./data/logs/" + fileName
	tempPath = "./data/temp/" + fileName

	# Dictionary of file details
	fileDetails = { "filePath": filePath, "logPath": logPath, "tempPath": tempPath }

	# Open the file and loop through it
	file = open(filePath, "r+")
	for line in file:
		splits = line.split("~")
		if len(splits) >= 2:
			key = __cleanString(splits[0])
			value = __cleanString(splits[1])
			isGoodPair = (key is not None) and (value is not None)
			if isGoodPair:
				fileDetails[key] = value
				
	#Close the file once done
	file.close()

	#Return teh details
	return fileDetails


# Get the CURL command used to check the site
def getCurlCommand(url, outputPath):
	agent = "\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36\""
	
	variables = (agent, outputPath, url)

	cmd = format("curl --user-agent %s -o %s %s" % variables)
	# cmd = "curl --user-agent " + self.agent + " -o " + self.output + " " + self.url
	return cmd


# Log the results of a check
def logResults(logFile, item, store, state):
		status = "AVAILABLE" if state == 1 else "sold out"
		log = open(logFile, "a+")
		current = datetime.now()
		logtime = current.strftime("%Y-%m-%d @%H:%M")
		variables = ()
		logline = format("%s : %s at %s == %s\n" % (logtime, item, store, status) )
		print(logline)
		log.write(logline)
		log.close()

# Add a file to heartbeat log file
def setHeartbeatLog(item, store, filePath):

	# Get if the file path is already in heartbeat
	alreadyThere = __checkHeartbeatLog(filePath)

	# Only add to the file if not already there
	if(not alreadyThere):
		log = open("./data/logs/_heartbeatLog.txt", "a+")
		logline = format("%s ~ %s ~ %s\n" % (item, store, filePath))
		log.write(logline)
		log.close()

# Check if a file is already in the heartbeat log
def __checkHeartbeatLog(filePath):
	alreadyThere = False
	log = open("./data/logs/_heartbeatLog.txt", "r")

	for line in log:
		splits = line.split(" ~ ")
		if len(splits) == 3:
			path = __cleanString(splits[2])
			givenPath = __cleanString(filePath)
			if(path == givenPath):
				alreadyThere = True
				return alreadyThere

	return alreadyThere		
