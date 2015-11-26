"""
Set StyleSheet
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *


def set_style(wid_obj, obj_type):
    if(obj_type == "app"):
        pass
    
    if(obj_type == "loc_button"):
        wid_obj.setFocusPolicy(Qt.NoFocus)
        wid_obj.setStyleSheet("QPushButton {\
                           background-color : rgb(252, 250, 250);\
                           font : normal 14px 'monospace';\
                           color : grey;\
                           border : 1px solid Gray;\
                           border-radius : 5px;\
                           padding : 0px;\
                           }")


    if(obj_type == "dev_button"):
        wid_obj.setStyleSheet("QPushButton {\
                               background-color : rgb(106, 159, 141);\
                               font : normal 18px 'Times';\
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
                               background-color : rgb(58, 85, 76);\
                               }")

    if(obj_type == "act_button"):
        wid_obj.setFocusPolicy(Qt.NoFocus)
        wid_obj.setStyleSheet("QPushButton {\
                               background-color : rgb(155, 176, 169);\
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
        
    if(obj_type == "act_button2"):
         wid_obj.setFocusPolicy(Qt.NoFocus)
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

    if(obj_type == "tool_button"):
        wid_obj.setFocusPolicy(Qt.NoFocus)
        wid_obj.setStyleSheet("QToolButton::menu-button {\
                              color : green;\
                              }"
                           "QToolButton {\
                           background-color : rgb(252, 250, 250);\
                           border : 0px outset gray;\
                           border-radius : 10px;\
                           }")


    if(obj_type == "frame"):
        return
        wid_obj.setStyleSheet("QFrame {\
                              border : 10px outset gray;\
                              border-radius : 10px;\
                              }")           

    if(obj_type == "sec_frame"):
        return
        wid_obj.setStyleSheet("QFrame {\
                              border : 10px outset gray;\
                              border-radius : 10px;\
                              }")   
   
    
    if(obj_type == "checkbox"):
        wid_obj.setFocusPolicy(Qt.NoFocus)
        wid_obj.setStyleSheet("QCheckBox::indicator:checked{\
                              image : url(icon/checked.png);\
                               }"
                              "QCheckBox::indicator:!checked{\
                              image : url(icon/unchecked.png);\
                               }")
                              
    if(obj_type == "label"):
        wid_obj.setStyleSheet("QLabel {\
                               font : bold 16px monospace;\
                               color : rgb(33, 54, 47);\
                              }")

                           
    

        
