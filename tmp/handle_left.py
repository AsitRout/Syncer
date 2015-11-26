from PyQt4.QtGui import *
from PyQt4.QtCore import *

#from env import *

def left_tick_handle(self, ob, action):
    if(self.start_handle == 2):
        if(action == "copy"):
            tree = self.tree2
            obj_list = left_cp_obj	#Variable at Line 87 in env
            TOT_FILE = TOT_CP_FILE	#Variable at Line 16 in env_progress
            
        if(action == "del"):
            tree = self.del_tree
            obj_list = left_del_obj	#Variable at Line 87 in env
            TOT_FILE = TOT_DEL_FILE	#Variable at Line 7 in env_progress
            
        tree.blockSignals(True)		#Block Other Signals to tree
        out_len = len(obj_list)
        outer_index = 0
        flag = 0
        in_index = 0
        
        #Finding index of the object in object_list
        while(outer_index < out_len):
            in_index =  0
            in_len = len(obj_list[outer_index])
            while(in_index < in_len):
                if(obj_list[outer_index][in_index] == ob):
                    flag = 1
                    break
                in_index = in_index + 1
            if(flag):
                break
            outer_index = outer_index + 1

        if(in_index == 0):	#It is a head and checked
            if(ob.checkState(0) == Qt.Checked):
                obj_list[outer_index][0].setCheckState(0, Qt.Checked)
                size = len(obj_list[outer_index])
                i = 1
                
                #Check Every Tail
                while(i < size):
                    if(obj_list[outer_index][i].checkState(0) == Qt.Unchecked):
                        obj_list[outer_index][i].setCheckState(0, Qt.Checked)
                        TOT_FILE[0] = TOT_FILE[0] + 1
                        self.handle_right(obj_list[outer_index][i], action)		#Reflect change to Tree in Dock3 func at Line 431
                    i = i + 1
                    
                tree.blockSignals(False)		#No more block signals from tree
                return
                    
            if(ob.checkState(0) == Qt.Unchecked):	#It is a head and unchecked
                obj_list[outer_index][0].setCheckState(0, Qt.Unchecked)
                size = len(obj_list[outer_index])
                i = 1
                
                #Uncheck Every Tail
                while(i < size):
                    if(obj_list[outer_index][i].checkState(0) == Qt.Checked):
                        obj_list[outer_index][i].setCheckState(0, Qt.Unchecked)
                        TOT_FILE[0] = TOT_FILE[0] - 1
                        self.handle_right(obj_list[outer_index][i], action)		#Reflect change to Tree in Dock3 func at Line 431
                    i = i + 1
                    
                tree.blockSignals(False)	#No more block signals from tree
                return

                
        if(ob.checkState(0) == Qt.Checked):		#It is Tail and Checked
            if(obj_list[outer_index][0].checkState(0) == Qt.Unchecked):
                obj_list[outer_index][0].setCheckState(0, Qt.Checked)
            TOT_FILE[0] = TOT_FILE[0] + 1
            handle_right(self, ob, action)		#Reflect change to Tree in Dock3 func at Line 431
            tree.blockSignals(False)			#No more block signals from tree
            return
        
        if(ob.checkState(0) == Qt.Unchecked):		#It is Tail and Unchecked
            TOT_FILE[0] = TOT_FILE[0] - 1
            size = len(obj_list[outer_index])
            i = 1
            flag = 0

            #Check If all tail of this head are unchecked
            while i < size:
                if(obj_list[outer_index][i].checkState(0) == Qt.Checked):
                    flag = 1
                    break
                i = i + 1
            
            if(not flag):	#All tails are Unchecked
                obj_list[outer_index][0].setCheckState(0, Qt.Unchecked)
            handle_right(self, ob, action)		#Reflect change to Tree in Dock3 func at Line 431
            tree.blockSignals(False)			#No more block signals from tree
            return
        
"""
It reflect changes made in dock2 to dock3 by calling dock3 handler function
"""
def handle_right(self, ob, action):
    if(action == "copy"):
        left = left_cp_flist		#Variable at Line 100 in env
        right = right_cp_flist		#Variable at Line 104 in env
        file_from = cp_file_from	        #Variable at Line 43 in env
        F_SIZE = TOT_CP_AMT			#Variable at Line 20 in env_progress
        
    if(action == "del"):
        left = left_del_flist		#Variable at Line 101 in env
        right = right_del_flist		#Variable at Line 105 in env
        file_from = del_file_from	        #Variable at Line 50 in env
        F_SIZE = TOT_DEL_AMT		#Variable at Line 11 in env_progress
        
    i = 0
    #Search index of object in object list
    size = len(left)
    while(i < size):
        if(left[i] == ob):
            break
        i = i + 1

    s = os.path.getsize(file_from[i])
    
    if(left[i].checkState(0) == Qt.Checked):
        F_SIZE[0] = F_SIZE[0] + s / 1000000
        right[i].setCheckState(0, Qt.Checked)		#Right treewidget handler called

    if(left[i].checkState(0) == Qt.Unchecked):
        F_SIZE[0] = F_SIZE[0] - s / 1000000
        right[i].setCheckState(0, Qt.Unchecked)		#Right treewidget handler called

    text4 = ("\t<COPY>Files: 000/%d\tAmount: 0000/%d(MB)\t\t\t<DELETE>Files: 000/%d\tAmount: 0000/%d(MB)" %(TOT_CP_FILE[0], TOT_CP_AMT[0], TOT_DEL_FILE[0], TOT_DEL_AMT[0]))
    TEXT2[0] = text4
    self.sig.prog_lab.emit()

    TEXT3[0] = ("%d Files To Copy and %d Files To Delete" %(TOT_CP_FILE[0], TOT_DEL_FILE[0]))
    self.sig.stat_bar.emit()
    
