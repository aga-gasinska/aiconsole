import logging
from functools import lru_cache
from pathlib import Path
from typing import Callable

from watchdog.observers import Observer

from aiconsole.utils.BatchingWatchDogHandler import BatchingWatchDogHandler

_log = logging.getLogger(__name__)


class FileObserver:
    def __init__(self):
        self._observer = Observer()
        self.observing: list[Path] = []

    def start(self, file_paths: list[Path], action: Callable):
        _log.info(f"[{self.__class__.__name__}] Starting observer...")

        if self._observer.is_alive():
            self.stop()

        for file_path in file_paths:
            if not isinstance(file_path, Path):
                _log.error(f"[{self.__class__.__name__}] Not a valid filepath: {file_path}")
                continue

            self._setup_observer(file_path, action)
            self.observing.append(file_path)

        if self.observing:
            self._observer.start()
            _log.info(f"[{self.__class__.__name__}] Observing for changes: {', '.join(map(str, self.observing))}.")

    def stop(self):
        if self._observer.is_alive():
            self._observer.stop()
            self._observer.join()
            self.observing.clear()
            _log.info(f"[{self.__class__.__name__}] Observer stopped.")

    def _setup_observer(self, path: Path, action: Callable):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            _log.error(f"[{self.__class__.__name__}] Error creating directory {path.parent}: {e}")

        self._observer.schedule(
            BatchingWatchDogHandler(action, path.name),
            str(path.parent),
            recursive=False,
        )


@lru_cache
def file_observer() -> FileObserver:
    return FileObserver()
