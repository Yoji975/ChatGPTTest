import streamlit as st
import streamlit.components.v1 as stc
import openai
#import pyttsx3
from gtts import gTTS
from io import BytesIO
import re
import requests

sound_file = BytesIO()

#tts = gTTS('hello', lang='en')
#tts.write_to_fp(sound_file)
#st.audio(sound_file)

#engine = pyttsx3.init('dummy')
#engine.say('hello')
#engine.runAndWait()

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key
freddy_content = st.secrets.Freddy.content

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": freddy_content}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("AI Freddy")
# stc.html("<p style='color:red;'> Streamlit is Awesome",scrolling=True,)

col1,col2 = st.columns(2)
with col1:
   st.image("Freddy.png")

with col2:
 if st.session_state["messages"]:
    messages = st.session_state["messages"]

    str = ""
    cnt = 0
    cnt2 = 0
    result = "hi"
    for message in reversed(messages[1:]):  # 直近のメッセージを上に
          str=str+message["content"]+"<br>"
          cnt=cnt+1
          cnt2=cnt2+1
          if cnt2==1:
            result=re.sub(r"[^a-zA-Z]", "",str)
            result = result.lstrip("Freddy")
            result = result.rstrip("rbrb")
          if cnt==2:
            str=str+"========="+"<br>"
            cnt=0
            
    tts=gTTS(result, lang='en')
    tts.write_to_fp(sound_file)
    url = "https://scapi-eu.readspeaker.com/a/speak?key=b6ddbe58ee4dae1f3987cb9f811f112f&lang=en_us&voice=Lizzy&text=Hello"
    #url = "https://scapi-eu.readspeaker.com/a/speak?key=b6ddbe58ee4dae1f3987cb9f811f112f&command=voiceinfo"
    r = requests.get(url)
    response = r.mp3()
    #response = r.json()
    #st.audio(sound_file)
    st.audio(response)
    #st.title(r)
    stc.html(str, height=400, scrolling=True,)
    

user_input = st.text_input("Freddyに話しかけよう！", key="user_input", on_change=communicate)
