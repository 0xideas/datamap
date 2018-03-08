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

		if len(settings.ignored)>0:
			print('No regular expressions found for the following iids: ' + ', '.join(settings.ignored))

	filepathsfile = settings.output_path + 'filepaths.txt'
	#read dependency tree, write paths to files to filepaths.txt
	if get_decision('Generate "filepaths.txt"?\n'):
		print('Collecting filepaths...')
		generate_pathfile(filepathsfile, settings.paths)



	with open(filepathsfile, 'r') as filepaths:
		path = filepaths.readline()
		filecount = 0
		linecount = 0
		checkfilesize = round(settings.outputsize/settings.maxlength)


		with open(settings.output_path + 'ignored_files.txt', 'w+') as ignrd_files:
			ignrd_files.write('Files that could not be opened at ' + ', '.join(settings.paths) + '\n')

		#with open(settings.output_path + 'ignored_files.txt', 'a') as ignrd_files:
		for inputpath in settings.paths:
			while True:
				samefile = True
				if not path:
					print(iidsfilename)
					break

				if inputpath[-1] != '/':
					inputpath = inputpath + '/'

				iidsfilename = inputpath.replace('/', '>') + 'iids_' + str(filecount)
				filecount += 1
				#create the output file _filecount
				with open(settings.output_path + iidsfilename, 'w+') as iids:
					#import return_names only if the names also need to be identified
					if settings.getnames:

						from return_names_ import return_names #IMPORT HERE

						#write header line
						iids.write('path, paragraph number, person, ' + ', '.join(list(settings.reglib.keys())) + '\n')
					else:
						#write header line
						iids.write('path, paragraph number, ' + ', '.join(list(settings.reglib.keys())) + '\n')

				with open(settings.output_path + iidsfilename, 'a') as iids:
					while path and samefile:
						with open(settings.output_path + 'ignored_files.txt', 'a') as ignrd_files:
							#read the second and subsequent lines. the first line is skipped. the [:-1] removes the \n character at the end of each line
							path = filepaths.readline()[:-1]
							print(path)

							#if the path exists
							if os.path.exists(path):
								#print('Path exists.')
								#get the text from the file
								maxinput = settings.maxinputsize
								Text = extract_text(path, maxinput)

								#print(Text[:11] in ['cannot_open', 'too_large', 'executable']																																																					)
								if Text in ['cannot_open', 'too_large', 'executable']:
									ignrd_files.write(path + ', ' + Text + '\n')
								else:
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
											if not persons:
												persons = 'NA'
											iids.write(path + ', ' + str(para_n) + ', '+ ' | '.join(persons) + ', ' + ', '.join(iids_in_paragraph) + '\n')
											linecount += 1
										#or write the results and the location data to file
										else:
											iids.write(path + ', ' + str(para_n) + ', ' + ', '.join(iids_in_paragraph) + '\n')
											linecount += 1

										if linecount % checkfilesize == 0:
											a = iids.tell()
											if a > settings.outputsize:
												samefile = False

										para_n += 1












