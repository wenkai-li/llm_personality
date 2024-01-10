import pickle
import csv

class KaggleDataset():
    def __init__(self, path_of_dataset="/home/zw3/anlp_final/data/Kaggle/test.pkl"):
        with open(path_of_dataset, 'rb') as f:
            self.data = pickle.load(f)
        self.poster_data = self.process_data()
    
    def process_data(self):
        poster = self.data['posts_text']
        label = self.data['annotations']
        label_lookup = {'E': 1, 'I': 0, 'S': 1, 'N': 0, 'T': 1, 'F': 0, 'J': 1, 'P': 0}
        poster_data = [{'posts': t, 'questions': ["N/A"]*50, 'label0': label_lookup[list(label[i])[0]],
                        'label1': label_lookup[list(label[i])[1]], 'label2': label_lookup[list(label[i])[2]],
                        'label3': label_lookup[list(label[i])[3]]} for i, t in enumerate(poster)]
        return poster_data
    
    def clean_data(self):
        for data_line in self.poster_data:
            for post in data_line['posts']:
                pass

class KaggleDatasetWithQuestion():
    def __init__(self, path_of_dataset="data/KaggleWithQuestion.csv"):
        file =  open(path_of_dataset, 'r')
        reader = csv.DictReader(file,delimiter='\t')
        self.poster_data = [{'posts': t["posts"].split("|||"), 'questions': t["questions"].split("|||"), 'label0': t["label0"],
                        'label1': t["label1"], 'label2': t["label2"],
                        'label3': t["label3"]} for t in reader]
        


class EssayDataset():
    def __init__(self, path_of_dataset="data/Essay/test.pkl"):
        with open('data/Essay/test.pkl', 'rb') as f:
            self.data = pickle.load(f)