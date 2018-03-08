"""
	Functions:
		validate_regex: test if a regular expression can be compiled and return bool. Option to pass update function
		get_inputs: take multiple inputs and return a list. Options for prompt, stopword to stop inputting, and max # of inputs
		remove_quotes: remove quotes from string in case of 'string-in_string'
		get_decision: display question and return bool based on answer
		test_list_validity: test if all items in list 1 are also in list 2.

"""
def validate_regex(regexvariable, inputfunction = None):
	try:
		re.compile(regexvariable)
		return True
	except:
		if inputfunction is not None:
			regexvariable = inputfunction()
		return False


def get_inputs(prompt = '\n', stopword = 'stop', maxins = None):
	results = []
	counter = 0
	while True:
		counter = counter + 1
		res = input(prompt)
		res = remove_quotes(res)
		if res == stopword:
			if len(results)==0:
				print('Please enter at least one item.')
			else:
				break
		else:
			results.append(res)
			if counter == maxins:
				break

	return(results)

def remove_quotes(string):
	try:
		temp = eval(string)
		if type(temp) == str:
			string = temp
	except:
		pass
	return string

def get_decision(question):
	while True:
		#print('Please type "Yes" or "No" to the following question: ')
		var = input(question)
		if ((var.lower() in 'yes') | (var.lower() in 'no')):
			break
			
	if (var.lower() in 'yes'):
		return True
	else:
		return False


def test_list_validity(inputlist, validvalues):
	co = True
	for item in inputlist:
		if item.lower() not in validvalues:
			co = False
	return(co)