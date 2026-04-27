import streamlit as st
import google.generativeai as genai

# ページ設定
st.set_page_config(page_title="Badminton AI Coach", page_icon="🏸")
st.title("🏸 バドミントンAIアドバイザー")

# SecretsからAPIキーを読み込み
if "GEMINI_API_KEY" not in st.secrets:
    st.error("SecretsにGEMINI_API_KEYが設定されていません。")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# キャラ設定
instruction = "あなたはバドミントンの3級公認審判員、兼コーチです。専門用語を使って親切に答えてください。"

# モデルの設定（最新のGemini 2.0 Flashを指定）
# 1.5で404が出る場合、こちらが正解です
try:
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash', 
        system_instruction=instruction
    )
except:
    # 万が一上記でエラーが出る場合の予備（古い名前）
    model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# チャット履歴を表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力
if prompt := st.chat_input("ルールや戦術、審判のコールについて聞いてね"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Geminiで回答生成
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # ここで、使えるモデルを一覧表示するデバッグ機能を追加
            st.error(f"エラーが発生しました: {e}")
            st.info("利用可能なモデルをチェックしてください。")
