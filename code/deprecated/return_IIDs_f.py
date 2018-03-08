# functions to search text via regular expressions

#takes a list of strings and returns a list of strings that contains only the numbers in the input strings
def return_numbers(listofstrings):

	assert type(listofstrings) == list
	import re

	listoflist = [re.findall('[0-9]*', string) for string in listofstrings]
	return [ ''.join(lisT) for lisT in listoflist]



#takes a string to be searched, the name of the IID type and the regular expression
def return_IID(text, regex, IIDname = 'none given'):
	import re
	try:
		assert type(IIDname) == str
		assert type(regex) == str
		print('Searching for ' + IIDname + 's...') 
		IIDRX = re.compile(regex)
		IIDlist = IIDRX.findall(text)
		return(IIDlist)
	except AssertionError:
		print('IIDname and regex need to be strings.')
		return ('not successful')
	except re.error:
		print('The regular expression was not valid. To check its validity, go to https://regex101.com/')
		return ('not successful')
	except:
		print('Some other error. Did your string start with "r"?')
		return ('not successful')


def return_IIDs(text, searchID = True, searchpassports = True, searchphonenumbers = True, 
				searchemails = True, searchbankaccounts = True, searchcreditcards = True, 
				searchcustomerID = False):

	assert type(text) == str
	import os
	#from return_IIDs.py import return_IID, return_numbers

	if (searchcustomerID):
		#ask for a regular expression as input and search for matches to that regular expression
		condition = True
		while(condition):
			try:
				condition = False
				customeridformat = input('Please enter a regular expression to caputure customer IDs on your system. Start with an "r" to prevent escaping with "\\": ')
				print(customeridformat)
				customerids = []
				customerids = return_IID(text, 'customer ID', eval(customeridformat))
				print(customerids)
				if (customerids == 'not successful'):
					condition = True
			except:
				print('repeating procedure...')
		
		#take input on whether to strip customer IDs of all non-numerical characters
		condition = True
		while(condition):
			try:
				customeridsareonlynumbers = input('Please enter 1 if your customer IDs are composed only of numbers, and 0 otherwise ')
				customeridsareonlynumbers = int(customeridsareonlynumbers)
				assert(customeridsareonlynumbers == 1 or customeridsareonlynumbers == 0)
				condition = False
			except:
				print('Your input was not either 1 or 0.')

		#stripping customer Ids of non-numerical characters
		if (customeridsareonlynumbers):
			customerids = return_numbers(customerids)
				
	#searches for matches to the various regular expressions in the text
	if (searchID):
		ids = return_IID(text, r'\b(\d{3}-?\d{6}<?\d{1}-?\d{2,3})\b', 'ID')
		ids = return_numbers(ids)

	if (searchpassports):
		passports = return_IID(text, r'\b[A-Z]{2}\d{6}\b', 'passport')

	if (searchphonenumbers):
		phonenumbers = return_IID(text, r'(?:\b0|\+)0?\d{1,3}[ ]?\d{1,3}[ ]?\d{2,3}(?:[ ]?\d{2}){1,2}\b', 'phone number')
		phonenumbers = return_numbers(phonenumbers)

	if (searchemails):
		emails = return_IID(text, r'\b(?:[a-zA-Z0-9_\-\.]+)@(?:[a-zA-Z0-9_\-\.]+)\.(?:[a-zA-Z]{2,5})\b', 'email')

	if (searchbankaccounts):
		ibanbbans = return_IID(text, r'\b(?:[A-Za-z]{2}[0-9]{2})?(?:[ ]?[0-9]{4}){3}\b', 'IBAN and BBAN')
		bankaccounts = return_IID(text, r'\b[0-9](?:[ ]?[0-9]{4})(?:[ ]?[0-9]{2})\b', 'bank account number')
		bankaccounts = return_numbers(bankaccounts)

	if (searchcreditcards):
		creditcards = return_IID(text, r'\b(?:\d{4}[\s_-]?){4}\b', 'credit card number')
		creditcards = return_numbers(creditcards)
	
	# if searchcustomerID:
	# 	return([customerids, ids, passports, phonenumbers, emails, ibanbbans, bankaccounts, creditcards])
	# else:
	# 	return([ids, passports, phonenumbers, emails, ibanbbans, bankaccounts, creditcards])

	if searchcustomerID:
		return([list(set(customerids)), list(set(ids)), list(set(passports)), list(set(phonenumbers)), list(set(emails)), 
			list(set(ibanbbans)), list(set(bankaccounts)), list(set(creditcards))])
	else:
		return([list(set(ids)), list(set(passports)), list(set(phonenumbers)), list(set(emails)), 
			list(set(ibanbbans)), list(set(bankaccounts)), list(set(creditcards))])


	
	
	

