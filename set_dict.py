import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#Extract Previous Setting
import pickle

#Contains variable for file action and checkboxes
from env import *

#Import Stylesheet
from style2 import *

class set_dict(QDialog):
    def __init__(self):
        super(set_dict, self).__init__()
	#Device Currently Selected
        self.sel_button = 0
		
	#Temporary list for actual list
        self.tmp_all_list = []
        self.tmp_list_name = []
        self.tmp_top_check = []
        self.tmp_left_check = []

        self.top_tick_obj = []
        self.left_tick_obj = []
        self.set_checkbox()
        self.make_window()
        self.make_leftframe()
        self.make_topframe(self.tmp_all_list[0])
        self.make_botframe()


    def make_window(self):
        self.left_frame = QFrame()
        set_style(self.left_frame, "frame")
        self.left_frame.setFrameShape(QFrame.StyledPanel)
        self.left_frame.setStyleSheet("QFrame {background-color : white;}")

        self.top_frame = QFrame()
        set_style(self.top_frame, "frame")
        self.top_frame.setFrameShape(QFrame.StyledPanel)
        self.top_frame.setStyleSheet("QFrame {background-color : white;}")
        
        self.bot_frame = QFrame()
        self.bot_frame.setFrameStyle(QFrame.HLine | QFrame.Raised)

        set_style(self.bot_frame, "frame")
        self.bot_frame.setFrameShape(QFrame.StyledPanel)
        self.bot_frame.setStyleSheet("QFrame {background-color : white;}")
        
        grid = QGridLayout()
        grid.setSpacing(0)
        grid.addWidget(self.left_frame, 0, 0, 10, 2)
        grid.addWidget(self.top_frame, 0, 2, 10, 8)
        grid.addWidget(self.bot_frame, 10, 0, 1, 10)
        self.setLayout(grid)  

    def set_checkbox(self):
        for item in left_check:
            self.tmp_left_check.append(item)
            self.left_tick_obj.append(item)
            
        for item in top_check:
            self.tmp_top_check.append([])
            self.top_tick_obj.append([])
            for it in item:
                self.tmp_top_check[-1].append(it)
                self.top_tick_obj[-1].append(it)
            
        for item in all_list:
            self.tmp_all_list.append([])
            for it in item:
                self.tmp_all_list[-1].append(it)
        
        for item in list_name:
            self.tmp_list_name.append(item)

        
    def make_leftframe(self):
        main_grid = QGridLayout()
        self.left_grid = QGridLayout()
        self.left_grid.setSpacing(0)
        lab = QLabel("Select Device(s)")
        set_style(lab, "label")
        space = QLabel("")
        
        self.update_leftframe()

        frame2 = QFrame()
        set_style(frame2, "sec_frame")
        grid2 = QGridLayout()
        add = QPushButton("ADD")
        set_style(add, "act_button")
        add.setMaximumWidth(80)
        add.setMinimumHeight(50)
        self.make_button(add, "", "", self.on_leftadd)

        frame3 = QFrame()
        frame3.setLayout(self.left_grid)
        frame2.setLayout(grid2)
        self.left_frame.setLayout(main_grid)
        
        main_grid.addWidget(lab, 0, 1, 1, 1)
        main_grid.addWidget(frame3, 1, 0, 15, 3)
        main_grid.addWidget(frame2, 15, 0, 1, 3)
        grid2.addWidget(add, 0, 1, 1, 1)
        
    
    def update_leftframe(self):
        for i in reversed(range(self.left_grid.count())): 
            self.left_grid.itemAt(i).widget().deleteLater()
        i = 0
        for item in self.tmp_list_name:
            but = QPushButton(item)
            but.setMinimumWidth(150)
            set_style(but, "dev_button")
            but.connect(but, SIGNAL("clicked()"), lambda who = i: self.on_leftdev(who))
            check = QCheckBox()
            self.left_tick_obj[i] = check
            
            if(self.tmp_left_check[i] == 1):
                check.setCheckState(Qt.Checked)
            set_style(check, "checkbox")
            check.connect(check, SIGNAL("clicked()"), lambda who = i: self.left_tick(who))

            tool = QToolButton()
            set_style(tool, "tool_button")
            tool.setPopupMode(QToolButton.MenuButtonPopup)
            tool.setMenu(QMenu(tool))
            tool.menu().addAction("Rename", lambda index = i: self.on_rename(index))
            tool.menu().addAction("Delete", lambda index = i: self.on_delete(index))
            tool.setMaximumWidth(20)

            but.setMaximumWidth(150)
            self.left_grid.addWidget(check, i, 0)
            self.left_grid.addWidget(but, i, 1)
            self.left_grid.addWidget(tool, i, 2)
            i = i + 1
        
        space = QLabel("")
        self.left_grid.addWidget(space, i, 0, 15, 3)
        return i

    def on_leftdev(self, i):
        self.sel_button = i        
        self.update_topframe(self.tmp_all_list[i])

    def left_tick(self, i):
        if(self.sel_button != i):
            self.sel_button = i
            self.update_topframe(self.tmp_all_list[self.sel_button])

        if(self.tmp_all_list[self.sel_button][0]['source'] == "" or self.tmp_all_list[self.sel_button][0]['target'] == ""):
            QMessageBox.about(self, "Warning!", "Please Fill The Empty Dictionary")
            self.update_leftframe()
            return
        
        loc_changed.append(1)
        if(self.tmp_left_check[i] == 0):
            self.tmp_left_check[i] = 1
            j = 0
            while(j < len(self.tmp_top_check[self.sel_button])):
                if(self.tmp_all_list[self.sel_button][j]['source'] == "" or self.tmp_all_list[self.sel_button][j]['target'] == ""):
                    j = j + 1
                    continue
                self.tmp_top_check[self.sel_button][j] = 1
                self.top_tick_obj[self.sel_button][j].setCheckState(Qt.Checked)
                j = j + 1
        else:
            self.tmp_left_check[i] = 0
            j = 0
            while(j < len(self.tmp_top_check[self.sel_button])):
                self.tmp_top_check[self.sel_button][j] = 0
                self.top_tick_obj[self.sel_button][j].setCheckState(Qt.Unchecked)
                j = j + 1

        self.left_grid.itemAt(3 * self.sel_button + 2).widget().setFocus()
        
        
    def on_rename(self, i):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter The New Name:')
        if(ok):
                loc_changed.append(1)
                self.tmp_list_name[i] = text
                self.update_leftframe()
        else:
            return

    def on_delete(self, i):
        reply = QMessageBox.question(self, 'Confirm', "Are you sure to Delete?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply == QMessageBox.No):
            return
        loc_changed.append(1)
        if(len(self.tmp_list_name) == 1):
            reply = QMessageBox.question(self, 'Confirm', "By Deleting Last Item Window Will Close\nAre You Sure To Delete?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if(reply == QMessageBox.Yes):
                self.tmp_list_name.remove(self.tmp_list_name[i])
                self.tmp_all_list.remove(self.tmp_all_list[i])
                self.tmp_left_check.remove(self.tmp_left_check[i])
                self.tmp_top_check.remove(self.tmp_top_check[i])
                self.savesetting()
                self.close()
                return

        self.sel_button = 0
        self.tmp_list_name.remove(self.tmp_list_name[i])
        self.tmp_left_check.remove(self.tmp_left_check[i])
        self.left_tick_obj.remove(self.left_tick_obj[i])
        self.update_leftframe()
        
        self.tmp_all_list.remove(self.tmp_all_list[i])
        self.top_tick_obj.remove(self.top_tick_obj[i])
        self.tmp_top_check.remove(self.tmp_top_check[i])
        self.update_topframe(self.tmp_all_list[0])
    
    def make_topframe(self, lname):            
        top_grid = QGridLayout()
        self.top_grid2 = QGridLayout()
        lab1 = QLabel("FROM")
        set_style(lab1, "label")
        lab2 = QLabel("TO")
        set_style(lab2, "label")
        space = QLabel("")
        self.frame2 = QFrame()
        set_style(self.frame2, "sec_frame")
        i = 0
        i = self.update_topframe(lname)
        
        frame3 = QFrame()
        set_style(frame3, "sec_frame")
        grid2 = QGridLayout()
        
        add = QPushButton("ADD")
        set_style(add, "act_button")
        add.setMaximumWidth(100)
        add.setMinimumHeight(50)
        self.make_button(add, "", "", self.on_topadd)

        top_grid.addWidget(lab1, 0, 1)
        top_grid.addWidget(lab2, 0, 3)
        top_grid.addWidget(self.frame2, 1, 0, 15, 5)
        self.top_grid2.addWidget(space, i + 1, 0, 15, 1)
        top_grid.addWidget(frame3, 16, 0, 1, 5)
        
        grid2.addWidget(add, 0, 8)
        
        frame3.setLayout(grid2)
        self.frame2.setLayout(self.top_grid2)
        self.top_frame.setLayout(top_grid)
    
    def update_topframe(self, list_name):
        for i in reversed(range(self.top_grid2.count())): 
            self.top_grid2.itemAt(i).widget().deleteLater()
        i = 0
        for path in list_name:
                source = path['source']
                target = path['target']
                check = QCheckBox()
                self.top_tick_obj[self.sel_button][i] = check

                if(self.tmp_top_check[self.sel_button][i] == 1):
                    if(self.tmp_all_list[self.sel_button][i]['source'] == "" or self.tmp_all_list[self.sel_button][i]['target'] == ""):
                        self.tmp_top_check[self.sel_button][i] == 0
                        check.setCheckState(Qt.Unchecked)
                    else:
                        check.setCheckState(Qt.Checked)

                check.setMaximumWidth(20)
                check.connect(check, SIGNAL("clicked()"), lambda who = i: self.top_tick(who))
                set_style(check, "checkbox")

                but1 = QPushButton(str(source))
                set_style(but1, "loc_button")
                but2 = QPushButton(str(target))
                set_style(but2, "loc_button")
                #but1.setStyleSheet("QPushButton {background-color : blue;}")
                but3 = QPushButton("DELETE")
                set_style(but3, "act_button")
                but3.setMaximumWidth(80)
                but1.setMaximumWidth(350)
                but2.setMaximumWidth(350)
                self.make_button(but1, "", "", self.on_source)
                self.make_button(but2, "", "", self.on_tar)
                but3.connect(but3, SIGNAL("clicked()"), lambda who = i: self.on_topdel(who))
                self.top_grid2.addWidget(check, i + 1, 0)
                self.top_grid2.addWidget(but1, i + 1, 1)
                self.top_grid2.addWidget(but2, i + 1, 2)
                self.top_grid2.addWidget(but3, i + 1, 3)
                i = i + 1

        space = QLabel("")
        self.top_grid2.addWidget(space, i + 1, 0, 5, 4)
        i = i + 1

        return i

    def top_tick(self, i):
        if(self.tmp_all_list[self.sel_button][i]['source'] == "" or self.tmp_all_list[self.sel_button][i]['target'] == ""):
            QMessageBox.about(self, "Warning!", "Please Fill The Empty Dictionary")
            self.update_topframe(self.tmp_all_list[self.sel_button])
            return

        loc_changed.append(1)
        if(self.tmp_top_check[self.sel_button][i] == 0):
            self.tmp_top_check[self.sel_button][i] = 1
        else:
            self.tmp_top_check[self.sel_button][i] = 0

           
        k = 0
        for j in range(len(self.tmp_top_check[self.sel_button])):
            if(self.tmp_top_check[self.sel_button][j] == 1):
                k = 1
                break
        if(k == 0):
            self.tmp_left_check[self.sel_button] = 0
            self.left_tick_obj[self.sel_button].setCheckState(Qt.Unchecked)
            
        if(k == 1):
            self.tmp_left_check[self.sel_button] = 1
            self.left_tick_obj[self.sel_button].setCheckState(Qt.Checked)
            
            

    def make_botframe(self):
        grid = QGridLayout()
        lab = QLabel("")
        
        but1 = QPushButton("OK")
        set_style(but1, "act_button2")
        self.make_button(but1, "", "", self.onok)
        but1.setMinimumHeight(50)
        but1.setMaximumWidth(100)
        
        but2 = QPushButton("CANCEL")
        set_style(but2, "act_button2")
        self.make_button(but2, "", "", self.oncancel)
        but2.setMinimumHeight(50)
        but2.setMaximumWidth(100)

        grid.addWidget(lab, 0, 0)
        grid.addWidget(but1, 0, 3)
        grid.addWidget(but2, 0, 4)
        grid.addWidget(lab, 0, 5)
        self.bot_frame.setLayout(grid)

    def make_button(self, item, text = "", icon = None, handle = None):
        item.setIcon(QIcon(icon))
        item.setIconSize(QSize(100, 30))
        item.connect(item, SIGNAL("clicked()"), handle)

    def onok(self):
        self.savesetting()
        self.close()

        
    def savesetting(self):
        if(loc_changed[-1] == 0):
            return
        
        all_list.clear()
        list_name.clear()
        left_check.clear()
        top_check.clear()

        for item in self.tmp_left_check:
            left_check.append(item)

        for item in self.tmp_top_check:
            top_check.append(item)

        for item in self.tmp_all_list:
            all_list.append(item)

        for item in self.tmp_list_name:
            list_name.append(item)

        tmp_list = []
        i = 0
        while(i < len(self.tmp_all_list)):
            j = 0
            while(j < len(self.tmp_all_list[i])):
                if(self.tmp_top_check[i][j] == 1):
                    tmp_list.append(self.tmp_all_list[i][j])
                j = j + 1
            i = i + 1
        
        sync_list.clear()
        
        for item in tmp_list:
            sync_list.append(item)
        
        os.chdir(curr)
        pickle.dump(left_check, open("setting/left_check.p", "wb"))
        pickle.dump(top_check, open("setting/top_check.p", "wb"))
        
        pickle.dump(all_list, open("setting/all_list.p", "wb"))
        pickle.dump(list_name, open("setting/list_name.p", "wb"))       

    def oncancel(self):
        quit_msg = "Do You Want To Save Changes?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if(reply == QMessageBox.No):
            loc_changed[-1] = 0
            self.close()
            return
        else:
            self.savesetting()
            self.close()
            

    def on_leftadd(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter Device Name:')
        if(ok):
            loc_changed.append(1)
            self.tmp_list_name.append(text)
            self.tmp_left_check.append( 0)
            self.left_tick_obj.append([])

            self.tmp_all_list.append([])
            self.sel_button = len(self.tmp_list_name) - 1
            
            self.update_leftframe()
            
            self.tmp_all_list[self.sel_button].append({'source' : "", 'target' : ""})
            self.top_tick_obj.append([0])
            self.tmp_top_check.append([])
            self.tmp_top_check[self.sel_button].append(0)
            
            self.update_topframe(self.tmp_all_list[self.sel_button])
        

    def on_topadd(self):
        dict_list = []
        if(self.tmp_all_list[self.sel_button][-1]['source'] == "" or self.tmp_all_list[self.sel_button][-1]['target'] == ""):
            QMessageBox.about(self, "Warning!", "Please Fill The Empty Dictionary")
            return
        
        loc_changed.append(1)
        self.tmp_all_list[self.sel_button].append({'source' : "", 'target' : ""})
        self.top_tick_obj[self.sel_button].append("")
        self.tmp_top_check[self.sel_button].append(0)

        self.update_topframe(self.tmp_all_list[self.sel_button])
        
    def on_topdel(self, i):
        reply = QMessageBox.question(self, 'Confirm', "Are you sure to Delete?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply == QMessageBox.No):
            return

        loc_changed.append(1)
        self.tmp_all_list[self.sel_button].remove(self.tmp_all_list[self.sel_button][i])
        self.tmp_top_check[self.sel_button].remove(self.tmp_top_check[self.sel_button][i])
        self.top_tick_obj[self.sel_button].remove(self.top_tick_obj[self.sel_button][i])
        if(len(self.tmp_all_list[self.sel_button]) == 0):
            self.tmp_all_list[self.sel_button].append({'source' : "", 'target' : ""})
            self.top_tick_obj[self.sel_button].append(0)
            self.tmp_top_check[self.sel_button].append(0)
        
        self.update_topframe(self.tmp_all_list[self.sel_button])

    def on_source(self):
        s_dirname = str(QFileDialog.getExistingDirectory(self, "Select Source Directory"))
        if(not s_dirname):
            return
        loc_changed.append(1)
        self.tmp_all_list[self.sel_button][-1]['source'] = s_dirname
        self.update_topframe(self.tmp_all_list[self.sel_button])
        
    def on_tar(self):
        t_dirname = str(QFileDialog.getExistingDirectory(self, "Select Target Directory"))
        if(not t_dirname):
            return
        loc_changed.append(1)
        self.tmp_all_list[self.sel_button][-1]['target'] = t_dirname
        self.update_topframe(self.tmp_all_list[self.sel_button])
