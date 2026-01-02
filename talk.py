from google import genai
from google.genai import types
import time

# --- 設定項目 ---
API_KEY = "あなたのAPIキーをここに記入"
MODEL_ID = "gemini-1.5-flash"  # または "gemini-1.5-pro"
MAX_TURNS = 5  # 往復回数
INITIAL_PROMPT = "「ローカルLLMを業務で活用するメリットと課題」について議論を始めてください。"

# モデルAの役割設定
CONFIG_A = types.GenerateContentConfig(
    system_instruction="あなたはセキュリティを重視するサーバーエンジニアです。データ漏洩リスクの観点からローカルLLMの必要性を説いてください。返答は簡潔に。",
    temperature=0.7,
)

# モデルBの役割設定
CONFIG_B = types.GenerateContentConfig(
    system_instruction="あなたはコストと運用効率を重視するITマネージャーです。ハードウェアコストやメンテナンスの負担の観点から慎重な意見を述べてください。返答は簡潔に。",
    temperature=0.7,
)

def start_dialogue():
    # クライアントの初期化
    client = genai.Client(api_key=API_KEY)

    # それぞれのチャットセッションを開始
    # google-genaiでは client.chats.create を使用します
    chat_a = client.chats.create(model=MODEL_ID, config=CONFIG_A)
    chat_b = client.chats.create(model=MODEL_ID, config=CONFIG_B)

    print(f"--- 対話開始：テーマ「{INITIAL_PROMPT}」 ---\n")

    current_input = INITIAL_PROMPT

    for i in range(1, MAX_TURNS + 1):
        print(f"【ターン {i} / {MAX_TURNS}】")

        # --- Model A の発言 ---
        response_a = chat_a.send_message(current_input)
        text_a = response_a.text
        print(f"\n[Gemini A]:\n{text_a}\n")
        
        current_input = text_a
        time.sleep(1) # レート制限対策

        # --- Model B の発言 ---
        response_b = chat_b.send_message(current_input)
        text_b = response_b.text
        print(f"[Gemini B]:\n{text_b}\n")
        
        current_input = text_b
        time.sleep(1)
        print("-" * 30)

    print("\n設定された往復回数に達したため、対話を終了します。")

if __name__ == "__main__":
    start_dialogue()