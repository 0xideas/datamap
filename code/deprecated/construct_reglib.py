from intitalise_parameters import test_list_validity, get_inputs

#takes a list of iid names, a list of county codes, and a searchcustomer ID parameter and returns a library of regular expressions
def get_reglib(iidlist = ['ip', 'iban','phone', 'email', 'phone', 'passport', 'idn','bankn', 'creditc', 'gender'], countries = ['BE'], searchcustomerID = False):
	
	#if the list of iids is empty, get list from user
	if len(iidlist) == 0:
		iidlist = input_iids()

	# construct regular expression
	reglib, __ = construct_reglib(iidlist, countries)

	#get regular expression for customerid from user
	if searchcustomerID:
		reglib['customerid'] = input_customerid()

	return reglib

#demands regex for customerid from user
def input_customerid():
	cond = True
	while cond:
		try:
			customeridRX = input('Please enter a regular expression to caputure customer IDs on your system. Start with an "r" to prevent escaping with "\\": ')
			returnvalue = eval(customeridRX)
			cond = False
		except:
			print('Please enter a valid regular expression for your customer IDs.')
	return returnvalue

#demands a list of iids from the user. checks their validity
def input_iids():
	cond = True
	while cond:
		stn_iids = standard_iids()
		print('Please enter the IIDs you wish to include. The options are: "ip", "email", "phone", "passport", "idn", "iban", "bankn", "creditc" and "gender". "customerid" is also valid, but you will have to enter a custom regular expression to search for them. Please enter "stop" to finish inputting.')
		list_of_IIDs = get_inputs()
		#if customeri
		cond = test_list_validity(list_of_IIDs, stn_iids + ['customerid'])
		if cond:
			print('Please enter a valid list.')

	return[iid.lower() for iid in list_of_IIDs]


#from a list of iid names (names are strings) and a list of two-letter country codes 
def construct_reglib(list_of_IID_names, countries):
	reglib1 = master_reglib()
	reglib2 = {}
	notincluded = []

	#copy the list so as to preserve the original list
	iidlisT = list(list_of_IID_names)

	#add international IID formats and remove them from list copy
	for iid in ['ip', 'email', 'iban']:
		if iid in iidlisT:
			reglib2[iid] = reglib1[iid]
			iidlisT.remove(iid)

	#if customerid is included in the list of iid names, get a regular expression from user
	if 'customerid' in iidlisT:
		reglib2['customerid'] = input_customerid()
		iidlisT.remove('customerid')

	#construct country iids and retrieve their regular expressions from master library of regular expressions
	for country in countries:
		for iid in iidlisT:
			country_iid = country + '_' + iid
			if country_iid in reglib1:
				reglib2[country_iid]= reglib1[country_iid]
			else:
				notincluded.append(country_iid)
	return reglib2, notincluded


#return the standard iids
def standard_iids():
	return ['ip', 'iban','phone', 'email', 'phone', 'passport', 'idn','bankn', 'creditc', 'gender']

#Return reference library of regular expressions for various iids and countries
def master_reglib():
	reglib = {
		'ip': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
		'iban': r'\b(?:[A-Za-z]{2}[0-9]{2})?(?:[ ]?[0-9]{4}){3}\b',
		'email': r'\b(?:[a-zA-Z0-9_\-\.]+)@(?:[a-zA-Z0-9_\-\.]+)\.(?:[a-zA-Z]{2,5})\b',
		'BE_phone': r'(?:\b0|\+)0?\d{1,3}[ ]?\d{1,3}[ ]?\d{2,3}(?:[ ]?\d{1,2}){1,2}\b',
		'BE_passport': r'\b[A-Z]{2}\d{6}\b',
		'BE_idn': r'\b(\d{3}-?\d{6}<?\d{1}-?\d{2,3})\b',
		'BE_bankn': r'\b[0-9](?:[ ]?[0-9]{4})(?:[ ]?[0-9]{2})\b',
		'BE_creditc': r'\b(?:\d{4}[\s_-]?){4}\b',
		'BE_gender':r'\bMale|male|Female|female\b'
		#MORE COUTNRIES GO HERE
		}

	return reglib