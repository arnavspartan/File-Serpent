import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# This defines where each file type is moved to
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
DESTINATIONS = {
    'Documents': ['.pdf', '.docx', '.txt'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Videos': ['.mp4', '.avi', '.mov'],
    'Music': ['.mp3', '.wav', '.flac'],
    'Others': []  # Catch-all for other file types
}

# This creates the destination folders if they don't exist
for folder in DESTINATIONS.keys():
    os.makedirs(os.path.join(DOWNLOADS_FOLDER, folder), exist_ok=True)

class FileMoverHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_name, file_extension = os.path.splitext(event.src_path)
            moved = False

            # This moves the file to the appropriate folder
            for folder, extensions in DESTINATIONS.items():
                if file_extension.lower() in extensions:
                    shutil.move(event.src_path, os.path.join(DOWNLOADS_FOLDER, folder))
                    moved = True
                    break

            # This moves the file to Others if no match found
            if not moved:
                shutil.move(event.src_path, os.path.join(DOWNLOADS_FOLDER, 'Others'))

def start_monitoring():
    event_handler = FileMoverHandler() #
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_FOLDER, recursive=False)
    observer.start()
    
    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitoring()
