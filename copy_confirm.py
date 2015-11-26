import os, sys
import magic
import time

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from env import *
from style4 import *

class cp_conf(QDialog):
    def __init__(self):
        super(cp_conf, self).__init__()
        self.size = len(conf_res)
        self.ind = 0
        self.file_size = ["", ""]
        self.set_window()        

    def set_window(self):
        frame1 = QFrame()
        frame2 = QFrame()
        frame3 = QFrame()
        frame4 = QFrame()
        set_style4(frame1, "frame")
        set_style4(frame2, "frame")
        set_style4(frame3, "frame")
        set_style4(frame4, "frame")

        main_grid = QGridLayout()
        self.f1_grid = QGridLayout()
        self.f2_grid = QGridLayout()
        self.f3_grid = QGridLayout()
        self.f4_grid = QGridLayout()        

        frame1.setLayout(self.f1_grid)
        frame2.setLayout(self.f2_grid)
        frame3.setLayout(self.f3_grid)
        frame4.setLayout(self.f4_grid)

        lab1 = QLabel("Another File With Same Name\nExists At The Target Location")
        lab2 = QLabel("File To Copy")
        lab3 = QLabel("Existing File")
        space2 = QLabel("")
        lab1.setStyleSheet("QLabel {font : normal 16rpx times; color : rgb(41, 46, 41);}")
        lab2.setStyleSheet("QLabel {font : normal 18px times; color : rgb(41, 46, 41);}")
        lab3.setStyleSheet("QLabel {font : normal 18px times; color : rgb(41, 46, 41);}")

        self.pic1 = QLabel()
        self.pic2 = QLabel()
        self.pic1.setMinimumHeight(100)
        self.pic1.setMinimumWidth(100)
        self.pic2.setMinimumHeight(100)
        self.pic2.setMinimumWidth(100)
        
        main_grid.addWidget(lab1, 1, 0, 1, 8)
        main_grid.addWidget(lab2, 3, 0, 1, 8)
        
        main_grid.addWidget(self.pic1, 4, 0, 6, 3)
        main_grid.addWidget(frame1, 4, 3, 6, 5)
        #main_grid.addWidget(space2, 10, 0, 1, 4)
        main_grid.addWidget(lab3, 11, 0, 1, 8)
        main_grid.addWidget(self.pic2, 12, 0, 6, 3)
        main_grid.addWidget(frame2, 12, 3, 6, 5)
        space3 = QLabel("")
        main_grid.addWidget(frame3, 19, 0, 1, 8)
        main_grid.addWidget(frame4, 20, 0, 1, 8)
        self.setLayout(main_grid)

        self.make_frame3()
        self.make_frame4()
        self.make_frame12(cp_file_from[conf_res[self.ind]], file2cp[conf_res[self.ind]])
        

    def make_frame12(self, src, tar):
        mime = magic.open(magic.MAGIC_MIME_TYPE)
        mime.load()
    
        src_name = src.split('/')
        src_name = src_name[-1]
        tar_name = tar.split('/')
        tar_name = tar_name[-1]
        
        self.get_size(os.path.getsize(src))

        src_det = mime.file(src)
        tar_det = mime.file(tar)
        time_crt = time.ctime(os.path.getmtime(src))
        time_mod = time.ctime(os.path.getctime(src))
        source = [src_name, self.file_size[0] + self.file_size[1], src_det, "Created: " + time_crt, "Modified: " + time_mod]
        
        space1 = QLabel("")
        space2 = QLabel("")

        icon1 = self.find_icon(src_det)
        icon2 = self.find_icon(tar_det)
        pic1 = QPixmap(icon1)
        self.pic1.setPixmap(pic1)
        pic2 = QPixmap(icon2)
        self.pic2.setPixmap(pic2)
        
        for i in reversed(range(self.f1_grid.count())): 
            self.f1_grid.itemAt(i).widget().deleteLater()

        for i in reversed(range(self.f2_grid.count())): 
            self.f2_grid.itemAt(i).widget().deleteLater()
        
        for i in range(5):
            lab = QLabel(str(source[i]))
            if(i == 0):
                lab.setStyleSheet("QLabel {font : normal 20px 'Serif'; color : rgb(116, 118, 110);}")
            if(i == 1 or i == 2):
                lab.setStyleSheet("QLabel {font : normal 16px 'Serif'; color : rgb(116, 118, 110);}")
            if(i == 3 or i == 4):
                lab.setStyleSheet("QLabel {font : italic 14px 'Serif'; color : rgb(116, 118, 110);}")
            lab.setMinimumHeight(20)
            self.f1_grid.addWidget(lab, i, 0, 1, 5)
        self.f1_grid.addWidget(space1, i, 0, 10, 5)


        self.get_size(os.path.getsize(tar))
        time_crt = time.ctime(os.path.getmtime(tar))
        time_mod = time.ctime(os.path.getctime(tar))
        target = [tar_name, self.file_size[0] + self.file_size[1], tar_det, "Created: " + time_crt, "Modified: " + time_mod]
        for i in range(5):
            lab = QLabel(str(target[i]))
            if(i == 0):
                lab.setStyleSheet("QLabel {font : normal 20px 'Serif'; color : rgb(116, 118, 110);}")
            if(i == 1 or i == 2):
                lab.setStyleSheet("QLabel {font : normal 16px 'Serif'; color : rgb(116, 118, 110);}")
            if(i == 3 or i == 4):
                lab.setStyleSheet("QLabel {font : italic 14px 'Serif'; color : rgb(116, 118, 110);}")
            lab.setMinimumHeight(20)
            self.f2_grid.addWidget(lab, i, 0, 1, 5)
        self.f2_grid.addWidget(space2, i, 0, 10, 5)

    def make_frame3(self):
        self.chk = QCheckBox()
        self.chk.setMaximumWidth(20)
        lab = QLabel("Apply this action to remaining files")
        #set_style4(lab, "check_lab")
        lab.setStyleSheet("QLabel {font : bold 16px 'Times'; color : rgb(41, 46, 41);}")
        lab.setMaximumHeight(20)

        self.f3_grid.addWidget(self.chk, 0, 0, 1, 8)
        self.f3_grid.addWidget(lab, 0, 1, 1, 8)

    def make_frame4(self):
        but1 = QPushButton("REPLACE")
        but2 = QPushButton("SKIP")
        but3 = QPushButton("COPY")
        but4 = QPushButton("CANCEL")
        but1.connect(but1, SIGNAL("clicked()"), lambda : self.on_replace())
        but2.connect(but2, SIGNAL("clicked()"), lambda : self.on_skip())
        but3.connect(but3, SIGNAL("clicked()"), lambda : self.on_copy())
        but3.connect(but4, SIGNAL("clicked()"), lambda : self.on_cancel())
        
        set_style4(but1, "button")
        set_style4(but2, "button")
        set_style4(but3, "button")
        set_style4(but4, "button")
        but1.setMinimumHeight(50)
        but2.setMinimumHeight(50)
        but3.setMinimumHeight(50)
        but4.setMinimumHeight(50)

        self.f4_grid.setSpacing(0)
        self.f4_grid.addWidget(but1, 0, 0)
        self.f4_grid.addWidget(but2, 0, 2)
        self.f4_grid.addWidget(but3, 0, 4)
        self.f4_grid.addWidget(but4, 0, 6)


    def on_skip(self):
        if(self.chk.checkState() == Qt.Checked):
            self.close()
            return
            
        self.ind = self.ind + 1
        if(self.ind >= self.size):
            self.close()
            return
        
        self.make_frame12(cp_file_from[conf_res[self.ind]], file2cp[conf_res[self.ind]])
        

    def on_replace(self):
        if(self.chk.checkState() == Qt.Checked):
            while(self.ind < self.size):
                left_cp_flist[conf_res[self.ind]].setCheckState(0, Qt.Checked)
                self.ind = self.ind + 1
            self.close()
            return

        left_cp_flist[conf_res[self.ind]].setCheckState(0, Qt.Checked)
        self.ind = self.ind + 1
        if(self.ind >= self.size):
            self.close()
            return
        
        self.make_frame12(cp_file_from[conf_res[self.ind]], file2cp[conf_res[self.ind]])


    def on_copy(self):
        if(self.chk.checkState() == Qt.Checked):
            while(self.ind < self.size):
                self.make_new_name()
                left_cp_flist[conf_res[self.ind]].setCheckState(0, Qt.Checked)
                self.ind = self.ind + 1
            self.close()
            return

        self.make_new_name()
        left_cp_flist[conf_res[self.ind]].setCheckState(0, Qt.Checked)
        self.ind = self.ind + 1
        if(self.ind >= self.size):
            self.close()
            return
        
        self.make_frame12(cp_file_from[conf_res[self.ind]], file2cp[conf_res[self.ind]])

    def on_cancel(self):
        self.close()
        return

    def make_new_name(self):
        file2cp[conf_res[self.ind]] = file2cp[conf_res[self.ind]] + "(copy###)"

    def get_size(self, size):
        tmp = ""
        if size < 1000: 
                self.file_size[0] = str(size)
                self.file_size[1] = "Bytes"
                return
            
        if size < 1000000: 
                size = size / 1000
                tmp = str(size).split('.')
                self.file_size[1] = "KB"
        if size > 1000000:
                size = size / 1000000
                tmp = str(size).split('.')
                self.file_size[1] = "MB"

        self.file_size[0] = tmp[0] + "." + tmp[1][0]


    def find_icon(self, det):
        det = det.split('/')
        if(det[1] == "x-empty"):
            return ("thumbs/empty.png")

        if(det[0] == "audio"):
            return ("thumbs/audio.png")

        if(det[0] == "image"):
            return ("thumbs/image.png")

        if(det[0] == "x-empty"):
            return ("thumbs/video.png")

        if(det[1] == "pdf"):
            return ("thumbs/pdf.png")

        if(det[0] == "text" or det[0] == "application"):
            return ("thumbs/text.png")
        else:
            return ("thumbs/other.png")
          
