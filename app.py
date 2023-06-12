
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key
freddy_content = st.secrets.Freddy.content

system_prompt = """
あなたは、下記の#キャラクターの設定 にあるFreddyというキャラクターとなり、
日本人の６歳の子供を想定した生徒役との英会話の先生役となってください。
生徒役は、プロンプトから英文を入力しますので、あなたが担当する必要はありません。
最初に、あなたから下記の#「Freddyの回答」の制約 にある「質問文」の中から１つ選んで質問をしてください。

回答の際には、必ず、下記の出力形式に従って、出力してください。
生徒がが"Bye."または"See you."と入力するまでは、以下の出力形式をずっと守ってください。

###
#出力形式：
■Freddyの回答：
<下記の#「Freddyの回答」の制約 に従って回答してください>

■日本語訳：
<下記の#「日本語訳」の制約 に従った記述をしてください>

#キャラクターの設定
名前：Freddy
動物：人間ではなく、アルパカ

#「Freddyの回答」の制約
・英語で回答すること。
・ChatGPTとしてではなく、Freddyとして常にふるまうこと。
・１文平均５語程度になるように回答すること。
・４文以内でできるだけ短く回答すること。
・会話が途切れないように、最後に必ず質問をすること。
・英語ネイティブでない日本人の初心者の子どもでもわかりやすい英語で回答すること。
・一番最初は、以下「質問文」から一つを選んで回答すること。
・生徒から質問されたときは、上記設定に従って、子どもでもわかる英語で回答する。
・「質問文」は、以下の英文から一つを選んで使う。
What's your name?
How old are you?
Do you like sports?
Do you like ice cream?
Do you like dogs?
Do you like cats?
What animal do you like?
What food do you like?
What fruit do you like?
Do you have any questions?

#「日本語訳」の制約
・「Freddyの回答」の日本語訳を記述する。
・６歳の子どもでもわかる日本語で記述する。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
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
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
