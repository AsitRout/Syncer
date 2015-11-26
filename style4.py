"""
Set StyleSheet
"""
from PyQt4.QtGui import *

def set_style4(wid_obj, obj_type):
    if(obj_type == "button"):
        wid_obj.setStyleSheet("QPushButton {\
                           background-color : rgb(252, 250, 250);\
                           font : bold 14px 'Times';\
                           color : rgb(106, 87, 71);\
                           border : 1px solid darkGray;\
                           border-radius : 5px;\
                           padding : 0px;\
                           }"
                           "QPushButton:pressed {\
                           background-color : black;\
                           }"
                           "QPushButton:focus {\
                           color : white;\
                           background-color : rgb(102, 142, 126);\
                           }")


    if(obj_type == "head_lab"):
        wid_obj.setStyleSheet("QLabel {\
                              font : normal 20px serif;\
                              color : black;\
                              background : white;\
                              border : 0px;\
                              }")
    if(obj_type == "sub_lab"):
        wid_obj.setStyleSheet("QLabel {\
                              font : normal 18px times;\
                              color : black;\
                              background : white;\
                              border : 0px;\
                              }")

    if(obj_type == "check_lab"):
        wid_obj.setStyleSheet("QLabel {\
                              font : normal 16px times;\
                              color : black;\
                              background : white;\
                              border : 0px;\
                              }")

    if(obj_type == "det_lab"):
        wid_obj.setStyleSheet("QLabel {\
                              font : normal 14px monospace;\
                              color : black;\
                              background : white;\
                              border : 0px;\
                              }")

    if(obj_type == "frame"):
        return
        wid_obj.setStyleSheet("QFrame {\
                              background : white;\
                              border : 1px solid gray;\
                              }")

