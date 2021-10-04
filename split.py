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
    df = pd.read_csv(input_path)

    trainingData = []
    testData = []
    
    for i, row in enumerate(csv_file):
        if i == 0:
            continue;
        if  i in testSet:
            testData.append(row)
        else:
            trainingData.append(row)
            
    dfTrain = pd.DataFrame(trainingData, columns = list(df.columns.values))
    dfTest = pd.DataFrame(testData, columns = list(df.columns.values))
    return dfTrain, dfTest
         
def write_into_csv(train_data, output_path):
      
    train_data.to_csv(output_path, index=False)           


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
    
    # divide dataset 
    trainingData, testData = divide_data(testSet, input_path)
    
    # write data into csv
    write_into_csv(trainingData, triainingSet_path)
    write_into_csv(testData, testSet_path)
    