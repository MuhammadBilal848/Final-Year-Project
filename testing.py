import os
from langchain.llms import OpenAI
import streamlit as st
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory


os.environ['OPENAI_API_KEY'] = 'LMAO'
llm = OpenAI(temperature=0.8)

# st.title('Search Interview Fields')
st.markdown(
    f"<h1 style='text-align: center;'>Search Interview Fields</h1>",
    unsafe_allow_html=True
)

first_question = PromptTemplate(
    input_variables = ['skill_qs'] ,
    template = 'Generate a difficult questions about {skill_qs} skill')

# OPENAI LLMS
# tempratture param controls how balance the reponse should be
question = LLMChain(llm=llm , prompt=first_question,verbose=True) 

qs = question.run('Artificial Neural Network')
# qs = qs.strip().split('\n')



first_answer = PromptTemplate(
    input_variables = ['skill_ans'] ,
    template = 'Check if {skill_ans} is correct and return a percentage of how correct this answer is')

answer = LLMChain(llm=llm , prompt=first_answer,verbose=True) 


st.write(qs)
input_text = st.text_input('Write your answer here')

if input_text:
    st.write(answer.run(input_text))

# for a in qs:
#     print(a)
#     st.write(a)
#     input_text = st.text_input('Write your answer here')
#     st.write(answer.run(input_text))
#     # if input_text:
        

