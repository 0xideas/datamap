import re

def init_reglib(ip = True, email = True, phone = True, passport = True, idn = True, iban = True, bankn = True, creditc = True, gender = True):
	
	cond = True
	while cond:
		searchcustid = input('Search for customer ID? Please type "yes" or "no". ')
		searchcustid = searchcustid.lower() 

		if ((searchcustid == 'yes') | (searchcustid == 'no')):
			cond = False

	reglib = {}
	if searchcustid == 'yes':
		customeridRX = input('Please enter a regular expression to caputure customer IDs on your system. Start with an "r" to prevent escaping with "\\": ')
		reglib['customerid'] = eval(customeridRX)
	if ip:
		reglib['ip'] = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
	if email:
		reglib['email'] = r'\b(?:[a-zA-Z0-9_\-\.]+)@(?:[a-zA-Z0-9_\-\.]+)\.(?:[a-zA-Z]{2,5})\b'
	if phone:
		reglib['phone'] = r'(?:\b0|\+)0?\d{1,3}[ ]?\d{1,3}[ ]?\d{2,3}(?:[ ]?\d{1,2}){1,2}\b'
	if passport:
		reglib['passport'] = r'\b[A-Z]{2}\d{6}\b'
	if idn:
		reglib['idn'] = r'\b(\d{3}-?\d{6}<?\d{1}-?\d{2,3})\b'
	if iban:
		reglib['iban'] = r'\b(?:[A-Za-z]{2}[0-9]{2})?(?:[ ]?[0-9]{4}){3}\b'
	if bankn:
		reglib['bankn'] = r'\b[0-9](?:[ ]?[0-9]{4})(?:[ ]?[0-9]{2})\b'
	if creditc:
		reglib['creditc'] = r'\b(?:\d{4}[\s_-]?){4}\b'
	if gender:
		reglib['gender'] = r'\bMale|male|Female|female\b'

	return reglib

def get_matches(pattern, string):
    """Return list of matches based on regex pattern"""
    return [s for s in re.findall(pattern, string) if s!='']

#DIFFERENT FROM screen_text IN SANDBOX.PY
def scan_text(text):
	targetdict = init_reglib()

	matches = {}
	for t in targetdict:
		print('Searching for ' + t + '...')
		tmatches = get_matches(targetdict[t], text)
		matches[t] = tmatches

	return matches




##A BRIEF TEST OF THE FUNCTIONS ABOVE FOLLOWS

sample = """Message-ID: <2159683.1075839978592.JavaMail.evans@thyme>
Date: Mon, 31 Dec 2001 00:37:36 -0800 (PST)
From: pete.davis@enron.com
To: pete.davis@enron.com
Subject: Start Date: 12/30/01; HourAhead hour: 23;
Cc: albert.meyers@enron.com, bill.williams@enron.com, craig.dean@enron.com, 
	geir.solberg@enron.com, john.anderson@enron.com, 
	mark.guzman@enron.com, michael.mier@enron.com, pete.davis@enron.com, 
	ryan.slinger@enron.com
Mime-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
Bcc: albert.meyers@enron.com, bill.williams@enron.com, craig.dean@enron.com, 
	geir.solberg@enron.com, john.anderson@enron.com, 
	mark.guzman@enron.com, michael.mier@enron.com, pete.davis@enron.com, 
	ryan.slinger@enron.com
X-From: Davis, Pete </O=ENRON/OU=NA/CN=RECIPIENTS/CN=PDAVIS1>
X-To: Davis, Pete </O=ENRON/OU=NA/CN=RECIPIENTS/CN=PDAVIS1>
X-cc: Meyers, Albert </O=ENRON/OU=NA/CN=RECIPIENTS/CN=BMEYERS>, Williams III, Bill </O=ENRON/OU=NA/CN=RECIPIENTS/CN=BWILLIA5>, Dean, Craig </O=ENRON/OU=NA/CN=RECIPIENTS/CN=CDEAN2>, Solberg, Geir </O=ENRON/OU=NA/CN=RECIPIENTS/CN=GSOLBER>, Anderson, John </O=ENRON/OU=NA/CN=RECIPIENTS/CN=JANDERS3>, Guzman, Mark </O=ENRON/OU=NA/CN=RECIPIENTS/CN=MGUZMAN3>, Mier, Michael </O=ENRON/OU=NA/CN=RECIPIENTS/CN=MMIER>, Davis, Pete </O=ENRON/OU=NA/CN=RECIPIENTS/CN=PDAVIS1>, Slinger, Ryan </O=ENRON/OU=NA/CN=RECIPIENTS/CN=RSLINGER>
X-bcc: 
X-Folder: \ExMerge - Williams III, Bill\Schedule Crawler
X-Origin: WILLIAMS-W3
X-FileName: 



Start Date: 12/30/01; HourAhead hour: 23;  No ancillary schedules awarded.  No variances detected. 

    LOG MESSAGES:

PARSING FILE -->> O:\Portland\WestDesk\California Scheduling\ISO Final Schedules\2001123023.txt
###Cannot locate a Preferred or Revised_Preferred Schedule that matches the FINAL Individual Interchange Schedule.  Unable to assign deal number.
###Cannot locate a Preferred or Revised_Preferred Schedule that matches the FINAL Individual Interchange Schedule.  Unable to assign deal number.	Message-ID: <2987443.1075839981550.JavaMail.evans@thyme>
Date: Wed, 26 Dec 2001 09:39:49 -0800 (PST)
From: pete.davis@enron.com
To: pete.davis@enron.com
Subject: Start Date: 12/26/01; HourAhead hour: 8;
Cc: albert.meyers@enron.com, bill.williams@enron.com, craig.dean@enron.com, 
	geir.solberg@enron.com, john.anderson@enron.com, 
	mark.guzman@enron.com, michael.mier@enron.com, pete.davis@enron.com, 
	ryan.slinger@enron.com
Mime-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
Bcc: albert.meyers@enron.com, bill.williams@enron.com, craig.dean@enron.com, 
	geir.solberg@enron.com, john.anderson@enron.com, 
	mark.guzman@enron.com, michael.mier@enron.com, pete.davis@enron.com, 
	ryan.slinger@enron.com
X-From: Davis, Pete </O=ENRON/OU=NA/CN=RECIPIENTS/CN=PDAVIS1>
X-To: Davis, Pete </O=ENRON/OU=NA/CN=RECIPIENTS/CN=PDAVIS1>
X-cc: Meyers, Albert </O=ENRON/OU=NA/CN=RECIPIENTS/CN=BMEYERS>, Williams III, Bill </O=ENRON/OU=NA/CN=RECIPIENTS/CN=BWILLIA5>, Dean, Craig </O=ENRON/OU=NA/CN=RECIPIENTS/CN=CDEAN2>, Solberg, Geir </O=ENRON/OU=NA/CN=RECIPIENTS/CN=GSOLBER>, Anderson, John </O=ENRON/OU=NA/CN=RECIPIENTS/CN=JANDERS3>, Guzman, Mark </O=ENRON/OU=NA/CN=RECIPIENTS/CN=MGUZMAN3>, Mier, Michael </O=ENRON/OU=NA/CN=RECIPIENTS/CN=MMIER>, Davis, Pete </O=ENRON/OU=NA/CN=RECIPIENTS/CN=PDAVIS1>, Slinger, Ryan </O=ENRON/OU=NA/CN=RECIPIENTS/CN=RSLINGER>
X-bcc: 
X-Folder: \ExMerge - Williams III, Bill\Schedule Crawler
X-Origin: WILLIAMS-W3
X-FileName: 

"""

screen_text(sample)







