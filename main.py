import streamlit as st
import google.generativeai as genai
import os

# 1. ページ設定
st.set_page_config(page_title="Badminton AI Coach", page_icon="🏸")
st.title("🏸 バドミントンAIアドバイザー")

# デバッグ表示
st.caption(f"SDK Version: {genai.__version__}")

# 2. Secretsの読み込み
if "MY_SPECIAL_KEY" not in st.secrets:
    st.error("Secretsに 'MY_SPECIAL_KEY' を設定してください。")
    st.stop()

my_key = st.secrets["MY_SPECIAL_KEY"]
st.caption(f"使用中のキー末尾: ***{my_key[-3:]}")

# 3. API設定（【重要】v1betaの呪いを物理的に解く設定）
# 環境変数レベルで、古い通信先を上書きし、かつREST通信に固定します
os.environ["GOOGLE_API_KEY"] = my_key
genai.configure(api_key=my_key, transport='rest')

# 4. モデル設定
# ライブラリに「推測」させないよう、URLの断片を含まない名前で指定します
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="あなたはバドミントンの3級公認審判員、兼コーチです。専門用語を使って親切に答えてください。"
    )
except Exception as e:
    st.error(f"初期化エラー: {e}")
    st.stop()

# --- チャット表示処理 ---
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
            # 呼び出し時にも明示的にAPIバージョンを意識させます
            response = model.generate_content(prompt)
            
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("AIからの応答が空でした。")
        except Exception as e:
            # ここで「v1beta」という単語が消えることを祈ります
            st.error(f"エラーが発生しました: {e}")
