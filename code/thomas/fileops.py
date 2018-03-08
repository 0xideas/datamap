"""Access files and folders"""

import os
import pandas as pd
from unidecode import unidecode


def find_files(path, extension='.txt'):
    """Scan directory of files and subfolders and return list of filepaths"""
    filepaths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if '~' not in file:
                filepaths.append(root+ '/' + file)
    print (filepaths)
    return filepaths

def get_ext(fpath):
    """Grab the extension of a filepath"""
    return os.path.splitext(fpath)[1][1:]


def write_file(fpath, text):
    """Write text to specified filepath"""
    with open(fpath, "w") as f:
        f.write(text)


def write_xlsx(df, fpath, sheetname='Sheet1'):
    """Save dataframe to Excel"""
    writer = pd.ExcelWriter(fpath)
    df.to_excel(writer, sheetname)
    writer.save()
    return print('Excel file saved to', fpath)


### DEPRECATED ###
# def read_files(filelist):
#     """
#     Reading all text from files --> Needs to become compatible for any filetype
#
#     Note: unidecode replaces non-ASCII with ASCII characters
#     """
#     text = ''
#     ignored = []
#     for file in filelist:
#         print(file)
#         try:
#             text = text +'\t'+ open_txt(file)
#             print(text)
#         except:
#             ignored.append(file)
#             print('ignored: ',file)
#     return unidecode(text), ignored
