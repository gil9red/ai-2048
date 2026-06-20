#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from logging import getLogger

from ai_2048.third_party.eshirazi_2048_bot.board_score_heuristics import (
    perfect_heuristic,
)
from ai_2048.third_party.eshirazi_2048_bot.board_score_strategy import (
    ExpectimaxStrategy,
)
from ai_2048.third_party.eshirazi_2048_bot.moves import Move, UP, DOWN, LEFT, RIGHT

from ai_2048.vision import detect_game_grid, GridResponse
from ai_2048.third_party.eshirazi_2048_bot.board import Board

log = getLogger(__name__)
strategy = ExpectimaxStrategy(perfect_heuristic)


def is_valid(cell: int) -> bool:
    valid_values: tuple[int, ...] = (
        0,
        2,
        4,
        8,
        16,
        32,
        64,
        128,
        256,
        512,
        1024,
        2048,
        4096,
        8192,
        16384,
        32768,
        65536,
        131072,
    )
    return cell in valid_values


def get_board_from_image(img_data: bytes) -> Board | None:
    rs: GridResponse = detect_game_grid(img_data)

    if rs.game_identified != "2048":
        log.warning(f"Not game '2048': {rs}")
        return None

    if rs.grid is None:
        log.warning("Not grid found")
        return None

    for row in rs.grid:
        for cell in row:
            if not isinstance(cell, int):
                raise ValueError(f"Must be integer ({cell}), but got {type(cell)}")
            if cell < 0:
                raise ValueError(f"Negative value {cell}")
            if not is_valid(cell):
                raise ValueError(f"Incorrect value {cell}")

    board = Board(rs.grid)
    log.debug(f"Board:\n{board}")

    if not board.has_legal_moves():
        log.warning("No legal moves")
        return None

    return board


def get_next_key(board: Board) -> str:
    move: Move = strategy.get_next_move(board)
    log.debug(f"Next move: {move}")

    key: str
    if move == UP:
        key = "ArrowUp"
    elif move == DOWN:
        key = "ArrowDown"
    elif move == LEFT:
        key = "ArrowLeft"
    elif move == RIGHT:
        key = "ArrowRight"
    else:
        raise ValueError(f"Unknown direction of movement: {move}")

    return key
