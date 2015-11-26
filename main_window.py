import sys, os
import pickle
import threading
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#Contains File Actions
from sync import *

#Contain Variables for file action, dock checkboxes and objects
from env import *

#Contains Filetype Variables
from env2 import *

#Contain Progress Related Variables
from env_progress import *

#Contains disk detail creation function
from disk_detail import *

#Contains File types list creation function
from make_dock2 import *

#Location define Window
from set_dict import *

#Log Window
from log import *

#StyleSheet
from style1 import *

from copy_confirm import *

from fetching import *
from fetch import *

"""
Signals for progress function update
"""
class signal(QObject):
    text_browser = pyqtSignal()	#Text Browser Signal
    prog_bar = pyqtSignal()	#ProgressBar Signal
    prog_lab = pyqtSignal()	#Progress Label Signal
    stat_bar = pyqtSignal()	#StatusBar Signal
    dock1 = pyqtSignal()	#Disk Detail Signal
    

"""
Centre Widgets for MainWindow
"""
class centre(QWidget):
    def __init__(self):
        super(centre, self).__init__()
        log_file = open(rec_log, "a+")
        line = "\n\n\n\n-----------------------------------------------------------------------\n"
        log_file.writelines(line)
        line = "[" + str(time.asctime()) + "]    program started    setting up window\n"
        log_file.writelines(line)
        
        try:
            """
            Start handling dock2 treewidget signal
            -1: TreeWidget not Created
            0: Creating TreeWidget, No Signal Processed
            2: TreeWidget Created, Signal will be processed
            """
            self.start_handle1 = -1
			
            """
            Fetch Function Has Been Called or Not
            0: Not Called
            1: Straight Fetch Called
            2: Reverse Fetch Called
            """
            self.fetched = 0	

	    #Connecting Signals To Handlers
            self.sig = signal()
            
            self.sig.prog_bar.connect(lambda: self.update_progbar())
            self.sig.prog_lab.connect(lambda: self.update_proglab())
            self.sig.stat_bar.connect(lambda: self.update_statbar())
            #self.sig.text_browser.connect(lambda: self.update_text1())
            self.sig.dock1.connect(lambda: self.make_dock1())

            #Load Pickled Lists
            self.loadlist()
            
            #Create Centre Widgets
            self.set_centre()
            self.sig.text_browser.connect(lambda: self.update_text1())
            
	    #Get Functions From MainWindow
            self.get_functions()
            
            #Update Dock3 with Source Folder
            self.update_dock3()
            
	    #Thread to Update ProgressBar, StatusBar, Progress Label and Disk Detail
            self.prog_thread = threading.Thread(target = self.start_thread, args = ())
            self.prog_thread.daemon = True
            self.prog_thread.start()
	    #Thread To Perform File Actions
            self.action_thread = threading.Thread(target = self.file_action, args = ())
            self.action_thread.daemon = True
            self.action_thread.start()
           
            line = "[" + str(time.asctime()) + "]    window set up completed successfully\n\n"
            log_file.writelines(line)
            log_file.close()
        except:
            line = "[" + str(time.asctime()) + "]    failed to setup window!!!CLOSING\n\n"
            log_file.writelines(line)
        log_file.close()
    
    
    def loadlist(self):
        try:
            list1 = pickle.load(open("setting/all_list.p", "rb"))
            list2 = pickle.load(open("setting/list_name.p", "rb"))
            list3 = pickle.load(open("setting/left_check.p", "rb"))
            list4 = pickle.load(open("setting/top_check.p", "rb"))
            for item in list1:
                all_list.append(item)		#Variable at Line 81 in env
            for item in list2:
                list_name.append(item)		#Variable at Line 83 in env
            for item in list3:
                left_check.append(item)		#Variable at Line 76 in env
            for item in list4:
                top_check.append(item)		#Variable at Line 78 in env
            self.make_synclist()
        except:
            pass
        """        
        TEXT1[0] = "Press A Button To Start Any Job"
        BOX_TEXT.append(TEXT1[0])
        self.sig.text_browser.emit()
        """
    
    def make_synclist(self):
        tmp_list = []
        i = 0
        while(i < len(all_list)):
            j = 0
            while(j < len(all_list[i])):
		#If Checked add to sync list
                if(top_check[i][j] == 1):
                    tmp_list.append(all_list[i][j])
                j = j + 1
            i = i + 1
            
        sync_list.clear()
        for item in tmp_list:
            sync_list.append(item)
        self.make_rev_list()	#Make List For Reverse Copy

        
        if(len(sync_list) == 0):
            TEXT3[0] = "No Locations Defined"
            self.sig.stat_bar.emit()
            
            TEXT1[0] = "Define Locations"
            BOX_TEXT.append(TEXT1[0])
            self.sig.text_browser.emit()
        
        
    def get_functions(self):
	#Update Dock3
        self.update_right_dock = getattr(central, "update_right_dock")
	#Lock Dock3 when file operations going on
        self.lock_right = getattr(central, "lock_right")

    def set_centre(self):
        dictionary = QPushButton("LOCATION")
        self.make_button(dictionary, "", "", self.dict)
        dictionary.setMinimumHeight(50)
        
        self.fetch1 = QPushButton("FETCH")
        self.make_button(self.fetch1, "", "", self.fetch_btn)
        self.fetch1.setMinimumHeight(50)

        self.copy1 = QPushButton("COPY 1-2")
        self.make_button(self.copy1, "", "", self.copy12)
        self.copy1.setMinimumHeight(50)

        self.copy2 = QPushButton("COPY 2-1")
        self.make_button(self.copy2, "", "", self.copy21)
        self.copy2.setMinimumHeight(50)

        self.del1 = QPushButton("DELETE 1")
        self.make_button(self.del1, "", "", self.delete1)
        self.del1.setMinimumHeight(50)

        self.del2 = QPushButton("DELETE 2")
        self.make_button(self.del2, "", "", self.delete2)
        self.del2.setMinimumHeight(50)

        self.sync1 = QPushButton("SYNC")
        self.make_button(self.sync1, "", "", self.sync)
        self.sync1.setMinimumHeight(50)

        log = QPushButton("LOG")
        self.make_button(log, "", "", self.log)
        log.setMinimumHeight(50)

        #Set StyleSheet
        but_obj = [dictionary, self.fetch1, self.copy1, self.copy2, self.del1, self.del2, self.sync1, log]
        set_style(but_obj, "button")
        
        self.dock1 = QDockWidget("", self)
        self.dock1.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.make_dock1()
        self.dock2 = QDockWidget("", self)
        self.dock2.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.make_dock2()
        self.text_box = QTextBrowser()
        set_style(self.text_box, "text_browser")
        
        self.progress_text = QLabel("\t| COPY | Files: 000/000\tAmount: 0000/0000(MB)\t\t\t| DELETE | Files: 000/000\tAmount: 0000/0000(MB)")
        set_style(self.progress_text, "prog_lab")
        self.pbar = QProgressBar(self)
        set_style(self.pbar, "prog_bar")
        self.pbar.setValue(0)
        self.progress_text.setMaximumHeight(20)
        self.pbar.setMaximumHeight(25)
        
        grid = QGridLayout()
        grid.setSpacing(0)
        grid.addWidget(dictionary, 0, 0)
        grid.addWidget(self.fetch1, 0, 1)
        grid.addWidget(self.copy1, 0, 2)
        grid.addWidget(self.copy2, 0, 3)
        grid.addWidget(self.del1, 0, 4)
        grid.addWidget(self.del2, 0, 5)
        grid.addWidget(self.sync1, 0, 6)
        grid.addWidget(log, 0, 7)
        
        grid.addWidget(self.dock1, 3, 0, 5, 4)
        grid.addWidget(self.dock2, 3, 4, 9, 4)
        grid.addWidget(self.text_box, 8, 0, 4, 4)
        grid.addWidget(self.progress_text, 12, 0, 1, 8)
        grid.addWidget(self.pbar, 13, 0, 1, 8)
        self.setLayout(grid)

        TEXT3[0] = "Press A Button To Start Any Job"
        self.sig.stat_bar.emit()



    def update_sec_dock(self, action):
        
        self.start_handle1 = 0	#Stop Processing Signals emitted due to change in treewidget
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
        self.start_handle1= 2	#Start Processing changes made to treewidget
        


            
    def make_dock1(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        grid = QGridLayout()

        show_disk(centre)
        i = 0
        j = 0
        while i < len(disk_info):
            detail = ""
            disk_label = QLabel(disk_info[i][0])
            disk_label.setStyleSheet("QLabel {font : Normal 14px 'Serif'; color : rgb(86, 90, 85); background-color : 0;}")
            disk_label.setMaximumWidth(150)
            bar = QProgressBar()
            set_style(bar, "disk_bar")
            bar.setValue((disk_info[i][2] / disk_info[i][1]) * 100)
            
            total = str(disk_info[i][1]).split('.')
            total = total[0] + "." + total[-1][:1]
            used = str(disk_info[i][2]).split('.')
            used = used[0] + "." + used[-1][:1]
            avail = str(disk_info[i][3]).split('.')
            avail = avail[0] + "." + avail[-1][:1]
            
            detail = "Total: " + total + "GB  Used: " + used + "GB  Available: " + avail + "GB"

            det = QLabel(detail)
            det.setStyleSheet("QLabel {font : Normal 12px 'Monospace'; color : rgb(38, 97, 94);}")
            det.setMaximumHeight(10)
            grid.addWidget(bar, j, 0, 1, 6)
            grid.addWidget(disk_label, j, 1)
            j = j + 1
            grid.addWidget(det, j, 0)
            j = j + 1
            i = i + 1

        space = QLabel("\n\n\n\n")
        grid.addWidget(space, j, 0)
        frame.setLayout(grid)
        self.dock1.setWidget(frame)


    def update_dock3(self):
        if(len(sync_list) == 0):
           return
        tmp  = []
        for item in sync_list:
            tmp.append(item['source'])
        tmp.sort()
            
        self.update_right_dock(self, tmp, "copy")
        self.update_right_dock(self, tmp, "del")

    def make_button(self, item, text = "", icon = None, handle = None):
        item.setIcon(QIcon(icon))
        item.setIconSize(QSize(50, 50))
        item.connect(item, SIGNAL("clicked()"), handle)

    def make_dock2(self):
        self.dock2.setMaximumWidth(500)
        self.dock2.setMinimumWidth(500)
        self.dock2.setObjectName("Log Dock")
        self.dock2.isEnabled
        
        self.tree2 = QTreeWidget()
        self.tree2.setFocusPolicy(Qt.NoFocus)
        set_style(self.tree2, "tree")
        self.tree2.setHeaderHidden(True)
        self.tree2.setColumnCount(3)
        self.tree2.setColumnWidth(0, 300)
        self.tree2.setColumnWidth(1, 80)
        self.tree2.setColumnWidth(2, 80)
        self.tree2.itemChanged.connect(lambda ob = self : self.left_tick_handle(ob, "copy"))
        
        self.del_tree = QTreeWidget()
        self.del_tree.setFocusPolicy(Qt.NoFocus)
        set_style(self.del_tree, "tree")
        self.del_tree.setHeaderHidden(True)
        self.del_tree.itemChanged.connect(lambda ob = self : self.left_tick_handle(ob, "del"))
        self.del_tree.setColumnCount(3)
        self.del_tree.setColumnWidth(0, 260)
        
        tab = QTabWidget()
        tab.setFocusPolicy(Qt.NoFocus)
        tab1 = QWidget()
        tab2 = QWidget()
        
        txt1 = "FILES TO COPY"
        txt2 = "FILES TO DELETE"
        tab.addTab(tab1, txt1)
        tab.addTab(tab2, txt2)
        #Set StyleSheet
        set_style(tab, "left_tab")
        
        cp_grid = QGridLayout()
        del_grid = QGridLayout()
        cp_grid.addWidget(self.tree2, 0, 0)
        del_grid.addWidget(self.del_tree, 0, 0)

        tab1.setLayout(cp_grid)
        tab2.setLayout(del_grid)

        self.dock2.setWidget(tab)        

        self.update_sec_dock("copy")
        self.update_sec_dock("del")
    
    def left_tick_handle(self, ob, action):
        if(self.start_handle1 == 2):
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
                self.handle_right(ob, action)		#Reflect change to Tree in Dock3 func at Line 431
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
                self.handle_right(ob, action)		#Reflect change to Tree in Dock3 func at Line 431
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
        
            

    """
    Update window when there is no file to copy or delete
    """
    def nofile(self):
        #Update Dock3 With Source Folder Only
        tmp  = []
        for item in sync_list:
            tmp.append(item['source'])
        tmp.sort()
            
        self.update_right_dock(self, tmp, "copy")
        self.update_right_dock(self, tmp, "del")
        self.update_sec_dock("copy")
        self.update_sec_dock("del")
        TEXT3[0] = "No Files To Take Action"
        TEXT1[0] = "No Files Left To Perform Next Task"
        BOX_TEXT.append(TEXT1[0])
        self.sig.text_browser.emit()
        self.sig.stat_bar.emit()
            
    """
    If there is no item in dictionary to fetch files from
    """
    def target_empty(self, fetch_list):
        if(len(fetch_list) == 0):
            self.clear_list()
            self.update_right_dock(self, cp_file_from, "copy")
            self.update_right_dock(self, del_file_from, "del")
            self.update_sec_dock("copy")
            self.update_sec_dock("del")
            
            TEXT1[0] = "Define Locations With LOCATION Button On Left"
            BOX_TEXT.append(TEXT1[0])
            self.sig.text_browser.emit()
            line = "------------------------------------------------------"
            TEXT1[0] = line
            BOX_TEXT.append(TEXT1[0])
            self.sig.text_browser.emit()
            
            TEXT3[0] = "No Locations Defined"
            self.sig.stat_bar.emit()
            return 0
        return 1

    """
    List required to be cleared for fetching process otherwise lists will be appended
    List Variable at Line 55 in env
    """
    def clear_list(self):
        list_size = len(lists)
        for i in range(list_size):
            lists[i].clear()

    def fetch_btn(self):
        self.call_fetch_btn(1)
        
    def call_fetch_btn(self, i):
        msg = "Are You Sure To Start\nFetchin Process"
        reply = QMessageBox.question(self, 'Message', msg, QMessageBox.Yes, QMessageBox.No)
        if(reply == QMessageBox.No):
            return
        
        self.clear_list()		        #Clear lists requred to store file and directory names
        
        if(i == 1):
            if(not self.target_empty(sync_list)):	#Check If There is no location in dictionary
                return
            FETCH[0] = i
            ACTION[0] = "fetch1"
        if(i == 2):
            if(not self.target_empty(rev_list)):	#Check If There is no location in dictionary
                return
            FETCH[0] = i
            ACTION[0] = "fetch2"
            
        self.show_busy()
        self.after_fetch()


    def after_fetch(self):
        os.chdir(curr)
        self.update_right_dock(self, cp_file_from, "copy")
        self.update_right_dock(self, del_file_from, "del")
        self.update_sec_dock("copy")
        self.update_sec_dock("del")
        self.make_mapping("copy")
        self.make_mapping("del")
        
        
    
        TEXT2[0] = ("\t<COPY>Files: 000/%d\tAmount: 0000/%d(MB)\t\t\t<DELETE>Files: 000/%d\tAmount: 0000/%d(MB)" %(TOT_CP_FILE[0], TOT_CP_AMT[0], TOT_DEL_FILE[0], TOT_DEL_AMT[0]))
        self.sig.prog_lab.emit()

        line = "------------------------------------------------------"
        TEXT1[0] = line
        BOX_TEXT.append(TEXT1[0])
        self.sig.text_browser.emit()
        
        text1 = str(len(dir2cp)) + " Folders and " + str(len(file2cp)) + " Files To Copy"
        TEXT1[0] = text1
        BOX_TEXT.append(TEXT1[0])
        self.sig.text_browser.emit()
        
        text2 = str(len(del_dir_from)) + " Folders and " + str(len(del_file_from)) + " Files To Delete"
        TEXT1[0] = text2
        BOX_TEXT.append(TEXT1[0])
        self.sig.text_browser.emit()

        TEXT1[0] = line
        BOX_TEXT.append(TEXT1[0])
        self.sig.text_browser.emit()
        
        text3 = str(TOT_CP_AMT[0]) + " MB" + " To Copy and "
        text4 = str(TOT_DEL_AMT[0]) + " MB" + " To Delete"
        TEXT3[0] = text3 + text4
        self.sig.stat_bar.emit()

        log_file = open(rec_log, "a+")
        line = "[" + str(time.asctime()) + "]    " + text1 + " and " + text2 + "\n"
        log_file.writelines(line)
        log_file.close()
        
        	
    #Copy from source to target        
    def copy12(self):
        if(not self.target_empty(sync_list)):	#If copy button pressed before fetch button this will do location check
            return
        
        if(self.fetched != 1):	#If straight fetch not done
            self.fetched = 1
            self.call_fetch_btn(1)	#Fetch
        
        if(not cp_file_from):	#If no files to copy
            self.nofile()	#Update Window
            return
            
        msg = "Are You Sure To Start The Copying Process?"
        reply = QMessageBox.question(self, 'Confirm', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply == QMessageBox.No):
            return
        if(col_cp_src):
            self.col_care()
        ACTION[0] = "copy12"	#Sets environment variable for file action thread to start copy process
       
    #Delete At Target
    def delete1(self):        
        if(not self.target_empty(sync_list)):
            return

        if(self.fetched != 1):
            self.fetched = 1
            self.call_fetch_btn(1)
            
        if(not del_file_from):
            self.nofile()
            return
            
        msg = "Are You Sure To Delete Extra Items From Target?"
        reply = QMessageBox.question(self, 'Confirm', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply == QMessageBox.No):
            return

        ACTION[0] = "del1"

    #Copy from Target to source
    def copy21(self):
        if(not self.target_empty(sync_list)):
            return
        
        if(self.fetched != 2):
            self.fetched = 2
            self.call_fetch_btn(2)

        if(not cp_file_from):
            self.nofile()
            return
        
        msg = "Are You Sure To Start The Reversed Copying Process?"
        reply = QMessageBox.question(self, 'Confirm', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply == QMessageBox.No):
            return
        if(col_cp_src):
            self.col_care()
        ACTION[0] = "copy21"

    #Delete At Source
    def delete2(self):        
        if(not self.target_empty(sync_list)):
            return
            
        if(self.fetched != 2):
            self.fetched = 2
            self.call_fetch_btn(2)
            
        if(not del_file_from):
            self.nofile()
            return
        
        msg = "Are You Sure To Delete Extra Item From Source?"
        reply = QMessageBox.question(self, 'Confirm', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply == QMessageBox.No):
            return
        ACTION[0] = "del2"
        

    """
    files in copy12 is same as del2
    files in copy21 is same as del1
    """

    """
    Thread that checks ACTION environment variable every 1 second 
    and perform action if it is set
    """
    def file_action(self):
        while True:

            if(ACTION[0] == "fetch1"):
                self.on_fetch(sync_list)
                ACTION[0] = " "
                BUSY[0] = " "
                continue

            if(ACTION[0] == "fetch2"):
                self.on_fetch(rev_list)
                ACTION[0] = " "
                BUSY[0] = " "
                continue
            
            if(ACTION[0] == "copy12"):
                self.lock_widgets("lock")
                
                mkdir(self, dir2cp)
                cp(self, file2cp, cp_file_from)

                ACTION[0] = " "
                self.lock_widgets("unlock")
                self.copy1.setFocus()
                continue
                
            if(ACTION[0] == "copy21"):
                self.lock_widgets("lock")
                
                mkdir(self, dir2cp)
                cp(self, file2cp, cp_file_from)

                ACTION[0] = " "
                self.lock_widgets("unlock")
                self.copy2.setFocus()
                continue
                
            if(ACTION[0] == "del1"):
                self.lock_widgets("lock")
                
                rm(self, del_file_from)
                rmdir(self, del_dir_from)

                ACTION[0] = " "
                self.lock_widgets("unlock")
                self.del1.setFocus()
                continue

            if(ACTION[0] == "del2"):
                self.lock_widgets("lock")
                
                rm(self, del_file_from)
                rmdir(self, del_dir_from)

                ACTION[0] == " "
                self.lock_widgets("unlock")
                self.del2.setFocus()
                continue
                
            time.sleep(1)

    def show_busy(self):    
        self.splash = busy()
        self.splash.resize(150, 150)

        desktopRect = QApplication.desktop().availableGeometry(self);
        middle = desktopRect.center();
        self.splash.move(middle.x() - 200 * 0.5, middle.y() - 200);
            
        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.white)
        self.splash.setPalette(pal)

        self.splash.setWindowFlags(Qt.FramelessWindowHint)
        self.splash.exec_()
        
    def col_care(self):
        conf_res.clear()
        i = 0
        j = 0
        size = len(col_cp_src)
        while(i < size):
            if(col_cp_src[i] == cp_file_from[j]):
                if(left_cp_flist[j].checkState(0) == Qt.Unchecked):
                    i = i + 1
                    j = j + 1
                    continue
                conf_res.append(j)
                i = i + 1
                j = j + 1
                continue
            j = j + 1
        if(not conf_res):
            return

        i = 0
        while(i < size):
            left_cp_flist[conf_res[i]].setCheckState(0, Qt.Unchecked)
            i = i + 1
            
        self.get_conf()
        
                
            
    def get_conf(self):
        conf = cp_conf()
        conf.setWindowTitle("File Collision Found")
        conf.resize(350, 400)

        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.white)
        conf.setPalette(pal)
    
        conf.exec_()
        
        
    """
    Locke centre widgets when file action is going on
    and unlock it when completed
    """
    def lock_widgets(self, action):
        if(action == "lock"):
            self.tree2.setDisabled(True)
            self.del_tree.setDisabled(True)
            self.fetch1.setDisabled(True)
            self.copy1.setDisabled(True)
            self.copy2.setDisabled(True)
            self.del1.setDisabled(True)
            self.del2.setDisabled(True)
            self.sync1.setDisabled(True)
            
            self.lock_right(self, "lock")	#Lock dock3

        if(action == "unlock"):
            self.tree2.setEnabled(True)

            self.fetch1.setEnabled(True)
            self.copy1.setEnabled(True)
            self.copy2.setEnabled(True)
            self.del1.setEnabled(True)
            self.del2.setEnabled(True)
            self.sync1.setEnabled(True)
            self.del_tree.setEnabled(True)

            self.lock_right(self, "unlock")	#Unlock dock3
        
    """
    Make reverse sync list for copy21 and del2
    """
    def make_rev_list(self):
        rev_list.clear()
        for item in sync_list:
	    #Swap dictionary values
            tmp = {'source': "", 'target' : ""}
            tmp['source'] = item['target']
            tmp['target'] = item['source']
            rev_list.append(tmp)
        
	
    def sync(self):
        if(not self.target_empty(sync_list)):
            return
        
        self.copy12()
        self.delete1()

    """
    Location Window Handler
    """
    def dict(self):
        if(len(all_list) == 0):	#If There is no device add a device
            text, ok = QInputDialog.getText(self, 'Input Dialog', 'Add a Device(Enter Name of Device):')
            if(ok):
                list_name.append(text)
                all_list.append([{'source' : "", 'target' : ""}])
                top_check.append([0])
                left_check.append(0)
            else:
                return
            
        top = set_dict()
        top.setWindowTitle("Select Locations")
        top.resize(900, 600)
        top.exec_()
        
        if(loc_changed[-1] == 1):	#If changes made in location window
            if(ACTION[0] == " "):
                self.fetched = 1
                self.call_fetch_btn(1)
                
            log_file = open(rec_log, "a+")
            line = "[" + str(time.asctime()) + "]    locations dictionary changed\n"
            log_file.writelines(line)
            log_file.close()

        loc_changed.clear()
        loc_changed.append(0)
        self.make_rev_list()

    """
    Progress Thread Handler
    Checks if any action going on every 1 seconds
    """
    def start_thread(self):
        i = 0
        while True:                
            if(ACTION[0] != " "):
                #Calls function if file action going on                
                self.progress_thread()
                continue
	    #Update Dock1 Every 5 seconds
            if(i == 5):
                self.sig.dock1.emit()
                i = 0
                
            time.sleep(1)
            i = i + 1

    """
    Update Progress and Dock1 untill file action goes on
    """
    def progress_thread(self):
	#If action is copy
        if(ACTION[0] == "copy12" or ACTION[0] == "copy21"):
            prev  = 0
            avg = 0
            i = 1
            while True:
                if(ACTION[0] == " "):	#If action completed but progress bar is not 100% due to time lag among two threads
                    if(VAL[0] != 100):
                         VAL[0] = 100
                         TEXT2[0] = ("\tFiles: %d/%d\tAmount: %d/%d(MB)\t\t\t\t\t\tElapsed: %d:%d\tAvg. Speed: %dMBPS" %(CP_FILE[0], TOT_CP_FILE[0], SIZE_COPIED[0], TOT_CP_AMT[0], mins, secs, avg_speed))
                         TEXT3[0] = "Copying: '%s'(%d/%d)MB 100%%" %(CURR_NAME[0], CURR_SIZE[0], CURR_SIZE[0])
    
                         self.sig.prog_bar.emit()
                         self.sig.prog_lab.emit()
                         self.sig.stat_bar.emit()
                         AVG_SPEED[0] = avg_speed
                         
                    return
                try:
                    cp_amt = (os.path.getsize(CURR_FILE[0])) / 1000000	#Find amount copied for current file
                except:
                    cp_amt = 0
                    
                amount = SIZE_COPIED[0] + cp_amt
                speed = (amount - prev) * 2
                prev = amount
                VAL[0] = (amount / TOT_CP_AMT[0]) * 100
                PRE_TIME[0] = PRE_TIME[0] + 0.5
                mins = PRE_TIME[0] / 60
                secs = PRE_TIME[0] % 60
                avg = avg + speed
                avg_speed = avg / i
                if(i % 5 == 0):
                    self.sig.dock1.emit()
                
                TEXT2[0] = ("\tFiles: %d/%d\tAmount: %d/%d(MB)\t\t\t\t\t\tElapsed: %d:%d\tAvg. Speed: %dMBPS" %(CP_FILE[0], TOT_CP_FILE[0], amount, TOT_CP_AMT[0], mins, secs, avg_speed))
                try:
                    TEXT3[0] = "Copying: '%s'(%d/%d)MB %d%%\t\t\tSpeed: %dMBPS" %(CURR_NAME[0], cp_amt, CURR_SIZE[0], (cp_amt / (CURR_SIZE[0]) * 100), speed)
                except:
                    TEXT3[0] = "Copying: '%s'(%d/%d)MB %d%%\t\t\tSpeed: %dMBPS" %(CURR_NAME[0], cp_amt, CURR_SIZE[0], 100, speed)
                    
                self.sig.prog_bar.emit()
                self.sig.prog_lab.emit()
                self.sig.stat_bar.emit()
                    
                time.sleep(0.5)
                i = i + 1
                
                        
		
	#If Delete action is going on
        if(ACTION[0] == "del1" or ACTION[0] == "del2"):
            while True:
                if(ACTION[0] == " "):	#If delete action completed but progress is not fully updated due to time lag among two threads
                    if(DEL_FILE[0] == TOT_DEL_FILE[0]):
                        TEXT2[0] = ("\tFiles: %d/%d\tAmount: %d/%d(MB)\t\t\t\t\t\tElapsed: %d:%d\tAvg. Speed: %dMBPS" %(CP_FILE[0], TOT_CP_FILE[0], SIZE_COPIED[0], TOT_CP_AMT[0], mins, secs, AVG_SPEED[0]))
                        TEXT3[0] = "Deleting: '%s'(%d)MB\t\tDeleted: %d/%d\t\tFreed: %d/%d(MB)" %(CURR_NAME[0], CURR_SIZE[0], TOT_DEL_FILE[0], TOT_DEL_FILE[0], TOT_DEL_AMT[0], TOT_DEL_AMT[0])
    
                        self.sig.prog_lab.emit()
                        self.sig.stat_bar.emit()
                    return
                PRE_TIME[0] = PRE_TIME[0] + 0.25
                mins = PRE_TIME[0] / 60
                secs = PRE_TIME[0] % 60

                TEXT2[0] = ("\tFiles: %d/%d\tAmount: %d/%d(MB)\t\t\t\t\t\tElapsed: %d:%d\tAvg. Speed: %dMBPS" %(CP_FILE[0], TOT_CP_FILE[0], SIZE_COPIED[0], TOT_CP_AMT[0], mins, secs, AVG_SPEED[0]))
                TEXT3[0] = "Deleting: '%s'(%d)MB\t\tDeleted: %d/%d\t\tFreed: %d/%d(MB)" %(CURR_NAME[0], CURR_SIZE[0], DEL_FILE[0], TOT_DEL_FILE[0], SIZE_DEL[0], TOT_DEL_AMT[0])
    
                self.sig.prog_lab.emit()
                self.sig.stat_bar.emit()
                    
                time.sleep(0.25)


    """
    BOX_TEXT is a pipe to which texts are pushed
    and this function flush them to Text Browser
    """
    def update_text1(self):        
        self.text_box.append("<font size = 3>" + BOX_TEXT[0] + "</font>")
        BOX_TEXT.remove(BOX_TEXT[0])
        self.text_box.moveCursor(QTextCursor.End)
        
    """
    Handler for progress label signal
    """
    def update_proglab(self):
        self.progress_text.setText(TEXT2[0])

    """
    Handler for Progress Bar Signal
    """
    def update_progbar(self):
        self.pbar.setValue(VAL[0])
       
    """
    Handler for Status Bar Signal
    """ 
    def update_statbar(self):
        central.status.showMessage(TEXT3[0])

    """
    Log Window
    """    
    def log(self):
        view_log = log_window()
        view_log.setWindowTitle("Log File")
        view_log.resize(900, 650)
        
        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.white)
        view_log.setPalette(pal)
        
        view_log.exec_()

    """
    Map dock2 file object and dock3 file object
    """
    def make_mapping(self, action):
        if(action == "copy"):
            right_list = right_cp_obj
            left_obj_map = cp_map
            left_list = left_cp_obj
            left_map = left_cp_flist
            right_map = right_cp_flist
            
        if(action == "del"):
            right_list = right_del_obj
            left_obj_map = del_map
            left_list = left_del_obj
            left_map = left_del_flist
            right_map = right_del_flist

        right_map.clear()
        left_map.clear()

        #Keeping only file object for dock3
        i = 0
        size = len(right_list)
        while(i < size):
            if(right_list[i][2] == 0):
                right_map.append(right_list[i][0])
            i = i + 1

        #Keeping only file objects for dock2
        tot_files = len(right_map)
        for i in range(tot_files):
            left_map.append(" ")

        out_len = len(left_obj_map)
        outer = 0
        while(outer < out_len):
            in_len = len(left_obj_map[outer])
            inner = 1
            while(inner < in_len):
                ind = left_obj_map[outer][inner]
                ele = left_list[outer][inner]
                left_map[ind] = ele
                inner = inner + 1
            outer = outer + 1


    
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


class central(QMainWindow):
    def __init__(self):
        super(central, self).__init__()
        """
        Start handling dock3 treewidget signal
        -1: TreeWidget not Created
        0: Creating TreeWidget, No Signal Processed
        2: TreeWidget Created, Signal will be processed
        """
        central.start_handle2 = -1

        self.init_menubar()
        self.init_statusbar()
        self.dock()
        self.def_central()	    #Set Centre Widgets

    
    def make_connection(self, text, icon = None, shortcut = None, statustip = "", check = False, connect = None):
        action = QAction(text, self)
        
        if (icon is not None):
            action.setIcon(QIcon(icon))
        if (shortcut is not None):
            action.setShortcut(shortcut)
        if (statustip is not None):
            action.setStatusTip(statustip)
            action.setToolTip(statustip)
        if (check):
            action.setCheckable(True)
        if (connect is not None):
            action.triggered.connect(connect)

        return action


    def init_menubar(self):
        menubar = self.menuBar()

        reset = menubar.addMenu("&Reset")
        reload = self.make_connection("Delete Locations", "icon.png", "ctrl+d", "Reset Locations", False, self.reset_loc)
        del_log = self.make_connection("Delete Logs", "icon.png", "ctrl+h", "Delete History", False, self.reset_history)
        self.add_submenu(reset, (reload, del_log))
        
        helpme = menubar.addMenu("&Help")
        about = self.make_connection("About", "icon.png", "ctrl+a", "About", False, self.about)
        sync_help = self.make_connection("Help", "icon.png", "ctrl+h", "View Help", False, self.help)
        visit = self.make_connection("Visit Web", "icon.png", "ctrl+v", "Visit Web", False, self.visit)
        self.add_submenu(helpme, (about, sync_help, visit))


    def init_statusbar(self):
        central.status = self.statusBar()
        set_style(central.status, "status_bar")
    
    def dock(self):
        self.log_dock = QDockWidget()
        self.log_dock.setMinimumWidth(300)
        self.log_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.log_dock.setObjectName("Log Dock")
        self.log_dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.log_dock)
        set_style(self.log_dock, "log_dock")
        
        
        central.tree = QTreeWidget()
        central.tree.setFocusPolicy(Qt.NoFocus)
        set_style(central.tree, "tree")
        self.tree.setHeaderLabels(["Files To Be Copied"])
        self.tree.setHeaderHidden(True)
        self.tree.setColumnCount(1)
        central.tree.itemChanged.connect(lambda ob = self : self.right_tick_handle(ob, "copy"))

        central.del_tree = QTreeWidget()
        central.del_tree.setFocusPolicy(Qt.NoFocus)
        set_style(central.del_tree, "tree")
        self.tree.setHeaderLabels(["Files To Be Deleted"])
        self.del_tree.setHeaderHidden(True)
        central.del_tree.itemChanged.connect(lambda ob = self : self.right_tick_handle(ob, "del"))
        
        tab = QTabWidget()
        tab.setFocusPolicy(Qt.NoFocus)
        tab1 = QWidget()
        tab2 = QWidget()

        set_style(tab, "tab")

        tab.addTab(tab1, "Files 2 Copy")
        tab.addTab(tab2, "Files 2 Delete")
        set_style(tab, "right_tab")
        self.log_dock.setWidget(tab)

        cp_grid = QGridLayout()
        del_grid = QGridLayout()
        cp_grid.addWidget(self.tree, 0, 0)
        del_grid.addWidget(self.del_tree, 0, 0)

        tab1.setLayout(cp_grid)
        tab2.setLayout(del_grid)

       
    #Add submenu to Menu            
    def add_submenu(self, menu, submenu):
        for item in submenu:
            if (item is None):
                menu.addSeparator()
            if (item):
                menu.addAction(item)


    #Delete Location Dictionaries and all settings related to them
    def reset_loc(self):
	#Pickled Files
        files = ['all_list.p', 'list_name.p', 'top_check.p', 'left_check.p']
        msg = "This Action Results\n"
        for item in files:
            msg = msg + "Delete '" + str(item) + "'\n"
            
        reply = QMessageBox.question(self, 'Confirm', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply == QMessageBox.No):
            return
        
        os.chdir(curr)
        for item in files:
            try:
                os.remove(item)
            except:
                pass

    #Delete All Log Files
    def reset_history(self):
        files = []
        #Find Log Files
        os.chdir(log_dir)
        for item in os.listdir('.'):
                files.append(item)

        msg = "This Action Results\n"
        for item in files:
            msg = msg + "Delete '" + str(item) + "'\n"
            
	#Confirm Action
        reply = QMessageBox.question(self, 'Confirm', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply == QMessageBox.No):
            return
        
        for item in files:
            try:
                os.remove(item)		#Delete Files
            except:
                pass
            
        os.chdir(curr)

    #Handler For About Menu
    def about(self):
        QMessageBox.about(self, "About Us", about_text)

    #Handler for Help Menu
    def help(self):
        webbrowser.open_new(help_link)
        
    #Handler for visit menu
    def visit(self):
        webbrowser.open_new(visit_link)

    #Set Centre Widget for Main Window
    def def_central(self):
        centre_widget = centre()
        #self.central_frame.setWidget(centre_widget)
        self.setCentralWidget(centre_widget)

    """
    Lock or Unlock Dock3 when File Acions going on
    """
    def lock_right(self, action):
        if(action == "lock"):
            central.tree.setDisabled(True)
            central.del_tree.setDisabled(True)
        if(action == "unlock"):
            central.tree.setEnabled(True)
            central.del_tree.setEnabled(True)

    
    def update_right_dock(self, file_list, action):
        central.start_handle2 = 0
        if(action == "del"):
            tree = central.del_tree
            right_del_obj.clear()
            
        if(action == "copy"):
            tree = central.tree
            right_cp_obj.clear()
            
        obj_list = []
        maps = []
        level = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]			#Stores Maximum and Current Levels For The TreeWidget
        level_name = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]	#Stores Previous File Path To Compare before adding file or folder to tree
        tree.clear()
        prev = ""
        tot_len = 2

        p = 0
        for file in file_list:
            if(os.path.isdir(file)):
                is_file = 0
            else:
                is_file = 1
            
            tmp_map = []
            
            file = file[1:]
            abs_path = file.split('/')
            abs_path_len = len(abs_path)
            filename = abs_path[-1]
            
            if(prev == file[:tot_len - 1]):
                #print("LOOOOOOOOOOOOP ------ 1")
                while (i < abs_path_len - 1):
                    level[level_counter + 1] = QTreeWidgetItem(level[level_counter], [abs_path[i]])

                    tmp_map.append(level[level_counter + 1])
                    tmp_map.append(level_counter + 1)
                    tmp_map.append(1)
                    obj_list.append(tmp_map)
                    tmp_map = []
                    
                    level[level_counter + 1].setCheckState(0, Qt.Checked)
                    tree.expandItem(level[level_counter + 1])
                    level_counter = level_counter + 1
                    level_name[i] = abs_path[i]
                    i = i + 1
                level[level_counter + 1] = QTreeWidgetItem(level[level_counter], [abs_path[i]])

                tmp_map.append(level[level_counter + 1])
                tmp_map.append(level_counter + 1)
                tmp_map.append(0)
                obj_list.append(tmp_map)
                tmp_map = []
                
                level[level_counter + 1].setCheckState(0, Qt.Checked)
                tree.expandItem(level[level_counter + 1])

                file_len = len(filename)
                tot_len = len(file) - file_len
                prev = file[:tot_len - 1]
                continue
                

            len2 = len(level_name)
            k = 0
            while k < abs_path_len and k < len2:
                if (level_name[k] == abs_path[k]):
                    k  = k + 1
                    continue
                break
            level_counter = k + 1
            i = level_counter - 1
            while k < abs_path_len:
                level_name[k] = abs_path[k]
                k = k + 1
            
            if level_counter > 1:
                #print("LOOOOOOOOOOOOP ------ 2")
                if(i == abs_path_len - 1):
                    level_counter = level_counter - 1
                while i < abs_path_len - 1:
                    level[level_counter] = QTreeWidgetItem(level[level_counter - 1], [abs_path[i]])

                    tmp_map.append(level[level_counter])
                    tmp_map.append(level_counter)
                    tmp_map.append(1)
                    obj_list.append(tmp_map)
                    tmp_map = []
                    
                    level[level_counter].setCheckState(0, Qt.Checked)
                    tree.expandItem(level[level_counter])
                    level_counter = level_counter + 1
                    level_name[i] = abs_path[i]
                    
                    i = i + 1
                    if i == abs_path_len - 1:
                            level_counter = level_counter - 1

                level[level_counter + 1] = QTreeWidgetItem(level[level_counter], [abs_path[i]])

                tmp_map.append(level[level_counter + 1])
                tmp_map.append(level_counter + 1)
                tmp_map.append(0)
                obj_list.append(tmp_map)
                tmp_map = []
                
                level[level_counter + 1].setCheckState(0, Qt.Checked)
                tree.expandItem(level[level_counter + 1])
                
                file_len = len(filename)
                tot_len = len(file) - file_len
                prev = file[:tot_len - 1]
                continue

            if(abs_path_len == 1):
                level[level_counter + 1] = QTreeWidgetItem(tree, [abs_path[i]])

                tmp_map.append(level[level_counter + 1])
                tmp_map.append(level_counter + 1)
                tmp_map.append(0)
                obj_list.append(tmp_map)
                tmp_map = []
                
                level[level_counter + 1].setCheckState(0, Qt.Checked)
                tree.expandItem(level[level_counter + 1])
                continue

            i = 1    
            #print("LOOOOOOOOOOOOP ------ 3")
            level[level_counter] = QTreeWidgetItem(tree, [abs_path[0]])

            tmp_map.append(level[level_counter])
            tmp_map.append(level_counter)
            tmp_map.append(1)
            obj_list.append(tmp_map)
            tmp_map = []
            
            level[level_counter].setCheckState(0, Qt.Checked)
            tree.expandItem(level[level_counter])
            level_name[level_counter - 1] = abs_path[0]       
                           
            while i < abs_path_len - 1:
                level[level_counter + 1] = QTreeWidgetItem(level[level_counter], [abs_path[i]])
                tmp_map.append(level[level_counter + 1])
                tmp_map.append(level_counter + 1)
                tmp_map.append(1)
                obj_list.append(tmp_map)
                tmp_map = []
                
                level[level_counter + 1].setCheckState(0, Qt.Checked)
                tree.expandItem(level[level_counter + 1])
                level_counter = level_counter + 1
                level_name[i] = abs_path[i]
                if i == abs_path_len - 1:
                        level_counter = level_counter - 1
                i = i + 1
            
            level[level_counter + 1] = QTreeWidgetItem(level[level_counter], [abs_path[i]])
            tmp_map.append(level[level_counter + 1])
            tmp_map.append(level_counter + 1)
            tmp_map.append(0)
            obj_list.append(tmp_map)
            tmp_map = []
                      
            level[level_counter + 1].setCheckState(0, Qt.Checked)
            tree.expandItem(level[level_counter + 1])
            level_name[i] = abs_path[i]
            
            file_len = len(filename)
            tot_len = len(file) - file_len
            prev = file[:tot_len - 1]
            p = p + 1
        
        if(action == "copy"):
            for item in obj_list:
                right_cp_obj.append(item)

        if(action == "del"):
            for item in obj_list:
                right_del_obj.append(item)
        central.start_handle2 = 2

	 
    #Handler for Dock3 TreeWidgets
    def right_tick_handle(self, ob, action):
        if(central.start_handle2 == 2):
            if(action == "copy"):
                tree = central.tree
                obj_list = right_cp_obj
            
            if(action == "del"):
                tree = central.del_tree
                obj_list = right_del_obj

            tree.blockSignals(True)

            pointer = 0
            list_len = len(obj_list)
            while(pointer < list_len):
                if(ob == obj_list[pointer][0]):
                    break
                pointer = pointer + 1

            #It Is Folder
            if(obj_list[pointer][2] == 1):
                if(obj_list[pointer][0].checkState(0) == Qt.Checked):
                    i = pointer + 1
                    while(i < list_len and obj_list[i][1] > obj_list[pointer][1]):
                        obj_list[i][0].setCheckState(0, Qt.Checked)
                        if(obj_list[i][2] == 0):
                            self.handle_left(obj_list[i][0], action)
                        i = i + 1

                    i = pointer - 1
                    level = obj_list[pointer][1]
                    while(i >= 0):
                        if(obj_list[i][1] < level and obj_list[i][2] == 1):
                            obj_list[i][0].setCheckState(0, Qt.Checked)
                            level = obj_list[i][1]
                        i = i - 1

                if(obj_list[pointer][0].checkState(0) == Qt.Unchecked):
                    i = pointer + 1
                    while(i < list_len and obj_list[i][1] > obj_list[pointer][1]):
                        obj_list[i][0].setCheckState(0, Qt.Unchecked)
                        if(obj_list[i][2] == 0):
                            self.handle_left(obj_list[i][0], action)
                        i = i + 1

                    i = pointer - 1
                    while(i >= 0):
                        flag = 0

                        i = pointer + 1
                        while(i < list_len and obj_list[i][1] >= obj_list[pointer][1]):
                            if(obj_list[i][0].checkState(0) == Qt.Checked):
                                flag = 1
                                break
                            i = i + 1
                            
                        i = pointer - 1
                        while(i >= 0 and obj_list[i][1] >= obj_list[pointer][1]):
                            if(obj_list[i][0].checkState(0) == Qt.Checked):
                                flag = 1
                                break
                            i = i - 1



                        if(not flag):
                            if(i >= 0):
                                obj_list[i][0].setCheckState(0, Qt.Unchecked)
                                pointer = i
                                continue
                            
                        if(flag):
                            break
                    


            #It Is File
            if(obj_list[pointer][2] == 0):
                if(obj_list[pointer][0].checkState(0) == Qt.Checked):
                    i = pointer - 1
                    level = obj_list[pointer][1]
                    while(i >= 0):
                        if(obj_list[i][1] < level and obj_list[i][2] == 1):
                            obj_list[i][0].setCheckState(0, Qt.Checked)
                            level = obj_list[i][1]
                        i = i - 1


                if(obj_list[pointer][0].checkState(0) == Qt.Unchecked):
                    i = pointer - 1
                    while(i >= 0):
                        flag = 0
                        i = pointer + 1
                        while(i < list_len and obj_list[i][1] >= obj_list[pointer][1]):
                            if(obj_list[i][0].checkState(0) == Qt.Checked):
                                flag = 1
                                break
                            i = i + 1
                            
                        i = pointer - 1
                        while(i >= 0 and obj_list[i][1] >= obj_list[pointer][1]):
                            if(obj_list[i][0].checkState(0) == Qt.Checked):
                                flag = 1
                                break
                            i = i - 1

                        if(not flag):
                            if(i >= 0):
                                obj_list[i][0].setCheckState(0, Qt.Unchecked)
                                pointer = i
                                continue
                            
                        if(flag):
                            break
                self.handle_left(ob, action)

            tree.blockSignals(False)
  
	   
     #Reflect change to Tree in Dock2  
    def handle_left(self, ob, action):
        if(action == "copy"):
            left = left_cp_flist
            right = right_cp_flist
            
        if(action == "del"):
            left = left_del_flist
            right = right_del_flist

        i = 0
        size = len(right)
        while(i < size):
            if(right[i] == ob):		#Find Index of object
                break
            i = i + 1

        if(right[i].checkState(0) == Qt.Checked):
            left[i].setCheckState(0, Qt.Checked)

        if(right[i].checkState(0) == Qt.Unchecked):
            left[i].setCheckState(0, Qt.Unchecked)
         

