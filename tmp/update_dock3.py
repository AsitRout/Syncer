
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

