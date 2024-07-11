<!-- Running on Dexpert -->
python run_psychobench.py \
  --model dexpert \
  --questionnaire BFI \
  --shuffle-count 0 \
  --test-count 1 \
  --name-exp dexpert_exp

<!-- Analysis on Dexpert -->
python run_psychobench.py \
  --model dexpert \
  --questionnaire BFI \
  --mode analysis \
  --name-exp dexpert_exp \
  --shuffle-count 0 \
  --test-count 1

<!-- Running on GPT -->
python run_psychobench.py \
  --model gpt-3.5-turbo \
  --questionnaire BFI \
  --openai-key "sk-proj-2BSJmj1uXhdGAbCfKMNlT3BlbkFJn6lprtjDaD1bKd30VJfj" \
  --shuffle-count 0 \
  --test-count 1