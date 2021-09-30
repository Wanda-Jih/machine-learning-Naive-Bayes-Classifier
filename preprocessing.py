# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# import pandas as pd
import csv
import sys


path = 'C:/Users/wenne/OneDrive/桌面/course/data mining/hw/hmw2/'

def read_write_data(input_path, output_path):
    
    # read csv file
    csv_file = csv.reader(open(input_path,'r'))
    data = []
    for row in csv_file:
        data.append(row)
    label = data[0]
    
    train_data = []
    for i,row in enumerate(data[1:]):
        train_data.append(row)
  
    
    # clean the quote and convert upper case to lower case
    train_data = clean_quote_and_lowercase(train_data)

    # assign number to some col
    train_data = value_assigned(train_data)
  
    # calculate the mean
    train_data = normalization(train_data, 15, 20, label)
    train_data = normalization(train_data, 9, 14, label)    
    
    # write the data into a new csv
    write_into_csv(train_data, label, output_path)
        
def clean_quote_and_lowercase(train_data):
    
    quote = 0
    upperCase = 0
    
    for  i, row in enumerate(train_data):
        
        race = row[3]
        race_o = row[4]
        field = row[8]

        # remove the quote
        if race[0] == '\'':
            train_data[i][3] = race[1:-1]
            # print(train_data[i][3]) # 2499
            quote += 1
            
        if race_o[0] == '\'':
            train_data[i][4] = race_o[1:-1]
            # print(train_data[i][4]) # 2517
            quote += 1
            
        if field[0] == '\'':
            train_data[i][8] = field[1:-1]
            # print(train_data[i][8]) # 3300
            quote += 1
        
        # change the field col from upperCase to lowerCase
        if(not field.islower()):
            row[8] = field.lower()
            upperCase += 1 # 5707
            
    print("Quotes removed from " + str(quote) + " cells.")
    print("Standardized " + str(upperCase) + " cells to lower case.")
    return train_data

def value_assigned(train_data):
    
    # gender
    train_data, new_dict = transfer_value(train_data, 0)
    print("Value assigned for male in column gender: "  + str(new_dict['male']) + ".")

    # race
    train_data, new_dict = transfer_value(train_data, 3)
    print("Value assigned for European/Caucasian-American in column race: "  + str(new_dict['European/Caucasian-American']) + ".")
               
    # race_o
    train_data, new_dict = transfer_value(train_data, 4)
    print("Value assigned for Latino/Hispanic American in column race o: "  + str(new_dict['Latino/Hispanic American']) + ".")

    # field
    train_data, new_dict = transfer_value(train_data, 8)
    print("Value assigned for law in column field: "  + str(new_dict['law']) + ".")
    
    return train_data
    
def transfer_value(train_data, col):
    
    new_list = []
    new_dict  = {}
    new_value = 0
            
    # create a new list to store every attribute in col
    for i, row in enumerate(train_data):
        train_data[i][col]=train_data[i][col].strip('\'')
        new_list.append(row[col])
     
    # according lexicographically/alphabetically to sort the list
    new_list.sort()
    
    # create the dictionary to story every attribute and it's new value
    for attribute in new_list:
        if attribute not in new_dict:
            new_dict[attribute] = new_value
            new_value += 1
            
    # assign new value to each attribute
    for i, row in enumerate(train_data):
        key = row[col]
        row[col] = new_dict[key]
        
    return train_data, new_dict

def normalization(train_data, i, j, label):
    
    new_dict = {}
 
    for count in range(len(train_data)):
        
        row = train_data[count]
        sum = 0
        
        # if the sum of the six attributes is not 100
        # need to normalize the data
        for k in range(i, j+1):
            sum += float(row[k])
        
        for k in range(i, j+1):
            row[k] = float(row[k])/sum
            
            # add up every row to each attribute
            # store them into dictionary
            if k not in new_dict.keys():
                new_dict[k] = 0
            new_dict[k] += row[k]
    
    # calculate the mean
    for k in range(i, j+1):
        show_label = label[k]
        mean = new_dict[k]/len(train_data)
        print("Mean of %s: %.2f." %(show_label, mean))
    
    return train_data

def write_into_csv(train_data, label, output_path):
        
    with open(output_path, 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
    
      writer.writerow(label)
      
      for i, row in enumerate(train_data):
          writer.writerow(row)
    
if __name__ == "__main__":
    
    if(len(sys.argv) != 3):
        input_path = "dating-full.csv"
        output_path = "dating.csv"
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
    
    read_write_data(input_path, output_path)
    