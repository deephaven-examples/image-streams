import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from deephaven import DynamicTableWriter, Types as dht, currentTime

def make_file_event_table_writer():
    columnNames = ["Timestamp", "Type", "Path"]
    columnTypes = [dht.datetime, dht.string, dht.string]
    return DynamicTableWriter(columnNames, columnTypes)

file_event_table_writer = make_file_event_table_writer()
file_events = file_event_table_writer.getTable()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        # print("WATCHER: event: ", event)

        # elif event.event_type == 'created':
        #     # Take any action here when a file is first created.
        #     print "WATCHER: Received created event - %s." % event.src_path

        # elif event.event_type == 'modified':
        #     # Taken any action here when a file is modified.
        #     print "WATCHER: Received modified event - %s." % event.src_path

        now = currentTime()
        print(f"WATCHER EVENT: now={now}, event={event}")
        file_event_table_writer.logRow(now, event.event_type, event.src_path)


class Watcher:
    def __init__(self, dir:str recursive:bool=False):
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




w = Watcher(dir="/data", recursive=True)
w.start()

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print "Exiting"
    w.stop()
