import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# 1. ページ設定
st.set_page_config(page_title="Badminton AI Coach", page_icon="🏸")
st.title("🏸 バドミントンAIアドバイザー")

# 2. SecretsからAPIキーを読み込み
if "GEMINI_API_KEY" not in st.secrets:
    st.error("SecretsにGEMINI_API_KEYが設定されていません。")
    st.stop()

# 3. API設定：REST通信を強制し、バージョンをv1に固定
genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"],
    transport='rest'
)

# 4. キャラ設定（システム命令）
instruction = "あなたはバドミントンの3級公認審判員、兼コーチです。専門用語を使って親切に答えてください。"

# 5. モデルの設定：明示的に v1 安定版のオプションを渡す
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instruction
    )
    # 通信オプションで API バージョンを強制
    request_options = RequestOptions(api_version='v1')
except Exception as e:
    st.error(f"モデルの初期化失敗: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ルールや戦術、審判のコールについて聞いてね"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ★ ここが修正の核心：request_options を渡して v1beta を回避
            response = model.generate_content(
                prompt,
                request_options=request_options
            )
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"エラー詳細: {e}")
