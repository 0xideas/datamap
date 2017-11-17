# functions to search text via regular expressions
#

def return_numbers(listofstrings):

    assert type(listofstrings) == list
    import re

    listoflist = [re.findall('[0-9]*', string) for string in listofstrings]
    return [ ''.join(lisT) for lisT in listoflist]
    


def return_IDs(text, askCustomerIDformat = False):
    
    assert type(text) == str
    
    import re
    idRX = re.compile(r'\b(\d{3}-?\d{6}<?\d{1}-?\d{2,3})\b')
    passportRX = re.compile(r'\b[A-Z]{2}\d{6}\b')
    phoneRX = re.compile(r'\b(?:\d{1,4}[ ]?){5}\b')
    emailRX = re.compile(r'\b(?:[a-zA-Z0-9_\-\.]+)@(?:[a-zA-Z0-9_\-\.]+)\.(?:[a-zA-Z]{2,5})\b')
    ibanbbanRX = re.compile(r'\b(?:[A-Za-z]{2}[0-9]{2})?(?:[ ]?[0-9]{4}){3}\b')
    bankaccountRX = re.compile(r'\b(?:[ ]?[0-9])(?:[ ]?[0-9]{4})(?:[ ]?[0-9]{2})\b')
    creditcardRX = re.compile(r'\b(?:\d{4}\s?){4}\b')
    
    if (askCustomerIDformat):print('do something')
    
    print('Searching for IDs...')
    ids = idRX.findall(text)
    print('Searching for passport numbers...')
    passports = passportRX.findall(text)
    print('Searching for phone numbers...')
    phones = phoneRX.findall(text)
    print('Searching for email addresses...')
    emails = emailRX.findall(text)
    print('Searching for IBAN, BBAN numbers...')
    ibanbbans = ibanbbanRX.findall(text)
    print('Searching bank account numbers....')
    bankaccounts = bankaccountRX.findall(text)
    print('Searching for credit cards...')
    creditcards = creditcardRX.findall(text)
    
    print('standardising results')
    print('ids')
    ids = return_numbers(ids)
    #passports should be in the proper format
    print('phones')
    phones = return_numbers(phones)
    #emails too
    print('ibanbbans')
    ibanbbans = return_numbers(ibanbbans)
    print('bankaccounts')
    bankaccounts = return_numbers(bankaccounts)
    print('creditcards')
    creditcards = return_numbers(creditcards)
    
    return([ids, passports, phones, emails, ibanbbans, bankaccounts, creditcards])
    
    
    

