import spacy
from datamapper_helpers import split_many

def return_names(text, language = 'xx', maxsigns = 10000):
	nlp = spacy.load(language)
	
	persons = []
	
	text = split_many(text, maxlength = maxsigns)
	for part in text:
		doc = nlp(part)
		persons.append([(e.text, e.start_char) for e in doc.ents if e.label_ == 'PERSON'])
		
	persons = [inner for outer in persons for inner in outer]
	persons = [inner for outer in persons for inner in outer if type(inner) == str]
	# persons = [inner for outer in persons for inner in outer] Also returns position in string

	return persons

