import sys
import json
import os
import argparse
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
sys.path.append('../')
from data_processing import preprocess
from sentence_transformers.util import cos_sim
from transformers import AutoTokenizer


model = SentenceTransformer("jinaai/jina-embedding-s-en-v1")

<<<<<<< HEAD
def sentence_embedding(data , key='questions'):
    embeddings = []
    questions = []
    posts = []
    labels0 = []
    labels1 = []
    labels2 = []
    labels3 = []
    
    # Filiter out the empty questions
    # for i in data:
        # i[key] = [s for s in i[key] if s.strip()]
    
    for i in data:
        posts.append(i['posts'])
        questions.append(i[key])
        embedding = model.encode(i[key])
        embeddings.append(embedding)
        labels0.append(i['label0'])
        labels1.append(i['label1'])
        labels2.append(i['label2'])
        labels3.append(i['label3'])
        
    return embeddings, questions, posts, labels0, labels1, labels2, labels3

def write_embedding_to_json(embeddings, posts, file_name):
    if len(embeddings) != len(posts):
=======
def sentence_embedding(data):
    pair_embeddings = []
    posts = []
    questions = []
    # Filiter out the empty posts
    # for i in data:
    #     i['posts'] = [s for s in i['posts'] if s.strip()]
        
    for i in data:
        pair = i['posts'] + i['questions']
        posts.append(i['posts'])
        questions.append(i['questions'])
        pair_embedding = model.encode(pair)
        pair_embeddings.append(pair_embedding)     
         
    return pair_embeddings, posts, questions  

def write_embedding_to_json(pair_embeddings, posts, questions, file_name):
    if len(pair_embeddings) != len(posts):
>>>>>>> test
        raise ValueError("embeddings and posts should have a same length")
    data_to_write = [{"index": i, "pair_embeddings": embedding.tolist(), "posts": post, "questions": question} for i, (embedding, post, question) in enumerate(zip(pair_embeddings, posts, questions))]
    with open(file_name, 'w') as file:
        json.dump(data_to_write, file)
        

def get_json_list(file_path, start_at=0, end_at=None):
    with open(file_path, "r") as f:
        json_list = []
        for idx, line in enumerate(f):
            if end_at is not None and idx >= end_at:
                return json_list
            elif idx < start_at:
                continue
            json_list.append(json.loads(line))
        return json_list
    
def get_similar_embeddings_list(embeddings):
    similarity_pairs = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            similarity = cos_sim(embeddings[i], embeddings[j]).item()
            similarity_pairs.append(((i, j), similarity))

    similarity_pairs.sort(key=lambda x: x[1])

    return similarity_pairs

def select_least_pair(data, max_tokens):
    tokenizer = AutoTokenizer.from_pretrained("/data/datasets/models/huggingface/meta-llama/Llama-2-70b-chat-hf")
    similarity_pairs = get_similar_embeddings_list(data['embeddings'])

    # Initialize selected_posts and a set for storing indices of selected posts
    selected_posts = []
    selected_indices = set()
    total_length = 0

    # Iterate over similarity pairs
    for (idx1, idx2), similarity in similarity_pairs:
        if total_length >= max_tokens:
            break

        post1 = data["posts"][idx1]
        question1 = data['questions'][idx1]
        post2 = data["posts"][idx2]
        question2 = data['questions'][idx2]

        # Calculate the length of post1 and question1
        length_1 = len(tokenizer.tokenize(post1) + tokenizer.tokenize(question1))

        # Check if idx1 is not in selected_indices and length constraints are met
        if idx1 not in selected_indices and total_length + length_1 <= max_tokens:
            selected_posts.append({"index": idx1, "post": post1, "question": question1, "label0": data['label0'], "label1": data['label1'], "label2": data['label2'], "label3": data['label3'], "similarity": similarity})
            total_length += length_1
            selected_indices.add(idx1)  # Add index to the set

        # Calculate the length of post2 and question2
        length_2 = len(tokenizer.tokenize(post2) + tokenizer.tokenize(question2))

        # Check if idx2 is not in selected_indices and length constraints are met
        if idx2 not in selected_indices and total_length + length_2 <= max_tokens:
            selected_posts.append({"index": idx2, "post": post2, "question": question2, "label0": data['label0'], "label1": data['label1'], "label2": data['label2'], "label3": data['label3'], "similarity": similarity})
            total_length += length_2
            selected_indices.add(idx2)  # Add index to the set

    return selected_posts, total_length

def get_total_length(data):
    tokenizer = AutoTokenizer.from_pretrained("/data/datasets/models/huggingface/meta-llama/Llama-2-70b-chat-hf")
    total_length = 0
    for post in data['posts']:
        total_length += len(tokenizer.tokenize(post))
    return total_length

def write_selected_to_json(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file)

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default="Kaggle", help="Kaggle or Essay")
    parser.add_argument("--embedding_path", type=str, default=None, help="Path to the embedding file")
    parser.add_argument("--max_tokens", type=int, default=3000, help="Max number of tokens to select")
    parser.add_argument("--selected_output_path", type=str, help="Path to the selected sentences output file")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = arg_parse()
    if args.data == "Kaggle":
        data = preprocess.KaggleDatasetWithQuestion('/home/wenkail/anlp_final/src/data/kaggleWithQuestion.csv').poster_data
        
    se, questions, posts, labels0, labels1, labels2, labels3 = sentence_embedding(data)
    print(len(se))
    print(len(questions))
    print(len(posts))
    if args.embedding_path is not None:
        write_embedding_to_json(se, questions, args.embedding_path)
    data = [{"index": i, "embeddings": embedding.tolist(), "questions": question, "posts": post, "label0": label0, "label1": label1, "label2": label2, "label3": label3} for i, (embedding, question, post, label0, label1, label2, label3) in enumerate(zip(se, questions, posts, labels0, labels1, labels2, labels3))]
    # print(data)
    all_original_data_length = []
    all_pairs = []
    all_data_length_after_selection = []
    combined_data = []
    for i in data:
        pairs, original_length, new_length = select_least_pair(i, max_tokens=args.max_tokens)
        all_pairs.append(pairs)
        all_original_data_length.append(original_length)
        all_data_length_after_selection.append(new_length)
    for pairs, original_length, new_length in zip(all_pairs, all_original_data_length, all_data_length_after_selection):
        combined_item = {
            "pairs": pairs
            # "original_length": original_length,
            # "new_length": new_length
        }
        combined_data.append(combined_item)
    # print(combined_data)
    write_selected_to_json(combined_data, args.selected_output_path)
    