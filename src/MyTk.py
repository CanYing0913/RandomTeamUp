import tkinter as tk
import sys
from tkinter import ttk
import traceback
import logging
from datetime import datetime

from pathlib import Path
from typing import Optional


def find_project() -> Path:
    if hasattr(sys, 'frozen'):
        project_path = Path.cwd()
    else:
        project_path = Path(__file__).parent.parent
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


class ScrollableNotebook(ttk.Notebook):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Create the canvas and scrollbar
        self.canvas = tk.Canvas(self, height=30)
        self.canvas.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.tab_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.tab_frame, anchor="nw")

        self.scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.TOP, fill=tk.X)

        # Pack the notebook itself below the scrollbar
        self.pack(expand=True, fill=tk.BOTH)

        # Update the scroll region
        self.tab_frame.bind("<Configure>", self._on_frame_configure)

        # Bind scroll event
        self.bind_all("<MouseWheel>", self._on_mouse_wheel)

        # To keep track of tab headers
        self.tab_headers = {}

    def _on_frame_configure(self, event):
        # Set the scroll region for the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel(self, event):
        # Scroll tabs horizontally with mouse wheel
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def add(self, child, **kw):
        """Add a new tab to the notebook and a corresponding tab label."""
        super().add(child, **kw)

        # Add the tab to the canvas frame
        tab_id = self.index("end") - 1  # Get index of the new tab
        tab_button = ttk.Label(self.tab_frame, text=kw['text'], relief="raised")
        tab_button.pack(side=tk.LEFT, padx=2)
        tab_button.bind("<Button-1>", lambda e, index=tab_id: self.select(index))
        self.tab_headers[tab_id] = tab_button

    def remove_all_tabs(self):
        """Remove all tabs and their corresponding labels."""
        for tab_id in self.tab_headers:
            self.forget(tab_id)  # Remove from notebook
            self.tab_headers[tab_id].destroy()  # Destroy the header
        self.tab_headers.clear()  # Clear the tab headers dictionary
