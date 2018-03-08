from construct_reglib import get_reglib


#asks user to input at least one path for scanning
def get_basepaths():
	print("Please enter the paths to the folders you wish to scan in\nthe order you wish to scan them. Enter 'stop' if you have \n entered all paths you want to scan")
	basepaths = get_inputs()
	return basepaths

#collects input and returns a list. Between each input the prompt is shown.
#the entering the stopword returns the inputs
#maxins is the maximum number of inputs allowed
def get_inputs(prompt = '\n', stopword = 'stop', maxins = None):
	results = []
	cond = True
	counter = 0
	while cond:
		counter = counter + 1
		res = input(prompt)
		res = remove_quotes(res)
		if res == stopword:
			if len(results)==0:
				print('Please enter at least one item.')
			else:
				cond = False
		else:
			results.append(res)
			if counter == maxins:
				cond = False

	return(results)

def remove_quotes(string):
	try:
		temp = eval(string)
		if type(temp) == str:
			string = temp
	except:
		pass
	return string

#returns the set of valid countries
def get_valid_countries():
	return ('be', 'nl', 'fr', 'uk', 'de')

#returns the set of valid languages
def get_valid_languages():
	return ('english', 'french', 'dutch', 'german')

#asks user to input the countries of the individuals the data is about, to determine the regular expressions that should be used
def get_countries():
	valid_countries = get_valid_countries()
	cond= True
	#while loop runs until the user enters a valid subset of the valid countries
	while cond:
		print('Please enter country codes from the list ["BE","NL","FR","UK","DE"]:\n')
		countries = get_inputs(maxins = 5)
		print(countries)
		cond = test_list_validity(countries, valid_countries)
		if cond:
			print('Please enter a valid list.')

	return(countries)

#takes a list and a list of possible correct values and checks that every item in the list is in the list of possible correct values
#returns True or False
def test_list_validity(inputlist, validvalues):
	try:
		for item in inputlist:
			assert item.lower() in validvalues
		cond = False
	except:
		cond = True
	return(cond)

#asks user to input the languages the document base is in
def get_languages():
	valid_languages = get_valid_languages()
	cond= True
	while cond:
		print('Please enter languages from ["dutch", "french", "english", "german"]:\n')
		languages = get_inputs(maxins = 4)
		cond = test_list_validity(languages, valid_languages)
		if cond:
			print('Please enter a valid list.')
	return(languages)	

#collects the basepaths, countries and languages
#returns a dictionary of these
def get_settings():
	basepaths = get_basepaths()
	countries = get_countries()
	languages = get_languages()
	return({'basepaths': basepaths, 'countries': countries, 'languages': languages})


#NO TEST FOR PATHS YET
def validate_settings(settings):
	valid_languages = get_valid_languages()
	valid_countries = get_valid_countries()

	cond = test_list_validity(settings['languages'], valid_languages)
	if cond:
		settings['languages'] = get_languages()

	cond = test_list_validity(settings['countries'], valid_countries)
	if cond:
		settings['countries'] = get_countries()	

	print(settings)
	return(settings)

def initialise_parameters(settings = {'basepaths':['/home/leon/live/sample/'], 'countries':['BE'], 'languages':['english']}, 
	iids = ['ip', 'iban','phone', 'email', 'phone', 'passport', 'idn','bankn', 'creditc', 'gender'], 
	customerid = '', reglib = {}):
	
	#INITIALISING SETTINGS
	#only if an empty directionary is passed to the settings variable can the settings be input during the program
	if len(settings) == 0:
		settings = get_settings()
	#else test that the languages and countries entered are valid. If they are not the user is asked to enter valid lists
	else:
		settings = validate_settings(settings = settings)

	#INITIALISING REGLIB
	#if no library of regular expressions was passed to the function
	if len(reglib) == 0:
		# and customerid is not in the list of iids (it isn't by default)
		inputcustomerID = False
		if 'customerid' in iids:
			inputcustomerID = True
			iids.remove('customerid')

		#the standard regular expression library is generated, if iids was not set to []
		reglib = get_reglib(iidlist = iids, countries = settings['countries'], searchcustomerID = inputcustomerID)

	#if a library of regular expressions was passed to the function then this is the library used
	else:
		assert type(reglib) == dict
		reglib = reglib

	#if a regular expression for customerid was passed to the function, it is added to the regex library
	if len(customerid) > 0:
		reglib['customerid'] = customerid

	return(settings, reglib)

















#Not currently needed
#takes a question to be asked and returns True if the answer is yes and False if the answer is no
def get_decision(question):
	cond = True
	while cond:
		print('Please type "Yes" or "No" to the following question: ')
		var = input(question)
		var = var.lower() 
		if ((var == 'yes') | (var == 'no')):
			cond = False
	if (var == 'yes'):
		var = True
	else:
		var = False
	return(var)