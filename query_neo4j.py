import hanlp
from neo4j import GraphDatabase

tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
sts = hanlp.load(hanlp.pretrained.sts.STS_ELECTRA_BASE_ZH)
custom_dict = set()


def read_txt_return_dict(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            custom_dict.add(word)
    return custom_dict


tok.dict_force = None
tok.dict_combine = read_txt_return_dict('entity.txt')


def cut(sentence):
    data = list(tok(sentence))
    print(data)
    for i in data:
        if i in custom_dict:
            return i,1
    most_sts = ""
    pre = 0
    for i in data:
        for j in custom_dict:
            if sts([i, j]) > pre:
                pre = sts([i, j])
                most_sts = j
    if pre == 0:
        return 0,0
    else:
        return most_sts,pre

def query_neo(word):
    # 创建Neo4j数据库驱动程序
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "123456"))

    # 创建Cypher查询语句
    query = "MATCH (n:Entity) - [r:Relation] - (b:Entity) where n.name = '{0}' return n,r,b".format(word)

    # 使用驱动程序执行查询
    with driver.session() as session:
        result = session.run(query)

        # 处理查询结果
        output = []

        for record in result:
            # print(record)
            # print(record['r'].nodes)
            #
            # print(record['r'].nodes[0].id)
            # print(record['r'].nodes[0]['name'])
            start = {}
            end = {}
            segments = []
            relationship = {}
            start={

                    "identity": record['r'].nodes[0].id,
                    "labels": ["Entity"],
                    "properties": {
                        "name": record['r'].nodes[0]['name']
                    }
                }

            end ={
                    "identity": record['r'].nodes[1].id,
                    "labels": ["Entity"],
                    "properties": {
                        "name": record['r'].nodes[1]['name']

                }}

            relationship ={


                    "identity": record['r'].id,
                    "start": record['r'].nodes[0].id,
                    "end": record['r'].nodes[1].id,
                    "type": record['r']['type'],

                    "properties": {
                        "name": record['r']['id'],
                    }
                }
            segments.append(
                {
                    "start": start,
                    "relationship": relationship,
                    "end": end,
                }
            )

            output.append({
               "p": {
                    "start": start,
                    "end": end,
                    "segments": segments,
                    "length": 1.0
                }}
            )
    return output
