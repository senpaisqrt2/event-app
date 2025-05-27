import redis
from datetime import datetime
import os
import time

LOG_PATH = "logs/log.txt"

def ensure_log_dir():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def main():
    print("[logger] Starting logger...", flush=True)
    r = redis.Redis(host="redis", port=6379, decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe("events")
    print("[logger] Subscribed to 'events'", flush=True)

    ensure_log_dir()

    while True:
        try:
            for msg in pubsub.listen():
                if msg["type"] == "message":
                    text = f"{datetime.now()} — {msg['data']}\n"
                    print(f"[logger] {text.strip()}", flush=True)
                    with open(LOG_PATH, "a") as f:
                        f.write(text)
                        f.flush()
        except Exception as e:
            print(f"[logger] Error: {e}", flush=True)
            time.sleep(2)

if __name__ == "__main__":
    main()
