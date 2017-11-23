# functions to search text via regular expressions
#

def return_numbers(listofstrings):

    assert type(listofstrings) == list
    import re

    listoflist = [re.findall('[0-9]*', string) for string in listofstrings]
    return [ ''.join(lisT) for lisT in listoflist]
    


def return_IDs(text, askCustomerIDformat = False):
    
    assert type(text) == str
    
    import re
    idRX = re.compile(r'\b(\d{3}-?\d{6}<?\d{1}-?\d{2,3})\b')
    passportRX = re.compile(r'\b[A-Z]{2}\d{6}\b')
    phoneRX = re.compile(r'(?:\b0|\+)0?\d{1,3}[ ]?\d{1,3}[ ]?\d{2,3}(?:[ ]?\d{2}){1,2}\b')
    emailRX = re.compile(r'\b(?:[a-zA-Z0-9_\-\.]+)@(?:[a-zA-Z0-9_\-\.]+)\.(?:[a-zA-Z]{2,5})\b')
    ibanbbanRX = re.compile(r'\b(?:[A-Za-z]{2}[0-9]{2})?(?:[ ]?[0-9]{4}){3}\b')
    bankaccountRX = re.compile(r'\b[0-9](?:[ ]?[0-9]{4})(?:[ ]?[0-9]{2})\b')
    creditcardRX = re.compile(r'\b(?:\d{4}[\s_-]?){4}\b')
    	
    if (askCustomerIDformat):
	    condition = askCustomerIDformat
	    while (condition):
	    	try:
	    		customeridformat = input('Please enter a regular expression to caputure customer IDs on your system: ')
	    		assert(type(customeridformat)==str)
	    		customeridRX = re.compile(r + customeridformat)
	    		condition = False
	    	except AssertionError:
	    		print('Please make sure that the regular expression submitted in quotes.')
	    	except:
	    		print('Please make sure your regular expression is valid. To check its validity, go to https://regex101.com/')
    	
	    condition = True
	    while(condition):
	    	try:
	    		customeridsareonlynumbers = input('Please enter 1 if your customer IDs are composed only of numbers, and 0 otherwise')
	    		assert(customeridsareonlynumbers == (1 or 0))
	    		condition = False
	    	except:
	    		print('Your input was not either 1 or 0.')

  	


    	print('Searching for customer IDs...')
    	customerids = customeridRX.findall(text)

    print('Searching for IDs...')
    ids = idRX.findall(text)
    print('Searching for passport numbers...')
    passports = passportRX.findall(text)
    print('Searching for phone numbers...')
    phones = phoneRX.findall(text)
    print('Searching for email addresses...')
    emails = emailRX.findall(text)
    print('Searching for IBAN, BBAN numbers...')
    ibanbbans = ibanbbanRX.findall(text)
    print('Searching bank account numbers....')
    bankaccounts = bankaccountRX.findall(text)
    print('Searching for credit cards...')
    creditcards = creditcardRX.findall(text)
    
    print('standardising results')
    if customeridsareonlynumbers:
    	print('customer IDs')
    	customerids = return_numbers(customerids)

    print('ids')
    ids = return_numbers(ids)
    #passports should be in the proper format
    print('phones')
    phones = return_numbers(phones)
    #emails too
    print('ibanbbans')
    ibanbbans = return_numbers(ibanbbans)
    print('bankaccounts')
    bankaccounts = return_numbers(bankaccounts)
    print('creditcards')
    creditcards = return_numbers(creditcards)
    
    if askCustomerIDformat:
    	return([customerids, ids, passports, phones, emails, ibanbbans, bankaccounts, creditcards])
    else:
    	return([ids, passports, phones, emails, ibanbbans, bankaccounts, creditcards])
    
    
    

