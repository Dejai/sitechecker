import os
import sys
import time
import helper

# All possible input fles;
all_inputs = os.listdir("./data/inputs")

'''
	checkSite:
		Runs a CURL command for a given site and checks if a certain keyword is on it
		This indicates whether something is available or expected
'''
def checkSite(fileDetails, isTestRun=False):

	# Get the key details from the file Details
	filePath = fileDetails["filePath"]
	logFile = fileDetails["logPath"]
	tempPath = fileDetails["tempPath"]
	item = fileDetails["item"]
	store = fileDetails["store"]
	url = fileDetails["url"]
	check = fileDetails["check"]
	notify = fileDetails["notify"]
	fromEmail = fileDetails["fromEmail"]
	frequency = fileDetails["frequency"]
	frequency_in_secs = int(frequency) * 60
	# Get the credentials for the email
	credentials = helper.getCredentials(fromEmail)

	# Helper variables
	sep1 = "*"*100
	sep2 = "-"*90

	print("\nProcessing file: %s;\nChecking for %s at %s\n" % (filePath, item, store))

	# Add file name to heartbeat log
	if(isTestRun):
		helper.setHeartbeatLog(item, store, logFile)

	# Get the CURL command to be run
	curl_command = helper.getCurlCommand(url, tempPath)

	# Stores the last "state" of the check (1=available; 0=sold out); assumes unavailable by default
	curr_state = 0
	# Loop through
	keepRunning = True
	while keepRunning:
		print(sep1)
		print("\nChecking: %s" % (url))

		print(sep2)
		# Step 1: Run the CURL to get site response
		os.system(curl_command)
		time.sleep(5) # allow some time for site to respond
		print(sep2)
		# Step 2: Check if the value is present to indicate it is available
		isAvailable = helper.checkAvailability(tempPath, check)
		print("\n")

		# Step 3 - Send notification based on availability;
		if (isAvailable):
			msg = format("AVAILABLE: %s is available at %s" % (item, store))
			helper.notifyPeople(credentials, notify, msg)
			curr_state = 1
		elif (not isAvailable and curr_state == 1):
			msg = format("SOLD OUT: %s is no longer available at %s" % (item, store))
			helper.notifyPeople(credentials, notify, msg)
			curr_state = 0
		elif (isTestRun):
			msg = format("TEST MESSAGE: Checking for %s at %s" %(item, store))
			helper.notifyPeople(credentials, notify, msg)

		# # Step 4 - Save latest check to the log file
		helper.logResults(logFile, item, store, curr_state)

		if(isTestRun):
			keepRunning = False
			print("END OF TEST RUN")
			print(sep1)
			return

		print("Will check again in %s minute(s)" % (frequency))
		print(sep1)
		time.sleep(frequency_in_secs)

'''
	MAIN Function: 
		Ensure that a single file name is given
		Compare it against the list of actual files (must be the right name)
		If valid, get credentials, and the file details
		Then, run the checker for that file (i.e. "checkSite" function)
'''
def main():

	paramCount = len(sys.argv) #number of parameters

	# Only continue if file name was included
	if(paramCount >= 2):

		fileName = sys.argv[1] #the given file name
		isTestRun = True if ((len(sys.argv) == 3) and sys.argv[2] == "--test") else False

		# Only process if it is a valid file name
		if(fileName in all_inputs):
			
			fileDetails = helper.getInputFileDetails(fileName)

			print(isTestRun)
			# Run the function the check the site
			checkSite(fileDetails, isTestRun)
		else:
			helper.exiting("Not valid file name. Double check files in ./data/inputs/")
	else:
		helper.exiting("File name not provided")


# only run if file called directly
if __name__ == "__main__":
	main()

