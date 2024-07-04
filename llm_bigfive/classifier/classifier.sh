
source ~/.bashrc
conda activate llm_persona

# python -m torch.distributed.launch --nproc_per_node=5 roberta_classifier.py
CUDA_VISIBLE_DEVICES=0,1,2 python roberta_classifier.py

# python classifier_inference.py 