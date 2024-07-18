<!-- Running on Dexpert -->
python run_psychobench.py \
  --model dexpert \
  --questionnaire BFI \
  --shuffle-count 0 \
  --test-count 2 \
  --name-exp dexpert_exp11112

<!-- Analysis on Dexpert -->
python run_psychobench.py \
  --model dexpert \
  --questionnaire BFI \
  --mode analysis \
  --name-exp dexpert_exp \
  --shuffle-count 0 \
  --test-count 2

<!-- Running on GPT -->
python run_psychobench.py \
  --model gpt-3.5-turbo \
  --questionnaire BFI \
  --openai-key "sk-proj-2BSJmj1uXhdGAbCfKMNlT3BlbkFJn6lprtjDaD1bKd30VJfj" \
  --shuffle-count 0 \
  --test-count 2

<!-- Running on LLama3-70b -->
python run_psychobench.py \
  --model llama3-70b \
  --questionnaire BFI \
  --shuffle-count 0 \
  --test-count 2


  <!-- 11111 -->
  <!-- eg. [0,2] 1111 -->