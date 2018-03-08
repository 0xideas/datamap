#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 15:55:49 2017

@author: leon
"""

#generating a sample from folder of txt files
#path is the path to the folder to be read
def generate_sample(path):  
    assert type(path) == str
    import os
    from unidecode import unidecode
    
    filepaths = []
    for root, dirs, files in os.walk(path):
        files = [f for f in files if not f[0] == '.']
        for file in files:
    #the following line can be used to determine what files should be read
            if file.endswith("."):
                filepaths.append(root+ '/' + file)

    #textlist is the list of the text in the files in the folder to be read
    textlist = []
    ignored = []
    for filepath in filepaths:
        try:
            file = open(filepath, 'r', encoding = 'utf-8')
            textlist.append(file.read())
        except:
            ignored.append(filepath)
            print('ignored: ' + filepath)

    #these are joined into one string, texttemp
    texttemp = '\t'.join(textlist)
    #unidecode tries to replace non-ASCII with ASCII characters
    return unidecode(texttemp) 

    #calls generate_sample and writes it to an existing file or a file to be created

#path is the path to the folder to be read, filepath is the path+filename of the file
#to which the output is written
def write_sample_to_file(path, filepath):
    assert type(path) == str
    from generate_write_sample import generate_sample
    
    text = generate_sample(path)
    file = open(filepath, "w+")
    file.write(text)
        
