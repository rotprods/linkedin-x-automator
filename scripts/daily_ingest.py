import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from signal_pipeline import store
from learning_loop import metrics as m

conn = store.connect()

# Posts publicados en las ultimas 24h (list_x_user_tweets, no replies)
tweets = [
    {"id": "2085186022082568476", "public_metrics": {"impression_count": 17, "like_count": 0, "reply_count": 0, "retweet_count": 0}},
    {"id": "2085186023395328156", "public_metrics": {"impression_count": 7, "like_count": 1, "reply_count": 0, "retweet_count": 0}},
    {"id": "2085124247228166398", "public_metrics": {"impression_count": 7, "like_count": 0, "reply_count": 0, "retweet_count": 0}},
    {"id": "2085063914220318758", "public_metrics": {"impression_count": 17, "like_count": 0, "reply_count": 1, "retweet_count": 0}},
    {"id": "2085063912827846955", "public_metrics": {"impression_count": 13, "like_count": 0, "reply_count": 1, "retweet_count": 0}},
]

n = m.ingest_x_metrics(conn, tweets)
conn.commit()
print(f"Ingested {n} X metrics rows")
print("metrics in DB(last day):",
      conn.execute("SELECT COUNT(*) FROM metrics WHERE collected_at >= date('now','-1 day')").fetchone()[0])
conn.close()