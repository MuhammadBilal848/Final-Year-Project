import os
from langchain.llms import OpenAI
import streamlit as st
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from constants import  openai_key


os.environ['OPENAI_API_KEY'] = openai_key
llm = OpenAI(temperature=0.8)

# st.title('Search Interview Fields')
st.markdown(
    f"<h1 style='text-align: center;'>Search Interview Fields</h1>",
    unsafe_allow_html=True
)

first_question = PromptTemplate(
    input_variables = ['skill_qs','experience'] ,
    template = 'Write 2 difficult questions about {skill_qs} skill for a person having {experience} years of experience')

# OPENAI LLMS
# tempratture param controls how balance the reponse should be
question = LLMChain(llm=llm , prompt=first_question,verbose=True) 

sk = ['ANN','Dockers','Scikit-learn','Sequence Models']

# input_text_qs = st.text_input('Write your answer here')

sk_exp = [('pandas',1),('tensorflow',3),('flask',2),('react.js',3),('Opencv',5)]
for skill,experience in sk_exp:
    response = question.run(skill_qs=skill, experience=experience)
    st.write(response)
    with open('questions.txt', 'a') as file:
        file.write(response)

# response = question.run(skill_qs='flask', experience=2)
# st.write(response)
# with open('questions.txt', 'a') as file:
#     file.write(response)
# qs = qs.strip().split('\n')

# first_answer = PromptTemplate(
#     input_variables = ['skill_ans'] ,
#     template = 'Check if {skill_ans} is correct and return a percentage of how correct this answer is')

# answer = LLMChain(llm=llm , prompt=first_answer,verbose=True) 


# qs_1 = ConversationBufferMemory(input_key='skill_qs',memory_key='chat_history')

# st.write(qs)
# input_text = st.text_input('Write your answer here')

# if input_text:
#     st.write(answer.run(input_text))

# if input_text_qs:
#     # with st.expander('Question'):
#         st.write(qs_1.buffer)

# print(qs_1)

# for a in qs:
#     print(a)
#     st.write(a)
#     input_text = st.text_input('Write your answer here')
#     st.write(answer.run(input_text))
#     # if input_text:
        

