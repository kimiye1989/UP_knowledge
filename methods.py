import math
import random
import json

from functions import read_json


def Single_keyword_Sort_Filter_By_Year(file_dir, display_threshold):
    new_dic = {}
    kw = read_json(file_dir)

    for yr, w_dic in zip(kw.keys(), kw.values()):
        # Descendingly sort the single keyword dictionary per year by their frequences, Pick top 20 to form a new dictionary
        sorted_w_dic = {k: v for k, v in sorted(w_dic.items(), key=lambda item: item[1], reverse = True)[:int(display_threshold)]}

        new_dic.update({yr:sorted_w_dic})
        # Output the top %threshould keywords by year

    return new_dic

def Single_keyword_All_Year(file_dir):
    # replace all keywords with accumulative counts in a shared dictionary whatever years
    All_dic = {}
    kw = read_json(file_dir)

    for w_dic in kw.values():
        key_lis = w_dic.keys()
        count_lis = w_dic.values()

        for k,c in zip(key_lis, count_lis):
            
            # Condition when key exists in All_dic
            if k not in All_dic.keys():
                All_dic.update({k:int(c)})
            
            # Otherwise
            else:
                old_count = int(All_dic[k])
                new_count = old_count + int(c)
                All_dic.update({k:new_count})
                
    return All_dic


def Single_keyword_Sort_Filter_All_Year(file_dir, display_threshold):
    new_dic = {}
    kw = read_json(file_dir)

    for yr, w_dic in zip(kw.keys(), kw.values()):
        # Descendingly sort the single keyword dictionary per year by their frequences, Pick top 20 to form a new dictionary
        sorted_w_dic = {k: v for k, v in sorted(w_dic.items(), key=lambda item: item[1], reverse = True)[:int(display_threshold)]}

        new_dic.update({yr:sorted_w_dic})
        # Output the top %threshould keywords by year
        
    return new_dic