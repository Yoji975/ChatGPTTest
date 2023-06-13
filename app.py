import streamlit as st
import streamlit.components.v1 as stc
import openai
#import pyttsx3

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
    for message in reversed(messages[1:]):  # 直近のメッセージを上に
          str=str+message["content"]+"<br>"
          cnt=cnt+1
          engine.say("Hello, World")
          engine.runAndWait()
          if cnt==2:
            str=str+"========="+"<br>"
            cnt=0
    #st.write(str)
    stc.html(str, height=400, scrolling=True,)
user_input = st.text_input("Freddyに話しかけよう！", key="user_input", on_change=communicate)
