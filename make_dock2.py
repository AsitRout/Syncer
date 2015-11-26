import os

#To Find Filetype
import magic

#Contains variables for file actions, checkbox and location
from env import *

#Contains variables for storing file detail
from env2 import *

#Contain variables for file action progress
from env_progress import *

"""
make_category(self, files, action)
files: A list containing name of files to be copied or deleted
action: Action to be performed on the list of files

This function use "magic" module to find filetypes
"""
def make_fcategory(self, files, action):
    if(not files):
        return

    if(action == "copy"):
        filetype = cp_filetype	#Variable at Line 27 in env2
        
    if(action == "del"):
        filetype = del_filetype	#Variable at Line 30 in env2

    mime = magic.open(magic.MAGIC_MIME_TYPE)
    mime.load()

    total_size = 0
    ind = -1
    for item in files:
        paths = item.split('/')
        fname = paths[-1]	#File Name
        
        detail = mime.file(item)
        name = detail.split('/')
        
        size = os.path.getsize(item)	#File Size
        total_size = total_size + size
        
        ind = ind + 1
        if(name[1] == "x-empty"):
            tmp_emp = []
            tmp_emp.append(fname)
            tmp_emp.append(size)
            tmp_emp.append("")
            tmp_emp.append(ind)
            filetype[5].append(tmp_emp)
            continue
        
        if(name[0] == "audio"):
            tmp_audio = []
            tmp_audio.append(fname)
            tmp_audio.append(size)
            tmp_audio.append(name[1])
            tmp_audio.append(ind)
            filetype[0].append(tmp_audio)
            continue
            
        if(name[0] == "image"):
            tmp_img = []
            tmp_img.append(fname)
            tmp_img.append(size)
            tmp_img.append(name[1])
            tmp_img.append(ind)
            filetype[1].append(tmp_img)
            continue

        if(name[0] == "video"):
            tmp_video = []
            tmp_video.append(fname)
            tmp_video.append(size)
            tmp_video.append(name[1])
            tmp_video.append(ind)
            filetype[2].append(tmp_video)
            continue

        if(name[1] == "pdf"):
            tmp_pdf = []
            tmp_pdf.append(fname)
            tmp_pdf.append(size)
            tmp_pdf.append("")
            tmp_pdf.append(ind)
            filetype[4].append(tmp_pdf)
            continue
            
        if(name[0] == "text" or name[0] == "application"):
            tmp_text = []
            tmp_text.append(fname)
            tmp_text.append(size)
            tmp_text.append(str(name[1]))
            tmp_text.append(ind)
            filetype[3].append(tmp_text)
            continue

        else:
            tmp_oth = []
            tmp_oth.append(fname)
            tmp_oth.append(size)
            tmp_oth.append(str(name[1]))
            tmp_oth.append(ind)
            filetype[6].append(tmp_oth)
            continue
   
    total_size = total_size / 1000000
    if(action == "copy"):
        TOT_CP_AMT[0] = total_size	#Variable at Line 20 in env_progress
        
    if(action == "del"):
        TOT_DEL_AMT[0] = total_size	#Variable at Line 11 in env_progress
