import csv
import sys
import pandas as pd
import matplotlib.pyplot as plt


def read_data(input_data):
    df = pd.read_csv(input_data)
    return df    

def divide_data(df, testSet, input_data):
    
    csv_file = csv.reader(open("temp/temp.csv",'r'))  
    trainingData = []
    
    for i, row in enumerate(csv_file):
        if i == 0:
            continue;
        if  i not in testSet:
            trainingData.append(row)      

    dfTrain = pd.DataFrame(trainingData, columns = list(df.columns.values))
    return dfTrain
 
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

    return df
 
def nbc(t_frac, dfTrain, dfTest, accTrain, accTest):

    
    # calculate prior probability
    prior_true_total, prior_false_total, prior_true, prior_false = prior_probability(dfTrain)


    # ceate multiple tables for probability
    trueList,  falseList = create_table(dfTrain, prior_true_total, prior_false_total)

    # evaluate the model and generate the accuracy
    result = evaluate(dfTrain, prior_true, prior_false, trueList, falseList)   
    accuracy = result/len(dfTrain["decision"])
    print('Training Accuracy: %.2f'%accuracy)
    accTrain.append(accuracy)
    
    
    # calculate prior probability
    prior_true_total, prior_false_total, prior_true, prior_false = prior_probability(dfTest)

    # evaluate the model and generate the accuracy
    result = evaluate(dfTest, prior_true, prior_false, trueList, falseList)   
    accuracy = result/len(dfTest["decision"])
    print('Training Accuracy: %.2f'%accuracy)   
    accTest.append(accuracy)
    
    return accTrain, accTest

def prior_probability(df):
    
    decision = []
    decision = df["decision"]
    
    prior_true_total = 0
    prior_false_total = 0
    for i in range(len(decision)):
        if(decision[i] == 1):
            prior_true_total += 1
        else:
            prior_false_total += 1
    
    total = prior_true_total + prior_false_total
    prior_true = prior_true_total / total
    prior_false = 1 - prior_true   
    
    return prior_true_total, prior_false_total, prior_true, prior_false
 
def create_table(df, prior_true_total, prior_false_total):
    
    trueList = [] # all columns if decision == 1
    falseList = [] # all columns if decision == 0
    for col in range(51): # run all columns except 'decision'
    
        trueDict = {}
        falseDict = {}
        trueTotal = 0; 
        falseTotal = 0;
    
        for i, row in df.iterrows(): # run all the rows
    
            if df.iloc[i, col] not in trueDict.keys():
                trueDict[df.iloc[i, col]] = 0
            if df.iloc[i, col] not in falseDict.keys():
                falseDict[df.iloc[i, col]] = 0
                
            elif(df.iloc[i, 52] == 1):
                trueDict[df.iloc[i, col]] += 1
                trueTotal += 1
            else:
                falseDict[df.iloc[i, col]] += 1
                falseTotal += 1
                
        # change the amount to probability        
        for key in trueDict:
            if trueDict[key] == 0:
                trueDict[key] = 1
                trueDict[key] /= (trueTotal + prior_true_total)
            else:
                trueDict[key] /= trueTotal
                
        for key in falseDict:
            if falseDict[key] == 0:
                falseDict[key] = 1
                falseDict[key] /= (falseTotal + prior_false_total)
            else:
                falseDict[key] /= falseTotal    
        
        trueList.append(trueDict)
        falseList.append(falseDict)
    return trueList,  falseList

def evaluate(df, prior_true, prior_false, trueList, falseList)  :
    trueCal = prior_true
    falseCal = prior_false
    result = 0
    
    for i, row in df.iterrows():
    
        trueCal = prior_true
        falseCal = prior_false
    
        for col in range(51):
            try:
                trueCal *= trueList[col][row[col]]
            except:
                trueCal *= 1
            try:
                falseCal *= falseList[col][row[col]]
            except:
                falseCal *= 1
    
        if trueCal > falseCal:
            target = 1
        else:
            target = 0
    
        if target == row[52]:
            result += 1
        
    return result
   
def draw_plot(bin_list, accTrain, accTest):
    
    plt.figure(figsize=(15,10),dpi=100,linewidth = 2)
    plt.plot(bin_list, accTrain,'s-',color = 'r', label="accTrain")
    plt.plot(bin_list, accTest,'o-',color = 'g', label="accTest")
    
    plt.title("Accuracy", x=0.5, y=1.03)
    plt.savefig("img/(5_2)different_bins.jpg")
    
    
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
    accTrain = []
    accTest = []
    for bin_num in bin_list:
        
        print("Bin size: " + str(bin_num))
        

        for col in divide_list:
            dfBin = bins(trainingSet, df, col, bin_num, info)
        dfBin.to_csv("temp/temp.csv", index=False)  
        

        testData = dfBin.sample(frac=0.2, random_state=47)
        testSet = set(testData.index)
        

        trainingData = divide_data(dfBin, testSet, input_path)
        trainingData.to_csv("temp/tempTrain.csv", index=False) 
        testData.to_csv("temp/tempTest.csv", index=False)  
        
        trainingData = pd.read_csv("temp/tempTrain.csv")  
        testData = pd.read_csv("temp/tempTest.csv")  
        accTrain, accTest = nbc(1, trainingData, testData, accTrain, accTest)
        
       
    draw_plot(bin_list, accTrain, accTest)

    