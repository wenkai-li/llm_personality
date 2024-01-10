from select_pipeline import get_json_list
import sys
sys.path.append('../')
import os
import csv
from tqdm import tqdm

def write_json_to_csv(json_data, file_path):
    # Open the file in append mode
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter='\t')

        # Write CSV Header
        writer.writerow(['posts', 'questions', 'label0', 'label1', 'label2', 'label3'])

        # Process and write each row of data
        for row in tqdm(json_data):
            posts = "|||".join([pair['post'] for pair in row['pairs']])
            questions = "|||".join([pair['question'] for pair in row['pairs']])
            labels = [row['pairs'][0]['label0'], row['pairs'][0]['label1'], row['pairs'][0]['label2'], row['pairs'][0]['label3']]

            writer.writerow([posts, questions] + labels)

data = get_json_list("/home/wenkail/anlp_final/src/data/selected_questions_pairs_max_length_3000.json")[0]
file_path = '/home/wenkail/anlp_final/src/data/kaggleWithQuestionSelected_3000.csv'
write_json_to_csv(data, file_path)