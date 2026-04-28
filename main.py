import streamlit as st
import google.generativeai as genai
from google.generativeai import client # これを追加

st.set_page_config(page_title="Badminton AI Coach", page_icon="🏸")
st.title("🏸 バドミントンAIアドバイザー")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("SecretsにGEMINI_API_KEYが設定されていません。")
    st.stop()

# API設定
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ★【最重要】ライブラリのバグを回避するため、APIバージョンを「v1」に固定
# これにより、エラーに出ていた v1beta を強制的にスキップします
my_client = client.get_default_generative_client(version='v1')

try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="あなたはバドミントンの3級公認審判員、兼コーチです。"
    )
except Exception as e:
    st.error(f"初期化失敗: {e}")
    st.stop()

# --- チャット履歴管理 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("質問をどうぞ"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ★ ここでも client を指定して、v1 で通信させる
            response = model.generate_content(prompt, client=my_client)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"エラー詳細: {e}")
