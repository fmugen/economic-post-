# 経済データを取得するスクリプトです
下記のように経済データの取得を行いLLMにより文書を作成します。その後設定したXアカウントに内容を投稿します。
- データ取得: FRED API（金利・原油・物価）
- 文章生成: Claude API
- 投稿先: X（Twitter）

---

## 🚀 クイックスタート（初心者向け）

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

## 環境変数の設定
.envをローカル環境のpost_economic_data.pyと同じ層に保存してください。下記のように.envないにapiキーを設定します。

|必要な環境変数|説明|入手方法|
|---|---|---|
|FRED_API_KEY| 米国経済データAPI | https://fred.stlouisfed.org/docs/api/api_key.html で取得|
|ANTHROPIC_API_KEY| Claude API | https://console.anthropic.com で取得|
|X_API_KEY| X（Twitter）API | X Developer Portal で取得|
|X_API_SECRET| X（Twitter）API |   〃|
|X_ACCESS_TOKEN| X（Twitter）API |   〃|
|X_ACCESS_SECRET| X（Twitter）API |   〃|

---

## 実行方法

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

## 動作環境
Python 3.12 以上

## 必要なライブラリ
- anthropic >= 0.86.0
- tweepy >= 4.14.0
- python-dotenv >= 1.0.0
