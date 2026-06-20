#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import unittest
from pathlib import Path

from ai_2048.vision import detect_game_grid

DIR: Path = Path(__file__).resolve().parent
PATH_DATA: DIR = DIR / "data"


class TestVision(unittest.TestCase):
    def test_invalid(self):
        for file_name in [
            "invalid-tetris.png",
            "invalid-tic-tac-toe.png",
            "invalid-minesweeper.png",
            "invalid-sudoku.png",
        ]:
            with self.subTest(file_name=file_name):
                img_data: bytes = (PATH_DATA / file_name).read_bytes()
                result = detect_game_grid(img_data)
                self.assertIsNone(result.grid)
                self.assertNotEqual(result.game_identified, "2048")

    def test_valid_adamalston_github_io_2048(self):
        for file_name, expected_grid in [
            (
                "adamalston.github.io_2048__1.png",
                [[0, 0, 0, 2], [0, 0, 0, 0], [0, 0, 0, 2], [0, 0, 0, 0]],
            ),
            (
                "adamalston.github.io_2048__2.png",
                [[8, 2, 0, 0], [4, 0, 0, 2], [4, 0, 0, 0], [0, 0, 0, 0]],
            ),
            (
                "adamalston.github.io_2048__3.png",
                [[2, 4, 8, 4], [0, 0, 16, 2], [0, 0, 2, 8], [0, 2, 0, 2]],
            ),
            (
                "adamalston.github.io_2048__4.png",
                [[32, 2, 0, 2], [2, 16, 4, 2], [16, 8, 0, 0], [4, 2, 0, 0]],
            ),
            (
                "adamalston.github.io_2048__5.png",
                [[2, 4, 32, 4], [2, 2, 64, 2], [8, 4, 32, 8], [4, 8, 4, 2]],
            ),
        ]:
            with self.subTest(file_name=file_name):
                img_data: bytes = (PATH_DATA / file_name).read_bytes()
                result = detect_game_grid(img_data)
                self.assertEqual(result.game_identified, "2048")
                self.assertEqual(result.grid, expected_grid)

    def test_valid_mgarciaisaia_github_io_2048(self):
        for file_name, expected_grid in [
            (
                "mgarciaisaia.github.io_2048__1.png",
                [[2, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            ),
            (
                "mgarciaisaia.github.io_2048__2.png",
                [[0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 8, 2], [0, 0, 0, 4]],
            ),
            (
                "mgarciaisaia.github.io_2048__3.png",
                [[0, 4, 2, 4], [0, 0, 16, 4], [0, 0, 2, 0], [0, 2, 0, 0]],
            ),
            (
                "mgarciaisaia.github.io_2048__4.png",
                [[2, 2, 2, 0], [128, 4, 4, 0], [16, 8, 0, 0], [4, 0, 2, 0]],
            ),
            (
                "mgarciaisaia.github.io_2048__5.png",
                [[2, 8, 2, 2], [16, 32, 16, 2], [4, 128, 4, 4], [2, 4, 2, 2]],
            ),
        ]:
            with self.subTest(file_name=file_name):
                img_data: bytes = (PATH_DATA / file_name).read_bytes()
                result = detect_game_grid(img_data)
                self.assertEqual(result.game_identified, "2048")
                self.assertEqual(result.grid, expected_grid)

    def test_valid_paradite_github_io_2048(self):
        for file_name, expected_grid in [
            (
                "paradite.github.io_2048__1.png",
                [[0, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 0], [2, 0, 0, 0]],
            ),
            (
                "paradite.github.io_2048__2.png",
                [[0, 0, 0, 0], [2, 0, 0, 0], [2, 0, 2, 0], [8, 0, 0, 0]],
            ),
            (
                "paradite.github.io_2048__3.png",
                [[0, 0, 8, 2], [2, 2, 32, 2], [0, 0, 0, 32], [8, 4, 2, 4]],
            ),
            (
                "paradite.github.io_2048__4.png",
                [[2, 0, 0, 0], [2, 64, 0, 2], [32, 64, 0, 0], [4, 4, 4, 0]],
            ),
            (
                "paradite.github.io_2048__5.png",
                [[8, 4, 2, 4], [16, 256, 64, 8], [4, 2, 2, 0], [2, 0, 2, 0]],
            ),
        ]:
            with self.subTest(file_name=file_name):
                img_data: bytes = (PATH_DATA / file_name).read_bytes()
                result = detect_game_grid(img_data)
                self.assertEqual(result.game_identified, "2048")
                self.assertEqual(result.grid, expected_grid)

    def test_valid_tpaddon_github_io_2048(self):
        for file_name, expected_grid in [
            (
                "tpaddon.github.io_2048__1.png",
                [[0, 2, 0, 0], [0, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0]],
            ),
            (
                "tpaddon.github.io_2048__2.png",
                [[2, 8, 4, 2], [0, 0, 4, 4], [0, 0, 0, 8], [2, 0, 0, 2]],
            ),
            (
                "tpaddon.github.io_2048__3.png",
                [[8, 2, 8, 2], [64, 4, 0, 0], [8, 0, 0, 2], [4, 0, 0, 0]],
            ),
            (
                "tpaddon.github.io_2048__4.png",
                [[4, 2, 64, 32], [0, 16, 32, 8], [0, 4, 8, 4], [0, 2, 4, 8]],
            ),
            (
                "tpaddon.github.io_2048__5.png",
                [[2, 4, 32, 2], [2, 128, 4, 2], [4, 16, 64, 8], [2, 8, 2, 4]],
            ),
            (
                "tpaddon.github.io_2048__6.png",
                [[4, 16, 2, 2], [32, 256, 2, 4], [512, 16, 16, 16], [4096, 2, 8, 2]],
            ),
        ]:
            with self.subTest(file_name=file_name):
                img_data: bytes = (PATH_DATA / file_name).read_bytes()
                result = detect_game_grid(img_data)
                self.assertEqual(result.game_identified, "2048")
                self.assertEqual(result.grid, expected_grid)

    def test_valid_console(self):
        img_data: bytes = (PATH_DATA / "console.png").read_bytes()
        result = detect_game_grid(img_data)

        expected_grid = [[1024, 128, 64, 16], [2, 2, 0, 4], [0, 0, 0, 4], [0, 0, 0, 0]]
        self.assertEqual(result.game_identified, "2048")
        self.assertEqual(result.grid, expected_grid)

    def test_valid_screenshot(self):
        img_data: bytes = (PATH_DATA / "screenshot.png").read_bytes()
        result = detect_game_grid(img_data)

        expected_grid = [[0, 0, 0, 256], [0, 2, 0, 128], [0, 0, 16, 64], [2, 4, 4, 16]]
        self.assertEqual(result.game_identified, "2048")
        self.assertEqual(result.grid, expected_grid)

    def test_valid_game_full(self):
        img_data: bytes = (PATH_DATA / "game_full.jpg").read_bytes()
        result = detect_game_grid(img_data)

        expected_grid = [
            [4, 8, 16, 32],
            [512, 256, 128, 64],
            [1024, 2048, 4096, 8192],
            [131072, 65536, 32768, 16384],
        ]
        self.assertEqual(result.game_identified, "2048")
        self.assertEqual(result.grid, expected_grid)


if __name__ == "__main__":
    unittest.main()
