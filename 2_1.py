import csv
import sys
import numpy as np
import matplotlib.pyplot as plt


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

def divid_gender(train_data):

    male_data = []
    female_data = []

    for i in range(len(train_data)):
        if train_data[i][0] == "0":
            male_data.append(train_data[i])
        else:
            female_data.append(train_data[i])

    return male_data, female_data

def calculate_mean(sub_dataset, label):

    size = len(sub_dataset)
    new_dict = {}
    new_list = []

    for i in range(size):
        for col in range(9, 15):
            if label[col] not in new_dict.keys():
                new_dict[label[col]] = 0
            new_dict[label[col]] += float(sub_dataset[i][col])

        
    for col in range(9, 15):
        new_dict[label[col]] /= size
        new_list.append(round(new_dict[label[col]], 2))
        print("Mean of %s : %.2f" %(label[col], new_dict[label[col]]))
          
    print("==================================")
    return new_list

def draw_barplot(male_mean, female_mean):
    
    # set width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))
     
    # Set position of bar on X axis
    br1 = np.arange(len(male_mean))
    br2 = [x + barWidth for x in br1]
     
    # Make the plot
    plt.bar(br1, male_mean, color ='b', width = barWidth,
            edgecolor ='grey', label ='male')
    plt.bar(br2, female_mean, color ='r', width = barWidth,
            edgecolor ='grey', label ='female')
     
    # Adding Xticks
    plt.xlabel('Attributes', fontweight ='bold', fontsize = 15)
    plt.ylabel('Mean', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(male_mean))],
            ["attractive","sincere","intelligence","funny","ambitious","interests"])
     
    plt.legend()
    plt.savefig("gender_attributes.jpg")

if __name__ == '__main__':
    
    if(len(sys.argv) != 2):
        input_path = "dating.csv"
    else:
        input_path = sys.argv[1]

    # read csv
    label, train_data = read_data(input_path)

    # divid dataset into sub_datasets
    male_data, female_data = divid_gender(train_data)

    # calculate the mean of six attributes
    print("Male data")
    male_mean = calculate_mean(male_data, label)
    print("Female data")
    female_mean = calculate_mean(female_data, label)
    
    # draw the barplot
    # output a .jpg
    draw_barplot(male_mean, female_mean)
    

    
