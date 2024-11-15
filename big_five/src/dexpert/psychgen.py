# import libraries
import argparse
import logging
import os
import random
import numpy as np
import torch
import pandas as pd
import time

from psychgen import PSYCHGEN
from peft import PeftModel

logger = logging.getLogger(__name__)


"""====================== METHODS DEFINITIONS ======================"""

def set_seed(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.n_gpu > 0:
        torch.cuda.manual_seed_all(args.seed)

def run_inference(model, args, device):
    
    # retrieve embeddings
    data_df = pd.read_csv(args.train_data_file, header = 0, index_col = 0)
    training_sentences_embeddings = data_df.iloc[:,1:].values

    # generate texts with input is psychological dimensions scores vector
    # for each dimenion, travel along the dimension range to generate text, while keep other dimensions as mean values (e.g. 0.0s)
    # examples of input:  [0,0,-2.std,0,0], [0,0,-1.std,0,0], [0,0,0,0,0], [0,0,+1.std,0,0], [0,0,+2.std,0,0]
    # the mean and std values for each dimenion will be retrieved from the training data files

    dimensions_name = data_df.columns[1:]
    if args.psych_variables == "big5":
        dimension_personality_dict = {"ope_z": "Openness", "con_z": "Conscientiousness", "ext_z": "Extroversion", "agr_z": "Agreeableness", "neu_z": "Neuroticism"}
    elif args.psych_variables == "dep":
        dimension_personality_dict = {"dep_score": "Depression"}
    elif args.psych_variables == "swl":
        dimension_personality_dict = {"swl": "Life-satisfaction"}
    else:
        assert False, "Currently, --psych_variables switch only supports: big5, dep, swl."
    dimensions_name = [dimension_personality_dict[item] for item in dimensions_name]
    means = np.mean(training_sentences_embeddings, axis = 0)
    stds = np.std(training_sentences_embeddings, axis = 0)


    # set parameters
    explore_std_range = [-args.std_range, args.std_range + 0.01]
    std_step_interval = args.generate_interval


    # generate text for each hidden dimension
    hidden_size = means.shape[0]
    for i in range(hidden_size):
    
        # print banner
        banner = "DIMENSION NUMBER {} ({}) : ".format(str(i), dimensions_name[i])
        print("="*len(banner))
        print(banner)   
        print("="*len(banner))

        # traveling std range and generating text
        for std_position in np.arange(explore_std_range[0], explore_std_range[1], std_step_interval):
        
            print("Sampling text at position Mean + ({})*Std:".format(round(std_position,2)))
            generated_samples = []   # avoid repeated generated_sample
            for _ in range(args.generate_num):     
                
                # sample embedding around embedding + std_position*stds[i]
                embedding_sample = np.copy(means)
                embedding_sample[i] = embedding_sample[i] + std_position*stds[i]

                # transform to tensor
                embedding_sample = torch.tensor(embedding_sample, device = device).float().unsqueeze(0)

                # generate sentence
                # caveat: when generating, remove duplicated generation by checking newly generated text with already generated set
                generated_count = 0    
                while True:
                    generated_sample, decoder_attentions_sample = model.inference(prompting_text = args.prompting_text, sentence_embedding = embedding_sample, args = args, device = device)
                    generated_sample =  model.tokenizer.decode(generated_sample[0].tolist(), clean_up_tokenization_spaces=True)
                    generated_count += 1
                    first_endoftext = generated_sample.find("<eos>") 
                    generated_sample_clean = generated_sample[:(first_endoftext + len("<eos>")) if first_endoftext>0 else len(generated_sample)]
                    generated_sample_clean = generated_sample_clean.replace("<bos>","<bos> ").replace("<eos>"," <eos>")
                    if (generated_sample_clean not in generated_samples) or generated_count >= 10:
                        generated_samples.append(generated_sample_clean)
                        break
                    
                # print generated sentence sample
                print("  ", generated_sample_clean)
            print("\n")

class Args:
    train_data_file = "/home/jiaruil5/personality/llm_personality/psychgenerator_opensource/data/big5_training_data.csv"
    output_dir = "/home/jiaruil5/personality/llm_personality/psychgenerator_opensource/checkpoints/big5_model"
    model_name_or_path = "google/gemma-2b"
    checkpoint_step = 30000
    psych_variables = "big5"
    latent_size = 5
    do_lower_case = False
    generate_num = 1
    generate_length = 256
    temperature = 0
    top_k = 10
    top_p = 0.9
    std_range = 3.0
    generate_interval = 3.0
    seed = 45
    prompting_text = "I like to"
    no_cuda = False
    from_checkpoint = False

class PsychGen():
    def __init__(self):
        self.args = Args
        device = torch.device("cuda" if torch.cuda.is_available() and not self.args.no_cuda else "cpu")    # CHECK! make sure we use all 3 GPUs
        self.args.n_gpu = torch.cuda.device_count()
        self.args.device = device
        # Setup logging
        logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                            datefmt = '%m/%d/%Y %H:%M:%S',
                            level = logging.INFO)
        # Set seed
        set_seed(self.args)
        
        
        # Building model
        model = PSYCHGEN(self.args.model_name_or_path, self.args.latent_size)
        
        # Load from checkpoint model
        output_dir_basemodel = os.path.join(self.args.output_dir, 'base_model')
        output_dir_currentstep = os.path.join(args.output_dir, 'checkpoint-{}'.format(args.checkpoint_step))
        # Load base model
        model.from_checkpoint(args, output_dir_basemodel)
        # Load peft
        peft_model_id = output_dir_currentstep
        model = PeftModel.from_pretrained(model, peft_model_id)

        # Send model to GPU
        model.to(args.device)    
        model.eval()

        # Logging info
        logger.info("Inference parameters %s", args)
        
        # Check model size on memory
        mem_params = sum([param.nelement()*param.element_size() for param in model.parameters()])
        mem_bufs = sum([buf.nelement()*buf.element_size() for buf in model.buffers()])
        mem = mem_params + mem_bufs # in bytes
        print("Memory usage: {}MB".format(mem//(1024**2)))

        # Testing inference
        args.model_config = model.model_config
        
"""====================== MAIN FUNCTION ======================"""

# main function
def main():

    # =========== bulilding model and inferencing  =========== #
    
    
    run_inference(model, args, device)    
    
if __name__ == "__main__":
    main()