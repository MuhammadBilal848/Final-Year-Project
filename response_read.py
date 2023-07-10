import os
from langchain.llms import OpenAI
import streamlit as st
from langchain import PromptTemplate
from langchain.chains import LLMChain
import pyttsx3 as sp


with open('questions.txt', 'r') as file:
    file_contents = file.readlines()

cleaned_contents = [line[3:].rstrip('\n') for line in file_contents if line != '\n']

speak = sp.init()

st.markdown(
    f"<h1 style='text-align: center;'>Questions</h1>",
    unsafe_allow_html=True
)
for content in cleaned_contents:
    st.write(content)
    speak.say(content)
    speak.runAndWait()

