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

# モデルの設定：最も無料枠が安定している「1.5-flash」を指定
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash', 
        system_instruction=instruction
    )
except Exception as e:
    st.error(f"モデルの起動に失敗しました: {e}")
    st.stop()

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
            # 安全のため、1回のリクエストで完結させる
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            st.info("APIの無料枠が反映されるまで数分かかる場合があります。")
