
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

def sentence_embedding(data):
    pair_embeddings = []
    posts = data['posts']
    questions = data['questions']
    pairs = []
        
    # Filiter out the empty posts
    # for i in data:
    #     i['posts'] = [s for s in i['posts'] if s.strip()]
    if len(posts) != len(questions):
        raise ValueError("posts and questions should have a same length")
    
    for i in range(len(questions)):
        if posts[i].strip() == "":
            continue
        pair = posts[i] + questions[i]
        pairs.append(pair)
        pair_embedding = model.encode(pair)
        pair_embeddings.append(pair_embedding.tolist())  
         
    return pair_embeddings, pairs

def write_embedding_to_json(pair_embeddings, pairs, file_name):
    if len(pair_embeddings) != len(pairs):
        raise ValueError("embeddings and posts should have a same length")
    print(pair_embeddings)
    data_to_write = {"pair_embeddings": pair_embeddings, "pair": pairs}
    with open(file_name, 'w') as file:
        json.dump(data_to_write, file)
        
data = preprocess.KaggleDatasetWithQuestion("data/kaggleWithQuestion.csv").poster_data[25]
pair_embeddings, pairs = sentence_embedding(data)
write_embedding_to_json(pair_embeddings, pairs, "data/embedding/embedding25.json")
        
