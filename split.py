import sys
import csv
import pandas as pd


def read_data(input_data):

    # read csv file
    csv_file = pd.read_csv(input_data)

    data = pd.DataFrame(csv_file)
    data = data.sample(frac=0.2, random_state=47)
    
    return set(data.index)

def divide_data(testSet, input_path):
    
    # read csv file
    csv_file = csv.reader(open(input_path,'r'))    
  
    label = []
    trainingData = []
    testData = []
    
    for i, row in enumerate(csv_file):
        if i == 0:
            label = row
        elif i in testSet:
            testData.append(row)
        else:
            trainingData.append(row)
            
    return label, trainingData, testData
         
def write_into_csv(train_data, label, output_path):
      
    with open(output_path, 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
    
      writer.writerow(label)
      
      for i, row in enumerate(train_data):
          writer.writerow(row)            

if __name__ == '__main__':
    
    if(len(sys.argv) != 2):
        input_path = "dating-binned.csv"
        triainingSet_path = "trainingSet.csv"
        testSet_path = "testSet.csv"
    else:
        input_path = sys.argv[1]
        triainingSet_path = sys.argv[2]
        testSet_path = sys.argv[3]

    # read csv
    testSet = read_data(input_path)
    
    # divide dataset : [label, training set, testing set]
    label, trainingData, testData = divide_data(testSet, input_path)
    
    # write data into csv
    write_into_csv(trainingData, label, triainingSet_path)
    write_into_csv(testData, label, testSet_path)
    