import pandas as pd


def read_csv_return_txt_unique(csv_path, txt_path):

    df = pd.read_csv(csv_path,encoding='gbk')


    col2 = set(df.iloc[:, 1])
    with open(txt_path, 'w',encoding='utf-8') as f:
        for text in col2:
            f.write(text + '\n')


read_csv_return_txt_unique('data/out/openai_gpt3_output.csv', 'entity.txt')

