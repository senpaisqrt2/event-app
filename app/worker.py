import redis
import time

def handle_event(msg):
    print(f"[worker] Event received: {msg['data']}", flush=True)

def main():
    print("[worker] Starting worker...", flush=True)
    r = redis.Redis(host="redis", port=6379, decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe("events")
    print("[worker] Subscribed to 'events'", flush=True)

    for msg in pubsub.listen():
        if msg["type"] == "message":
            handle_event(msg)

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"[worker] Error: {e}", flush=True)
            time.sleep(3)