import streamlit as st
import google.generativeai as genai

# 1. ページ設定（※一番最初に書く必要があります）
st.set_page_config(page_title="Badminton AI Coach", page_icon="🏸")
st.title("🏸 バドミントンAIアドバイザー")

# デバッグ情報の表示
st.caption(f"SDK Version: {genai.__version__}")

# 2. Secretsの読み込み（MY_SPECIAL_KEY に合わせました）
if "MY_SPECIAL_KEY" not in st.secrets:
    st.error("Secretsに 'MY_SPECIAL_KEY' が見当たりません。設定を確認してください。")
    st.stop()

my_key = st.secrets["MY_SPECIAL_KEY"]
st.caption(f"使用中のキー末尾: ***{my_key[-3:]}")

# 3. API設定
genai.configure(api_key=my_key)

# 4. モデル設定（v1betaを回避するための標準的な指定）
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="あなたはバドミントンの3級公認審判員、兼コーチです。専門用語を使って親切に答えてください。"
    )
except Exception as e:
    st.error(f"モデルの初期化に失敗しました: {e}")
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
            # 生成
            response = model.generate_content(prompt)
            
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("AIからの応答が空でした。")
        except Exception as e:
            # 404 v1beta が出るか、ここで運命が決まります
            st.error(f"エラーが発生しました: {e}")
