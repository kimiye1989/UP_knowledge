import math
import random
import json

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from functions import read_json, Write_to_json

def Single_keyword_By_Year(file_dir, display_threshold):
    new_dic = {}
    count_dic = {}
    kw = read_json(file_dir)

    for yr, w_dic in zip(kw.keys(), kw.values()):
        # Descendingly sort the single keyword dictionary per year by their frequences, Pick top 20 to form a new dictionary
        sorted_w_dic = {k: v for k, v in sorted(w_dic.items(), key=lambda item: item[1], reverse = True)[:int(display_threshold)]}
        sum_count = sum(w_dic.values())

        new_dic.update({yr:sorted_w_dic})
        count_dic.update({yr:sum_count})
        # Output the top %threshould keywords by year
    return new_dic, count_dic

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

def Plot_Whole_Year_Barchart(file_dir, display_threshold_all_years):

    whole_dic, original_occur = Single_keyword_Sort_Filter_All_Year(file_dir, display_threshold_all_years)

    X_lis = whole_dic.keys()
    Y_lis_temp = whole_dic.values()

    # Make sure every accum num is a positive integer
    Y_lis = [int(max(y,0)) for y in Y_lis_temp]

    Y_pesudo = [y/sum(Y_lis) for y in Y_lis_temp]
    Y_perc_lis = [y/int(original_occur) for y in Y_lis]

    fig = plt.figure(figsize=(15,7))
    ax1 = fig.add_axes([0, 0, 1, 1])
    ax2 = ax1.twinx()
    ax1.set(facecolor = "whitesmoke")
    ax1.grid(axis='both', color='lightgray')

    ax1.bar(X_lis, Y_lis, align='center', color='gray', label='Cumulative Occurences', alpha = 0.8)
    ax2.plot(X_lis, Y_pesudo, linewidth=2, color='blue', label='Percentiles (to Top %d Keywords)'%display_threshold_all_years) 
    ax2.plot(X_lis, Y_perc_lis, linewidth=2, color='red', label='Percentiles (to All Keywords)')

    ax2.scatter(X_lis, Y_pesudo, s=15, color='k')
    ax2.scatter(X_lis, Y_perc_lis, s=15, color='k')

    ax2.axvline(x=9, c='k', lw=1.5, linestyle='dashed', alpha = 0.6)
    ax2.axvline(x=19, c='k', lw=1.5, linestyle='dashed', alpha = 0.6)
    ax2.axvline(x=29, c='k', lw=1.5, linestyle='dashed', alpha = 0.6)
    ax2.axvline(x=39, c='k', lw=1.5, linestyle='dashed', alpha = 0.6, label='Per 10 Keywords')
    #ax1.annotate(10, max(Y_lis), (10, max(Y_lis)), c='k', fontsize = 12)

    ax1.text(-1, max(Y_lis)+0.5, str(max(Y_lis)), horizontalalignment='center', color = 'k',verticalalignment='center', fontsize = 16)
    ax2.text(-1, max(Y_pesudo)-0.007, "{0:.0%}".format(max(Y_pesudo)), horizontalalignment='center', color = 'blue',verticalalignment='center',fontsize = 16)
    ax2.text(-1, max(Y_perc_lis), "{0:.0%}".format(max(Y_perc_lis)), horizontalalignment='center', color = 'red', verticalalignment='center',fontsize = 16)
    
    ax1.set_xlabel('Keywords', fontsize=18)
    ax1.set_xticklabels(X_lis, rotation=90)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=None, symbol='%', is_latex=False))

    ax1.set_ylabel("Accumulative Occurences", fontsize=15, labelpad=12)
    ax2.set_ylabel("Percentile Occurences", fontsize=15, labelpad=12)

    ax1.set_title('Frequencies of Top %d Keywords of Year Spectrum (1923-1990)'%display_threshold_all_years, fontsize=18, y=1.06)

    plt.legend(loc='upper right', fontsize=16, ncol=1)

    plt.tight_layout()

    plt.savefig('./Outputs/All_year_single_word_frequencies.png', dpi=300, bbox_inches='tight')
    plt.show()

def Plot_Single_Year_Barchart(file_dir, display_threshold_per_year):

    dic_yr, original_occur_dic = Single_keyword_By_Year(file_dir, display_threshold_per_year)
    years_lis = dic_yr.keys()

    for yr in years_lis:
        whole_dic = dic_yr[yr]
        original_occur = int(original_occur_dic[yr])

        X_lis = whole_dic.keys()
        Y_lis_temp = whole_dic.values()

        # Make sure every accum num is a positive integer
        Y_lis = [int(max(y,0)) for y in Y_lis_temp]

        Y_pesudo = [y/sum(Y_lis) for y in Y_lis_temp]
        Y_perc_lis = [y/int(original_occur) for y in Y_lis]

        fig = plt.figure(figsize=(8,5))
        ax1 = fig.add_axes([0, 0, 1, 1])
        ax2 = ax1.twinx()
        ax1.set(facecolor = "whitesmoke")
        ax1.grid(axis='both', color='lightgray')

        ax1.bar(X_lis, Y_lis, align='center', color='gray', label='Cumulative Occurences', alpha = 0.8)
        ax2.plot(X_lis, Y_pesudo, linewidth=2, color='blue', label='Percentiles (to Top %d Keywords)'%display_threshold_per_year) 
        ax2.plot(X_lis, Y_perc_lis, linewidth=2, color='red', label='Percentiles (to All Keywords)')

        ax2.scatter(X_lis, Y_pesudo, s=15, color='k')
        ax2.scatter(X_lis, Y_perc_lis, s=15, color='k')

        #ax2.axvline(x=9, c='k', lw=1.5, linestyle='dashed', alpha = 0.6, label='Per 10 Keywords')
        #ax1.annotate(10, max(Y_lis), (10, max(Y_lis)), c='k', fontsize = 12)
        
        ax1.text(-1, max(Y_lis)+0.5, str(max(Y_lis)), horizontalalignment='center', color = 'k',verticalalignment='center', fontsize = 16)
        ax2.text(-1, max(Y_pesudo), "{0:.00%}".format(max(Y_pesudo)), horizontalalignment='center', color = 'blue',verticalalignment='center',fontsize = 16)
        ax2.text(-1, max(Y_perc_lis), "{0:.00%}".format(max(Y_perc_lis)), horizontalalignment='center', color = 'red', verticalalignment='center',fontsize = 16)
        
        ax1.set_xlabel('Keywords', fontsize=22)
        ax1.set_xticklabels(X_lis, rotation=90)
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=None, symbol='%', is_latex=False))

        ax1.set_ylabel("Accumulative Occurences", fontsize=15, labelpad=12)
        ax2.set_ylabel("Percentile Occurences", fontsize=15, labelpad=12)

        ax1.set_title('Frequencies of Top %d Keywords of Year %s'%(display_threshold_per_year, yr), fontsize=18, y=1.06)

        plt.legend(loc='upper right', fontsize=16, ncol=1)
        plt.tight_layout()
        plt.savefig('./Outputs/Per_Year/%s_Single_word_frequencies.png'%yr, dpi=90, bbox_inches='tight')
