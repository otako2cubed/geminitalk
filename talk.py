import google.generativeai as genai
import time

# --- 設定項目 ---
API_KEY = "あなたのAPIキーをここに記入"
MODEL_NAME = "gemini-1.5-flash"  # または "gemini-1.5-pro"
MAX_TURNS = 5  # 往復回数（A→Bで1カウント）
INITIAL_PROMPT = "「AIが感情を持つことは可能か」というテーマについて、議論を始めてください。"

# モデルAの役割設定
SYSTEM_INSTRUCTION_A = "あなたは科学的な視点を持つ論理的な哲学者です。相手の意見に対して批判的な検討を行い、さらなる議論を促してください。返答は短めに（200文字程度）してください。"
# モデルBの役割設定
SYSTEM_INSTRUCTION_B = "あなたは技術的な視点を持つAIエンジニアです。最新の技術動向を踏まえ、楽観的な見解を述べてください。返答は短めに（200文字程度）してください。"

# APIの初期化
genai.configure(api_key=API_KEY)

def start_dialogue():
    # 2つの異なるインスタンス（役割）を作成
    model_a = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_INSTRUCTION_A
    )
    model_b = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_INSTRUCTION_B
    )

    # 各モデルの会話履歴を管理するオブジェクト
    chat_a = model_a.start_chat(history=[])
    chat_b = model_b.start_chat(history=[])

    print(f"--- 対話開始：テーマ「{INITIAL_PROMPT}」 ---\n")

    current_input = INITIAL_PROMPT

    for i in range(1, MAX_TURNS + 1):
        print(f"【ターン {i} / {MAX_TURNS}】")

        # --- Model A の発言 ---
        response_a = chat_a.send_message(current_input)
        text_a = response_a.text
        print(f"\n[Gemini A]:\n{text_a}\n")
        
        # モデルBへの入力として渡す
        current_input = text_a
        
        # APIのレート制限回避のための短い待機（必要に応じて調整）
        time.sleep(1)

        # --- Model B の発言 ---
        response_b = chat_b.send_message(current_input)
        text_b = response_b.text
        print(f"[Gemini B]:\n{text_b}\n")
        
        # 次のループでモデルAへの入力として渡す
        current_input = text_b
        
        time.sleep(1)
        print("-" * 30)

    print("\n設定された往復回数に達したため、対話を終了します。")

if __name__ == "__main__":
    start_dialogue()