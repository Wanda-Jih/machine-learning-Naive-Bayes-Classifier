import csv
import numpy as np
import re
import sys
import pandas as pd
def get_Train_data(file_path,train_index):
    csv_file = csv.reader(open(file_path, 'r'))
    train_data= []
    aim_data=[]
    label_info=None#init
    for i,row in enumerate(csv_file):
        if i==0:
            label_info=row
            continue
        if i in train_index:
            train_data.append(row[:-1])
            aim_data.append(row[-1])
    #print(aim_data[0])
    return train_data,aim_data,label_info
def get_Test_data(file_path):
    csv_file = csv.reader(open(file_path, 'r'))
    train_data= []
    aim_data=[]
    label_info=None#init
    for i,row in enumerate(csv_file):
        if i==0:
            label_info=row
            continue

        train_data.append(row[:-1])
        aim_data.append(row[-1])
    #print(aim_data[0])
    return train_data,aim_data,label_info
def Transfer_Array(data):
    if type(data[0])==int:
        m,n=len(data),1
    else:
        m,n=len(data),len(data[0])
    final_data=np.zeros([m,n])
    for i in range(m):
        if n!=1:
            for j in range(n):
                final_data[i][j]= float(data[i][j])
        else:
            final_data[i] = float(data[i])
    return final_data

def Build_dict(train_data,column,value_dict,aim_data,label):
    #print(aim_data.shape)
    work_on_index=np.argwhere(aim_data==label)
    # if(column == 0): 
    #     print(work_on_index.shape)
    #     print(work_on_index[0])
    #     print(work_on_index[1])
    #     print(work_on_index[2])
    #     print(work_on_index[3])
    #     print(work_on_index[4])
    #     print(work_on_index[5])
    #     print(work_on_index[6])
    #     print(work_on_index[7])
    #     print(work_on_index[8])
    #print(work_on_index[0])
    #print(work_on_index[1])
    #print(work_on_index.shape)
    #print(column)
    work_on_sample=train_data[work_on_index,column]
    # print(train_data)
    # if(column == 0): 
    #     print(work_on_sample.shape)
    #     # print(train_data[work_on_index,column])
    #     for i in range(40):
    #     # print(train_data[work_on_index,column])
    #         print(work_on_sample[i])

    #print(work_on_sample.shape)
    #exit()
    probability_dict={}
    for value in value_dict:
        probability_dict[value]=len(np.argwhere(work_on_sample==value))/len(work_on_sample)
        if column == 0:
            print(len(np.argwhere(work_on_sample==value)))
            print(len(work_on_sample))  
    probability_dict['total']=len(work_on_sample)
    if column == 0:
        print(probability_dict)
    return probability_dict


def Form_conditional_probability(train_data,aim_data,i):
    value_dict=set()
    for k in range(len(train_data)):
        if int(train_data[k,i]) not in value_dict:
            value_dict.add(int(train_data[k,i]))
            # if i == 8   :
            #     print(int(train_data[k,i]))
    #deal with "ZERO COUNTS ARE A PROBLEM"

    all_dict={}
    label=1
    #print(i)
    all_dict[label]=Build_dict(train_data,i,value_dict,aim_data,label)
    label = 0
    all_dict[label] = Build_dict(train_data, i, value_dict, aim_data, label)
    return all_dict
def Calcu_condition(example,label_info,record_dict,label):
    times_Result=1
    for i in range(len(example)):
        choose_feature=label_info[i]
        feature_dict=record_dict[choose_feature]
        feature_under_label=feature_dict[label]
        feature_value=int(example[i])
        if feature_value in feature_under_label.keys():
            tmp_p=feature_under_label[feature_value]
        else:
            tmp_p=1/(feature_under_label['total']+len(feature_under_label))#Deal with 0 count problem.
        times_Result*=tmp_p
    return times_Result
def Predict_example(example,label_info,record_dict,prior_true):
    label=0
    likelihood1=Calcu_condition(example,label_info,record_dict,label)*(1-prior_true)
    label = 1
    likelihood2 = Calcu_condition(example, label_info, record_dict, label) * (1 - prior_true)
    if likelihood1>likelihood2:
        return 0
    else:
        return 1
def Evaluate(train_data,aim_data,label_info,record_dict,prior_true):
    count=0
    for i,example in enumerate(train_data):
        predicted=Predict_example(example,label_info,record_dict,prior_true)
        if predicted==aim_data[i]:
            count+=1
    return count/len(train_data)

def nbc(t_frac):
    input_path = 'trainingSet.csv'
    pd_reader = pd.read_csv(input_path, delimiter=',')
    result = pd_reader.sample(random_state=47, frac=t_frac)
    use_index=result.index
    train_data, aim_data, label_info=get_Train_data(input_path,use_index)
    
    
    # print(train_data)
    #Change the data to np array
    train_data=Transfer_Array(train_data)
    aim_data=Transfer_Array(aim_data)

    # print(train_data)
    #print(aim_data.shape)
    #exit()
    #Now we need to calculate the prior probability
    prior_true=len(np.argwhere(aim_data==1))/len(aim_data)
    # prior_false=1-prior_true
    # #Calculate the conditional probability
    record_dict={}
    
    for i in range(len(train_data[0])):
        record_dict[label_info[i]]=Form_conditional_probability(train_data,aim_data,i)
    # #deal with "ZERO COUNTS ARE A PROBLEM"
    # #print(record_dict)
    # #Evaluating on the training set and then on the validation set
    accuracy=Evaluate(train_data,aim_data,label_info,record_dict,prior_true)
    print('Training Accuracy: %.2f'%accuracy)
    
    
    # #test performance
    # input_path = 'testSet.csv'
    # train_data, aim_data, label_info = get_Test_data(input_path)
    # train_data = Transfer_Array(train_data)
    # aim_data = Transfer_Array(aim_data)
    # aim_data = aim_data[:, 0]
    # accuracy=Evaluate(train_data,aim_data,label_info,record_dict,prior_true)
    # print('Testing Accuracy: %.2f'%accuracy)

if __name__ == '__main__':
    nbc(1)