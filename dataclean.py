import re
from win32com.client import Dispatch, DispatchEx
import pandas as pd
import os
import tqdm

# path = r'E:\konwledgegrapes\规范数据集\JGJ333-2014 会展建筑电气设计规范.rtf'  # 写绝对路径，相对路径会报错
basepath = r'E:\py-repositories\kgqa\data\rawdata'

file_name_list = os.listdir(basepath)
for i in tqdm.tqdm(file_name_list):
    try:
        print(i)
        word = Dispatch('Word.Application')  # 打开word应用程序

        # word = DispatchEx('Word.Application')  # 启动独立的进程

        word.Visible = 0  # 后台运行,不显示

        word.DisplayAlerts = 0  # 不警告
        doc = word.Documents.Open(FileName=os.path.join(basepath, i), Encoding='gbk')
        content = ""

        for para in doc.paragraphs:
            content += str(para.Range.Text)
        doc.Close()
        word.Quit()
        print(len(content))


        def cutting(content):
            pre1 = re.sub(pattern=" ", string=content, repl="")
            pre = re.sub(pattern="\r", string=pre1, repl="")
            result = re.split('((?<!表|第|、|）|.)(?<!\d)\d{1,2}\.\d{1,2}\.\d{1,2})', pre)
            result = re.split('((?<!表|第|、)(?<!\d)\d{1,2}\.\d{1,2}\.\d{1,2})', pre)
            return result


        result = cutting(content)
        result = [i for i in result if i != '']

        # print(result)

        n = 1
        total = {"文件信息": result[0]}
        for j in result:
            if result[n] in list(total.keys()):
                total[result[n]]
                total[result[n]] = total[result[n]] + result[n + 1]
            else:
                total[result[n]] = result[n + 1]
            if n < len(result) - 3:
                n += 2
            else:
                break

        ##条目内容分离
        node = []  # 内容
        flag = []  # 条目
        for k, v in total.items():
            node.append(v)
            flag.append(k)
        df_data = pd.DataFrame({'flag': flag, 'node': node})

        df_data.to_csv(r'E:\py-repositories\kgqa\data\results' + '\\' + i.replace('.rtf', '') + '.csv')
        dict_node = []  ##字典内容
        dict_flag = []  ##字典条目
        for j in flag:
            if re.search('^2', j) != None:
                dict_flag.append(j)

        for j in dict_flag:
            dict_node.append(total[j])

        F = open(r'.\node\node_' + i.replace('.rtf', '') + ".txt", 'w+', encoding='utf-8')
        for j in node:
            F.write(str(j) + '\n')
        F.close()

        dict = []  ##字典
        for j in dict_node:
            match = re.match(r'^[\u4e00-\u9fa5]+', j)
            if match != None:
                dict.append(match.group())

        F = open(r'.\dict\dict_' + i.replace('.rtf', '') + ".txt", 'w+', encoding='utf-8')
        for i in dict:
            F.write(str(i) + '\n')
        F.close()
    except Exception as e:
        pass
    continue

