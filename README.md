# AI Log Anomaly Detector

URL http://54.175.216.54:8000/docs

AI(機械学習)を用いてシステムログの異常をリアルタイムに検知し、Discordへ通知するバックエンドシステムです。

##概要
大量のシステムログから「普段とは違うパターン」をロジスティック回帰モデルで分析。異常を検知した際は、詳細な内容をDiscord Webhookを通じて管理者にアラート送信します。

##技術スタック
- **Language:** Pyhon 3.11
- **Framework:** FastAPI (Asynchronous API)
- **AI/ML:** Scikit-learn (Logistic Regression), Pandas
- **Database:** PostgreSQL, SQLAlchemy (ORM)
- **Infrastructure:** Docker, Docker Compose
- **Notification:** Discord Webhook API

## テストの実行方法
DATABASE_URL=sqlite:///./test.db python3 -m pytest
