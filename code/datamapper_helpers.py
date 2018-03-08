"""
	functions that support the functionality of datamapper.py
	
	functions:
		split_many: takes a text or a list of texts and returns a list of texts that are either the size of maxlength or number nparts*# of texts in input
		split_by: takes a text or a list of texts and a criterion and returns a list of the parts of each text in the list split by that criterion
		split_text: splits text by criteria passed to it, and then any parts of texts so that no part is longer than maxlength
		remove_empty: removes empty strings from lists of strings
		extract_text: opens a file and returns its text
		get_matches: returns the matches to a regular expression in a string
		generate_pathfile: generates file of list of paths dependent on the input path

"""




import os
import re

def split_many(text, maxlength = 1000, nparts = None):
	if type(text) == str:
		text = [text]

	splittext = []
	for part in text:
		if nparts is None:
			nparts = round((len(part)/maxlength)+0.5)
		else:
			maxlength = round((len(part)/nparts)+0.5)

		for x in range(nparts):
			splittext.append(part[x*maxlength:(x+1)*maxlength])

	return splittext

def split_by(text, criterion = '\n\n'):
	if type(text) == str:
		text = [text]

	splittext = []
	for part in text:
		splittext.extend(part.split(criterion))

	return splittext

def split_text(text, maxlength = 1000, criteria = ['\n\n']):
	if type(text) == str:
		text = [text]

	for criterion in criteria:
		text = split_by(text, criterion)

	if max(len(part) for part in text) > maxlength:
		newtext = []
		for part in text:
			if len(part) > maxlength:
				newtext.extend(split_many(part, maxlength))
			else:
				newtext.append(part)
	else:
		newtext = text
	
	return newtext


def remove_empty(textlist):
	return [text for text in textlist if text != '']



def extract_text(path, maximum = 200 * 1000 * 1000):
	if not is_executable(path):
		if os.path.getsize(path) < maximum:
			try:
				with open(path, 'r') as file:
					text = file.read()
			except:
				text = 'cannot_open'
				print('File at ' + path + ' could not be opened.')
		else:
			text = 'too_large'
			print('File at ' + path + ' is too large.')
	else:
		text = 'executable'
		print('File at ' + path + ' is executable and will not be opened')

	return text



def is_executable(path):
	return os.access(path, os.X_OK)  

def get_matches(pattern, string):
	"""Return list of matches based on regex pattern"""
	return [s for s in re.findall(pattern, string) if s!='']




#THIS WORKS
def generate_pathfile(outputpath, paths, pos_conditions = [], neg_conditions = ['/.'], filepaths = True, dirpaths = False):
	"""
		1. the output file is created
		2. the output file is opened again in append mode
		3. os walks the dependency tree
		4. if one of the positive conditions is not met, the path is not written to file
		5. if one of the negative conditions is met, the path is not written to file
		6. the path to the directory or the file is written to the output file
	"""

	if type(paths) == str:
		paths = [paths]

	with open(outputpath, 'w+') as file:
		basepaths = 'basepaths: ' + ', '.join(paths)  + '\n'
		file.write(basepaths)

	with open(outputpath, 'a') as file:
		for path in paths:
			for r, d, f in os.walk(path):
				fulfillsconditions = True

				for condition in pos_conditions:
					if condition not in r:
						fulfillsconditions = False
						break

				if fulfillsconditions:
					for condition in neg_conditions:
						if condition in r:
							fulfillsconditions = False
							break

				if fulfillsconditions:
					if len(d) and dirpaths:
						for di in d:
							if r[-1] != '/':
								write = r +'/' + di + '\n'
							else:
								write = r + di + '\n'
							print('Saving path to folder ' + write)
							file.write(write)

					if len(f) and filepaths:
						for fi in f:
							if r[-1] != '/':
								write = r +'/' + fi + '\n'
							else:
								write = r + fi + '\n'
							print('Saving path to file ' + write)
							file.write(write)