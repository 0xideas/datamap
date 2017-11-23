#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 18:02:45 2017

@author: leon
"""

#if __name__ == "main":
from generate_write_sample import generate_sample, write_sample_to_file
from return_IDs import return_numbers, return_IDs

for x in range(1,27,1):

	write_sample_to_file('/home/leon/Desktop/enron_mail/batch'+ str(x), '/home/leon/Desktop/enron_mail/text_batch' + str(x))
