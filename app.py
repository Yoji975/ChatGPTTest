
import streamlit as st
import openai

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
col1,col2 = st.columns(2)
with col1:
   st.image("Freddy.png")

with col2:
 if st.session_state["messages"]:
    messages = st.session_state["messages"]

    # for message in reversed(messages[1:]):  # 直近のメッセージを上に
    st.write(messages[1])

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

