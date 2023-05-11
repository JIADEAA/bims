import openai
import pandas as pd
import tqdm

openai.api_key = 'xxxx'
input_file_path = 'data/results/GB51348-2019 民用建筑电气设计标准.csv'
output_file_path = 'data/out/openai_gpt3_output.csv'
import re
import csv

chunksize = 800

def extract_entities(text):
    try:
        pre = "请对文本\""
        suffix = "\"进行知识抽取，返回三元组\n三元组保持格式对齐。"
        suffix2 = "\n例如文本：变电所设计和电气设备的安装应采取抗震措施，并应符合现行国家标准《电力设施抗震设计规范》GB50260的规定\n返回：(变电所设计和电气设备的安装, 应采取, 抗震措施)\n(变电所设计和电气设备的安装, 应符合, 国家标准《电力设施抗震设计规范》GB50260的规定)"
        prompt = pre + third_column[i] + suffix + suffix2
        response = openai.Completion.create(
            model='davinci:ft-personal:kgqa-2023-05-01-13-10-46',
            prompt=prompt,
            temperature=0.5,
            max_tokens=300,
            top_p=1,
            n=1,
            echo=False,)

        result = response.choices[0].text
    except KeyError:
        print("Error: 'choices' key not found in response. Retrying...")
        return extract_entities(text)
    return result

for chunk in pd.read_csv(filepath_or_buffer=input_file_path, encoding='gbk', skiprows=2345, chunksize=chunksize):
    third_column = []
    second_column = []
    for index, row in chunk.iterrows():
        if re.match(r'^[3-9]\d*|^[1-9]\d{1,}', row[1]):
            third_column.append(row[2])
            second_column.append(row[1])


    length = len(third_column)

    for i in tqdm.tqdm(range(length)):
        result = extract_entities(i)
        try:
            for line in result.split('\n'):
                if line:
                    with open(output_file_path, mode='a+', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        s, p, o = line.strip("()").split(', ')
                        writer.writerow([second_column[i], s, p, o])
                        csvfile.close()

        except ValueError:
            print('{}出现错误'.second_column[i])

