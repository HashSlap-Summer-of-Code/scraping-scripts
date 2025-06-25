#!/usr/bin/env python3

"""
Unsplash Image Scraper (Selenium)

Scrapes the first 20 image URLs from Unsplash search results for a given keyword.
Exports the URLs to a text file and optionally downloads the images to a folder.

Usage:
    python unsplash-image-scraper.py <keyword> [--download]
"""

import os
import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from shutil import which

def setup_driver():
    chrome_path = which("chrome") or which("google-chrome") or which("brave-browser")
    chromedriver_path = which("chromedriver")

    if not chrome_path or not chromedriver_path:
        print("[!] Chrome or ChromeDriver not found in PATH. Please install them.")
        sys.exit(1)

    chrome_options = Options()
    chrome_options.binary_location = chrome_path
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(chromedriver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def get_image_urls(keyword, limit=20):
    print(f"[i] Searching Unsplash for '{keyword}'...")
    driver = setup_driver()
    driver.get(f"https://unsplash.com/s/photos/{keyword}")

    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    images = driver.find_elements(By.TAG_NAME, "img")
    urls = []

    for img in images:
        src = img.get_attribute("src")
        if src and "images.unsplash.com" in src:
            urls.append(src)
        if len(urls) >= limit:
            break

    driver.quit()
    return urls

def save_urls(urls, filename="image_urls.txt"):
    with open(filename, "w") as f:
        for url in urls:
            f.write(url + "\n")
    print(f"[+] Saved {len(urls)} image URLs to {filename}")

def download_images(urls, folder="downloads"):
    os.makedirs(folder, exist_ok=True)
    print(f"[↓] Downloading {len(urls)} images to '{folder}'...")
    for i, url in enumerate(urls, 1):
        try:
            img_data = requests.get(url).content
            with open(os.path.join(folder, f"image_{i}.jpg"), "wb") as f:
                f.write(img_data)
            print(f"  → image_{i}.jpg downloaded")
        except Exception as e:
            print(f"  [!] Failed to download image {i}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python unsplash-image-scraper.py <keyword> [--download]")
        return

    keyword = sys.argv[1]
    should_download = "--download" in sys.argv

    urls = get_image_urls(keyword)
    if urls:
        save_urls(urls)
        if should_download:
            download_images(urls)

if __name__ == "__main__":
    main()
