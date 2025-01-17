import os
import json
import subprocess
import sys
import time

# Ensure required packages are installed
REQUIRED_PACKAGES = ["selenium", "webdriver-manager", "yt-dlp"]

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

def fetch_reposted_urls(username, output_file="reposted_urls.json"):
    """Fetch reposted TikTok video URLs and save them to a JSON file."""
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    try:
        profile_url = f"https://www.tiktok.com/@{username}?lang=en"
        driver.get(profile_url)
        time.sleep(5)

        # Click the "Reposts" tab
        reposts_tab = driver.find_element(By.XPATH, "//span[text()='Reposts']")
        reposts_tab.click()
        time.sleep(5)

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
        with open(output_file, "w") as json_file:
            json.dump(reposts_list, json_file, indent=4)

        print(f"Reposted URLs saved to {output_file}")
        return reposts_list

    finally:
        driver.quit()

def download_videos(video_urls, output_dir="tiktok_videos"):
    """Download TikTok videos using yt-dlp."""
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),  # Simplified filename format
        'format': 'mp4',
        'quiet': False,
        'windowsfilenames': True,
        'ignoreerrors': True,
        'sleep_interval': 2,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_urls)
    except Exception as e:
        print(f"Error encountered: {str(e)}")

if __name__ == "__main__":
    username = input("Enter your TikTok username: ")

    reposted_urls = fetch_reposted_urls(username)

    print("Starting video downloads...")
    download_videos(reposted_urls)
    print("Video download process completed!")