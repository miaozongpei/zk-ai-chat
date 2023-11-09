from langchain.vectorstores import Milvus
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.retrieval_qa.base import RetrievalQA
from typing import Any
from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate, FAISS

from embedding.xinghuo_embedding import XhEmbeddings
from llm.spark_llm import Spark
import config

#embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
#llm = ChatOpenAI(openai_api_key=config.OPENAI_API_KEY, temperature=0, model_name="gpt-3.5-turbo-16k")

embeddings =XhEmbeddings(appid=config.embedding_xh_appid,
                       api_key=config.embedding_xh_api_key,
                       api_secret=config.embedding_xh_api_secret,
                       embedding_url=config.embedding_xh_embedding_url
                       )
llm = Spark(version=3)
def get_vector_chain(collection_name) -> Any:
    Spark(version=3)
    template = """
    Use the following context (delimited by <ctx></ctx>) and the chat history (delimited by <hs></hs>) to answer the question:
    ------
    <ctx>
    {context}
    </ctx>
    ------
    <hs>
    {history}
    </hs>
    ------
    {question}？
    
    Answer in Chinese:
    """

    #Answer in the language in which the question was asked:

    prompt = PromptTemplate(
        input_variables=["history", "context", "question"],
        template=template,
    )

    vector_db = Milvus(
        embedding_function=embeddings,
        connection_args={"host": config.Milvus_host, "port": config.Milvus_port},
        collection_name=collection_name,
    )
    chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 3}),
        chain_type="stuff",
        chain_type_kwargs={
            "prompt": prompt,
            "memory": ConversationBufferMemory(
                memory_key="history",
                input_key="question"),
        },
    )
    return chain

def answer_bydoc(collection_name, question):
    chain = get_vector_chain(collection_name)
    return chain.run(question)

def answer_bybase(question):
    result = llm(question)
    return result

#eplay=answer("my_doc1","你们周六上班吗" )
#replay=answer("my_doc1","我周六可以去吗" )
#print(replay)

#replay=answer("my_doc1","你好" )
#print(replay)