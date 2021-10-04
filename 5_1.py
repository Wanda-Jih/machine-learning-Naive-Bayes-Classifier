import pandas as pd
import sys

def nbc(t_frac):
    if(len(sys.argv) != 2):
        training_path = "trainingSet.csv"
        test_path = "testSet.csv"
    else:
        training_path = sys.argv[1]
        test_path = sys.argv[2]

    # read trainingSet.csv
    df = read_data(training_path, t_frac)

    # calculate prior probability
    prior_true, prior_false = prior_probability(df)

    # ceate multiple tables for probability
    trueList,  falseList = create_table(df)

    # evaluate the model and generate the accuracy
    result = evaluate(df, prior_true, prior_false, trueList, falseList)   
    accuracy = result/len(df["decision"])
    print('Training Accuracy: %.2f'%accuracy)
    
     # read testSet.csv
    df = read_data(test_path, t_frac)   
    
    # calculate prior probability
    prior_true, prior_false = prior_probability(df)

    # evaluate the model and generate the accuracy
    result = evaluate(df, prior_true, prior_false, trueList, falseList)   
    accuracy = result/len(df["decision"])
    print('Training Accuracy: %.2f'%accuracy)    

def read_data(input_data, t_frac):
    df = pd.read_csv(input_data)
    if input_data == "trainingSet.csv":
        df = df.sample(random_state=47, frac=t_frac)
    return df    

def prior_probability(df):
    
    decision = []
    decision = df["decision"]
    
    prior_true = 0
    prior_false = 0
    for i in range(len(decision)):
        if(decision[i] == 1):
            prior_true += 1
        else:
            prior_false += 1
            
    total = prior_true + prior_false
    prior_true /= total
    prior_false = 1 - prior_true   
    
    return prior_true, prior_false
    
def create_table(df):
    
    trueList = [] # all columns if decision == 1
    falseList = [] # all columns if decision == 0
    
    for col in range(51): # run all columns except 'decision'
        trueDict = {}
        falseDict = {}
        trueTotal = 0; 
        falseTotal = 0;
        
        for i, row in df.iterrows(): # run all the rows
            if(df.iloc[i, 52] == 1):
                if df.iloc[i, col] not in trueDict.keys():
                        trueDict[df.iloc[i, col]] = 0
                trueDict[df.iloc[i, col]] += 1
                trueTotal += 1
            else:
                if df.iloc[i, col] not in falseDict.keys():
                    falseDict[df.iloc[i, col]] = 0
                falseDict[df.iloc[i, col]] += 1
                falseTotal += 1
                
        # change the amount to probability        
        for key in trueDict:
            trueDict[key] /= trueTotal
        for key in falseDict:
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
            trueCal *= trueList[col][df.iloc[0,col]]
            falseCal *= falseList[col][df.iloc[0,col]]
        
        if trueCal >= falseCal:
            target = 1
        else:
            target = 0
    
        if target == row[52]:
            result += 1
        
    return result


if __name__ == "__main__":

    nbc(1)