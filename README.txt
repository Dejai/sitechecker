HOW TO USE THIS SCRIPT

Step 1: Configuration

	* Under the folder /data/inputs, you will have to add a .txt file. 
		> Recommended to name this file without any spaces (use underscores in replace of spaces)
	* This file should contains the following key details:
	
		item	    ~	[This should be a friendly name of the item]
		store	    ~	[Enter the name of the store/site where you are checking]
		url		    ~  	[Enter the full URL of the site you're checking]
		check	    ~	[Enter a specific word that is visible on the page when an item IS available]
		frequency   ~   [Enter a number for how frequently (in minutes) the script should check; ]
		notify	    ~	[Enter an email or a phone number with an email domain]
		fromEmail	~	[Enter the email account that will be used to send the notifications]
	
	* For the "notify" setting, you can lookup your phone provider's email domain
		> For example, Verizon = @vtext.com;
		> So if your number was 123-456-7890 ...
		> ... then your email would be 1234567890@vtext.com


Step 2: Update your Gmail Account

	* In order to send an email/text to notify you (i.e. the fromEmail setting) you will use your Gmail Account
	* Your account will need to updated to allow for "Less secure apps"
	* To do this, do the following:
		> Go to https://myaccount.google.com/
		> Go to tab = "Security"
		> Find section for "Less secure app access"
		> Make sure it is set to "On"
	* You can keep this setting for as long as you intend to use this script


Step 3: Test Your Setup:

	* Once you've done Step 2, you should be able to run a complete test of the checker
	* This test will check the site, and send a generic message to the email(s) listed in the "notify" setting
	* To run the test, use the following syntax (updating the "<name_of_file>" with the name of your file

		> python3 main.py <name_of_file> --test

		(note: be sure to update the placeholder "<name_of_file>" with the name of your file)
	
	* The output on the screen should indicate 
	* It will prompt you for your email password (used to ensure it can send an email from your account)
	* If it works, you will get a message shortly


Step 4: Test your Site

	* As a part of your testing, you should try running the script with a URL for a page where something IS available
	* This way, you can be sure your "check" value will work as expected
	* First, update the URL in your configuration input file (to be one for a page with something available)
	* Then, run the same test command as in Step 3


Step 5: Ready for the Real Thing

	* Once your test looks all good, you can put back your real URL 
	* Then, you can just run teh same script as in Step 3:

		> python3 main.py <name_of_file>

		(note: be sure to update the placeholder "<name_of_file>" with the name of your file)

	* NOTE: You should leave the script running on whatever machine you are using. So it can continue to check.


Step 6 (OPTIONAL): Heartbeat Page 

	* If you want to see the last time the script checked the site, you can start the Heartbeat page
	* Simply open a new Terminal window, and navigate to the folder
	* Then, run the following command:

		> python3 -m http.server 7000

		(note: if port number 7000 is already taken, you can use any other value in the thousands range)
	
	* This will start an HTTP server that allows you to open the "index.html" file in this folder.
	* It will show output of the last time a site was checked.

