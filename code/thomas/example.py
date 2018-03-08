import json
import os

from text2pd import screen_files
from fileops import find_files, write_xlsx


# Path set to basepath from where script is run
# basepath = os.getcwd()
basepath = input('Please enter a basepath for scanning:\n')

df = screen_files(find_files(basepath))
write_xlsx(df,'output.xlsx')
