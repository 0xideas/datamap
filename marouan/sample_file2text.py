import pandas as pd
import re
import requests
import sys
import time
import os
from os import walk
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader

# BeautifulSoup
from bs4 import BeautifulSoup


def read_pdf(filename):
    """Read pdf and return pdf reader object"""
    pdfFileObj = open(filename,'rb')
    return PyPDF2.PdfFileReader(pdfFileObj)


def pdf2txt(pdfFileObj):
    """Convert pdf file reader object to text

    This function starts by initializing a string to which text is added
    page by page. Empty spaces or pdf metadata are cleaned at the end
    """
    text = ""
    nrpages = pdfFileObj.getNumPages()
    for p in range(nrpages):
        page = pdfFileObj.getPage(p).extractText()
        text += re.sub('\d\d:\d\d| +|\n', ' ', page)
    return text


def add_web(url):
    """Simple scraper that reads all text from a single web page"""
    r = requests.get(url).content
    soup = BeautifulSoup(r, "html.parser")
    attrs_list = ['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'strong']
    raw = ' '.join([tag.text for tag in soup.findAll(name=attrs_list)])
    text = re.sub(' +|\n|\t', ' ', raw)
    return text


def add_pdf(url):
    """Read url to pdf file"""
    r = requests.get(url)
    with open('temp/newfile.pdf', 'wb') as f:
        f.write(r.content)
    return pdf2txt(read_pdf('temp/newfile.pdf'))


def add_local():
    """Example of how to open and read files stored in folder"""
    df = pd.read_excel('db/know.xlsx')
    sourcelist = []
    root = 'FOLDER_PATH'
    for (dirpath, dirnames, filenames) in walk(root):
        sourcelist.extend(dirnames)

    for source in sourcelist:
        flist = [] # list of files
        path = os.path.join(root, source)
        for (dirpath, dirnames, filenames) in walk(path):
            flist.extend(filenames)
        for i, file in enumerate([f for f in flist if f not in df['file'].tolist()]):
            if file[-3:]=='pdf':
                fpath = os.path.join(path, file)
                print(fpath)
                try:
                    pdf = read_pdf(fpath)
                    row = pd.DataFrame({'file':[file],
                                        'text': [pdf2txt(pdf)],
                                        'source': [source],
                                        'type':['tbd'],
                                        'url':['']})
                    df = df.append(row)
                    print(file+' added')
                except:
                    print(file, 'not stored properly')
                    continue
            elif file[-3:]=='txt':
                fpath = os.path.join(path, file)
                print(fpath)
                openfile = open(fpath, "r", encoding='utf-8')
                row = pd.DataFrame({'file':[file],
                                    'text': [''.join(openfile.readlines())],
                                    'source': [source],
                                    'url':['']})
                print(file+' added')
                openfile.close()
                df = df.append(row)

    df.to_excel('db/know.xlsx', index=False)
    return print('new files added')


if __name__ == '__main__':
    url = input('please enter url:\n')
    add_url(url)
