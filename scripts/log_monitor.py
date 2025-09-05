import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".log"):
            print(f"📡 Event detected: {event.event_type} → {event.src_path}")
            print(f"📁 New log detected: {event.src_path}")
            print("🔍 Running analyzer script...")
            subprocess.run(["python", "scripts/analyzer.py"])      

if __name__ == "__main__":
    path_to_watch = "logs"
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()
    print(f"🕵️‍♂️ Monitoring folder: {path_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
