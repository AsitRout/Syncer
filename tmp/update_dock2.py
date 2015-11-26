from PyQt4.QtGui import *
from PyQt4.QtCore import *

from env import *
from make_dock2 import *
from env2 import *

def update_sec_dock(self, action):
    self.start_handle = 0	#Stop Processing Signals emitted due to change in treewidget
    if(action == "copy"):
        tree = self.tree2
        file_cat = cp_filetype	#Variable at Line 27 in env2
        left_cp_obj.clear()
        obj_list = left_cp_obj	#Variable at Line 87 in env
        cp_map.clear()
        maps = cp_map		#Variable at Line 92 in env
        
    if(action == "del"):
        tree = self.del_tree
        file_cat = del_filetype	#Variable at Line 30 in env2
        left_del_obj.clear()
        obj_list = left_del_obj	#Variable at Line 88 in env2
        del_map.clear()
        maps = del_map		#Variable at Line 93 in env2

            
    if(action == "copy"):
        for i in range(len(cp_filetype)):
            cp_filetype[i].clear()
        make_fcategory(self, cp_file_from, "copy")		#Function at Line 22 in make_dock2
        
    if(action == "del"):
        for i in range(len(del_filetype)):
            del_filetype[i].clear()
        make_fcategory(self, del_file_from, "del")		#Function at Line 22 in make_dock2
    

    tree.clear()
    i = 0
    for item in file_cat:
        out_list = []
        out_map = []
        heading = type_name[i] + "(" + str(len(file_cat[i])) + ")"
        head = QTreeWidgetItem(tree, [heading])
        out_list.append(head)
        out_map.append(-1)
        head.setCheckState(0, Qt.Checked)
        head.setExpanded(True)
        if(len(item) == 0):
            head.setDisabled(True)
            head.setCheckState(0, Qt.Unchecked)
            
        for fname in file_cat[i]:
            size = fname[1]
            unit = ""
            if size < 1000:
                size = size
                unit = "Bytes"
            if size < 1000000: 
                size = size / 1000
                unit = "KB"
            if size > 1000000:
                size = size / 1000000
                unit = "MB"
            
            tmp_size = str(size)
            tmp_size = tmp_size.split('.')
            fsize = tmp_size[0]  + '.' + tmp_size[1][:1] + unit
            tail = QTreeWidgetItem(head, [fname[0], fsize, fname[2]])
            out_list.append(tail)
            out_map.append(fname[3])
            tail.setCheckState(0, Qt.Checked)

        obj_list.append(out_list)
        maps.append(out_map)
        i = i + 1
    self.start_handle = 2	#Start Processing changes made to treewidget
    
