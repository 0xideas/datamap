import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))



from return_IIDs_f import return_IIDs, return_IID, return_numbers

file = open('/home/leon/Desktop/enron_mail/text_batch26', 'r')

sample = file.read()

iidslist = return_IIDs(sample)

writefile = open('/home/leon/Desktop/enron_mail/text_batch26_IIDs.txt', 'w+')

for iid in iidslist:
	for line in iid:
		writefile.write(line)
		writefile.write('\n')

writefile.close()


print(iidslist)

