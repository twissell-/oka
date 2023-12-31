import json
import logging
import os
import sys
from datetime import datetime

from oka.common import config

_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "oka.db")
logger = logging.getLogger(__name__)


def get(key: str):
    key = str(key)

    try:
        with open(_path, "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        with open(_path, "w") as data_file:
            json.dump({}, data_file)

        return get(key)
    except json.JSONDecodeError:
        with open(_path, "w") as data_file:
            json.dump({}, data_file)

        return get(key)

    if not data.get(key):
        return {}

    return data[key]


def set(key: str, value: dict):
    key = str(key)

    with open(_path, "r") as data_file:
        data = json.load(data_file)

    now = datetime.now()
    value["_last_update"] = now.strftime("%Y-%m-%d %H:%M:%S")
    data[key] = value

    with open(_path, "w") as data_file:
        json.dump(data, data_file, indent=2, sort_keys=True)
