#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SiteConfig:
    url: str
    name: str
    selector_board: str
    selectors_retry: list[str] = field(default_factory=list)


SITE_CONFIGS: list[SiteConfig] = [
    SiteConfig(
        url="https://paradite.github.io/2048/",
        name="paradite",
        selector_board=".board",
        selectors_retry=[],
    ),
    SiteConfig(
        url="https://tpaddon.github.io/2048-dark-edition/",
        name="tpaddon",
        selector_board=".game-container",
        selectors_retry=[".retry-button"],
    ),
    SiteConfig(
        url="https://adamalston.github.io/2048/",
        name="adamalston",
        selector_board="#game-board",
        selectors_retry=[
            "#win-message #continue",
            "body:has(#lose-message) #newgame-button",
        ],
    ),
    SiteConfig(
        url="https://mgarciaisaia.github.io/2048",
        name="mgarciaisaia",
        selector_board=".game-container",
        selectors_retry=[
            ".game-won .keep-playing-button",
            ".game-over .retry-button",
        ],
    ),
]
