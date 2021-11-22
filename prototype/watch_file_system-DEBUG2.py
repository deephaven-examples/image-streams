import time
from watchgod import watch
import threading

def thread_function():
    for changes in watch("./data"):
        print(changes)
        now = time.time()
        print(f"WATCHER EVENT: now={now}, changes={changes}")

    print("THREAD EXITING")

print("WATCHER: STARTUP")
thread = threading.Thread(target=thread_function)
thread.start()

try:
    while True:
        print("WATCHER: ALIVE")
        time.sleep(5)
except KeyboardInterrupt:
    print("WATCHER: SHUTDOWN")
    w.stop()

print("WATCHER: DONE")
