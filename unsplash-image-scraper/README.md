# 📸 Unsplash Image Scraper

A Python script that uses Selenium to scrape the first 20 image URLs from Unsplash search results for a given keyword. Optionally, it can also download the images to a local folder.

---

## ✅ Features

- Scrapes image URLs from Unsplash using a keyword
- Saves URLs to `image_urls.txt`
- Optionally downloads the images to a `downloads/` folder
- Headless browser mode (no popups)
- Works with Brave, Google Chrome, or Chromium

---

## 📦 Prerequisites

Make sure the following are installed on your system:

- Python 3.7+
- Google Chrome, Chromium, or Brave
- ChromeDriver (matching your browser version)
- Python packages:
  - `selenium`
  - `requests`

### Install dependencies:

```bash
pip install selenium requests
