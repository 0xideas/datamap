# functions to search text via regular expressions
#

def return_numbers(listofstrings):

	assert type(listofstrings) == list
	import re

	listoflist = [re.findall('[0-9]*', string) for string in listofstrings]
	return [ ''.join(lisT) for lisT in listoflist]




def return_IID(text, IIDname, regex):
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
				askCustomerIDformat = False):

	assert type(text) == str
	import os
	#from return_IIDs.py import return_IID, return_numbers

	if (askCustomerIDformat):
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
		
		condition = True
		while(condition):
			try:
				customeridsareonlynumbers = input('Please enter 1 if your customer IDs are composed only of numbers, and 0 otherwise ')
				customeridsareonlynumbers = int(customeridsareonlynumbers)
				print(type(customeridsareonlynumbers))
				assert(customeridsareonlynumbers == 1 or customeridsareonlynumbers == 0)
				condition = False
			except:
				print('Your input was not either 1 or 0.')

		if (customeridsareonlynumbers):
			customerids = return_numbers(customerids)
				

	if (searchID):
		ids = return_IID(text, 'ID', r'\b(\d{3}-?\d{6}<?\d{1}-?\d{2,3})\b')
		ids = return_numbers(ids)

	if (searchpassports):
		passports = return_IID(text, 'passport', r'\b[A-Z]{2}\d{6}\b')

	if (searchphonenumbers):
		phonenumbers = return_IID(text, 'phone number', r'(?:\b0|\+)0?\d{1,3}[ ]?\d{1,3}[ ]?\d{2,3}(?:[ ]?\d{2}){1,2}\b')
		phonenumbers = return_numbers(phonenumbers)

	if (searchemails):
		emails = return_IID(text, 'email', r'\b(?:[a-zA-Z0-9_\-\.]+)@(?:[a-zA-Z0-9_\-\.]+)\.(?:[a-zA-Z]{2,5})\b')

	if (searchbankaccounts):
		ibanbbans = return_IID(text, 'IBAN and BBAN', r'\b(?:[A-Za-z]{2}[0-9]{2})?(?:[ ]?[0-9]{4}){3}\b')
		bankaccounts = return_IID(text, 'bank account number', r'\b[0-9](?:[ ]?[0-9]{4})(?:[ ]?[0-9]{2})\b')
		bankaccounts = return_numbers(bankaccounts)

	if (searchcreditcards):
		creditcards = return_IID(text, 'credit card number', r'\b(?:\d{4}[\s_-]?){4}\b')
		creditcards = return_numbers(creditcards)
	
	if askCustomerIDformat:
		return([customerids, ids, passports, phonenumbers, emails, ibanbbans, bankaccounts, creditcards])
	else:
		return([ids, passports, phonenumbers, emails, ibanbbans, bankaccounts, creditcards])
	
	
	

