import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from deephaven import DynamicTableWriter, Types as dht
from deephaven.DBTimeUtils import currentTime

def make_file_event_table_writer():
    columnNames = ["Timestamp", "Type", "Path", "IsDir"]
    columnTypes = [dht.datetime, dht.string, dht.string, dht.bool_]
    return DynamicTableWriter(columnNames, columnTypes)

file_event_table_writer = make_file_event_table_writer()
file_events = file_event_table_writer.getTable()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        now = currentTime()
        print(f"WATCHER EVENT: now={now}, event={event}")
        file_event_table_writer.logRow(now, event.event_type, event.src_path, event.is_directory)


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

w = Watcher(dir="/data", recursive=True)
w.start()

# try:
#     while True:
#         print("WATCHER: ALIVE")
#         time.sleep(5)
# except KeyboardInterrupt:
#     print("WATCHER: SHUTDOWN")
#     w.stop()

# print("WATCHER: DONE")
