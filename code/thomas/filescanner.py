import os
import platform
import psutil
import pandas as pd

def kern():
    """Platform independent retrieval of systeminfo

    Note do we need the other info, because I don't have those parameters set on my device?"""
    return platform.uname()

def mpt():
    """returns a dict of all disks/drives/devices connected"""
    lbl_drives = ['device','mountpoint','fstype']
    disks = [d[0:3] for d in psutil.disk_partitions()]
    drives = [dict(zip(lbl_drives,ds)) for ds in disks]
    return [d['mountpoint']for d in drives]

def find_files(basepath):
    """Returns all files found on a mountpoint"""
    allfiles = [os.path.join(r, name) for r,d,f, in os.walk(basepath) for name in f]
    exts = [os.path.splitext(file)[1].upper() for file in allfiles]
    df = pd.DataFrame([allfiles, exts]).T
    df.columns = ['filepath','ext']
    df['ext'] = df['ext'].astype('category')
    return df

base = r'C:\Users\Thomas\Google Drive\Projects\Data privacy\projects\data mapping'
df = find_files(base)
print(df.head().T)
