from langchain.vectorstores import Milvus
from langchain.chains.retrieval_qa.base import RetrievalQA
from typing import Any
from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate, FAISS
from langchain.schema import Document


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
    Use the following context (delimited by <ctx></ctx>) and the chat history (delimited by <hs></hs>) to answer the question:{question}
    ，If you don't know, please answer:'抱歉，从我目前的知识体系中，并没有找准确答案。'
    ------
    <ctx>
    {context}
    </ctx>
    ------
    <hs>
    {history}
    你好
        欢迎您参观邮乐公司总部，请问领导嘉宾，您有什么需要了解的吗
    你叫什么
        我是邮乐AI数字人，我叫小邮，您可以问我关于邮政集团还有邮乐公司的介绍哦
    </hs>
    ------
    Answer in Chinese，The answer cannot exceed 200:
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

def query_doc(collection_name, question):
    vector_db = Milvus(
        embedding_function=embeddings,
        connection_args={"host": config.Milvus_host, "port": config.Milvus_port},
        collection_name=collection_name,
    )
    retriever = vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(question)
    return docs

def add_doc(collection_name, question,content):
    vector_db = Milvus(
        embedding_function=embeddings,
        connection_args={"host": config.Milvus_host, "port": config.Milvus_port},
        collection_name=collection_name,
    )
    doc = Document(page_content=question+" "+content,
                   metadata={"source": question})
    docs=[]
    docs.append(doc)
    vector_db.add_documents(docs)


#eplay=answer("my_doc1","你们周六上班吗" )
#replay=answer("my_doc1","我周六可以去吗" )
#print(replay)

#replay=answer("my_doc1","你好" )
#print(replay)