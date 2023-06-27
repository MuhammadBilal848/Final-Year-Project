import os
from constants import openai_key
from langchain.llms import OpenAI
import streamlit as st

os.environ['OPENAI_API_KEY'] = openai_key

st.title('Testing LangChain')
input_text = st.text_input('Search any topic you want:')


# OPENAI LLMS
# tempratture param controls how balance the reponse should be
llm = OpenAI(temperature=0.8)
 

if input_text:
    st.write(llm(input_text))
