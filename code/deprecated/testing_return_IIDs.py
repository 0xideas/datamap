if __name__ == '__main__':

	import sys
	import os.path

	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

	from return_IIDs_f import return_IIDs, return_IID, return_numbers

	#open and read a file to try return_IIDs function on
	file = open('/home/leon/Desktop/enron_mail/text_batch26', 'r')
	sample = file.read()

	#try the function
	iidslist = return_IIDs(sample)

	#write the matches to file, one per line
	writefile = open('/home/leon/Desktop/enron_mail/text_batch26_IIDs.txt', 'w+')

	for iid in iidslist:
		for line in iid:
			writefile.write(line)
			writefile.write('\n')

	writefile.close()

	print(iidslist)

