import streamlit as st
import google.generativeai as genai

# 1. ページ設定
st.set_page_config(page_title="Badminton AI Coach", page_icon="🏸")
st.title("🏸 バドミントンAIアドバイザー")

# 2. SecretsからAPIキーを読み込み
if "GEMINI_API_KEY" not in st.secrets:
    st.error("SecretsにGEMINI_API_KEYが設定されていません。")
    st.stop()

# 3. API設定
genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"],
    transport='rest' # 通信方式をウェブ標準に固定
)

# 4. キャラ設定
instruction = "あなたはバドミントンの3級公認審判員、兼コーチです。専門用語を使って親切に答えてください。"

# 5. モデルの設定
try:
    # ★ 修正ポイント：モデル名を絶対パス形式に変更
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-flash',
        system_instruction=instruction
    )
except Exception as e:
    st.error(f"モデルの初期化失敗: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# チャット表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 入力
if prompt := st.chat_input("ルールや戦術、審判のコールについて聞いてね"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # 6. 生成実行
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # ここでもしまた v1beta 404 が出るなら、Google側の反映ラグが濃厚です
            st.error(f"エラー詳細: {e}")
            st.info("APIキーの作成直後は、Google内部の同期に最大30分ほどかかるケースがあります。")
