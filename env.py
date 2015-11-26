import os, time, sys

#To Find UserName
import getpass
"""-----------------------------------------------
	| Lists Involving Environment Variables for |
	| Directory names and File names 			|
--------------------------------------------------"""
#Username
user_name = getpass.getuser()

#Current Directory
curr = os.getcwd()

#Directory Where Log File will be created
log_dir = curr + "/log/"

if(sys.platform == 'linux'):
    #Home Directory
    home = "/home/" + user_name + "/"

    #Location Where Disks Are Stored
    disk_path = "/media/" + user_name + "/"

#Date
date = time.strftime("%d-%m-%Y")

#Log File Location
rec_log = log_dir + date



"""-----------------------------------------------
	| Lists Involving Copying, Deleting Actions |
--------------------------------------------------"""
#Dictionary Containing Source and Target of Locations	[{'source' : "", 'target' : ""}, ...]
sync_list = []

#Reverse Of Above Dictionary to Perform Backward Copy
rev_list = []

#List Contains Source File Locations
cp_file_from = []
#Location of Target Where File Will Be Copied
file2cp = []
#Directories To Be Created At The Target
dir2cp = []

#Extra Files At Target To Be Deleted
del_file_from = []
#Extra Target Directories To Be Deleted
del_dir_from = []

#File Source Location For Collision File
col_cp_src = []

conf_res = []

#Contains Lists To Be Emptied Before Starting Fetching Process
lists = [cp_file_from, del_file_from, del_dir_from, file2cp, dir2cp, col_cp_src]

#Cotains Disk Details	[[name, total_size, amt_used, amt_available], ...]
disk_info = []

#Stores 1 if Changes Done With Locations Window
loc_changed = [0]

#About Text for About Menu in MenuBar
about_text = "<b>Synchronizer</b> <p><i>Uranus Lab</i></p><p>This Application can be used to syncronise between Places and Devices</p>"
#Link to find Help in Help Menu
help_link = "http://0.0.0.0"
#Link to Website
visit_link = "http://0.0.0.0"

"""-----------------------------------------------
	| Lists Involving Checking and Unchecking  |
	| actions in Location Window and Docks	   |
--------------------------------------------------"""
"""Location Window"""
#Checkbox status for left frame	[1, 0, 1, ....]
left_check = []
#Checkbox status for top frame	[[1, 0, 1, ...], .....]
top_check = []

#Dictionaries	[[{'source': "", 'target': ""}, ...], [], ...]
all_list = []
#Names of Left Devices
list_name = []

"""Docks"""
#Contains object of dock2 tree item	[[head object, tail, tail , ....], [], ...]
left_cp_obj = []
left_del_obj = []

#Contains index of file in copy list wrt object in dock2 object list	[[-1, index, index, .....], ........] 
#-1: for head which is not a file
cp_map = []
del_map = []

#Contains object of dock3 tree item	[object, level, file/folder], ...]
right_cp_obj = []
right_del_obj = []

#Contains dock 2 object of only files	[file1_obj, file2_obj, ...]	Files are in serial manner
left_cp_flist = []
left_del_flist = []

#Contains dock3 object of only files or tails	[object, level, file], .....]  Files are in serial manner
right_cp_flist = []
right_del_flist = []

