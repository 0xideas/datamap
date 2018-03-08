"""
	Main datamapping program. Generates Settings object, creates filepaths.txt file, and writes results to table.
"""


from set_settings import *
from datamapper_helpers import *
#from return_NEs import return_names NOW IN 
import pandas as pd
import os


if __name__ == '__main__':

	#generate Settings object
	settings = Settings()
	#verify settings/take in new settings
	while True:
		settings.show()
		if get_decision('Are these settings correct? \n'):
			break		
		settings.configure()
		settings.generate_reglib()

	filepathsfile = settings.output_path + 'filepaths.txt'
	#read dependency tree, write paths to files to filepaths.txt
	if get_decision('Generate "filepaths.txt"?\n'):
		print('Collecting filepaths...')
		generate_pathfile(filepathsfile, settings.paths)


	# for each target basepath
	for path in settings.paths:
		#create a file with the [path]>iids as name
		iidsfilename = path.replace('/', '>') + '>iids'
		with open(settings.output_path + iidsfilename, 'w+') as iids:
			#import return_names only if the names also need to be identified
			if settings.getnames:

				from return_names_ import return_names #IMPORT HERE

				#write header line
				iids.write('path, paragraph number, person, ' + ', '.join(list(settings.reglib.keys())) + '\n')
			else:
				#write header line
				iids.write('path, paragraph number, ' + ', '.join(list(settings.reglib.keys())) + '\n')

		#open the output in append mode
		with open(settings.output_path + iidsfilename, 'a') as iids:
			#open the file with the list of file paths
			with open(filepathsfile, 'r') as filepaths:
				#read the first line of the file
				path = filepaths.readline()
				while path:
					#read the second and subsequent lines. the first line is skipped
					path = filepaths.readline()[:-1]
					print(path)
					#not yet written
					#Text = extract_text(path)

					#if the path exists
					if os.path.exists(path):
						print('Path exists.')
						#get the text from the file
						Text = extract_text(path)

						if Text != 'empty':
							print('Text length: ', len(Text))

							#split the text first by two returns, then by one return, then so that each chunk is smaller than the maximum allowed length
							if len(Text) > settings.maxlength:
								text = split_text(Text, maxlength = settings.maxlength, criteria = ['\n\n', '\n'])
							else:
								text = [Text]

							para_n = 1
							#for each paragraph
							for paragraph in text:
								assert type(paragraph) == str

								iids_in_paragraph = []

								#for each specific IID name (e.g. BE_bankn)
								for country_iid in settings.reglib:
									#find instances
									iids_found = get_matches(settings.reglib[country_iid], paragraph)
									#join them to one string
									iids_found = ' | '.join(remove_empty(iids_found))

									if not iids_found:
										iids_found = 'NA'
									#append to list of IID instances found
									iids_in_paragraph.append(iids_found)

								#find person names in document, depending on the setting
								if settings.getnames:
									persons = return_names(paragraph)
									iids.write(path + ', ' + str(para_n) + ', '+ ' | '.join(persons) + ', '.join(iids_in_paragraph) + '\n')
								#or write the results and the location data to file
								else:
									iids.write(path + ', ' + str(para_n) + ', ' + ', '.join(iids_in_paragraph) + '\n')
								para_n += 1
					else:
						pass