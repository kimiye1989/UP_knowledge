import matplotlib.pyplot as plt
import json

import pandas as pd

def read_json(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

def Write_to_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def Add_to_tabu_json(word, json_file):
    d = read_json(file_name)
    d.update({word})

def Add_to_replace_json(word, main_word, json_file):
    read_json(file_name)

