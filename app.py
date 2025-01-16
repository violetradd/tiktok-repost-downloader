import os
import json
import re
import subprocess
import sys
from datetime import datetime

# Ensure required packages are installed
REQUIRED_PACKAGES = [
    "selenium",
    "webdriver-manager",
    "yt-dlp"
]

def install_dependencies():
    """Install missing dependencies."""
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package.replace("-", "_"))  # Import to check if installed
        except ImportError:
            print(f"Installing missing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_dependencies()

import yt_dlp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time

def fetch_reposted_urls(username, output_file="reposted_urls.json"):
    """Fetch reposted TikTok video URLs and save them to a JSON file."""
    # Check if the output file exists and is not empty
    if os.path.exists(output_file):
        with open(output_file, "r") as json_file:
            try:
                data = json.load(json_file)
                if data:  # File exists and is not empty
                    print(f"Reposted URLs already exist in {output_file}. Skipping fetch.")
                    return data
            except json.JSONDecodeError:
                print(f"{output_file} is empty or invalid. Refetching URLs.")

    # Initialize WebDriver for Firefox
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Run without opening a browser window
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    try:
        # Navigate to profile page
        profile_url = f"https://www.tiktok.com/@{username}?lang=en"
        driver.get(profile_url)
        time.sleep(5)

        # Click the "Reposts" tab
        reposts_tab = driver.find_element(By.XPATH, "//span[text()='Reposts']")
        reposts_tab.click()
        time.sleep(5)  # Wait for the Reposts tab to load

        # Scroll and collect reposts
        reposts = set()
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Find all video elements on the page
            video_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/video/']")
            for video in video_elements:
                reposts.add(video.get_attribute("href"))  # Use a set to avoid duplicates

            # Scroll down to load more videos
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Allow time for new content to load

            # Check if we've reached the bottom of the page
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Save reposts to a JSON file
        reposts_list = list(reposts)
        with open(output_file, "w") as json_file:
            json.dump(reposts_list, json_file, indent=4)

        print(f"Reposted URLs saved to {output_file}")
        return reposts_list

    finally:
        driver.quit()

def sanitize_filename(title, max_length=100):
    """Remove invalid characters and truncate filename."""
    title = re.sub(r'[\\/*?:"<>|]', "", title)  # Remove invalid characters
    return title[:max_length]  # Truncate if longer than max_length

def log_error(error_message):
    """Log errors to a file."""
    with open("error_log.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {error_message}\n")

def progress_hook(d):
    """Hook to display progress and sanitize title during download."""
    if d['status'] == 'finished':
        original_title = d['info_dict'].get('title', 'video')
        sanitized_title = sanitize_filename(original_title)
        print(f"Downloaded and saved: {sanitized_title}")

def download_videos(video_urls, output_dir="tiktok_videos"):
    """Download TikTok videos using yt-dlp."""
    os.makedirs(output_dir, exist_ok=True)

    # yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title).50s.%(ext)s'),  # Truncate title to 50 characters
        'format': 'mp4',                                             # Preferred format
        'quiet': False,                                              # Show download progress
        'windowsfilenames': True,                                    # Adapt for Windows filename conventions
        'ignoreerrors': True,                                        # Skip errors
        'progress_hooks': [progress_hook],                           # Use the progress hook
        'postprocessors': [{'key': 'FFmpegMetadata'}],
        'sleep_interval': 2,                                         # Pause between downloads
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_urls)
    except Exception as e:
        log_error(f"Unexpected error: {str(e)}")
        print(f"Error encountered: {str(e)}. Check 'error_log.txt' for details.")

if __name__ == "__main__":
    # Prompt user for username
    username = input("Enter your TikTok username: ")

    # Fetch reposted URLs
    reposted_urls = fetch_reposted_urls(username)

    # Download videos
    print("Starting video downloads...")
    download_videos(reposted_urls)
    print("Video download process completed!")
