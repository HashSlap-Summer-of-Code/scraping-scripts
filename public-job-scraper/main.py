"""
Scrapes job titles, company names, and job links from a static job board
(Real Python's demo site) and saves them to a timestamped JSON file.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def scrape_jobs(url: str, output_dir: str):
    """
    Fetches Python-related job listings from a static page and writes them to a timestamped JSON file.

    Args:
        url (str): The job board URL to scrape.
        output_dir (str): Directory to save the output JSON.
    """

    try:
        # Make the HTTP request
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error fetching the page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []

    # Parse job listings
    for job_card in soup.select('div.card-content'):
        title_tag = job_card.find('h2', class_='title')
        company_tag = job_card.find('h3', class_='company')
        link_tag = job_card.find('a', text='Apply')

        if title_tag and company_tag and link_tag:
            title = title_tag.text.strip()
            company = company_tag.text.strip()
            link = link_tag['href']

            if 'python' in title.lower():
                jobs.append({
                    "title": title,
                    "company": company,
                    "link": link
                })

    if not jobs:
        print("⚠️ No Python-related jobs found.")
        return

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = os.path.join(output_dir, f"jobs_{timestamp}.json")

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=4)
        print(f"✅ Saved {len(jobs)} Python jobs to '{output_path}'")
    except Exception as e:
        print(f"❌ Failed to write JSON: {e}")

if __name__ == "__main__":
    target_url = "https://realpython.github.io/fake-jobs/"
    output_folder = "output"
    scrape_jobs(target_url, output_folder)
