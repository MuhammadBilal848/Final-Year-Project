import os
from constants import openai_key
from langchain.llms import OpenAI
import streamlit as st
from langchain import PromptTemplate
from langchain.chains import LLMChain

os.environ['OPENAI_API_KEY'] = openai_key
llm = OpenAI(temperature=0.8)

# st.title('Search Interview Fields')
st.markdown(
    f"<h1 style='text-align: center;'>Search Interview Fields</h1>",
    unsafe_allow_html=True
)

first_question = PromptTemplate(
    input_variables = ['skill_name'] ,
    template = 'Generate 3 difficult questions about {skill_name} skill')

# first_answer = PromptTemplate(
#     input_variables = ['skill_name'] ,
#     template = 'Generate 3 difficult questions about {skill_name} skill')


# OPENAI LLMS
# tempratture param controls how balance the reponse should be
chain = LLMChain(llm=llm , prompt=first_question,verbose=True) 

qs = chain.run('tensorflow')
qs = qs.strip().split('\n')

input_text = st.text_input('Write your answer here')

for a in qs:
    print(a)
    st.write(a)
    if input_text:
        st.write(input_text)
        

# if input_text:
#     st.write(chain.run(input_text))



# qs = chain.run('tensorflow')
# my_list = qs.strip().split('\n')
# print(my_list)

