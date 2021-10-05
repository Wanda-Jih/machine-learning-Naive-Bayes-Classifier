import csv
import sys
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

def get_fraction(train_data, attribute):
    
    all_participants = {}
    success_participants = {}
    success_rate = {}
   
    for i, row in enumerate(train_data):
        key = float(row[attribute])
        decision = row[52]
        if key not in all_participants.keys():
            all_participants[float(key)] = 0
            success_participants[float(key)] = 0
            success_rate[float(key)] = 0      
            
        all_participants[float(key)] += 1
        
        if(int(decision) == 1):
            success_participants[float(key)] += 1          
           
    for i, key in enumerate(all_participants):
        success_rate[key] = round(success_participants[key] / all_participants[key], 4)
    
    return success_rate   

def draw_scatter_plot(success_rate, label_name):
    
    x = []
    for key in list(success_rate.keys()):
        x.append(key)
    
    y = list(success_rate.values())

    plt.figure()
    plt.scatter(x, y)
    plt.title(label_name + ' success rate')
    plt.xlabel('Value')
    plt.ylabel('Success Rate')
    plt.savefig('img/' + label_name + '_success_rate.jpg')
    
if __name__ == '__main__':
    
    if(len(sys.argv) != 2):
        input_path = "dating.csv"
    else:
        input_path = sys.argv[1]

    # read csv
    label, train_data = read_data(input_path)
    
    # run six attributes
    for attribute in range(26,32):
        # calcualte the success rates and store them into the dictionary
        success_rate = get_fraction(train_data, attribute)
        
        # draw six scatter plots
        draw_scatter_plot(success_rate, label[attribute])
    

    
