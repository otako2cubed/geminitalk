from google import genai
from google.genai import types, errors
import time
import re

# --- 設定項目 ---
API_KEY = "あなたのAPIキーをここに記入"
MODEL_ID = "gemini-1.5-flash" # エラーログに合わせて gemini-3-flash 等に変更可
MAX_TURNS = 5
INITIAL_PROMPT = "「ローカルLLMを業務で活用するメリットと課題」について議論を始めてください。"

client = genai.Client(api_key=API_KEY)

def send_message_with_retry(chat_session, message):
    """
    429エラーが発生した場合に、指示された時間待機してリトライする関数
    """
    while True:
        try:
            return chat_session.send_message(message)
        except errors.ClientError as e:
            if "429" in str(e):
                # エラーメッセージから待機秒数を抽出（例: "24.944s"）
                wait_time = 30  # デフォルト待機時間
                match = re.search(r"retry in ([\d\.]+)s", str(e))
                if match:
                    wait_time = float(match.group(1)) + 1  # 少し余裕を持たせる
                
                print(f" [!] レート制限に達しました。 {wait_time:.1f}秒待機して再試行します...")
                time.sleep(wait_time)
            else:
                # 429以外のエラー（認証エラーなど）はそのまま投げる
                raise e

def start_dialogue():
    config_a = types.GenerateContentConfig(
        system_instruction="あなたはセキュリティ重視のエンジニアです。簡潔に話してください。",
        temperature=0.7,
    )
    config_b = types.GenerateContentConfig(
        system_instruction="あなたはコスト重視のITマネージャーです。簡潔に話してください。",
        temperature=0.7,
    )

    chat_a = client.chats.create(model=MODEL_ID, config=config_a)
    chat_b = client.chats.create(model=MODEL_ID, config=config_b)

    print(f"--- 対話開始 ---\n")
    current_input = INITIAL_PROMPT

    for i in range(1, MAX_TURNS + 1):
        print(f"【ターン {i} / {MAX_TURNS}】")

        # Model A の発言
        response_a = send_message_with_retry(chat_a, current_input)
        text_a = response_a.text
        print(f"\n[Gemini A]:\n{text_a}\n")
        
        current_input = text_a
        time.sleep(2) # ターン間の基本待機時間を少し長めに

        # Model B の発言
        response_b = send_message_with_retry(chat_b, current_input)
        text_b = response_b.text
        print(f"[Gemini B]:\n{text_b}\n")
        
        current_input = text_b
        time.sleep(2)
        print("-" * 30)

    print("\n対話を終了しました。")

if __name__ == "__main__":
    start_dialogue()