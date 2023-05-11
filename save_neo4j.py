import pandas as pd
from neo4j import GraphDatabase, basic_auth
import math
import csv
# 配置Neo4j数据库连接
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "123456"
driver = GraphDatabase.driver(neo4j_uri, auth=basic_auth(neo4j_user, neo4j_password))

input_csv = "data/out/openai_gpt3.csv"
chunksize = 1000  # 调整这个值以适应您的内存限制

# 分块读取CSV文件
reader = pd.read_csv(input_csv, header=None,quoting=csv.QUOTE_NONE, chunksize=chunksize,error_bad_lines=False)
def store_data_in_neo4j(tx, data):
    for row in data:
        # 处理 NaN 值
        entity1 = row[1] if not pd.isna(row[1]) else None
        entity2 = row[3] if not pd.isna(row[3]) else None

        # 确认实体名称不为空
        if entity1 is not None and entity2 is not None:
            tx.run("""
                MERGE (a:Entity {name: $entity1})
                MERGE (b:Entity {name: $entity2})
                MERGE (a)-[r:Relation {id: $id}]->(b)
                SET r.type = $relation
            """, id=row[0], entity1=entity1, relation=row[2], entity2=entity2)

# 处理每个数据块
for chunk in reader:
    data = chunk.values.tolist()
    with driver.session() as session:
        session.write_transaction(store_data_in_neo4j, data)

# 关闭数据库驱动程序
driver.close()