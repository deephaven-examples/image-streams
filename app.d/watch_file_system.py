import os
import time
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
from deephaven import DynamicTableWriter
import deephaven.dtypes as dht

from deephaven.time import now as currentTime

def make_file_event_table_writer():
    columnT={"Timestamp":dht.DateTime, "Type":dht.string, "Path":dht.string, "IsDir":dht.bool_}
    return DynamicTableWriter(columnT)

file_event_table_writer = make_file_event_table_writer()
file_events = file_event_table_writer.table


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        now = currentTime()
        print(f"WATCHER EVENT: now={now}, event={event}")
        file_event_table_writer.write_row(now, event.event_type, event.src_path, event.is_directory)


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

image_dir = "/data/images/"
os.makedirs(image_dir, exist_ok=True)
w = Watcher(dir=image_dir, recursive=True)
w.start()
