from env import *
from env_progress import *
from sync import *

#The Fetch Function
def on_fetch(self, fetch_list):
    """
    Initialize environment variables for progress updates
    """
    TOT_DEL_FILE[0] = 0
    TOT_DEL_AMT[0] = 0

    TOT_CP_FILE[0] = 0
    TOT_CP_AMT[0] = 0

    for item in fetch_list:
        tar_name = item['target']
        source_name = item['source']

        #Temporary List for storing file paths and directory paths
        tmp_tcp_dir = []
        tmp_tcp_file = []
        tmp_scp_dir = []
        tmp_scp_file = []
        tmp_cp_file_from = []
        tmp_cp_dir_from = []
        tmp_file2cp = []
        tmp_dir2cp = []
        tmp_file2del = []
        tmp_dir2del = []
        tmp_col_src = []
        tmp_col_tar = []
        empty = []
        #Above temporary lists which are required to be cleared before next making list operation
        tmp_list_name = [empty, tmp_col_src, tmp_col_tar, tmp_tcp_dir, tmp_tcp_file, tmp_scp_dir, tmp_scp_file, tmp_cp_file_from, tmp_cp_dir_from, tmp_file2cp, tmp_dir2cp, tmp_file2del, tmp_dir2del]

        """
        Making File List For COPYING operation
        Function in sync file
        """
        make_list(self, item, tmp_tcp_dir, tmp_tcp_file, tmp_scp_dir, tmp_scp_file, tmp_cp_file_from, tmp_cp_dir_from, "copy")
        
        #Find Directories to be copied
        onfetch(self, tmp_scp_dir, tmp_tcp_dir, tmp_dir2cp, tmp_cp_dir_from, empty, "copy")
        s = len(tmp_dir2cp)
        
        i = 0
        while(i < s):
            dir2cp.append(tar_name + tmp_dir2cp[i][1:])		#Append to main lists
            i = i + 1
            
        
        #Find Files to be copied
        onfetch(self, tmp_scp_file, tmp_tcp_file, tmp_file2cp, tmp_cp_file_from, tmp_col_src, "copy")
        s = len(tmp_cp_file_from)

        i = 0
        while(i < s):
            file2cp.append(tar_name + tmp_file2cp[i][1:])	#Append to main list
            cp_file_from.append(tmp_cp_file_from[i])		#Append to main list
            i = i + 1

        i = 0
        col_len = len(tmp_col_src)
        while(i < col_len):
            col_cp_src.append(tmp_col_src[i])           #Append Collision File To Main List
            i = i + 1

        i = 0
        while(i < len(tmp_list_name)):
              tmp_list_name[i].clear()		#Clear temporary lists to make delete list
              i = i + 1

        #Store sizes in env_progress variables
        TOT_CP_FILE[0] = TOT_CP_FILE[0] + s
    
        """
        Make list of file paths and directory pathsfor delete operation
        """
        make_list(self, item, tmp_tcp_dir, tmp_tcp_file, tmp_scp_dir, tmp_scp_file, tmp_cp_file_from, tmp_cp_dir_from, "del")
        
        #Find Directories to be deleted
        onfetch(self, tmp_scp_dir, tmp_tcp_dir, tmp_dir2del, tmp_cp_dir_from, empty, "del")
        s = len(tmp_cp_dir_from)
        i = 0
        while(i < s):
            del_dir_from.append(tmp_cp_dir_from[i])		#Append to main list
            i = i + 1
        
        #Find Files to be deleted
        onfetch(self, tmp_scp_file, tmp_tcp_file, tmp_file2del, tmp_cp_file_from, empty, "del")
        s = len(tmp_cp_file_from)
        i = 0
        while(i < s):
            del_file_from.append(tmp_cp_file_from[i])	#Append to main list
            i = i + 1	

        TOT_DEL_FILE[0] = TOT_DEL_FILE[0] + s
