#!/usr/bin/env python3

"""
multi_price_tracker.py
-----------------------
Tracks the price of a product across Amazon, Flipkart, and Snapdeal using product keywords.
Stores historical price data in a CSV file.
Requirements: requests, beautifulsoup4
Optional: matplotlib (for trend visualization)
"""

import requests
from bs4 import BeautifulSoup
import csv
import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

def fetch_amazon(keyword):
    url = f"https://www.amazon.in/s?k={keyword.replace(' ', '+')}"
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.select_one('h2 a span')
        price = soup.select_one('.a-price-whole')
        link = soup.select_one('h2 a')

        if title and price and link:
            return {
                "platform": "Amazon",
                "title": title.text.strip(),
                "price": price.text.strip().replace(',', ''),
                "url": "https://www.amazon.in" + link['href']
            }
    except Exception as e:
        print(f"[Amazon] Error: {e}")
    return None

def fetch_flipkart(keyword):
    url = f"https://www.flipkart.com/search?q={keyword.replace(' ', '+')}"
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.select_one('._4rR01T') or soup.select_one('.s1Q9rs')
        price = soup.select_one('._30jeq3')
        link = title.parent if title else None

        if title and price and link:
            return {
                "platform": "Flipkart",
                "title": title.text.strip(),
                "price": price.text.strip()[1:].replace(',', ''),
                "url": "https://www.flipkart.com" + link['href']
            }
    except Exception as e:
        print(f"[Flipkart] Error: {e}")
    return None

def fetch_snapdeal(keyword):
    url = f"https://www.snapdeal.com/search?keyword={keyword.replace(' ', '%20')}"
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.select_one('.product-title')
        price = soup.select_one('.product-price')
        link = title.parent if title else None

        if title and price and link:
            return {
                "platform": "Snapdeal",
                "title": title.text.strip(),
                "price": price.text.strip().replace('Rs. ', '').replace(',', ''),
                "url": "https://www.snapdeal.com" + link['href']
            }
    except Exception as e:
        print(f"[Snapdeal] Error: {e}")
    return None

def save_to_csv(data, keyword):
    filename = f"{keyword.replace(' ', '_')}_price_history.csv"
    today = datetime.date.today().isoformat()

    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for entry in data:
            writer.writerow([today, entry['platform'], entry['title'], entry['price'], entry['url']])

    print(f"✅ Data saved to {filename}")

def main():
    keyword = input("🔎 Enter product keyword: ").strip()
    results = []

    print("\n⏳ Fetching prices...")

    for func in [fetch_amazon, fetch_flipkart, fetch_snapdeal]:
        result = func(keyword)
        if result:
            results.append(result)

    if results:
        for r in results:
            print(f"\n📌 {r['platform']}")
            print(f"Title: {r['title']}")
            print(f"Price: ₹{r['price']}")
            print(f"Link: {r['url']}")

        save_to_csv(results, keyword)
    else:
        print("⚠️ Could not retrieve data. Try again later or with a different keyword.")

if __name__ == "__main__":
    main()
