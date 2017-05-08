from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import time

import logging
logger = logging.getLogger("bibsync")

class BibSourceHandler(PatternMatchingEventHandler):
    
    def __init__(self, src, func):
        super().__init__(patterns=src, ignore_directories=True)
        logger.debug("Initializing handler with patterns '{}'".format(self.patterns))
        self.func = func

    def on_modified(self, event):
        logger.debug("{} detected on '{}'.".format(
            type(event).__name__, event.src_path))
        self.func(event)

def watch(watch_paths, callback):
    logger.debug("Watch paths {}".format(watch_paths))

    observer = Observer()
    for path, files in watch_paths.items():
        patterns = ['*{}'.format(f) for f in files]
        event_handler = BibSourceHandler(patterns, callback)
        observer.schedule(event_handler, path)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()