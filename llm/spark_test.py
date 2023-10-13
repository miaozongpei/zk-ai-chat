from llm.spark_llm import Spark
import config

llm = Spark(version=1)
# data =json.dumps(llm._construct_query(prompt="你好啊", temperature=llm.temperature, max_tokens=llm.max_tokens))
# print (data)
# print (type(data))
result = llm("你好啊")
print(result)