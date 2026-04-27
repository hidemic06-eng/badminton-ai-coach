import streamlit as st
import google.generativeai as genai

# ページ設定
st.set_page_config(page_title="Badminton AI Coach", page_icon="🏸")
st.title("🏸 バドミントンAIアドバイザー (Gemini版)")

# SecretsからAPIキーを読み込み
if "GEMINI_API_KEY" not in st.secrets:
    st.error("SecretsにGEMINI_API_KEYが設定されていません。")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# キャラ設定（システム命令）
instruction = "あなたはバドミントンの3級公認審判員、兼コーチです。専門用語を使って親切に答えてください。"

# モデルの設定：ここを「gemini-1.5-flash」のみに修正
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instruction
    )
except Exception as e:
    st.error(f"モデルの初期化に失敗しました: {e}")
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
            # 履歴なしのシンプルな生成
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("AIからの応答が空でした。")
        except Exception as e:
            # 具体的なエラーを表示するように修正
            st.error(f"AIが応答できませんでした。エラー詳細: {e}")
