# 経済データ自動投稿スクリプト

## 📋 概要

このスクリプトは、FRED（Federal Reserve Economic Data）から経済データを定期的に取得し、Claude AIで自動的にツイート文を生成してX（Twitter）に投稿するツールです。

### なぜFREDを使うのか？

FRED = Federal Reserve Economic Data。米国のセントルイス連邦準備銀行が運営する、**世界規模の経済データベース**です。

日本のデータを直接取るには、日銀や総務省のAPIを個別に叩く必要があり、仕様もバラバラで面倒です。FREDなら：
- **APIの仕様が統一** - 金利も原油もCPIも同じコードで取得できる
- **包括的** - 日銀・総務省・IMF・世銀など世界中のデータを集約
- **無料** - 50万件以上のデータセットにアクセス可能

### 使用データ

| 変数名 | シリーズID | 説明 |
|---|---|---|
| oil_wti | DCOILWTICO | WTI原油価格（$/バレル） |
| japan_rate | IRSTCB01JPM156N | 日銀政策金利（%） |
| japan_cpi | CPALTT01JPM657N | 日本CPI前年比（%） |

### 動作フロー

1. **データ取得** - FRED API から経済データを取得
2. **文章生成** - Claude API で日本語ツイートを自動生成
3. **投稿** - X API で生成されたツイートを投稿

---


---

## 🚀 クイックスタート

### 1️⃣ リポジトリをクローン
```bash
git clone https://github.com/fmugen/economic-post-.git
cd economic-post
```

### 2️⃣ 依存関係をインストール

#### オプション A: `uv` を使う場合（推奨・高速）
```bash
uv sync
uv run post_economic_data.py
```

#### オプション B: システムPythonを使う場合
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install anthropic tweepy python-dotenv
python post_economic_data.py
```

### 3️⃣ APIキーを設定

`.env` ファイルをプロジェクト直下に作成して、以下の内容を記入します：

```
FRED_API_KEY=xxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
X_API_KEY=xxxxxxxxxxxx
X_API_SECRET=xxxxxxxxxxxx
X_ACCESS_TOKEN=xxxxxxxxxxxx
X_ACCESS_SECRET=xxxxxxxxxxxx
```

### 4️⃣ 実行
```bash
uv run post_economic_data.py
```

---

## ⚙️ APIキー設定

`.env`ファイルをプロジェクト直下に作成して、各APIキーを設定します。

|必要な環境変数|説明|入手方法|
|---|---|---|
|FRED_API_KEY| 米国経済データAPI | https://fred.stlouisfed.org/docs/api/api_key.html で取得|
|ANTHROPIC_API_KEY| Claude API | https://console.anthropic.com で取得|
|X_API_KEY| X（Twitter）API | X Developer Portal で取得|
|X_API_SECRET| X（Twitter）API |   〃|
|X_ACCESS_TOKEN| X（Twitter）API |   〃|
|X_ACCESS_SECRET| X（Twitter）API |   〃|

---

## 💾 実行方法

### 手動実行
```bash
# uv を使う場合
uv run post_economic_data.py

# または仮想環境のPythonで実行
.venv\Scripts\python.exe post_economic_data.py  # Windows
source .venv/bin/activate && python post_economic_data.py  # macOS / Linux
```

### 毎日自動実行（Windows）
タスクスケジューラで以下の設定をしてください：
- 実行ファイル: `.venv\Scripts\python.exe`
- 引数: `post_economic_data.py`
- 作業ディレクトリ: `/path/to/economic-post`
- 実行頻度: 毎日 08:00

---

## 🛠️ 動作環境・必要なライブラリ

**Python**: 3.12 以上

**依存パッケージ**:
- anthropic >= 0.86.0
- tweepy >= 4.14.0
- python-dotenv >= 1.0.0
