"""
translate well chart to something python can use

"""

import os
import csv
import time
import math



	# make sures that arr2d is a rectangel or makes it one
def _csv_to_arr(path) :
    arr2d = []
    with open(path, "r") as csvfile :
        my_reader = csv.reader(csvfile)
        for row in my_reader :
            for i,item in enumerate(row) :
                if isinstance(item,str) :
                    if item.isnumeric() :
                        row[i]=float(item)
            arr2d.append(row)
    return arr2d

def csv_to_arr(path) :
    arr2d = []
    with open(path, "r") as csvfile :
        my_reader = csv.reader(csvfile)
        for row in my_reader :
            arr2d.append(row)
    return arr2d

def arr_to_csv_asrows(arr2d,path,mode="a") :
    with open(path, mode) as csvfile :
        my_writer = csv.writer(csvfile)
        [my_writer.writerow(arr) for arr in arr2d]
    return

	# requires a rectangle
def arr_to_csv_ascols(arr2d,path,mode="a") :
    arr2d = make_rec(arr2d)
    with open(path, mode) as csvfile :
        my_writer = csv.writer(csvfile)
        [my_writer.writerow([arr[i] for arr in arr2d]) for i in range(0,len(arr2d[0]))]
    return

def make_rec(arr) :
    longest = len(arr[0])
    gotta_change = False
    for i in range(0,len(arr)) :
        if len(arr[i]) > longest :
            gotta_change = True
            longest = len(arr[i])
    if gotta_change :
        for i, item in enumerate(arr) :
            while(len(item)<longest) :
                item.append("")
    return arr

def rotate(arr1) :
    #arr1 = make_rec(arr1)
    arr2 = []
    for i in range(0,len(arr1[0])) :
        arr2.append([arr[i] for arr  in arr1])
    return arr2

global butts
butts = 0
def make_arr_num(arr1) :
    #print(arr1)
    global butts
    #print("hi")
    #print(len(arr))
    arr2 = []
    for row in arr1 :
        temp = []
        for item in row :
            
            if isinstance(item,str) :
                #if butts < 10 : print(item)
                if (not item == '') and is_num(item) :
                    #if butts < 10:
                        #print(type(item))
                    if butts < 100 : 
                        print(repr(item),end = " ")
                        print(type(item), end = " ")
                    temp.append(float(item))
                    if butts < 100 : print(type(temp[-1]))
                    #if butts < 10 : print(type(temp[-1]))
                else : 
                    temp.append(item)
                    if butts < 100 : print (repr(item))
            else : temp.append(item)
        
        arr2.append(temp)
        if butts < 2 :
            for row in arr2 :
                for item in row :
                    pass#print(type(item))
        butts+=1
    return arr2

path = "C:/Users/localuser/Desktop/Code Laboratory/Spanky (Nov)/6-28-2017_well-chart.csv"

def is_num(s) :
    my_chars = set('0123456789.-')
    chars = set(s)
    if chars.issubset(my_chars) : return True
    else : return False
    

chart_rows = csv_to_arr(path)
chart_cols = rotate(chart_rows)

chart_keys = []#[chart_rows[0]]

for let in chart_cols[0][1:]:
#    print(item)
    temp = []
    for num in chart_rows[0][1:]:
        temp.append(let+num)
    chart_keys.append(temp)
    
temp = chart_cols[1:]
temp2 = rotate(temp)
data_rows = temp2[1:]

#for row in temp3 :
#    for item in row :
#        print(item[0:5], end=" ")
#    print()

index_dict = {}
data_list = []
for data_row, key_row, in zip(data_rows, chart_keys) :
    for data, key in zip(data_row,key_row) :
        index_dict[key] = data.strip(" ")
        data_list.append(data.strip(" "))
#print(data_list)

#
data_set = set(data_list)
#print(data_set)

#data_list = []
#for row in data_rows :
#    data_list.extend(row)
#data_set = set(data_list)

drug_dict = {}
for item in data_set :
    #print(repr(item))
    drug_dict[item] = []
    

for k, v in index_dict.items() :
    drug_dict[v].append(k)

    





summary_sht_path = "C:/Users/localuser/Desktop/Code Laboratory/Spanky (Nov)/6-28-2017_cell-velocities_summary-sheet.csv"
save_file_path = "C:/Users/localuser/Desktop/Code Laboratory/Spanky (Nov)/6-28-2017_cell-velocities_summary-sheet2.xlsx"

summary_rows = csv_to_arr(summary_sht_path)
summary_cols = rotate(summary_rows)
#print(summary_rows)


def weighted_avg(spec_arr_rows) :
    #print(spec_arr_rows[0])
    wav_col = ["weighted avg","",""]
    cell_count_row = spec_arr_rows[1]
    #print(cell_count_row)
    for i,item in enumerate(cell_count_row) :
        cell_count_row[i] = int(item)
    
    num_rows = spec_arr_rows[2:]
    for row in num_rows :
        #print(row)
        row_sum = 0
        count = 0
        for i, item in enumerate(row) :
            if not (item == "" or i == 0):
                row_sum += float(item)*cell_count_row[i]
                count += cell_count_row[i]
        
        if not count == 0 : wav_col.append(row_sum/count)
    return wav_col

def inter_col(row_count) :
    inter_col = ["", "cell count", ""]
    for i in range(0,row_count-3) :
        inter_col.append(str((i+1)*10) + " - " + str((i+2)*10))
    return inter_col
    
         
        
wb = xlerate.Workbook()
row_count = 110
all_wav_cols = [inter_col(row_count)]

for key in drug_dict.keys() :
    spec_arr_cols = []
    for item in drug_dict[key] :
        try :
            i = summary_rows[0].index("_" + item)
        except : pass
        spec_arr_cols.append(summary_cols[i])
        #print(spec_arr_rows)
    
    spec_arr_rows = rotate(spec_arr_cols)
    wav_col = weighted_avg(spec_arr_rows)
    #print(wav_col)
    
        ### **********    !!!!    ********
    spec_arr_cols.append(wav_col)
    temp = rotate(spec_arr_cols)
    #print(temp)
    out_rows = make_arr_num(temp)
    #print(out_rows)
    
    wb.new_sheet(key, out_rows)
    
    wav_col[0] = key
    all_wav_cols.append(wav_col)
out_summary_rows = rotate(all_wav_cols)
wb.new_sheet("Summary", out_summary_rows)
wb.save(save_file_path)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    