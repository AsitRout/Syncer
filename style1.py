"""
Set StyleSheet
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def set_style(wid_obj, obj_type):
    if(obj_type == "button"):
        for item in wid_obj:
            item.setStyleSheet("QPushButton {\
                               background-color : rgb(252, 250, 250);\
                               font : normal 14px 'Times';\
                               color : rgb(106, 87, 71);\
                               border : 1px outset darkGray;\
                               border-radius : 10px;\
                               padding : 0px;\
                               }"
                               "QPushButton:pressed {\
                               background-color : black;\
                               }"
                               "QPushButton:focus {\
                               color : white;\
                               background-color : rgb(102, 142, 126);\
                               }")

    if(obj_type == "left_tab"):
        wid_obj.setStyleSheet("QTabWidget::pane {\
                              border : 0px outset white;\
                              border-radius : 0px;\
                              top : -10px;\
                              bottom : -9px;\
                              }"
                              "QTabBar::tab:selected {\
                              font : bold 15px serif;\
                              color : white;\
                              background : rgb(133, 152, 125);\
                              border : 1px solid grey;\
                              width : 248px;\
                              }"
                              "QTabBar::tab:!selected {\
                              font : Normal 14px 'Serif';\
                              color : gray;\
                              background : 'white';\
                              border : 1px solid grey;\
                              width : 248px;\
                              }")

    if(obj_type == "right_tab"):
        wid_obj.setStyleSheet("QTabWidget::pane {\
                              border : 0px outset gray;\
                              border-radius : 0px;\
                              top : -10px;\
                              bottom : -9px;\
                              }"
                              "QTabBar::tab:selected {\
                              font : Bold 15px 'Serif';\
                              color : white;\
                              background : rgb(133, 152, 125);\
                              border : 1px solid grey;\
                              width : 147px;\
                              }"
                              "QTabBar::tab:!selected {\
                              font : Normal 14px 'Serif';\
                              color : gray;\
                              background : white;\
                              border : 1px solid grey;\
                              width : 147px;\
                              }")
        
    if(obj_type == "disk_bar"):
        wid_obj.setStyleSheet("QProgressBar {\
                          text-align : center;\
                          font : Bold 14px 'Serif';\
                          color : rgb(86, 90, 85);\
                          border : 1px solid rgb(183, 207, 200);\
                          }"
                            "QProgressBar::chunk {\
                             background-color :rgb(183, 207, 200);\
                             border-radius : 0px;\
                          }")
        
    if(obj_type == "dock"):
        wid_obj.setStyleSheet("QMainWindow::splitter {\
                              width : 0px;\
                              }"
                              "QSplitter::handle {\
                              width : 0px;\
                              background-color : black;\
                              }"
                              "QDockWidget {\
                              border : 10px outset gray;\
                              border-radius : 10px;\
                              }")

    if(obj_type == "log_dock"):
        wid_obj.setStyleSheet("QSplitter::handle:horizontal {\
                              height : 0px;\
                              background-color : black;\
                              }"
                              "QDockWidget {\
                              border : 10px outset gray;\
                              border-radius : 10px;\
                              }")

    if(obj_type == "prog_lab"):
        wid_obj.setStyleSheet("QLabel {\
                              font : normal 16px times;\
                              color : black;\
                              background : rgb(248, 244, 244);\
                              }")


    if(obj_type == "text_browser"):
        wid_obj.setStyleSheet("QTextBrowser {\
                              font : normal 12px monospace;\
                              color : rgb(118, 112, 112);\
                              border : 1px outset gray;\
                              border-radius : 10px;\
                              selection-background-color : rgb(177, 201, 191);\
                              }"
                              "QScrollBar {\
                              border : 0px outset grey;\
                              background : white;\
                              width : 8px;\
                              }"
                              "QScrollBar::handle:vertical {\
                              border : 1px solid grey;\
                              background : lightgray;\
                              }")
    
    if(obj_type == "tree"):
        wid_obj.setStyleSheet("QTreeWidget {\
                              font : normal 12px ariel;\
                              color : rgb(55, 65, 73);\
                              border : 1px outset gray;\
                              border-radius : 10px;\
                              }"
                              "QTreeWidget::item:selected {\
                              background : rgb(153, 172, 164);\
                              }"
                              "QTreeWidget::item:disabled {\
                              color : gray;\
                              }"
                              "QScrollBar {\
                              border : 0px outset grey;\
                              background : white;\
                              width : 8px;\
                              }"
                              "QScrollBar::handle:vertical {\
                              border : 1px solid grey;\
                              background : lightgray;\
                              }"
                              "QTreeWidget::indicator:checked {\
                              image : url(icon/checked.png);\
                              }"
                              "QTreeWidget::indicator:!checked {\
                              image : url(icon/unchecked.png);\
                              }"
                              "QCheckBox::indicator {\
                              height : 15px;\
                              width : 15px;\
                              }")
                

    if(obj_type == "status_bar"):
        wid_obj.setStyleSheet("QStatusBar {\
                              background : rgb(248, 244, 244);\
                              font : normal 16px 'times';\
                              color : black;\
                              border : 1px inset white;\
                              border-radius : 0px;\
                              }")

    if(obj_type == "prog_bar"):
        wid_obj.setStyleSheet("QProgressBar {\
                          text-align : center;\
                          font : Bold 14px 'Serif';\
                          color : black;\
                          border : 1px solid rgb(174, 179, 173);\
                          }"
                            "QProgressBar::chunk {\
                             background-color : rgb(174, 179, 173);\
                             border-radius : 0px;\
                          }")
              
