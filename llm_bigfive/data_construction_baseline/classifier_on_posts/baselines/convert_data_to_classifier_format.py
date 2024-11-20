import json
import pandas as pd


# if __name__ == "__main__":
#     df = pd.read_csv("/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/classifier_on_posts/baselines/human_eval_new_full.csv")
#     df['ope_z_label'] = 2
#     df['con_z_label'] = 2
#     df['ext_z_label'] = 2
#     df['agr_z_label'] = 2
#     df['neu_z_label'] = 2
#     df.rename(inplace=True, columns={"expert": "message"})
#     df.loc[(df['trait'] == 'o') & (df['level'] == 'high'), 'ope_z_label'] = 0
#     df.loc[(df['trait'] == 'o') & (df['level'] == 'low'), 'ope_z_label'] = 1
#     df.loc[(df['trait'] == 'c') & (df['level'] == 'high'), 'con_z_label'] = 0
#     df.loc[(df['trait'] == 'c') & (df['level'] == 'low'), 'con_z_label'] = 1
#     df.loc[(df['trait'] == 'e') & (df['level'] == 'high'), 'ext_z_label'] = 0
#     df.loc[(df['trait'] == 'e') & (df['level'] == 'low'), 'ext_z_label'] = 1
#     df.loc[(df['trait'] == 'a') & (df['level'] == 'high'), 'agr_z_label'] = 0
#     df.loc[(df['trait'] == 'a') & (df['level'] == 'low'), 'agr_z_label'] = 1
#     df.loc[(df['trait'] == 'n') & (df['level'] == 'high'), 'neu_z_label'] = 0
#     df.loc[(df['trait'] == 'n') & (df['level'] == 'low'), 'neu_z_label'] = 1
#     for trait in ['o', 'c', 'e', 'a', 'n']:
#         tmp_df = df.loc[df['trait'] == trait]
#         tmp_df.to_csv(f"/home/jiaruil5/personality/llm_personality/llm_bigfive/classifier/results_baselines_new_expert/generator_predictions_{trait}.csv")


if __name__ == "__main__":
    df = pd.read_csv("/home/jiaruil5/personality/llm_personality/llm_bigfive/data_construction_baseline/classifier_on_posts/baselines/human_eval_big5_chat_200.csv")
    df['ope_z_label'] = 2
    df['con_z_label'] = 2
    df['ext_z_label'] = 2
    df['agr_z_label'] = 2
    df['neu_z_label'] = 2
    df.rename(inplace=True, columns={"response_llama3_70b": "message"})
    df.loc[(df['trait'] == 'o') & (df['level'] == 'high'), 'ope_z_label'] = 0
    df.loc[(df['trait'] == 'o') & (df['level'] == 'low'), 'ope_z_label'] = 1
    df.loc[(df['trait'] == 'c') & (df['level'] == 'high'), 'con_z_label'] = 0
    df.loc[(df['trait'] == 'c') & (df['level'] == 'low'), 'con_z_label'] = 1
    df.loc[(df['trait'] == 'e') & (df['level'] == 'high'), 'ext_z_label'] = 0
    df.loc[(df['trait'] == 'e') & (df['level'] == 'low'), 'ext_z_label'] = 1
    df.loc[(df['trait'] == 'a') & (df['level'] == 'high'), 'agr_z_label'] = 0
    df.loc[(df['trait'] == 'a') & (df['level'] == 'low'), 'agr_z_label'] = 1
    df.loc[(df['trait'] == 'n') & (df['level'] == 'high'), 'neu_z_label'] = 0
    df.loc[(df['trait'] == 'n') & (df['level'] == 'low'), 'neu_z_label'] = 1
    for trait in ['o', 'c', 'e', 'a', 'n']:
        tmp_df = df.loc[df['trait'] == trait]
        tmp_df.to_csv(f"/home/jiaruil5/personality/llm_personality/llm_bigfive/classifier/results_baselines_big5chat_baseline/generator_predictions_{trait}.csv")