import os, sys

#Contains Variables To store disk information
from env import *

from wrapper import *

"""
It's a simple function to find total, free, available space of a disk
"""

def disk_usage(path):
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return (total, used, free)

def show_disk(self):
    #disk_info.clear()
    #disk_info = []
    clear_list([disk_info])
    disk = []
    tmp = []
    tmp.append('ROOT')
    info = disk_usage(home)
    tmp.append(info[0] / 1000000000)
    tmp.append(info[1] / 1000000000)
    tmp.append(info[2] / 1000000000)
    disk_info.append(tmp)
    disk.append(home)
    os.chdir(disk_path)
    for item in os.listdir('.'):
        tmp = []
        tmp.append(item)
        info = disk_usage(item)
        tmp.append(info[0] / 1000000000)
        tmp.append(info[1] / 1000000000)
        tmp.append(info[2] / 1000000000)
        disk_info.append(tmp)
    os.chdir(curr)
