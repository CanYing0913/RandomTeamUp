import datetime
import tkinter as tk
import json
import random
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path

from .MyTk import MyTk, ScrollableNotebook, find_project, setup_logger


class App:
    __slots__ = ['project', 'logger', 'root', 'width', 'height', 'font', 'data', 'container']

    def __init__(self):
        self.project: Path = find_project()
        self.project.joinpath('record').mkdir(exist_ok=True)
        self.logger = setup_logger(self.project)
        self.root = MyTk(self.logger)
        self.root.title("App")

        width, height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.width, self.height = width // 2, height // 2
        center_x = (width - self.width) // 2
        center_y = (height - self.height) // 2

        self.root.geometry(f'{self.width}x{self.height}+{center_x}+{center_y}')

        # Customize
        self.font = font.Font(family="Helvetica", size=12, weight="bold")

        # Data
        datapath = self.project.joinpath('data').joinpath('database.json')
        assert datapath.exists() and datapath.is_file(), "Database file not found."
        with open(self.project.joinpath('data').joinpath('database.json'), 'r') as f:
            self.data = json.load(f)

        # Set up the listbox and scrollbar
        self.container = tk.Frame(self.root)
        self.container.pack(expand=True, fill='both')
        self.create_manager()
        self.create_options()
        self.create_group()

    def create_manager(self):
        manager_frame = tk.Frame(self.container)
        manager_frame.pack(side=tk.LEFT, fill='both', expand=True)
        self.container.manager = manager_frame

        listbar_frame = tk.Frame(manager_frame)
        listbar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(listbar_frame, orient=tk.VERTICAL)
        listbox = tk.Listbox(listbar_frame, height=10, width=20, yscrollcommand=scrollbar.set,
                             font=self.font, justify='center')
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        listbox.bind('<Delete>', self.remove_member)
        listbox.bind('<BackSpace>', self.remove_member)
        manager_frame.member_list = listbox
        manager_frame.member_list_scrollbar = scrollbar

        # Set up the input entry and buttons
        entry_frame = tk.Frame(manager_frame)
        entry_frame.pack(padx=10, pady=10)

        entry_label = tk.Label(entry_frame, text="Name:")
        entry_label.pack(side=tk.LEFT)
        entry = tk.Entry(entry_frame, width=10)
        manager_frame.entry = entry
        entry.bind('<Return>', self.add_member)
        entry.pack(side=tk.LEFT, padx=5)

        button_frame = tk.Frame(manager_frame)
        button_frame.pack(padx=10, pady=10)

        add_button = tk.Button(button_frame, text="Add", command=self.add_member)
        add_button.pack(side=tk.LEFT, pady=5)

        remove_button = tk.Button(button_frame, text="Remove", command=self.remove_member)
        remove_button.pack(side=tk.LEFT, pady=5)

        # Refresh listbox with initial data
        self.refresh_listbox()

    def create_options(self):
        option_frame = tk.Frame(self.container)
        option_frame.pack(side=tk.LEFT, fill='both', expand=True)
        self.container.option = option_frame

        def on_entry_change(*args):
            """Update the scale when the entry changes."""
            try:
                value = int(entry_var.get())
                scale.set(value)
            except ValueError:
                pass  # Ignore invalid input in the entry

        def on_scale_change(value):
            """Update the entry when the scale changes."""
            entry_var.set(value)

        # Set up the variable to store the value
        value_var = tk.IntVar()
        value_var.set(1)
        self.container.option.group_var = value_var

        # Entry widget
        entry_var = tk.StringVar()
        entry_var.set(str(value_var.get()))

        entry_frame = tk.Frame(option_frame)
        entry_frame.pack(padx=10, pady=10)
        label = tk.Label(entry_frame, text="Members/Team:")
        label.pack(side=tk.LEFT)
        entry = tk.Entry(entry_frame, textvariable=entry_var, width=2, justify='center')
        entry.pack(side=tk.LEFT, padx=5)

        # Scale (slider) widget
        scale = tk.Scale(option_frame, from_=1, to=6, width=15, length=150, orient='horizontal',
                         showvalue=False, variable=value_var, command=on_scale_change)
        scale.pack(pady=5)

        button = tk.Button(option_frame, text="TeamUP!", command=self.team_up)
        button.pack(padx=5)

        # Set up tracing
        entry_var.trace_add("write", on_entry_change)

    def create_group(self):
        group_frame = tk.Frame(self.container)
        group_frame.pack(side=tk.LEFT, fill='both', expand=True)
        self.container.group = group_frame

        title = tk.Label(group_frame, text="Groups Generated")
        title.pack(side=tk.TOP)

        notebook = ScrollableNotebook(group_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        self.container.group.notebook = notebook

    def refresh_listbox(self):
        """Refresh the listbox to display the current population list."""
        self.container.manager.member_list.delete(0, tk.END)
        for index, member in enumerate(self.data['members']):
            self.container.manager.member_list.insert(tk.END, member)

    def add_member(self, event=None):
        """Add a member to the population list."""
        name = self.container.manager.entry.get()
        if name:
            name = f'180cm-{name}'
            self.data['members'].append(name)
            self.container.manager.entry.delete(0, tk.END)
            self.refresh_listbox()
            self.logger.debug(f'{name} added to database.')
        else:
            messagebox.showwarning("Input Error", "Please enter a name")

    def remove_member(self, event=None):
        """Remove the selected member from the population list."""
        try:
            selected_index = self.container.manager.member_list.curselection()[0]
            self.logger.debug(f'{self.data['members'][selected_index]} removed from database.')
            self.data['members'].pop(selected_index)
            self.refresh_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a member to remove")

    def team_up(self):
        # Remove current assignments
        # for tab in self.container.group.notebook.tabs():
        #     self.container.group.notebook.nametowidget(tab).destroy()
        self.container.group.notebook.remove_all_tabs()

        population = self.data['members']
        group_size = self.container.option.group_var.get()

        # Shuffle the list to randomize
        random.shuffle(population)

        # Split the list into groups
        teams = [population[i:i + group_size] for i in range(0, len(population), group_size)]

        teams_dict = {f'Team {idx:2d}': team for idx, team in enumerate(teams)}

        with open(self.project.joinpath('record').joinpath(
                datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.json'), 'w') as f:
            json.dump(teams_dict, f, indent=4)

        for idx, team in enumerate(teams):
            cur_tab = ttk.Frame(self.container.group.notebook)
            group_list = tk.Listbox(cur_tab, justify='center', width=15)
            group_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            for member in team:
                group_list.insert(tk.END, member)

            self.container.group.notebook.add(cur_tab, text=f'team {idx:2d}')

    def gui(self):
        try:
            self.root.mainloop()
        finally:
            with open(self.project.joinpath('data').joinpath('database.json'), 'w') as f:
                json.dump(self.data, f, indent=4)
