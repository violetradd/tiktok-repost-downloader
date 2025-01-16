
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
   - FFmpeg is required by yt-dlp for post-processing tasks (e.g., adding metadata).
   - [Download FFmpeg](https://ffmpeg.org/download.html)
   - Add FFmpeg to your system PATH.

3. **Git** (Optional)
   - For downloading the repository.
   - [Download Git](https://git-scm.com/)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/violetradd/tiktok-repost-downloader.git
   cd tiktok-repost-downloader
   ```

   Or you could just download the source from GitHub if you want.

2. **Install Dependencies**:
   The script automatically installs Python dependencies (if missing):
   - `selenium`
   - `webdriver-manager`
   - `yt-dlp`

   If you prefer manual installation:
   ```bash
   pip install selenium webdriver-manager yt-dlp
   ```

3. **Install FFmpeg**:
   Follow the [FFmpeg installation guide](https://ffmpeg.org/download.html) to install and add FFmpeg to your system PATH.

---

## Usage

1. **Run the Script**:
   ```bash
   python app.py
   ```

2. **Enter Your TikTok Username**:
   When prompted, enter your TikTok username.

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
- To update the dependencies manually:
  ```bash
  pip install --upgrade selenium webdriver-manager yt-dlp
  ```
- Ensure you're logged into TikTok on Firefox and that your profile is set to 'Pubic'
---

## License
This project is licensed under The Unlicense. Go wild.
