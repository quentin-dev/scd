import pathlib
import re

_DEFAULT_TITLE = re.compile(r"([^\(]*\([0-9]{4}\)).*")


def strip_after_year(name: str) -> str:
    extension = pathlib.Path(name).suffix
    matches = _DEFAULT_TITLE.fullmatch(name)

    if matches is None:
        # FIXME: Log falling back to default
        return name

    title = matches.group(1)
    return f"{title}{extension}"


def get_folder_from_clean_name(name: str) -> str:

    name = name[:-4]
    indices = [occ.start() for occ in re.finditer(" ", name)]

    return f"{name[:indices[-2]]}{name[indices[-1]:]}"


def remove_year_from_folder(name: str) -> str:
    return name[:-6].strip()
