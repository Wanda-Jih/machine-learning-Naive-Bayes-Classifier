import csv
import sys


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

if __name__ == "__main__":
    
    if(len(sys.argv) != 3):
        input_path = "trainingSet.csv"
    else:
        input_path = sys.argv[1]
    
    read_data(input_path)