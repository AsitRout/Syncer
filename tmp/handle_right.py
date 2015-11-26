
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
                        central.handle_left(central, obj_list[i][0], action)
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
                        central.handle_left(central, obj_list[i][0], action)
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
            central.handle_left(central, ob, action)

        tree.blockSignals(False)
      
#Reflect change to Tree in Dock2  
def handle_left(central, ob, action):
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
     
