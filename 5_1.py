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
    prior_true_total, prior_false_total, prior_true, prior_false = prior_probability(df)

    # ceate multiple tables for probability
    trueList,  falseList = create_table(df, prior_true_total, prior_false_total)

    # evaluate the model and generate the accuracy
    result = evaluate(df, prior_true, prior_false, trueList, falseList)   
    accuracy = result/len(df["decision"])
    print('Training Accuracy: %.2f'%accuracy)
    
     # read testSet.csv
    df = read_data(test_path, t_frac)   
    
    # calculate prior probability
    prior_true_total, prior_false_total, prior_true, prior_false = prior_probability(df)

    # evaluate the model and generate the accuracy
    result = evaluate(df, prior_true, prior_false, trueList, falseList)   
    accuracy = result/len(df["decision"])
    print('Testing Accuracy: %.2f'%accuracy)    

def read_data(input_data, t_frac):
    df = pd.read_csv(input_data)
    if input_data == "trainingSet.csv":
        df = df.sample(random_state=47, frac=t_frac)
    return df    

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


if __name__ == "__main__":

    nbc(1)