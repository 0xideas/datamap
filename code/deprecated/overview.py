import json
import os
import pandas as pd
import re
from PyPDF2 import PdfFileWriter, PdfFileReader


#GET FILES
basepath = input('Please enter a basepath for scanning:\n')

files, filepaths = find_files(basepath)

#this is the master table that all other results will be appended to
table = pd.DataFrame({'filename': files, 'filepaths': filepaths})


#changed to also return file names
def find_files(path, extension='.txt'):
    """Scan directory of files and subfolders and return list of filepaths"""
    files = []
    filepaths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if '~' not in file:
                filepaths.append(root+ '/' + file)
                files.append(file)
    #print (filepaths)
    return (files, filepaths)

#no change
def get_ext(fpath):
    """Grab the extension of a filepath"""
    return os.path.splitext(fpath)[1][1:]

#no change, returns the text from the file
def open_file(fpath, fdict=fdict):
    """Convert the string instruction to a function call"""
    return fdict[get_ext(fpath)](fpath)

































#THE FUNCTIONS FOR INDIVIDUAL FILE TYPES
fdict = {
        'txt': extract_txt,
        'pdf': extract_pdf,
        'xlsx': extract_xlsx
    }

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