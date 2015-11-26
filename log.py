from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
from env import *

from style3 import *

class log_window(QDialog):
    def __init__(self):
        super(log_window, self).__init__()
        self.logs = []
        self.curr_sel = -1
        self.size = 0
        self.set_widgets()
        self.addWidgets()

    def set_widgets(self):
        left_frame = QFrame()
        self.text = QTextBrowser()
        set_style(self.text, "text_browser")
        bot_frame = QFrame()
        left_frame.setStyleSheet("QFrame {background-color : white;}")
        bot_frame.setStyleSheet("QFrame {background-color : white;}")

        grid = QGridLayout()
        self.left_grid = QGridLayout()
        self.bot_grid = QGridLayout()
        self.left_grid.setSpacing(0)
        self.bot_grid.setSpacing(0)

        left_frame.setLayout(self.left_grid)
        bot_frame.setLayout(self.bot_grid)

        grid.addWidget(left_frame, 0, 0, 10, 1)
        grid.addWidget(self.text, 0, 1, 9, 5)
        grid.addWidget(bot_frame, 9, 1, 1, 5)
        self.setLayout(grid)

    def addWidgets(self):
        self.but1 = QPushButton("PREV")
        self.but1.setMinimumHeight(60)
        set_style(self.but1, "act_button")
        self.but2 = QPushButton("DELETE")
        self.but2.setMinimumHeight(60)
        set_style(self.but2, "act_button")
        self.but3 = QPushButton("NEXT")
        self.but3.setMinimumHeight(60)
        set_style(self.but3, "act_button")

        self.but1.connect(self.but1, SIGNAL("clicked()"), lambda : self.on_action("prev"))
        self.but2.connect(self.but2, SIGNAL("clicked()"), lambda : self.on_action("del"))
        self.but3.connect(self.but3, SIGNAL("clicked()"), lambda : self.on_action("next"))

        
        self.bot_grid.addWidget(self.but1, 0, 1)
        self.bot_grid.addWidget(self.but2, 0, 2)
        self.bot_grid.addWidget(self.but3, 0, 3)

        for file in os.listdir(log_dir):
            if(file[-1] == '~'):
                continue
            self.logs.append(log_dir + file)
        self.update_log()

    def update_log(self):
        self.size = len(self.logs)
        i = 0
        while(i < self.size):
            lg_name = self.logs[i].split('/')[-1]
            but = QPushButton(lg_name)
            but.setMaximumHeight(30)
            set_style(but, "loc_button")
            but.connect(but, SIGNAL("clicked()"), lambda who = i: self.on_click(who))
            self.left_grid.addWidget(but, i, 0)
            i = i + 1
            
        if(self.size != 0):
            self.but1.setDisabled(True)
            if(self.size == 1):
                self.but3.setDisabled(True)
            else:
                self.but3.setEnabled(True)
            self.on_click(0)
        else:
            self.but1.setDisabled(True)
            self.but2.setDisabled(True)
            self.but3.setDisabled(True)
            self.text.clear()
            self.text.append("<font size = 3>" + "No Logs To Show" + "</font>")
        
        space = QLabel(" ")
        self.left_grid.addWidget(space, i, 0, 10, 1)

    def on_click(self, name):
        self.curr_sel = name

        if(self.curr_sel < 0):
            self.text.clear()
            self.text.append("<font size = 3>" + "No Logs To Show" + "</font>")
            return
        if(self.curr_sel == 0):
            self.but1.setDisabled(True)
            if(self.size > 1):
                self.but3.setEnabled(True)

        if(self.curr_sel == self.size - 1):
            self.but3.setDisabled(True)
            if(self.size > 1):
                self.but1.setEnabled(True)

        with open(self.logs[name], "r") as file:
            lines = file.readlines()

        self.text.clear()
        for item in lines:
            self.text.append("<font size = 3>" + str(item) + "</font>")
 
        self.left_grid.itemAt(name).widget().setFocus()

    def on_action(self, action):
        if(self.curr_sel == -1):
            self.text.clear()
            self.text.append("<font size = 3>" + "No Logs To Display" + "</font>")
            return

        if(action == "prev" and self.curr_sel != 0):
            self.but3.setEnabled(True)
            self.curr_sel = self.curr_sel - 1
            if(self.curr_sel == 0):
                self.but1.setDisabled(True)
                
            self.on_click(self.curr_sel)
            return

        if(action == "next" and self.curr_sel != self.size):
            self.but1.setEnabled(True)
            self.curr_sel = self.curr_sel + 1
            if(self.curr_sel == self.size - 1):
                self.but3.setDisabled(True)
            
            self.on_click(self.curr_sel)
            return

        if(action == "del"):
            os.remove(self.logs[self.curr_sel])
            self.logs.remove(self.logs[self.curr_sel])
            
            if(self.curr_sel > -1):
                for i in reversed(range(self.left_grid.count())): 
                    self.left_grid.itemAt(i).widget().deleteLater()
            
                self.update_log()
                self.curr_sel = 0    
