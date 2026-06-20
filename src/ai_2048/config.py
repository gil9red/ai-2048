#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import os
import shutil
import logging.config

from pathlib import Path
from typing import Any

from dotenv import load_dotenv, find_dotenv

BASE_DIR: Path

pyproject_path: str = find_dotenv("pyproject.toml")
if pyproject_path:
    BASE_DIR = Path(pyproject_path).parent

    dotenv_path: Path = BASE_DIR / ".env"
    example_path: Path = BASE_DIR / ".env.example"

    if not dotenv_path.exists() and example_path.exists():
        shutil.copyfile(example_path, dotenv_path)
        print(f"Created local configuration file: {dotenv_path}")

    load_dotenv(dotenv_path)
else:
    load_dotenv()
    BASE_DIR = Path.cwd()

OLLAMA_URL: str = os.getenv("OLLAMA_URL")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
FILE_LOG_LEVEL: str = os.getenv("FILE_LOG_LEVEL", "DEBUG").upper()

LOGS_DIR: Path = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_PATH: Path = BASE_DIR / "logging_config.json"
if CONFIG_PATH.exists():
    config_text: str = CONFIG_PATH.read_text(encoding="utf-8")

    config_text = config_text.replace("${LOG_LEVEL}", LOG_LEVEL)
    config_text = config_text.replace("${FILE_LOG_LEVEL}", FILE_LOG_LEVEL)
    config_text = config_text.replace(
        # NOTE: Separator is '/'
        "${LOGS_DIR}",
        LOGS_DIR.as_posix(),
    )

    LOGGING_CONFIG: dict[str, Any] = json.loads(config_text)
    logging.config.dictConfig(LOGGING_CONFIG)
else:
    logging.basicConfig(level=LOG_LEVEL)
    logging.warning(f"Logging configuration file not found at: {CONFIG_PATH}")
