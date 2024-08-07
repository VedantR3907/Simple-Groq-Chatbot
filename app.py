import asyncio
import streamlit as st
import requests
from streamlit_extras.bottom_container import bottom
from functions.save_data_to_json import save_to_json
from functions.chat_history import display_chat_history, read_chat_history

FASTAPI_URL = "http://127.0.0.1:8000/groq_api_generator_response"



def bottom_container():
    with bottom():      
        user_prompt = st.chat_input("Write a question")
        if user_prompt:
            return user_prompt


def generate_answer(user_prompt, system_prompt):
    response = requests.post(
        FASTAPI_URL,
        json={"system_prompt": system_prompt, "user_prompt": user_prompt},
        stream=True
    )

    if response.status_code == 200:
        # Process streaming response
        answer = response.text
        final_response = ''
        for i in answer.split(' '):
            text = i + " "
            yield text
            final_response += text
        save_to_json(user_prompt, final_response)

    else:
        st.error(f"Error: {response.status_code}")

async def main():
    st.header("GROQ API CHATBOT")
    user_prompt = bottom_container()
    if user_prompt is not None and user_prompt != '':
        answer = generate_answer(user_prompt, "you are an helpful assistant.")
        with st.container(border=True, height=500):
            chat_history = await read_chat_history()
            display_chat_history(chat_history)
            
            with st.chat_message("HUMAN", avatar='./assets/user.png'):
                st.markdown(user_prompt)
                
            with st.chat_message("AI", avatar='./assets/meta.png'):
                st.write(answer)

asyncio.run(main())