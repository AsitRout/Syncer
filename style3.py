"""
Set StyleSheet
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def set_style(wid_obj, obj_type):
    if(obj_type == "app"):
        pass
    
    if(obj_type == "loc_button"):
        wid_obj.setStyleSheet("QPushButton {\
                               background-color : rgb(116, 118, 110);\
                               font : normal 14px 'Times';\
                               color : white;\
                               border : 1px outset darkGray;\
                               border-radius : 4px;\
                               padding : 0px;\
                               }"
                               "QPushButton:pressed {\
                               background-color : black;\
                               }"
                               "QPushButton:focus {\
                               color : white;\
                               background-color : rgb(80, 82, 75);\
                               }")


    if(obj_type == "act_button"):
        wid_obj.setFocusPolicy(Qt.NoFocus)
        wid_obj.setStyleSheet("QPushButton {\
                               background-color : rgb(173, 177, 163);\
                               font : normal 14px 'Times';\
                               color : rgb(78, 80, 75);\
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
                               }"
                              "QPushButton:disabled {\
                               color : lightgrey;\
                               background-color : rgb(221, 227, 209);\
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
   








        
