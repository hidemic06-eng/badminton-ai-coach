import streamlit as st
import google.generativeai as genai

# 1. ページ設定
st.set_page_config(page_title="Badminton AI Coach", page_icon="🏸")
st.title("🏸 バドミントンAIアドバイザー")

# 2. SecretsからAPIキーを読み込み
if "GEMINI_API_KEY" not in st.secrets:
    st.error("SecretsにGEMINI_API_KEYが設定されていません。")
    st.stop()

# 3. API設定：REST通信を強制（これでv1beta問題を回避しやすくします）
genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"],
    transport='rest'
)

# 4. キャラ設定（システム命令）
instruction = "あなたはバドミントンの3級公認審判員、兼コーチです。専門用語を使って親切に答えてください。"

# 5. モデルの設定
try:
    # 引数エラーを防ぐため、RequestOptionsを使わずシンプルに定義
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instruction
    )
except Exception as e:
    st.error(f"モデルの初期化失敗: {e}")
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

    with st.chat_message("assistant"):
        try:
            # 6. 生成実行：オプションを付けずにライブラリのデフォルトに任せる
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # ここで「404」が出る場合は、Google側の反映待ちです
            st.error(f"エラー詳細: {e}")
            st.info("APIキーを新しく作った直後の場合、反映まで10分ほどかかることがあります。")
