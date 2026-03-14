import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


CONFIG = {'configurable': {'thread_id': 'thread-1'}}

# loading the previous conversation history

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


user_input = st.chat_input("Type your message here...")

if user_input:

    # first add message to the history, then display it in the UI
    st.session_state['message_history'].append({'role':'user', 'content': user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)

    ai_message = response['messages'][-1].content

    with st.chat_message("assistant"):

         # first add message to the history, then display it in the UI
        st.session_state['message_history'].append({'role':'assistant', 'content': ai_message})
        st.markdown(ai_message)