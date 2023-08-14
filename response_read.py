import os
from langchain.llms import OpenAI
import streamlit as st
from langchain import PromptTemplate
from langchain.chains import LLMChain
import time
import pyttsx3 as sp
from constant import openai_key

os.environ['OPENAI_API_KEY'] = openai_key

with open('questions.txt', 'r') as file:
    file_contents = file.readlines()

cleaned_contents = [line[3:].rstrip('\n') for line in file_contents if line != '\n']

speak = sp.init()
# speak.setProperty('rate', 100)
st.markdown(
    f"<h1 style='text-align: center;'>Questions</h1>",
    unsafe_allow_html=True
)

# llm = OpenAI(temperature=0.8)


# first_ans = PromptTemplate(
#     input_variables = ['qs','ans'] ,
#     template='Given the question "\{qs}"\, how accurate do you believe this answer "\{ans}"\ is on a percentage scale?')


# correct_per = LLMChain(llm=llm , prompt=first_ans,verbose=True) 

for content in cleaned_contents:
    st.write(content)
    speak.say(content)
    answer = st.text_input('Answer')
    time.sleep(20)
    response = correct_per.run(qs=content , ans = answer)
    st.write(response)

############################################################################################################

# import os
# import streamlit as st
# import pyttsx3 as sp
# from langchain.llms import OpenAI
# from langchain.chains import LLMChain
# from langchain import PromptTemplate
# from constant import openai_key
# import time

# os.environ['OPENAI_API_KEY'] = openai_key

# with open('questions.txt', 'r') as file:
#     file_contents = file.readlines()

# cleaned_contents = [line[3:].rstrip('\n') for line in file_contents if line != '\n']

# speak = sp.init()
# st.markdown(
#     f"<h1 style='text-align: center;'>Questions</h1>",
#     unsafe_allow_html=True
# )

# llm = OpenAI(temperature=0.8)

# first_ans = PromptTemplate(
#     input_variables=['qs', 'ans'],
#     template='Given the question "\{qs}"\, how accurate do you believe this answer "\{ans}"\ is on a percentage scale?'
# )

# correct_per = LLMChain(llm=llm, prompt=first_ans, verbose=True)

# def display_question(index):
#     print(f'index ----------------------------------------------------------------> {index}')
#     content = cleaned_contents[index]
#     st.write(content)
#     speak.say(content)
#     return content

# current_index = 0

# if current_index < len(cleaned_contents):
#     print('Current index ------------------------------------------------------->',current_index)
#     content= display_question(current_index)
#     print('delay starts')
#     answer = st.text_input(f'You have 2 minutes to answer {current_index}')
#     time.sleep(20)
#     print('delay ends')
#     print(f'Answer len --------------------------------------------------------->{len(answer)}')
#     response = correct_per.run(qs=content, ans=answer)
#     st.write(response)
#     print('Current index ------------------------------------------------------->',current_index)
#     current_index += 1

############################################################################################################

# import os
# import streamlit as st
# import pyttsx3 as sp
# from langchain.llms import OpenAI
# from langchain.chains import LLMChain
# from langchain import PromptTemplate
# from constant import openai_key

# os.environ['OPENAI_API_KEY'] = openai_key

# with open('questions.txt', 'r') as file:
#     file_contents = file.readlines()

# cleaned_contents = [line[3:].rstrip('\n') for line in file_contents if line != '\n']

# speak = sp.init()
# st.markdown(
#     f"<h1 style='text-align: center;'>Questions</h1>",
#     unsafe_allow_html=True
# )

# llm = OpenAI(temperature=0.8)

# first_ans = PromptTemplate(
#     input_variables=['qs', 'ans'],
#     template='Given the question "\{qs}"\, how accurate do you believe this answer "\{ans}"\ is on a percentage scale?'
# )

# correct_per = LLMChain(llm=llm, prompt=first_ans, verbose=True)

# def display_question(index):
#     print('inside display_question')
#     content = cleaned_contents[index]
#     print('contents printing ---------->', content)
#     st.write(content)
#     print('writing contents to scr using streamlit')
#     speak.say(content)
#     print('speaking the contents')
#     # answer = st.text_input(f'Answer_{index}')
#     print('getting answer from user')
#     answer = st.text_input(f'Answer')
#     print('returning content and answer')
#     return content, answer

# def increase_ind():
#     global current_index
#     print('increasing indeXXXXXXXXXXXXXXXXXXXXXX') 
#     current_index += 1

# current_index = 0

# if current_index < len(cleaned_contents):
#     print('inside if')
#     print('calling display_question func')
#     content, answer = display_question(current_index)
#     print('After running display_question function',content,answer)
#     print('asking model the answer is correct')
#     response = correct_per.run(qs=content, ans=answer)
#     print('getting response------------>',response)
#     print('writing response to the screen')
#     st.write(response)
#     print('printing current index count ->>>>>>>>>>>>>>>>>>>',current_index)
#     st.button('Next',on_click=increase_ind)
#     print('checking whether count is increase or not->>>>>>>>>>>>',current_index)
