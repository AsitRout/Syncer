import os, sys

#To get disks information
import shutil

#Contains Variables To store disk information
from env import *


"""
It's a simple function to find total, free, available space of a disk
"""
def show_disk(self):
    disk_info.clear()
    disk = []
    tmp = []
    tmp.append('ROOT')
    info = shutil.disk_usage(home)
    tmp.append(info.total / 1000000000)
    tmp.append(info.used / 1000000000)
    tmp.append(info.free / 1000000000)
    disk_info.append(tmp)
    disk.append(home)
    os.chdir(disk_path)
    for item in os.listdir('.'):
        tmp = []
        tmp.append(item)
        info = shutil.disk_usage(item)
        tmp.append(info.total / 1000000000)
        tmp.append(info.used / 1000000000)
        tmp.append(info.free / 1000000000)
        disk_info.append(tmp)
    os.chdir(curr)
