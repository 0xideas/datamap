#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 15:55:49 2017

@author: leon
"""

#generating a sample from folder of txt files
def generate_sample(path):
    assert type(path) == str
    import os
    from unidecode import unidecode
    
    filepaths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("."):
                 filepaths.append(root+ '/' + file)

    textlist = []
    for filepath in filepaths:
        file = open(filepath)
        textlist.append(file.read())
    
    texttemp = '\t'.join(textlist)
    return unidecode(texttemp) 

#calls generate_sample and writes it to an existing file or a file to be created
def write_sample_to_file(path, filepath):
    assert type(path) == str
    from generate_write_sample import generate_sample
      
    text = generate_sample(path)
    file = open(filepath, "w+")
    file.write(text)
        

