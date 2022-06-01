import time
# from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        now = time.time()
        print(f"WATCHER EVENT: now={now}, event={event}")


class Watcher:
    def __init__(self, dir:str, recursive:bool=False):
        self.observer = Observer()
        self.dir = dir
        self.recursive = recursive

    def start(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.dir, recursive=self.recursive)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()


print("WATCHER: STARTUP")

w = Watcher(dir="/Users/ckent/dev/OSS/image-streams/data", recursive=True)
w.start()

try:
    while True:
        print("WATCHER: ALIVE")
        time.sleep(5)
except KeyboardInterrupt:
    print("WATCHER: SHUTDOWN")
    w.stop()

print("WATCHER: DONE")
