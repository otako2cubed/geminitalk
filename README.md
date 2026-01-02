# geminitalk
ご指摘の通り、Googleは現在、よりモダンで統合的な**Google GenAI SDK (`google-genai`)** への移行を推奨しています。この新ライブラリでは、`Client` オブジェクトをベースとした直感的な操作が可能になっています。

新しい `google-genai` ライブラリを使用した、回数指定付きの対話スクリプトを再作成しました。

### 事前準備

1. **新ライブラリのインストール:**
```bash
pip install -U google-genai

```


2. **APIキーの取得:** [Google AI Studio](https://aistudio.google.com/) で取得した既存のキーがそのまま使えます。

---

### Pythonサンプルコード（google-genai 版）

```python
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

```

---

### 旧ライブラリからの主な変更点

1. **インポート文:** `from google import genai` になりました。
2. **クライアント制:** `client = genai.Client(api_key=...)` のように、インスタンスを作って操作する形式に統一されました。
3. **設定の集約:** `system_instruction` や `temperature` などのパラメータは、`types.GenerateContentConfig` オブジェクトとしてまとめて渡すスタイルになっています。
4. **チャットの開始:** `client.chats.create(model=...)` でセッションを開始します。

### 発展的な活用方法

* **履歴の保存:** 各ターンの `text_a` と `text_b` をリストに保存し、最後にテキストファイルやJSONとして書き出す処理を加えると、後でログを確認しやすくなります。
* **異なるモデルの対決:** `MODEL_ID` を Model A は `gemini-1.5-pro`、Model B は `gemini-1.5-flash` と分けることで、知能指数の異なるモデル同士の壁打ちをシミュレーションすることも可能です。

次は、この対話結果をテキストファイルに自動保存する機能などを追加しましょうか？ご要望があればお知らせください。