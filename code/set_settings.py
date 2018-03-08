from set_settings_helpers import *

"""
Classes:
	Settings: Object to store, update and generate settings
"""

import re
import os
from collections import OrderedDict

class Settings(object):
	"""Stores settings, updates them via assignment or via command line dialogue and generates a reglib from them

	Attributes:
		getnames: logical, search for person names or not
		output_path: path to the output folder
		max_length: maximum length of a paragraph to search for regular expression matches
		outputsize: target size for each output file
		maxinputsize: maximum file size for input files
		paths: list of paths
		iids: list of iid names 
		customerid: regular expression for customer id
		languages: list of languages
		countries: list of countries
		reglib: library of regular expressions
		ignored: list of iid names not included in reglib
		_valid_iids: list of iid names that are valid
		_valid_languages: list of languages that are valid
		_valid_countries: list of countries that are valid
		_master_reglib: library of all regular expressions to identify country specific iids

	Methods:
		__init__: initialise with default values or custom values and generate reglib
		show: print out public attributes except for 'ignored'
		configure: change any of the public attributes via command line
		set_output_path: set the output path
		set_maxlength: set the maximum length of paragraphs in characters
		set_outputsize: set the size of outputfiles
		set_maxinputsize: set maxinputsize
		set_getnames: set whether person names should be searched for
		set_path: input a list of paths and check that they exist
		set_iids: input a list of iids and check that they are allowed
		set_customerid: input a regular expression and check its validity
		set_languages: input a list of languages and check their validity
		set_countries: input a list of countries and check their validity
		_set_setting: take name of setting name and list of valid values and return input values
		validate_settings: check the validity of all the settings
		validate_paths: check existence for every path in the list and return True only if all exist, False otherwise
		_validate_setting: take current setting, a list of valid values for setting and setting update function and update if current setting is invalid
		generate_reglib: validates settings and generates a library of regular expressions from them
	""" 

	def __init__ (self, output_path = '/home/leon/live/datamap_output/', maxlength = 1000, outputsize = 100 * 1000 * 1000, maxinputsize = 200 * 1000 * 1000,
	getnames = False,  paths = ['/home/leon/live/'], languages = ['french', 'dutch', 'english', 'german'], 
	countries = ['BE'], iids = ['ip', 'iban', 'email', 'phone', 'passport', 'idn','bankn', 'creditc'], 
	customerid = None):
		self.getnames = getnames
		self.output_path = output_path
		self.maxlength = maxlength
		self.outputsize = outputsize
		self.maxinputsize = maxinputsize
		self.paths = paths
		self.iids = iids
		self.customerid = customerid
		self.languages = languages
		self.countries = countries
		self.reglib = OrderedDict()
		self.ignored = []
		self._valid_iids = ['ip', 'iban','phone', 'email', 'passport', 'idn','bankn', 'creditc']
		self._valid_languages = ['french', 'dutch', 'english', 'german']
		self._valid_countries = ['be', 'nl', 'fr', 'uk', 'de']
		self._master_reglib =  {
		'ip': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
		'iban': r'\b(?:[A-Za-z]{2}[0-9]{2})?(?:[ ]?[0-9]{4}){3}\b',
		'email': r'\b(?:[a-zA-Z0-9_\-\.]+)@(?:[a-zA-Z0-9_\-\.]+)\.(?:[a-zA-Z]{2,5})\b',
		'BE_phone': r'(?:\b0|\+)0?\d{1,3}[ ]?\d{1,3}[ ]?\d{2,3}(?:[ ]?\d{1,2}){1,2}\b',
		'BE_passport': r'\b[A-Z]{2}\d{6}\b',
		'BE_idn': r'\b(\d{3}-?\d{6}<?\d{1}-?\d{2,3})\b',
		'BE_bankn': r'\b[0-9](?:[ ]?[0-9]{4})(?:[ ]?[0-9]{2})\b',
		'BE_creditc': r'\b(?:\d{4}[\s_-]?){4}\b'
		#MORE COUTNRIES GO HERE
		}
		
		if len(self.reglib) == 0:
			self.generate_reglib()
		#this only happens if a dict was passed to the object directly
		else:
			while type(self.reglib) != OrderedDict:
				print('Please pass an ordered dict to self.reglib. \n')
				try:
					self.reglib = eval(input())
				except:
					print('This is not an ordered dict.\n')


	def show(self):
		print("Current settings: \n Output Path: \t {0.output_path} \n Output File Size in MB: \t {1} \n Maximum Input Size in MB: \t {2} \n Maximum Paragraph Length: \t {0.maxlength} \n Get Names: \t {0.getnames} \n Paths: \t {0.paths} \n IIDs: \t\t {0.iids} \n Customer ID: \t {0.customerid} \n Languages: \t {0.languages} \n Countries: \t {0.countries} \n".format(self, self.outputsize/1000000, self.maxinputsize/1000000))

	def configure(self):
		self.show()

		self.set_getnames()

		if get_decision('Do you wish to change the output path?\n'):
			self.set_output_path()

		if get_decision('Do you wish to change the maximum paragraph length?\n'):
			self.set_maxlength()

		if get_decision('Do you wish to change the target size of the output files?\n'):
			self.set_outputsize()

		if get_decision('Do you wish to change the maximum size of the input files?\n'):
			self.set_maxinputsize()

		if get_decision('Do you wish to change the list of paths to search?\n'):
			self.set_paths()

		if get_decision('Do you wish to change the list of iids to search?\n'):
			self.set_iids()

		if get_decision('Do you wish to add Customer ID to the library of regular expressions?\n'):
			self.set_customerid()

		if get_decision('Do you wish to change the list of languages to search?\n'):
			self.set_languages()

		if get_decision('Do you wish to change the list of countries to search?\n'):
			self.set_countries()

	def set_output_path(self):
		while True:
			self.output_path = input('Please enter the path to the output folder.\n')
			if os.path.exists(self.output_path) and self.output_path[-1] == '/':
				break

	def set_maxlength(self):
		while True:
			try:
				self.maxlength = int(input('Please enter the maximum number of characters per paragraph.\n'))
				if type(self.maxlength) == int:
					break
			except:
				pass

	def set_outputsize(self):
		while True:
			try:
				self.outputsize = int(input('Please enter the target file size for the output files.\n'))
				if type(self.outputsize) == int:
					if self.outputsize < 1000000:
						print('The minimum output file size is 1 MB. Please enter a number larger than 1 MB.\n')
					else:
						break
			except:
				pass

	def set_maxinputsize(self):
		while True:
			try:
				self.maxinputsize = int(input('Please enter the target file size for the output files.\n'))
				if type(self.maxinputsize) == int:
					break
			except:
				pass

	def set_getnames(self):
		self.getnames = get_decision('Should the paths be searched for person names? This takes much longer and requires the spaCy package.\n')

	def set_paths(self):
		print("Please enter the paths to the folders you wish to scan in the order you wish to scan them.\n")
		while True:
			self.paths = get_inputs()
			if self.validate_paths():
				break
			else:
				print('At least one path was not valid. Please enter them again.\n')

	def set_iids(self):
		self.iids = self._set_setting('iids', self._valid_iids)

	def set_customerid(self):
		while True:
			try:
				customeridRX = input('Please enter a regular expression to caputure customer IDs on your system. Start with an "r" to prevent escaping with "\\": \n')
				self.customerid = eval(customeridRX)
				break
			except:
				print('Please enter a valid regular expression for your customer IDs.\n')


	def set_languages(self):
		self.languages = self._set_setting('languages', self._valid_languages)

	def set_countries(self):
		self.countries = self._set_setting('countries', self._valid_countries)

	def _set_setting(self, name, validlist):
		while True:
			print('Please enter {0} from the following list: {1} \n'.format(name, validlist))
			setting = get_inputs(maxins = len(validlist))
			if test_list_validity(setting, validlist):
				return setting
			else:
				print('Please enter a valid list. \n')				


	def validate_paths(self):
		co = []
		for path in self.paths:
			co.append(os.path.exists(path))
		return min(co)

	def validate_settings(self):
		if not type(self.getnames) == bool:
			self.set_getnames()

		if not os.path.exists(self.output_path):
			self.set_output_path()

		if not type(self.maxlength) == int:
			self.set_maxlength()

		if not type(self.outputsize) == int:
			self.set_outputsize()

		if not self.validate_paths():
			self.set_paths()

		if self.customerid is not None:
			__ = validate_regex(self.customerid, self.set_customerid)

		self._validate_setting(self.iids, self._valid_iids, self.set_iids)
		self._validate_setting(self.languages, self._valid_languages, self.set_languages)
		self._validate_setting(self.countries, self._valid_countries, self.set_countries)


	def _validate_setting(self, setting, validsetting, setsettingfunction):
		co = test_list_validity(setting, validsetting)
		if not co:
			setting = setsettingfunction()


	def generate_reglib(self):
		self.validate_settings()
		self.ignored = []
		self.reglib = OrderedDict()
		#International reglibs
		for iid in ['ip', 'email', 'iban']:
			if iid in self.iids:
				self.reglib[iid] = self._master_reglib[iid]

		#National reglibs
		for country in self.countries:
			for iid in self.iids:
				if iid not in ['ip', 'email', 'iban']:
					country_iid = country + '_' + iid
					if country_iid in self._master_reglib:
						self.reglib[country_iid] = self._master_reglib[country_iid]
					else:
						self.ignored.append(country_iid)


		#Custom customer id regular expression
		if self.customerid is not None:
			self.reglib['customerid'] = self.customerid



