import os
from constants import openai_key
from langchain.llms import OpenAI
import streamlit as st
from langchain import PromptTemplate
from langchain.chains import LLMChain

os.environ['OPENAI_API_KEY'] = openai_key


# st.title('Search Interview Fields')
st.markdown(
    f"<h1 style='text-align: center;'>Search Interview Fields</h1>",
    unsafe_allow_html=True
)

input_text = st.text_input('You can search here')

first_prompt = PromptTemplate(
    input_variables = ['skill_name'] ,
    template = 'Generate 3 questions about {skill_name} skill' 
                             )

# OPENAI LLMS
# tempratture param controls how balance the reponse should be
llm = OpenAI(temperature=0.8)
chain = LLMChain(llm=llm , prompt=first_prompt,verbose=True) 

if input_text:
    st.write(chain.run(input_text))


qs = chain.run(input_text)
print(qs)


# add a validation system that checks the answers
