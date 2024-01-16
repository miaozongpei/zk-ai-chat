from answer.chatgpt_answer import answer_bydoc
from answer.chatgpt_answer import question_derive


replay = question_derive("你好")
print(replay)
replay = answer_bydoc("youle2","新准入经代需要符合哪些资格")
print(replay)
replay = answer_bydoc("my_doc4","请介绍下邮政集团公司")
print(replay)







