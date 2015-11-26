from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys, time
import threading
from env_progress import *

class busy(QDialog):
    def __init__(self):
        super(busy, self).__init__()
        
        self.make_window()
        self.st_thread = threading.Thread(target = self.status, args = ())
        #self.st_thread.daemon = True
        self.st_thread.start()
        
    def make_window(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        if(FETCH[0] == 1):
            ACTION[0] = "fetch1"

        if(FETCH[0] == 2):
            ACTION[0] = "fetch2"
        BUSY[0] = "source"
        
        head = QLabel("FETCHING FILES")
        head.setStyleSheet("QLabel {\
                            font : normal 17px times;\
                            color : black;\
                            background : white;\
                            }")

        gif = QLabel()
        gif.setMinimumHeight(130)
        gif.setMinimumWidth(130)
        movie = QMovie("icon/busy.gif", QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        movie.setSpeed(100)
        gif.setMovie(movie)
        
        self.lab = QLabel("Making Source List")
        self.lab.setStyleSheet("QLabel {\
                              font : normal 16px times;\
                              color : darkcyan;\
                              background : white;\
                              }")
        self.ela = QLabel("Elapsed: 0:0")
        #self.ela.setAlignment(Qt.centrealigned)
        self.ela.setStyleSheet("QLabel {\
                              font : normal 16px times;\
                              color : gray;\
                              background : white;\
                              }")
        
        self.grid.addWidget(head, 0, 0, 1, 2)
        self.grid.addWidget(gif, 1, 0, 1, 2)
        self.grid.addWidget(self.lab, 2, 0, 1, 2)
        self.grid.addWidget(self.ela, 3, 0, 1, 2)
        
        movie.start()
            
    def status(self):
        secs = 0
        while True:
            mins = int(secs / 60)
            sec = secs % 60
            line = "Elapsed: " + str(mins) + ":" + str(sec)
            if(BUSY[0] == " "):
                self.deleteLater()
                return
            
            if(BUSY[0] == "source"):
                self.lab.setText("Making Source List")
                self.ela.setText(line)
                time.sleep(1)
                secs = secs + 1
                continue

            if(BUSY[0] == "target"):
                self.ela.setText(line)
                self.lab.setText("Making Target List")
                time.sleep(1)
                secs = secs + 1
                continue

            if(BUSY[0] == "find"):
                self.ela.setText(line)
                self.lab.setText("Finding Files List")
                time.sleep(1)
                secs = secs + 1
                continue
