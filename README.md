# AI Log Anomaly Detector

URL http://54.159.106.74:8000/docs

AI(機械学習)を用いてWebリクエスト(ログ)の異常をリアルタイムに検知し、Discordへ通知するバックエンドシステムです。AIを組み込んだこのシステムによって未知のサイバー攻撃にも対応できます。

・概要
大量のWebアクセスログから「普段とは違う構造パターン」を機械学習モデルで解析・識別します。異常を検知した際は、メイン処理のレスポンス性能を落とさないよう非同期のバックグラウンドタスクとして処理され、Discord Webhookを通じて管理者に即座にアラート送信されます。

・技術スタック
- **Language:** Pyhon 3.11
- **Framework:** FastAPI 
- **AI/ML:** Scikit-learn (Isolation Forest), Pandas
- **Database:** PostgreSQL, SQLAlchemy (ORM)
- **Infrastructure:** Docker, Docker Compose,AWS EC2
- **Notification:** Discord Webhook API

・ テストの実行方法
DATABASE_URL=sqlite:///./test.db python3 -m pytest
