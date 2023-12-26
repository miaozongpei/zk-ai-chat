import uvicorn
from fastapi import FastAPI
from answer.chatgpt_answer import answer_bydoc,answer_bybase
import random

app = FastAPI()

@app.get("/ask_ai/{question}")
async def ask(question: str):
    replay = answer_bybase(question)
    return {"message": replay}

@app.get("/ask_doc/{docs}/{question}")
async def ask(docs: str, question: str):
    if q_black_list(question):
        return {"message": "抱歉，小邮，没办法回复你这个问题"}


    replay = answer_bydoc(docs, question)
    if replay.find("don't") != -1 or replay.find("对不起") != -1 or replay.find("无法回答") != -1 or replay.find(
            "不知道") != -1 or replay.find("不清楚") != -1 or replay.find("不太明白") != -1 or replay.find("抱歉") != -1:
        ai_replay = answer_bybase(question+"，回答请不要超过"+str(random.randint(100, 200))+"字")
        replay = str(ai_replay)


    with open("./answer/black_list.txt", "r", encoding='utf-8') as f:
        keywords = f.read().split(",")
        for keyword in keywords:
            if keyword and (keyword in replay):
                replay = "抱歉，小邮，没办法回复你这个问题"
                break  # 匹配到关键字就退出循环
    return {"message": replay}
def q_black_list(question):
    with open("answer/question_black_list.txt", "r", encoding='utf-8') as f:
        keywords = f.read().split(",")
        for keyword in keywords:
            if keyword and (keyword in question):
                return True
    return False

def ai_black_list(question):
    with open("answer/ai_black_list.txt", "r", encoding='utf-8') as f:
        keywords = f.read().split(",")
        for keyword in keywords:
            if keyword and (keyword in question):
                return True
    return False
@app.get("/ask/{docs}/{question}")
async def ask(docs: str, question: str):
    replay = answer_bydoc(docs, question)
    if replay.find("don't") != -1 or replay.find("对不起") != -1 or replay.find("无法回答") != -1 or replay.find("不知道") != -1 or replay.find("不清楚") != -1 or replay.find("不太明白") != -1:
        replay = answer_bybase(question)
    return {"message": replay}

@app.get("/blacklist/{keyword}")
async def blacklist(keyword: str):
    with open("./answer/black_list.txt", "a", encoding='utf-8') as f:
        f.write(keyword+",")
    return {"message": "ok"}

@app.get("/blacklist")
async def blacklist():
    with open("./answer/black_list.txt", "r", encoding='utf-8') as f:
        data = f.read()
    return {"blacklist": data}

if __name__ == "__main__":
    # 修改端口号为8000
    uvicorn.run(app, host="0.0.0.0", port=5555)