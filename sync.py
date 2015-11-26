import os, time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#To Copy File
import shutil

#Contains variable for file action
from env import *

#Contains variable to update progress of actions
from env_progress import *

"""
Fetches Files from Source location and Target location
"""
def make_list(self, path, t_dir, t_file, s_dir, s_file, file_from, dir_from, action):
        if(action == "copy"):
            source = path['source']
            target = path['target']

        if(action == "del"):
            target = path['source']
            source = path['target']
    
        if(not os.path.isdir(target)):
            TEXT1[0] = ("Target \"%s\" Not Found" %target)
            BOX_TEXT.append(TEXT1[0])
            self.sig.text_browser.emit()
            return
        if(not os.path.isdir(source)):
            TEXT1[0] = ("Source \"%s\" Not Found" %source)
            BOX_TEXT.append(TEXT1[0])
            self.sig.text_browser.emit()
            return

        BUSY[0] = "target"
        os.chdir(target)
        for (dirname, subdir, fname) in os.walk('./'):
                t_dir.append(dirname)
                for file in fname:
                        t_file.append(os.path.join(dirname, file))
        

        BUSY[0] = "source"
        os.chdir(source)
        for (dirname, subdir, fname) in os.walk('./'):
                s_dir.append(dirname)
                dir_from.append(os.path.abspath(dirname))
                for file in fname:
                        s_file.append(os.path.join(dirname, file))
                        file_from.append(os.path.abspath(os.path.join(dirname, file)))
        os.chdir(target)
    
      
"""
Compares Source file list and Target file list and produce the differrence
"""
def onfetch(self, s_file, t_file, tar_list, path_from, col_src, action):
    BUSY[0] = "find" 
    i = 0
    j = 0
    k = 0
    item1 = len(s_file)
    item2 = len(t_file)
                    
    s_file.sort()
    t_file.sort()
    path_from.sort()
    
    #When no more files left in Target list but there are files in Source list
    while (i < item1):
        if(j >= item2):
            tar_list.append(s_file[i])
            i = i + 1
            continue

        source = str(s_file[i])
        target = str(t_file[j])
        #File exists in target           
        if(target == source):
            #File at target is not completely copied
            if(os.path.getsize(target) != os.path.getsize(path_from[k])):
               tar_list.append(s_file[i])
               col_src.append(path_from[k])
               k = k + 1
               i = i + 1
               
            else:    
                path_from.remove(path_from[k])
                i = i +1
                j = j + 1
                continue
            
        #!!! !!!
        if(target < source):
            #path_from.remove(path_from[i])
            j = j + 1
            continue
        
        #File does't exist at Target
        if(target > source):
            tar_list.append(s_file[i])
            i = i + 1
            k = k + 1
            continue


def mkdir(self, d_list):
        log_file = open(rec_log, "a+")
        line = "[" + str(time.asctime()) + "]    creating target directory\n"
        log_file.writelines(line)
        
        for dname in d_list:
            name = dname.split('/')
            try:
                os.makedirs(dname)		#Making directory
                TEXT1[0] = ("'%s' Directory Created" %name[-1])
                log_file.writelines(TEXT1[0] + "\n")
                BOX_TEXT.append(TEXT1[0])
                self.sig.text_browser.emit()
            except:
                TEXT1[0] = ("Cannot Create Directory '%s'" %name[-1])
                log_file.writelines(TEXT1[0] + "\n")
                BOX_TEXT.append(TEXT1[0])
                self.sig.text_browser.emit()

        line = "[" + str(time.asctime()) + "]    target directories created\n\n"
        log_file.writelines(line)
        log_file.close()
        
def cp(self, f_list, file_from):
        #When files to copy are small, it gives time to progress thread to update
        if(TOT_CP_AMT[0] < 100):
                time.sleep(1.5)
        log_file = open(rec_log, "a+")
        line = "[" + str(time.asctime()) + "]    started file copying\n"
        log_file.writelines(line)
        
        SIZE_COPIED[0] = 0
        CP_FILE[0] = 0
        length = len(f_list)
        i = 0
        PRE_TIME[0] = 0
        while(i < length):
            name = file_from[i].split('/')
            if(right_cp_flist[i].checkState(0) == Qt.Checked):
                    tname = f_list[i]
                    sname = file_from[i]
                    
                    CURR_SIZE[0] = (os.path.getsize(sname)) / 1000000
                    TEXT1[0] = ("Copying '%s'(%dMB)" %(name[-1], CURR_SIZE[0]))
                    log_file.writelines(TEXT1[0])
                    BOX_TEXT.append(TEXT1[0])
                    self.sig.text_browser.emit()
                    CURR_NAME[0] = name[-1]
                    CURR_FILE[0] = tname
                    CP_FILE[0] = CP_FILE[0] + 1
                    
                    try:
                            if(os.path.isfile(tname) and CURR_SIZE[0] == (os.path.getsize(tname) / 1000000)):
                                    TEXT1[0] = "File Already Exist"
                                    log_file.writelines(TEXT1[0] + "\n")
                                    BOX_TEXT.append(TEXT1[0])
                                    self.sig.text_browser.emit()
                                    SIZE_COPIED[0] = SIZE_COPIED[0] + CURR_SIZE[0]
                                    i = i + 1
                                    continue
                    except:
                            pass
        
                    shutil.copyfile(sname, tname)		#Copying File
                    SIZE_COPIED[0] = SIZE_COPIED[0] + CURR_SIZE[0]

                    TEXT1[0] = ("'%s' Copied\t\t[TOTAL: %dMB]" %(name[-1], SIZE_COPIED[0]))
                    log_file.writelines(TEXT1[0] + "\n")
                    BOX_TEXT.append(TEXT1[0])
                    self.sig.text_browser.emit()
                                
            i = i + 1
        line = "[" + str(time.asctime()) + "]    file copying ended\n\n"
        log_file.writelines(line)
        log_file.close()
       
def rm(self, f_list):
        if(TOT_DEL_AMT[0] < 100):
                time.sleep(1.5)
        log_file = open(rec_log, "a+")
        line = "[" + str(time.asctime()) + "]    started file deletion\n"
        log_file.writelines(line)
        
        length = len(f_list)
        i = 0
        SIZE_DEL[0] = 0
        DEL_FILE[0] = 0
        while(i < length):
            fname = f_list[i]
            name = fname.split('/')
            if(right_del_flist[i].checkState(0) == Qt.Checked):
                TEXT1[0] = ("Deleting '%s'" %name[-1])
                log_file.writelines(TEXT1[0])
                BOX_TEXT.append(TEXT1[0])
                self.sig.text_browser.emit()
                CURR_NAME[0] = name[-1]
                CURR_SIZE[0] = os.path.getsize(fname) / 1000000
                DEL_FILE[0] = DEL_FILE[0] + 1
                try:
                    os.remove(fname)		#Delete File
                    TEXT1[0] = ("'%s' File Deleted" %name[-1])
                    log_file.writelines(TEXT1[0] + "\n")
                    BOX_TEXT.append(TEXT1[0])
                    self.sig.text_browser.emit()
                except:
                    TEXT1[0] = ("Cannot Delete File : '%s'" %name[-1])
                    log_file.writelines(TEXT1[0] + "\n")
                    BOX_TEXT.append(TEXT1[0])
                    self.sig.text_browser.emit()
                SIZE_DEL[0] = SIZE_DEL[0] + CURR_SIZE[0]

            i = i + 1
            
        line = "[" + str(time.asctime()) + "]    file deletion ended\n\n"
        log_file.writelines(line)
        log_file.close()
            
                    
def rmdir(self, d_list):
        log_file = open(rec_log, "a+")
        line = "[" + str(time.asctime()) + "]    started directory deletion\n"
        log_file.writelines(line)
        
        size = len(d_list)
        i = 0
        while(i < size):
            dname = d_list[i]
            name = dname.split('/')
            TEXT1[0] = ("Deleting Directory '%s'" %name[-1])
            log_file.writelines(TEXT1[0])
            BOX_TEXT.append(TEXT1[0])
            self.sig.text_browser.emit()
            try:
                os.rmdir(dname)		#Delete Directory
                TEXT1[0] = ("'%s' Directory Deleted" %name[-1])
                log_file.writelines(TEXT1[0] + "\n")
                BOX_TEXT.append(TEXT1[0])
                self.sig.text_browser.emit()
            except:
                TEXT1[0] = ("Cannot Delete Directory : '%s'" %name[-1])
                log_file.writelines(TEXT1[0] + "\n")
                BOX_TEXT.append(TEXT1[0])
                self.sig.text_browser.emit()
            i = i + 1

        line = "[" + str(time.asctime()) + "]    directory deletion ended\n\n"
        log_file.writelines(line)
        log_file.close()
