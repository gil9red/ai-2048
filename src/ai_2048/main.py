#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import argparse
import time

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from logging import getLogger

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)

from ai_2048.logic import get_board_from_image, get_next_key
from ai_2048.site_config import SiteConfig, SITE_CONFIGS

from ai_2048.third_party.eshirazi_2048_bot.board import Board

log = getLogger(__name__)


def get_element_screenshot(page: Page, selector: str) -> bytes | None:
    log.debug(f"Get screenshot by selector {selector!r}")
    try:
        locator = page.locator(selector)
        locator.wait_for(state="visible", timeout=5_000)
        return locator.screenshot()
    except PlaywrightTimeoutError as e:
        log.warning(f"Element {selector!r} not found\n{e}")
        return None


def wait_for_element_screenshot(page: Page, selector: str) -> bytes:
    while True:
        img_data: bytes | None = get_element_screenshot(page, selector)
        if img_data is not None:
            return img_data


def click_any_element(
    page: Page,
    selectors: list[str],
    timeout_ms: int = 1_000,
) -> bool:
    log.debug(f"Click any elements by: {selectors}")
    for selector in selectors:
        try:
            locator = page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout_ms)
            locator.click()
            log.info(f"Click on element {selector!r}")
            return True
        except PlaywrightTimeoutError:
            pass

    return False


def make_single_move(page: Page, site: SiteConfig) -> bool:
    timestamp_str: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    img_data: bytes = wait_for_element_screenshot(page, site.selector_board)
    log.debug(
        f"{timestamp_str}. Screenshot ({len(img_data)} bytes): {img_data[:50]}..."
    )

    board: Board | None = get_board_from_image(img_data)
    if board is None:
        return False

    key: str = get_next_key(board)
    page.keyboard.press(key)

    return True


def play_game_loop(page: Page, site: SiteConfig) -> None:
    step: int = 1
    while True:
        log.info(f"Step {step}. Site name {site.name!r}")
        try:
            click_any_element(page, selectors=site.selectors_retry)

            move_success: bool = make_single_move(page, site)
            if not move_success:
                continue

            step += 1

        finally:
            time.sleep(1)


def run_site(site: SiteConfig) -> None:
    log.info(f"Run {site.name!r}")

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)

        page = browser.new_page()
        page.set_default_timeout(timeout=10_000)

        log.info(f"Load: {site.url!r}")
        page.goto(site.url, wait_until="commit")

        play_game_loop(page, site)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Autonomous 2048 game player using Playwright and Qwen-VL"
    )
    parser.add_argument(
        "--sites",
        nargs="+",
        choices=[cfg.name for cfg in SITE_CONFIGS],
        help="Space-separated site configuration names to run. Runs all by default.",
    )
    args = parser.parse_args()

    selected_configs: list[SiteConfig] = (
        [cfg for cfg in SITE_CONFIGS if cfg.name in args.sites]
        if args.sites
        else SITE_CONFIGS
    )

    max_workers: int = len(selected_configs)

    log.info(
        f"Starting {max_workers} parallel automation tasks for: "
        f"{[cfg.name for cfg in selected_configs]}"
    )

    with ThreadPoolExecutor(
        max_workers=max_workers,
        thread_name_prefix="PlaywrightWorker",
    ) as executor:
        executor.map(run_site, selected_configs)

    log.info("Program execution completed. All workers have finished.")
