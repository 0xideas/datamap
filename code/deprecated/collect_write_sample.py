#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 15:55:49 2017

@author: leon
"""

#generating a sample from folder of txt files
#path is the path to input folder
def collect_sample(path, extension = '.txt'):
    assert type(path) == str
    assert type(extension) == str
    import os
    from unidecode import unidecode
    
    filepaths = []
    #append the paths to the files with a particular extension to the filepaths list
    for root, dirs, files in os.walk(path):
        files = [f for f in files if not f[0] == '.']
        for file in files:
    		#the following line can be used to determine what files should be read
            if file.endswith(extension):
                filepaths.append(root+ '/' + file)

    #textlist is the list of the text in the files in the folder to be read
    textlist = []
    ignored = []
    #read files and append the contents to the 
    for filepath in filepaths:
        try:
            with open(filepath, 'r', encoding = 'utf-8') as file:
            	textlist.append(file.read())
        #if a file cannot be opened, its path is appended to the ignored list
        except:
            ignored.append(filepath)
            print('ignored: ' + filepath)

    #these are joined into one string, texttemp
    texttemp = '\t'.join(textlist)
    #unidecode replaces non-ASCII with ASCII characters
    return (unidecode(texttemp), ignored)

    #calls collect_sample and writes it to an existing file or a file to be created

#path is the path to the folder to be read, filepath is the path+filename of the file
#to which the output is written
def write_sample(path, filepath, extension = '.txt', saveignored = False):
    assert type(path) == str
    from collect_write_sample import collect_sample
    
    text, ign = collect_sample(path, extension)
    print(text)
    with open(filepath, "w+") as file:
    	file.write(text)

    #writes filepaths of files that could not be read to a file
    if saveignored:
    	with open(filepath + '_ignored', "w+") as file:
    		file.write(ign)
        
