import math
import random
import json

import matplotlib.pyplot as plt

from functions import read_json, Write_to_json


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
    sum_num = 0

    for w_dic in kw.values():
        key_lis = w_dic.keys()
        count_lis = w_dic.values()

        # cumulate all counts
        sum_num += sum(count_lis)

        for k,c in zip(key_lis, count_lis):
            
            # Condition when key exists in All_dic
            if k not in All_dic.keys():
                All_dic.update({k:int(c)})
            
            # Otherwise
            else:
                old_count = int(All_dic[k])
                new_count = old_count + int(c)
                All_dic.update({k:new_count})
    return All_dic, sum_num


def Single_keyword_Sort_Filter_All_Year(file_dir, display_threshold):
    # Acquire the comprehensive dictionary of sampled data
    whole_dict, sum_count = Single_keyword_All_Year(file_dir)

    # Descendingly sort the whole keyword dictionary by their frequences, Pick top 20 to form a new dictionary
    sorted_whole_dic = {k: v for k, v in sorted(whole_dict.items(), key=lambda item: item[1], reverse = True)[:int(display_threshold)]}
    return sorted_whole_dic, sum_count


def Add_to_tabu_json(word, json_file):
    d = read_json(json_file)
    # Adding tabu words to the dictionary (list)
    dic = d['Tabu']

    if word in d['Tabu']:
        print("The word '%s' already exists"%word)

    else:
        dic.append(word)
        d.update({'Tabu':dic})
        print("Succeed! The new word '%s' has been add to excluding list"%word)
    Write_to_json(json_file, d)


def Add_to_replace_json(word, main_word, json_file):
    d = read_json(json_file)
    replace_dic = d['Replacement']

    # Adding new words to the main_word for replacement
    if main_word in replace_dic.keys():
        exis_lis = replace_dic[main_word]
        exis_lis.append(word)
        replace_dic.update({main_word:exis_lis})
        print("Succefully added '%s' to existing mainword '%s'"%(word, main_word))
    
    # Create new mainword
    else:
        replace_dic.update({main_word:[word]})
        print("Succefully created '%s' as a new mainwords and newly added '%s'"%(main_word, word))

    d.update({'Replacement':replace_dic})

    Write_to_json(json_file, d)

    
