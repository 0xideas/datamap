#!/usr/bin/harrison python3
#-*- coding: utf-8 -*-
import os, psutil, requests, bs4, lxml, string, json
import pandas as pd
from selenium import webdriver
from random import choice

def kern():
	# returns a dict of usefull attributes of the environment
	# The rest of this document deals with a Linux system. For the others, some changes on the code are required.
	lbl_kern = ['system', 'node', 'release', 'version', 'machine', 'processor']
	kern = dict(zip(lbl_kern,list(os.uname())))
	# add some attributes
	kern['user'] = os.environ['USER']
	kern['lang'] = os.environ['LANG']
	return kern

def mpt():
	# returns a dict of all disks/drives/devices connected
	lbl_drives = ['device','mountpoint','fstype']
	disks = [d[0:3] for d in psutil.disk_partitions()]
	drives = [dict(zip(lbl_drives,ds)) for ds in disks]
	mountpoints = [d['mountpoint']for d in drives]
	return mountpoints	

def all_files():
	# returns all files found on a mountpoint
	path = '/home/marouan/Bureau/test_datamap'
	allfiles = [os.path.join(r, name) for r,d,f, in os.walk(path) for name in f]
	exts = [os.path.splitext(file)[1].upper() for file in allfiles]
	df = pd.DataFrame([allfiles, exts]).T
	df.columns = ['filepath','ext']
	df['ext'] = df['ext'].astype('category')
	# df.ext.value_counts().nlargest(10)
	return df