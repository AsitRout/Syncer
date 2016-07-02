def clear_list(lst):
    for lst_item in lst:
        for i in range(len(lst_item)):
            lst_item.pop()
