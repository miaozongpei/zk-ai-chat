import uvicorn
from fastapi import FastAPI
from answer.chatgpt_answer import answer_bydoc,answer_bybase

app = FastAPI()

@app.get("/ask_ai/{question}")
async def ask(question: str):
    replay = answer_bybase(question)
    return {"message": replay}

@app.get("/ask_doc/{docs}/{question}")
async def ask(docs: str, question: str):
    replay = answer_bydoc(docs, question)
    return {"message": replay}

@app.get("/ask/{docs}/{question}")
async def ask(docs: str, question: str):
    replay = answer_bydoc(docs, question)
    if replay.find("don't") != -1 or replay.find("对不起") != -1 or replay.find("无法回答") != -1 or replay.find("不知道") != -1 or replay.find("不清楚") != -1:
        replay = answer_bybase(question)
    return {"message": replay}



if __name__ == "__main__":
    # 修改端口号为8000
    uvicorn.run(app, host="0.0.0.0", port=5555)