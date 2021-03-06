import re

from os.path import basename
from urllib.parse import unquote
from pathlib import Path

import requests

import PySimpleGUI as sg

from scd.logic.naming import (
    strip_after_year,
    get_folder_from_clean_name,
    remove_year_from_folder,
)


def download_file(
    url: str, window: sg.Window, create_folder: bool = False, ignore_year: bool = False
):
    data = requests.get(url, allow_redirects=True, stream=True)
    decoded_url = unquote(data.url)
    filename = strip_after_year(basename(decoded_url))

    root = sg.user_settings_get_entry("-downloadroot-", ".")

    path_to = root

    if create_folder:
        folder = get_folder_from_clean_name(filename)

        if ignore_year:
            exp = re.compile(fr"{remove_year_from_folder(folder)} \([0-9]{{4}}\)")
            current_dirs = [
                basename(path) for path in Path(path_to).iterdir() if path.is_dir()
            ]

            if any((match := exp.match(dir) for dir in current_dirs)):
                folder = match.group(0)

        path_to = f"{path_to}/{folder}"
        Path(path_to).mkdir(exist_ok=True)

    fullpath = f"{path_to}/{filename}"

    content_length = data.headers["content-length"]
    size = int(content_length) if content_length is not None else 1024
    downloaded = 0

    with open(fullpath, "wb") as file:
        for chunk in data.iter_content(1024):
            window.write_event_value(
                "-INCREMENTDLPROGRESS-", round((downloaded / size) * 100)
            )
            file.write(chunk)
            downloaded += len(chunk)
