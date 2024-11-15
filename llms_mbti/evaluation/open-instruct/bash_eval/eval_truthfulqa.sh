source ~/.bashrc
conda activate llm_personality
cd ~/llm_personality/llms_mbti/evaluation/open-instruct/bash_eval


python -m eval.truthfulqa.run_eval \
    --data_dir data/eval/truthfulqa \
    --save_dir results/trutufulqa/llama2-7B \
    --model_name_or_path ../hf_llama2_models/7B \
    --tokenizer_name_or_path ../hf_llama2_models/7B \
    --metrics truth info mc \
    --preset qa \
    --hf_truth_model_name_or_path allenai/truthfulqa-truth-judge-llama2-7B \
    --hf_info_model_name_or_path allenai/truthfulqa-info-judge-llama2-7B \
    --eval_batch_size 20 
    # --load_in_8bit