import streamlit as st
import google.generativeai as genai

# 1. ページ設定（※st.writeより前に実行する必要があります）
st.set_page_config(page_title="Badminton AI Coach", page_icon="🏸")
st.title("🏸 バドミントンAIアドバイザー")

# デバッグ情報の表示
st.caption(f"SDK Version: {genai.__version__}")

# 2. 変数名を変えて、Secretsから確実に取得する
# GEMINI_API_KEY という名前を避けることで、システムの古い環境変数との干渉を防ぎます
# ※StreamlitのSecrets画面で、左側の名前を「MY_NEW_KEY」に書き換えてから実行してください
if "MY_NEW_KEY" not in st.secrets:
    st.error("StreamlitのSecretsで、名前を 'MY_NEW_KEY' にしてAPIキーを保存し直してください。")
    st.stop()

my_key = st.secrets["MY_NEW_KEY"]
st.caption(f"使用中のキー末尾: ***{my_key[-3:]}")

# 3. API設定
# 明示的にAPIキーを渡し、余計な設定を初期化します
genai.configure(api_key=my_key)

# 4. モデル設定
# 'models/' を含めず、かつ最新を明示しない最もシンプルな指定にします。
# 実はSDK 0.8.6ではこれが最も「v1」に繋がりやすい指定です。
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
            # 念のため、安全な生成オプションを最小限で指定
            response = model.generate_content(prompt)
            
            # responseの中身を安全に取得
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("AIからの応答が空でした。")
        except Exception as e:
            # ここで出るエラーメッセージに「v1beta」が含まれるかどうかが重要です
            st.error(f"エラーが発生しました: {e}")
