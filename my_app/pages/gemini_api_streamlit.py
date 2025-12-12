import streamlit as st
from google import genai
from google.genai import types 
client=genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
st.subheader("Gemini AI")
if "messages" not in st.session_state:
    st.session_state.messages=[]


for message in st.session_state.messages:
    if message["role"] == "model":
        role = "assistant"
    else:
        role= message["role"]
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])
prompt = st.chat_input("Say Something")
if prompt:
    #display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    #save the state session
    st.session_state.messages.append({
        "role":"user",
        "parts" : [{"text":prompt}]
    })
    response=client.models.generate_content_stream(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
             system_instruction="You are Tom."
        ),
        contents=st.session_state.messages,
        )
    #display ai response
    with st.chat_message("assistant"):
        container=st.empty()
        full_reply=""
        for chunk in response:
            text_piece = None

            if hasattr(chunk, "text") and chunk.text:
                    text_piece = chunk.text
                
            elif hasattr(chunk, "candidates"):
                    try:
                        text_piece = chunk.candidates[0].content.parts[0].text
                    except:
                        pass

            if text_piece:
                    full_reply += text_piece
                    container.markdown(full_reply)


    st.session_state.messages.append({
            "role":"model",
            "parts" : [{"text":full_reply}]
        })
    st.rerun()