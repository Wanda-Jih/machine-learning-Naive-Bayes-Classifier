import csv
import sys
import numpy as np


def read_data(input_data):

    # read csv file
    csv_file = csv.reader(open(input_path, 'r'))
    data = []
    for row in csv_file:
        data.append(row)
    label = data[0]

    train_data = []
    for i, row in enumerate(data[1:]):
        train_data.append(row)

    return label, train_data

def convert_data(train_data):
    
    if type(train_data[0]) == int:
        row, col = len(train_data), 1
    else:
        row, col = len(train_data), len(train_data[0])
        
    revised_data = np.zeros([row, col])
    for i in range(row):
        for j in range(col):
            if col != 1:
              revised_data[i][j] = float(train_data[i][j])                  
            else:
               revised_data[i] = float(train_data[i])

    return revised_data

def clean_data(train_data, label):
    
    clean_list = [6, 7]
    for i in range(21, len(label)-4):
        clean_list.append(i)
    clean_list.append(len(label)-3)
    clean_list.append(len(label)-2)
    
    for col in clean_list:
        for row in range(len(train_data)):
            if float(train_data[row][col]) > 10:
                train_data[row][col] = 10
                
    return train_data

def divide_data(train_data, label, col):
    
    # for col in divide_list:
    max_value = np.max(train_data[:, col])
    min_value = np.min(train_data[:, col])
    divide_value = (max_value - min_value)/5

    new_records = [0]*5
    start_value = min_value
    
    for k in range(5):
        end_value =  start_value + divide_value
        for i in range(len(train_data)):
            value = train_data[i, col]
            if value >= start_value and value < end_value:
                new_records[k] += 1
                train_data[i, col] = k
                
            # the biggest value
            if value == max_value and k == 4:
                new_records[k] += 1
                train_data[i, col] = k        
        start_value = end_value
        
    print('%s: %s'%(label[col],str(new_records)))
    
    return train_data
    
def write_into_csv(train_data, label, output_path):
      
    with open(output_path, 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
    
      writer.writerow(label)
      
      for i, row in enumerate(train_data):
          writer.writerow(row)            

if __name__ == '__main__':
    
    if(len(sys.argv) != 2):
        input_path = "dating.csv"
    else:
        input_path = sys.argv[1]

    # read csv
    label, train_data = read_data(input_path)

    # convert dataset to nump dataset
    train_data = convert_data(train_data)
    
    # clean data [0~10]
    train_data = clean_data(train_data, label)
    
    # convert continuous attributes to categorical attributes
    divide_list = [1,2,6,7]
    count= 0
    for i in range(9, len(label)-1):
        divide_list.append(i)
    for i in divide_list:
        train_data = divide_data(train_data, label, i)
        count += 1

    print(count)
    # write the dataset into a new csv
    output_path = "dating-binned.csv"
    write_into_csv(train_data, label, output_path)
    