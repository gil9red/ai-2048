#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import io
from logging import getLogger
from typing import Annotated

import ollama

from PIL import Image

from pydantic import BaseModel, Field, NonNegativeInt

from ai_2048.config import OLLAMA_URL, OLLAMA_MODEL

type Size4[T] = Annotated[list[T], Field(min_length=4, max_length=4)]


class GridResponse(BaseModel):
    game_identified: str = Field(description="Name of the game in the image")
    grid: Size4[Size4[NonNegativeInt]] | None = Field(
        default=...,
        description="4x4 grid of tiles. Empty tiles MUST be represented as 0. "
        "Negative numbers are strictly prohibited by the schema type.",
    )


log = getLogger(__name__)


client = ollama.Client(host=OLLAMA_URL)


PROMPT: str = """
1. Identify the game in the image.
2. If the game is NOT "2048" (e.g., it is Minesweeper, Sudoku, etc.), or contains invalid tiles like 1 or 3:
   - Set "game_identified" to the actual game name.
   - Set "grid" to null.
3. If it IS 2048:
   - Set "game_identified" to "2048".
   - Extract tiles (only powers of 2: 2, 4, 8...).
   - Empty tile = 0.
   - For empty tiles, ALWAYS use the integer 0.
   - Every single value in the grid matrix MUST be a positive power of 2 or exactly 0.
   - Absolutely FORBIDDEN to use negative numbers, minus signs (-), or values like null/-1.
Strictly JSON.
"""

DEFAULT_IMAGE_MAX_SIZE: int = 800


def preprocess_image(
    image_bytes: bytes,
    max_size: int = DEFAULT_IMAGE_MAX_SIZE,
) -> bytes:
    with Image.open(io.BytesIO(image_bytes)) as img:
        log.debug(f"img: {img}")
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            log.debug(f"img thumbnail: {img}")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()


def detect_game_grid(img_data: bytes) -> GridResponse:
    img_data = preprocess_image(img_data)

    response = client.generate(
        model=OLLAMA_MODEL,
        prompt=PROMPT,
        images=[img_data],
        format=GridResponse.model_json_schema(),
        options={
            "temperature": 0,
            "num_predict": 512,
        },
        think=False,
    )
    log.debug(f"Response AI: {response}")

    tps = response.eval_count / (response.eval_duration / 1e9)
    log.debug(
        f"AI Statistics:\n"
        f"Generation speed: {tps:.2f} tokens/sec\n"
        f"Total time: {response.total_duration / 1e9:.2f} sec\n"
        f"Tokens (Prompt/Completion): {response.prompt_eval_count} / {response.eval_count}\n"
    )

    rs_text: str = response.response or response.thinking
    log.debug(f"Response text: {rs_text}")

    return GridResponse.model_validate_json(rs_text)
