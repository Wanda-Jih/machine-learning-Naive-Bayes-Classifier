import csv
import sys
import pandas as pd


def read_data(input_data):
    df = pd.read_csv(input_data)
    return df    

def divide_data(testSet, input_data):
    
    # read csv file
    csv_file = csv.reader(open(input_path,'r'))   
    df = read_data(input_data)
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
 
    
def bins(trainingSet, df, col, bin_num, info):

    max_value = trainingSet.iloc[:, col].max()
    min_value = trainingSet.iloc[:, col].min()
    divide_value = (max_value - min_value) / bin_num
    
    if (col == 1 or col == 2):
        max_value = 58
        min_value = 18
        divide_value = (max_value - min_value) / bin_num    
        
    new_records = [0]*bin_num
    start_value = min_value
    
    for k in range(bin_num):
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
 
def nbc(t_frac, dfTrain, dfTest):

    # calculate prior probability
    prior_true, prior_false = prior_probability(dfTrain)

    # ceate multiple tables for probability
    trueList,  falseList = create_table(dfTrain)

    # evaluate the model and generate the accuracy
    result = evaluate(dfTrain, prior_true, prior_false, trueList, falseList)   
    accuracy = result/len(dfTrain["decision"])
    print('Training Accuracy: %.2f'%accuracy)
    
    
    # # calculate prior probability
    # prior_true, prior_false = prior_probability(dfTest)

    # # evaluate the model and generate the accuracy
    # result = evaluate(dfTest, prior_true, prior_false, trueList, falseList)   
    # accuracy = result/len(dfTest["decision"])
    # print('Training Accuracy: %.2f'%accuracy)   

def prior_probability(df):
    
    decision = []
    decision = df["decision"]
    
    prior_true = 0
    prior_false = 0
    for i in range(len(decision)):
        if(int(decision[i]) == 1):
            prior_true += 1
        elif (int(decision[i]) == 0):
            prior_false += 1
     
    total = prior_true + prior_false
    prior_true /= total
    prior_false = 1 - prior_true   
    
    return prior_true, prior_false
 
def create_table(df):
    
    trueList = [] # all columns if decision == 1
    falseList = [] # all columns if decision == 0
    
    for col in range(1): # run all columns except 'decision'
        trueDict = {}
        falseDict = {}
        trueTotal = 0; 
        falseTotal = 0;
        print(df.iloc[i, 52])
        for i, row in df.iterrows(): # run all the rows
            if(int(df.iloc[i, 52]) == 1):
                if int(df.iloc[i, 52]) not in trueDict.keys():
                        trueDict[int(df.iloc[i, 52])] = 0
                trueDict[int(df.iloc[i, 52])] += 1
                trueTotal += 1
            else:
                if int(df.iloc[i, 52]) not in falseDict.keys():
                    falseDict[int(df.iloc[i, 52])] = 0
                falseDict[int(df.iloc[i, 52])] += 1
                falseTotal += 1
                
        # change the amount to probability        
        for key in trueDict:
            trueDict[key] /= trueTotal
        for key in falseDict:
            falseDict[key] /= falseTotal
            
        
        trueList.append(trueDict)
        falseList.append(falseDict)
        print("trueList = " + str(trueList))
        print("falseList = " + str(falseList))

    return trueList,  falseList   
 
def evaluate(df, prior_true, prior_false, trueList, falseList)  :
    trueCal = prior_true
    falseCal = prior_false
    result = 0
    
    for i, row in df.iterrows():
        
        trueCal = prior_true
        falseCal = prior_false
        
        for col in range(51):
            if trueList[col][int(df.iloc[0,col])] == 0:
                trueList[col][int(df.iloc[0,col])] = 1
            if falseList[col][int(df.iloc[0,col])] == 0:
                falseList[col][int(df.iloc[0,col])] = 1
                
            trueCal *= trueList[col][int(df.iloc[0,col])]
            falseCal *= falseList[col][int(df.iloc[0,col])]
        
        if trueCal >= falseCal:
            target = 1
        else:
            target = 0
    
        if target == row[52]:
            result += 1
    
    print("result = " + str(result))
    return result
   
if __name__ == '__main__':
    
    if(len(sys.argv) != 2):
        input_path = "dating.csv"
    else:
        input_path = sys.argv[1]

    # read csv
    trainingSet = read_data(input_path)
    df = read_data(input_path)
    df1 = read_data(input_path)

    # convert continuous attributes to categorical attributes
    divide_list = [1,2,6,7]
    for i in range(9, 52):
        divide_list.append(i)
      
    info = list(df.columns.values)
    bin_list = [2, 5, 10, 50, 100, 200]
    for bin_num in bin_list:
        
        print("Bin size: " + str(bin_num))
        
        for col in divide_list:
            bins(trainingSet, df, col, bin_num, info)
        
        data = df.sample(frac=0.2, random_state=47)
        testSet =  set(data.index)
        trainingData, testData = divide_data(testSet, input_path)
        nbc(1, trainingData, testData)
        
        

    