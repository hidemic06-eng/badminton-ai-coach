import streamlit as st
import google.generativeai as genai

st.write(f"SDK Version: {genai.__version__}")
# Secretsが本当に更新されているか、末尾3文字だけ確認する
key = st.secrets["GEMINI_API_KEY"]
st.write(f"現在使用中のキー（末尾3文字）: ***{key[-3:]}")

# 1. ページ設定
st.set_page_config(page_title="Badminton AI Coach", page_icon="🏸")
st.title("🏸 バドミントンAIアドバイザー")

# 2. APIキーの確認
if "GEMINI_API_KEY" not in st.secrets:
    st.error("SecretsにGEMINI_API_KEYを設定してください。")
    st.stop()

# 3. API設定（最も標準的な形に戻します）
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 4. モデル設定（昨日成功しなかった原因である v1beta を、名前で回避します）
try:
    # モデル名の前に 'models/' を付けるのが、実は今の公式の推奨です
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-flash',
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
            # 余計な client 指定などをすべて排除
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
