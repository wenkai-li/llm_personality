python3 run_psychobench.py \
    --model llama3_70b \
    --model_mode direct \
    --model_path /compute/babel-8-11/jiaruil5/.cache/models--TechxGenus--Meta-Llama-3-70B-Instruct-GPTQ/snapshots/e147aa8799dd05d5077f60c79be0d972b002b3ac/ \
    --questionnaire BFI \
    --shuffle-count 10 \
    --test-count 1 \
    --name-exp direct_debug