
import streamlit as st #网站创建

# App framework
# 如何创建自己的网页机器人
st.title('😬牙医帮帮我😬') #用streamlit app创建一个标题
# 创建一个输入栏可以让用户去输入问题
query = st.text_input('欢迎来到AI牙科诊所,你可以问我关于牙科的问题，例如：洗一次牙多少钱？')

my_bar = st.progress(0, text='等待投喂问题哦')

