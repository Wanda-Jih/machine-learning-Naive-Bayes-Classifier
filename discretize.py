import csv
import sys
import pandas as pd


def read_data(input_data):
    df = pd.read_csv(input_data)
    return df    

def divide_dataset(trainingSet, df, col, info):

    max_value = trainingSet.iloc[:, col].max()
    min_value = trainingSet.iloc[:, col].min()
    divide_value = (max_value - min_value) / 5
    
    if (col == 1 or col == 2):
        max_value = 58
        min_value = 18
        divide_value = (max_value - min_value) / 5  
        
    new_records = [0]*5
    start_value = min_value
    
    for k in range(5):
        end_value =  start_value + divide_value
        for i in range(len(df.index)):
            value = trainingSet.iloc[i, col]
                
            if k == 0 and value == min_value:
                new_records[k] += 1
                df.iloc[i, col] = k  
                
            if value > start_value and value <= end_value:
                new_records[k] += 1
                df.iloc[i, col] = k

        start_value = end_value
        
    print('%s: %s'%(info[col],str(new_records)))
    
    
def write_into_csv(df, output_path):
    df.to_csv(output_path, index=False)  
    
    
if __name__ == '__main__':
    
    if(len(sys.argv) != 2):
        input_path = "dating.csv"
    else:
        input_path = sys.argv[1]

    # read csv
    trainingSet = read_data(input_path)
    df = read_data(input_path)

    # convert continuous attributes to categorical attributes
    divide_list = [1,2,6,7]
    for i in range(9, 52):
        divide_list.append(i)
      
    info = list(df.columns.values)
    for col in divide_list:
        divide_dataset(trainingSet, df, col, info)


    # write the dataset into a new csv
    output_path = "dating-binned.csv"
    write_into_csv(df, output_path)
    