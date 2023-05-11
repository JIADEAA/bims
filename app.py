from flask import Flask,json, render_template, jsonify,request
from query_neo4j import cut,query_neo
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

data = []

@app.route('/query',methods=["POST"])
def query():
    sentence = request.json.get("sentence")
    # 创建Neo4j数据库驱动程序

    word,pre = cut(sentence)
    if pre < 0.1:
        result = {
            "code": 500,
            "msg": "对不起，知识库暂未收录该内容"
        }
        return json.dumps(result)
    else:
        output = query_neo(word)
        result = {
            "code": 200,
            "msg": output
        }
        json_output = json.dumps(result, ensure_ascii=False, indent=2)
        return json_output

if __name__ == '__main__':
    app.run()
