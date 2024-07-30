import tkinter as tk
import traceback
import logging
from datetime import datetime

from pathlib import Path
from typing import Optional


def find_project() -> Path:
    project_path = Path(__file__).parent.parent
    if not project_path.is_dir():
        project_path = Path.cwd()
    print(f"Project path: {project_path}")
    return project_path


def setup_logger(path: Optional[Path | str]) -> logging.Logger:
    log_folder = Path(path).joinpath("log")
    log_folder.mkdir(exist_ok=True)
    log_path = log_folder.joinpath(Path('log_' + datetime.now().strftime("%y%m%d_%H%M%S") + '.txt'))
    logger = logging.getLogger('GUI')
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.debug('Logging setup finished.')

    return logger


class MyTk(tk.Tk):
    def __init__(self, logger, *args, **kwargs):
        self.logger = logger
        self.screen_width = self.screen_height = 0
        super().__init__(*args, **kwargs)

    def report_callback_exception(self, exc, val, tb):
        trace = ''.join(traceback.format_exception(exc, val, tb))
        self.logger.error(f"Exception: \n{trace}")
        super().report_callback_exception(exc, val, tb)
