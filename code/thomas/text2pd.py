"""Functions to scan text"""


import pandas as pd
#from pptx import Presentation
from PyPDF2 import PdfFileWriter, PdfFileReader
import re

from fileops import get_ext

#takes a list of strings and returns a list of strings that contains only the numbers in the input strings
reglib = {
        'number': '[0-9]*',
        'ip': '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
        'email': r'\b(?:[a-zA-Z0-9_\-\.]+)@(?:[a-zA-Z0-9_\-\.]+)\.(?:[a-zA-Z]{2,5})\b',
        'phone': r'(?:\b0|\+)0?\d{1,3}[ ]?\d{1,3}[ ]?\d{2,3}(?:[ ]?\d{2}){1,2}\b',
        'passport': r'\b[A-Z]{2}\d{6}\b',
        'iid': r'\b(\d{3}-?\d{6}<?\d{1}-?\d{2,3})\b',
        'IBAN': r'\b(?:[A-Za-z]{2}[0-9]{2})?(?:[ ]?[0-9]{4}){3}\b',
        'bank account number': r'\b[0-9](?:[ ]?[0-9]{4})(?:[ ]?[0-9]{2})\b',
        'creditcards': r'\b(?:\d{4}[\s_-]?){4}\b'
}

def get_matches(pattern, string):
    """Return list of matches based on regex pattern"""
    return [s for s in re.findall(pattern, string) if s!='']

def screen_text(pattern, text):
    """Return list of matches based on regex pattern"""
    return get_matches(pattern, text)

def get_pers_data(text):
    """Create a dictionary with a list of matches for each pattern"""
    match_dict = {}
    for p in reglib:
        matches = screen_text(reglib[p], text)
        match_dict[p] = [m for m in matches if m]
    return match_dict

#_______________________________________________________________________________
"""TXT"""

def extract_txt(fpath):
    """Open txt file and read contents"""
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

#_______________________________________________________________________________
"""PPTX"""

def open_pptx(fpath):
    return Presentation(fpath)

def pptx2txt(prs):
    text = ''
    for slide in prs.slides:
        for shape in slide.shapes:
            text = text + shape.text.replace('\n',' ')
    return text

def extract_pptx(fpath):
    return pptx2txt(open_pptx(fpath))

#_______________________________________________________________________________
def open_xlsx(fpath):
    """Read xlsx path as pandas Excel file"""
    return pd.ExcelFile(fpath)

def xlsx2txt(xl):
    """Access excel sheet and extract text for each column"""
    text = ''
    for sheet in xl.sheet_names:
        df = xl.parse(sheet).astype(str)
        for col in df.columns:
            coltext = ','.join(df[col].tolist())
            text = text+','+coltext
    return text

def extract_xlsx(fpath):
    return xlsx2txt(open_xlsx(fpath))

#_______________________________________________________________________________
def open_pdf(filename):
    """Read pdf and return pdf reader object"""
    pdfFileObj = open(filename,'rb')
    return PdfFileReader(pdfFileObj)

def pdf2txt(pdfFileObj):
    """Convert pdf file reader object to text

    This function starts by initializing a string to which text is added
    page by page. Empty spaces or pdf metadata are cleaned at the end
    """
    text = ''
    nrpages = pdfFileObj.getNumPages()
    for p in range(nrpages):
        page = pdfFileObj.getPage(p).extractText()
        text += page # will add text cleaning steps later
    return text

def extract_pdf(fpath):
    return pdf2txt(open_pdf(fpath))

"""Putting it all together"""
#_______________________________________________________________________________

fdict = {
        'txt': extract_txt,
        'pdf': extract_pdf,
        'xlsx': extract_xlsx
    }

def open_file(fpath, fdict=fdict):
    """Convert the string instruction to a function call"""
    return fdict[get_ext(fpath)](fpath)


def screen_files(filelist):
    df = pd.DataFrame()
    for f in filelist:
        print('screening:', f, 'of type', get_ext(f))
        if get_ext(f) in fdict:
            df[f] = pd.Series(get_pers_data(open_file(f)))
    return df.T


def count_matches(df):
    """Quickly count the number of records per field"""
    return df.applymap(lambda x: len(x))
