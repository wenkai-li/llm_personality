# bash run_llama3_70b_tgi.sh > logs/stdout_llama3_70b_tgi.txt 2> logs/stderr_llama3_70b_tgi.txt

MODEL_DIR="/scratch/jiaruil5/.cache/models--meta-llama--Meta-Llama-3-70B-Instruct/snapshots/7129260dd854a80eb10ace5f61c20324b472b31c/"

text-generation-launcher --model-id $MODEL_DIR --port 9570 --max-input-length 4096 --max-total-tokens 8192