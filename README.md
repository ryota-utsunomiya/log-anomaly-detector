# AI Log Anomaly Detector

URL http://54.159.106.74:8000/docs

AI(機械学習)を用いてWebリクエスト(ログ)の異常をリアルタイムに検知し、Discordへ通知するバックエンドシステムです。AIを組み込んだこのシステムによって未知のサイバー攻撃にも対応できます。

##概要
大量のシステムログから「普段とは違うパターン」をIsolation Forestで分析。異常を検知した際は、詳細な内容をDiscord Webhookを通じて管理者にアラート送信します。

##技術スタック
- **Language:** Pyhon 3.11
- **Framework:** FastAPI 
- **AI/ML:** Scikit-learn (Logistic Regression), Pandas
- **Database:** PostgreSQL, SQLAlchemy (ORM)
- **Infrastructure:** Docker, Docker Compose
- **Notification:** Discord Webhook API

## テストの実行方法
DATABASE_URL=sqlite:///./test.db python3 -m pytest
