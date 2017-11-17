# information-extraction.py

import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')

string = """


I like the idea of a first quarter review of 2000.  We just may not be able 
to pull off to the extent we did last year.  Did Stan indicate exactly what 
he had in mind?  Does he want to video stream again?  If so, we should start 
planning now to ensure we get a large enough space booked early as well as 
booking the video company and working with the EBS folks.  I have the 
presentation we used for 1999's review in my right cabinet above my desk.  If 
it's ok with you, I'll ask you to communicate with Kimberly on the details.

We're getting ready to leave for the hospital!  I can't believe today is the 
day!  Keith and I both are quite nervous and confident at the same time!  
Please keep us in your prayers and as soon as we name the baby, we'll call 
the office.  Kimberly is on point to send out an email.

Have a great Thursday!

Gina





Shelley Corman
11/29/2000 01:36 PM
To: Gina Taylor/OTS/Enron@Enron
cc:  

Subject: Re: Revised ETS Story  

Good luck on your big day tomorrow.  I have been thinking about you all week.

FYI - Stan is interested in having a year in review session in the first 
quarter of 2001.  I'm going to have Kimberly start working on this.  Stan 
said that he felt like this was a very successful event last year & would 
like to use it as an opportunity to get Dan out in front of all of the 
employees.


"""

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names    
    
    
#if __name__ == '__main__':
numbers = extract_phone_numbers(string)
emails = extract_email_addresses(string)
names = extract_names(string)
print(numbers, emails, names)
