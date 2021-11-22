
import os
import time

def watch(dir, sleep=1):
    old = set()
    try:
        while True:
            print("WATCHER: ALIVE")
            new = set(os.listdir(dir))
            changes = new-old
            print(f"WATCHER: now={time.time()} changes={changes} new={new}")
            old = new
            time.sleep(sleep)
    except KeyboardInterrupt:
        print("WATCHER: SHUTDOWN")
        w.stop()
        
watch("./data", 5)