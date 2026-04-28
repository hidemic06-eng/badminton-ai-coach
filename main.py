import streamlit as st
from groq import Groq

# 1. ページ設定
st.set_page_config(page_title="Badminton AI Coach", page_icon="🏸")
st.title("🏸 バドミントンAIアドバイザー (Groq版)")

# 2. APIキーの確認
if "GROQ_API_KEY" not in st.secrets:
    st.error("SecretsにGROQ_API_KEYを設定してください。")
    st.stop()

# 3. Groqクライアントの初期化
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- チャット履歴の管理 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 入力処理 ---
if prompt := st.chat_input("ルールや戦術、審判のコールについて聞いてね"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Groqでの生成（Llama 3.1 70B は非常に賢く日本語も堪能です）
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "あなたはバドミントンの3級公認審判員、兼コーチです。専門用語を使って親切に答えてください。"},
                    *[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]
                ],
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
