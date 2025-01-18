
# TikTok Repost Downloader

A Python script to automate the process of downloading all videos from the "Reposts" tab of your TikTok profile. The script uses Selenium to fetch video URLs and yt-dlp to download the videos.

---

## Features
- Fetch all video URLs from the "Reposts" tab of a specified TikTok username.
- Download videos with yt-dlp, automatically handling filenames and metadata.
- Automatically installs required Python dependencies.
- Logs errors to a file for debugging.

---

## Requirements

Before running the script, ensure the following are installed:

1. **Python 3.7 or higher**
   - [Download Python](https://www.python.org/downloads/)
   - Make sure Python is added to your system PATH.

2. **FFmpeg**
   - FFmpeg is required by yt-dlp for post-processing tasks, e.g., adding metadata.
   - [Download FFmpeg](https://ffmpeg.org/download.html)
   - Add FFmpeg to your system PATH.

3. **Firefox**
   - The script is set up to work with Firefox because that's what I use and it's my repo so I make the rules.
   - [Download Firefox](https://www.mozilla.org/en-US/firefox/new/)
   - Make sure you're signed into TikTok in Firefox.

4. **Git** (Optional)
   - For downloading the repository.
   - [Download Git](https://git-scm.com/)

---

## Installation

1. **Install the Repository via Pip**:
   ```bash
   $ pip install https://github.com/violetradd/tiktok-repost-downloader.git
   ```
   [pipx](https://pipx.pypa.io/latest/) is highly recommended over pip. pipx does better application encapsulation/isolation than pip.

2. **Install FFmpeg**:
   Follow the [FFmpeg installation guide](https://ffmpeg.org/download.html) to install and add FFmpeg to your system PATH.

---

## Usage

1. **Run the Script**:
   ```bash
   $ tiktok-repost-downloader
   ```

2. **Enter Your TikTok Username**:
   When prompted, enter your TikTok username.

   You can alternatively specify your username on the commandline, e.g.,
   ```bash
   $ tiktok-repost-downloader --username <tiktok-username>
   ```

3. **Fetching URLs**:
   - The script will check if a `reposted_urls.json` file exists and is not empty.
   - If the file is missing or empty, the script will use Selenium to fetch all video URLs from your "Reposts" tab.

4. **Download Videos**:
   - The script will download videos to a folder named `tiktok_videos`.
   - Video titles are sanitized and truncated to avoid invalid filenames.

---

## Output Files
- **Downloaded Videos**:
  All downloaded videos will be saved in the `tiktok_videos` folder.
  
- **Error Logs**:
  Any errors encountered during the download process will be logged in `error_log.txt`.

---

## Notes
- Ensure that your TikTok profile has a "Reposts" tab; otherwise, the script will fail to fetch URLs.
- If the script encounters issues (e.g., unable to find elements), update your Selenium WebDriver or modify the XPaths/CSS Selectors in the code.
- To update the dependencies manually, do the following:
  ```bash
  # If using pip:
  $ pip install --upgrade selenium webdriver-manager yt-dlp
  # If using pipx:
  $ pipx upgrade tiktok-repost-downloader
  ```
- Ensure you're logged into TikTok on Firefox and that your profile is set to 'Pubic'
---

## License
This project is licensed under The Unlicense. Go wild.
