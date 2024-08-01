import sys

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning
build_exe_options = {
    "build_exe": "dist",
    "include_files": [
        "record",
        "log",
        "data",
    ],

}
build_msi_options = {}
build_mac_options = {}
build_appimage_options = {}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable(
        "main.py",
        copyright="Copyright (C) 2024 CanYing0913.github.io",
        base=base,
        # base="Console",
        icon="icon.ico",
        target_name="TeamUP180",
    )
]

setup(
    name="180 TeamUP",
    version="0.1",
    description="Ramdom TeamUP generator for 180 PUBG custom matches",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": build_msi_options,
        "bdist_mac": build_mac_options,
        "bdist_appimage": build_appimage_options,
    },
    executables=executables,
)