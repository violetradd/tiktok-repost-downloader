#!/usr/bin/env python
"""Download all Repost videos for a given TikTok account.

This requires an actual TikTok account, Firefox, ffmpeg, and to be logged in to the
TikTok account in Firefox.
"""
from __future__ import annotations

import argparse
import json
import logging
import pathlib
import shutil
import time
from typing import TYPE_CHECKING

import yt_dlp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

if TYPE_CHECKING:
    import os


def setup_logging(level: int = logging.INFO) -> None:
    """Set up the root logger for this script.

    This also impacts other APIs which use the root logger or a descendent without
    customizing its own log levels.

    Arguments:
        level: logging level.

    """
    logging.basicConfig(
        format="%(processName)s: %(levelname)s: %(message)s",
        level=level,
    )


DOWNLOAD_DIR = "tiktok_videos"
REPOSTED_URLS_FILE = "reposted_urls.json"


def fetch_reposted_urls(
    username: str,
    hide_browser: bool,  # noqa: FBT001
    profile_get_timeout: int = 5,
    reposts_tab_click_timeout: int = 5,
    reposts_urls_file: os.PathLike = pathlib.Path(REPOSTED_URLS_FILE),
) -> list[str]:
    """Fetch reposted TikTok video URLs and save them to a JSON file.

    Arguments:
        username: TikTok username.

        hide_browser: hide the Firefox browser when running Selenium.

        profile_get_timeout: seconds to wait for the profile to be fetched.

        reposts_tab_click_timeout: seconds to wait after clicking the `reposts_urls`
                                   tab.

        reposts_urls_file: the path to save the results of the reposts URLs tab to.

    Returns:
        A list of reposts URLs.

    """
    options = webdriver.FirefoxOptions()
    if hide_browser:
        options.add_argument("--headless")
    try:
        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=options,
        )
    except Exception:
        logging.exception(
            "Could not initialize Selenium Driver. Did you install Firefox?",
        )
        raise

    try:
        profile_url = f"https://www.tiktok.com/@{username}?lang=en"
        driver.get(profile_url)
        time.sleep(profile_get_timeout)

        # Click the "Reposts" tab
        reposts_tab = driver.find_element(By.XPATH, "//span[text()='Reposts']")
        reposts_tab.click()
        time.sleep(reposts_tab_click_timeout)

        # Scroll and collect reposts
        reposts = set()
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            video_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/video/']")
            for video in video_elements:
                reposts.add(video.get_attribute("href"))

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        reposts_list = list(reposts)
        with reposts_urls_file.open("w") as json_file:
            json.dump(reposts_list, json_file, indent=4)
        logging.info("Reposted URLs saved to %s", reposts_urls_file)

    except Exception:
        logging.exception(
            "A failure occurred when downloading/saving the reposts list URLs",
        )
        raise
    else:
        return reposts_list
    finally:
        driver.quit()


def download_videos(video_urls: list[str], download_dir: os.PathLike) -> None:
    """Download TikTok videos using yt-dlp.

    Arguments:
        video_urls: a list of repost videos to download.

        download_dir: destination to put the downloaded videos.

    """
    try:
        download_dir.mkdir(exist_ok=True, parents=True)
    except OSError:
        logging.exception("Could not create the output directory: %s.", download_dir)
        raise

    ydl_opts = {
        "outtmpl": str(download_dir / "%(id)s.%(ext)s"),  # Simplified filename format
        "format": "mp4",
        "quiet": False,
        "windowsfilenames": True,
        "ignoreerrors": True,
        "sleep_interval": 2,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_urls)
    except Exception:
        logging.exception("An error encountered when downloading videos")
        raise


def main(argv: list[str] | None = None) -> int:
    """Eponymous main."""
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Output debug logging messages.",
    )
    argparser.add_argument(
        "--download-dir",
        help="Where to store downloaded videos.",
        default=DOWNLOAD_DIR,
    )
    argparser.add_argument(
        "--show-browser",
        action="store_true",
        default=False,
        help="Show browser when running Selenium.",
    )
    argparser.add_argument(
        "--reposted-urls-file",
        help="Where to cache/output the reposted URLs.",
        default=REPOSTED_URLS_FILE,
    )
    argparser.add_argument(
        "--username",
        help="TikTok username. You will be prompted if a username is not provided.",
    )
    args = argparser.parse_args(argv)

    setup_logging(level=logging.DEBUG if args.debug else logging.INFO)

    if shutil.which("ffmpeg") is None:
        logging.error("ffmpeg executable not found in $PATH / %PATH%.")
        return 1

    username = args.username or input("Enter your TikTok username: ")

    try:
        logging.info("Fetching reposted URLs for %s", username)
        reposted_urls = fetch_reposted_urls(
            username,
            hide_browser=not args.show_browser,
            reposts_urls_file=pathlib.Path(args.reposted_urls_file),
        )

        logging.info("Starting video downloads (this will take a while)...")
        download_videos(reposted_urls, download_dir=pathlib.Path(args.download_dir))
    except Exception:  # noqa: BLE001
        logging.debug("Exception raised", exc_info=True)
        return 1
    logging.info("Video download process completed!")

    return 0


if __name__ == "__main__":
    main()
