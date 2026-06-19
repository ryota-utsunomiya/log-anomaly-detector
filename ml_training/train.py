import re
import random
import pickle
import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest



# SQLインジェクション、XSS、ディレクトリートレーバサルなどの混在データ
dataset_url = "https://raw.githubusercontent.com/payloadbox/xss-payload-list/master/Intruder/xss-payload-list.txt"
# サブとしてSQLインジェクションも一部混ぜる
sqli_url = "https://raw.githubusercontent.com/payloadbox/sql-injection-payload-list/master/Intruder/exploit.txt"

try:
    # XSSデータの読み込み
    res1 = requests.get(dataset_url)
    anomalies = res1.text.splitlines()
    
    # SQLiデータも少し混ぜて「未知の攻撃全般」のバリエーションを作る
    res2 = requests.get(sqli_url)
    anomalies.extend(res2.text.splitlines()[:500])
except Exception as e:
    print(f"読み込みエラー: {e}")
    anomalies = ["<script>alert(1)</script>", "' OR 1=1", "../../../etc/passwd", "&& id"]

# # 2. 汎用的な前処理関数の定義（あらゆる未知の攻撃に対応）
def preprocess_payload(text):
    """
    特定の変数名に依存せず、すべての『値』を完全に抽象化する。
    これにより、通常とは違う記号（<, >, ', ", %, /, .）が少しでも混ざると即座に異常判定できる。
    """
    if not isinstance(text, str):
        text = str(text)
        
    text = text.lower()
    
    text = re.sub(r'\d+', '[NUM]', text)
    
    text = re.sub(r'(=)[a-zA-Z_0-9]+', r'=[VAL]', text)
    
    return text

base_normals = [
    "id=123&cat=books", 
    "page=1&query=search", 
    "user=ryota&session=abc",
    "action=login&method=post", 
    "view=item&id=99", 
    "search=python&page=2",
    "lang=ja&theme=dark", 
    "mode=edit&item=10&status=active",
    "file=readme&ext=txt" # パス・トラバーサル防御用
]

# ランダム性を加えて水増し
normals = []
for _ in range(500):
    for pattern in base_normals:
        # ランダムな値を混ぜてバリエーションを作る
        if "id=" in pattern:
            pattern = pattern.replace("123", str(random.randint(1, 1000)))
        normals.append(pattern)

# DataFrameの構築
df_normal = pd.DataFrame({'payload': normals, 'label': 0})
df_anomaly = pd.DataFrame({'payload': anomalies[:50], 'label': 1})
df = pd.concat([df_normal, df_anomaly]).sample(frac=1).reset_index(drop=True)


# 正常データのみを抽出して前処理を適用
train_data_raw = df[df['label'] == 0]['payload'].astype(str)
train_data = train_data_raw.apply(preprocess_payload)


vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 5), min_df=2)
X_train = vectorizer.fit_transform(train_data)

model = IsolationForest(contamination=0.01, random_state=42)
model.fit(X_train)
