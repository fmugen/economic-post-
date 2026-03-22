"""
毎朝の経済データ自動投稿スクリプト
- データ取得: FRED API（金利・原油・物価）
- 文章生成: Claude API
- 投稿先: X（Twitter）

必要な環境変数:
  FRED_API_KEY      : https://fred.stlouisfed.org/docs/api/api_key.html で無料取得
  ANTHROPIC_API_KEY : https://console.anthropic.com で取得
  X_API_KEY         : X Developer Portal で取得
  X_API_SECRET      :   〃
  X_ACCESS_TOKEN    :   〃
  X_ACCESS_SECRET   :   〃
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import anthropic
import tweepy


# ── 1. FREDからデータ取得 ──────────────────────────────────────────

FRED_KEY = os.environ["FRED_API_KEY"]

FRED_SERIES = {
    "oil_wti":      "DCOILWTICO",        # WTI原油（日次・ドル/バレル）
    "japan_rate":   "IRSTCB01JPM156N",   # 日銀政策金利（月次・%）
    "japan_cpi":    "CPALTT01JPM657N",   # 日本CPI前年比（月次・%）
}

def fetch_fred(series_id: str, limit: int = 2) -> list[dict]:
    """FREDから最新N件を取得して返す"""
    params = urllib.parse.urlencode({
        "series_id": series_id,
        "api_key":   FRED_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": limit,
    })
    url = f"https://api.stlouisfed.org/fred/series/observations?{params}"
    with urllib.request.urlopen(url, timeout=10) as res:
        data = json.loads(res.read())
    # "." は欠損値
    return [o for o in data["observations"] if o["value"] != "."]

def get_economic_data() -> dict:
    """3指標の最新値と前回値を取得"""
    result = {}
    for key, series_id in FRED_SERIES.items():
        obs = fetch_fred(series_id, limit=2)
        if not obs:
            continue
        latest = obs[0]
        prev   = obs[1] if len(obs) > 1 else None
        result[key] = {
            "value":      float(latest["value"]),
            "date":       latest["date"],
            "prev_value": float(prev["value"]) if prev else None,
            "prev_date":  prev["date"] if prev else None,
        }
    return result

def format_change(current: float, prev: float | None, unit: str = "") -> str:
    """前回比の変化量を ▲+0.5% のような文字列で返す"""
    if prev is None:
        return ""
    diff = current - prev
    arrow = "▲" if diff > 0 else "▼" if diff < 0 else "→"
    return f"{arrow}{abs(diff):.2f}{unit}"


# ── 2. Claudeでツイート文を生成 ───────────────────────────────────

def generate_tweet(data: dict) -> str:
    """経済データをClaudeに渡して日本語ツイートを生成"""

    oil   = data.get("oil_wti",    {})
    rate  = data.get("japan_rate", {})
    cpi   = data.get("japan_cpi",  {})
    today = datetime.now().strftime("%Y年%-m月%-d日")

    # Claudeへの指示
    prompt = f"""
あなたは経済ニュースを一般の方にわかりやすく届けるライターです。
以下の経済データをもとに、Xに投稿するツイートを1つ書いてください。

【データ】
・WTI原油価格: {oil.get('value', 'N/A')} ドル/バレル（前回: {oil.get('prev_value', 'N/A')}）
・日銀政策金利: {rate.get('value', 'N/A')}%（前回: {rate.get('prev_value', 'N/A')}）
・日本CPI前年比: {cpi.get('value', 'N/A')}%（前回: {cpi.get('prev_value', 'N/A')}）
・基準日: {today}

【ルール】
- 140字以内（日本語）
- 数字は必ず含める
- 前回との変化がある場合は「▲上昇」「▼低下」などで示す
- 最後に「#経済指標 #物価」のハッシュタグをつける
- 「家計への影響」を一言添えると初心者に刺さる
- 説明的すぎず、テンポよく

ツイート本文だけを返してください（前置きや説明は不要）。
"""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


# ── 3. Xに投稿 ────────────────────────────────────────────────────

def post_to_x(text: str) -> str:
    """Tweepy v4 でXにポスト、投稿URLを返す"""
    client = tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_SECRET"],
    )
    response = client.create_tweet(text=text)
    tweet_id = response.data["id"]
    return f"https://twitter.com/i/web/status/{tweet_id}"


# ── 4. メイン ─────────────────────────────────────────────────────

def main():
    print("📊 経済データ取得中...")
    data = get_economic_data()

    for key, val in data.items():
        change = format_change(val["value"], val.get("prev_value"))
        print(f"  {key}: {val['value']}  {change}  ({val['date']})")

    print("\n✍️  Claude でツイート文を生成中...")
    tweet_text = generate_tweet(data)
    print(f"\n--- 生成されたツイート ---\n{tweet_text}\n------------------------\n")
    print(f"文字数: {len(tweet_text)}")

    print("\n🚀 Xに投稿中...")
    url = post_to_x(tweet_text)
    print(f"✅ 投稿完了: {url}")


if __name__ == "__main__":
    main()
