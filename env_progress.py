"""-----------------------------------------------
	| Lists Involving Copying, Deleting		   |
	| action progress to update status info	   |
--------------------------------------------------"""

#No of files to delete
TOT_DEL_FILE = [0]
#No of file Deleted
DEL_FILE = [0]
#Total amount to delete
TOT_DEL_AMT = [0]
#Amount Deleted
SIZE_DEL = [0]

#No of files to copy
TOT_CP_FILE = [0]
#No of files Copied
CP_FILE = [0]
#Total Amount To copy
TOT_CP_AMT = [0]
#Amount Copied
SIZE_COPIED = [0]

#Current filename on which action is being performed
CURR_FILE = [""]
#Current Filename
CURR_NAME = [""]
#Current File size
CURR_SIZE = [1]

#Time Elapsed
PRE_TIME = [0]

#Action to perform
ACTION = [" "]
BUSY = [" "]

#Average Speed of copying (only used to pass argument to delete progress function)
AVG_SPEED = [0]

#Text for TextBrowser
TEXT1 = [" "]
#Text For Progress Label
TEXT2 = [" "]
#Value for ProgressBar
VAL = [0]
#Text For StatusBar
TEXT3 = [" "]

#Text Browser PIPE
BOX_TEXT = []


FETCH = [0]
GUI = [" "]
CURR_OBJ = []
CURR_ACT = [" "]
ACT_FILE_LIST = []

start_handle1 = 0
start_handle2 = 0
