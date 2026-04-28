import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Badminton AI Coach", page_icon="🏸")
st.title("🏸 バドミントンAIアドバイザー")

# Secretsから読み込み
if "GEMINI_API_KEY" not in st.secrets:
    st.error("SecretsにAPIキーを設定してください")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 最も標準的な設定
model = genai.GenerativeModel('gemini-1.5-flash')

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
            # 標準的な生成（余計なオプションなし）
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"エラー詳細: {e}")
