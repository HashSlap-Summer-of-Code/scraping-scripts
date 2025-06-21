import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from scrapers.base_scraper import BaseScraper
from typing import List, Dict

class TimesOfIndiaScraper(BaseScraper):
    """Times of India scraper"""
    
    def __init__(self):
        super().__init__("Times of India", "https://timesofindia.indiatimes.com/")
    
    def scrape_headlines(self) -> List[Dict[str, str]]:
        """Scrape Times of India headlines"""
        soup = self.fetch_page(self.base_url)
        headlines = []
        
        # Multiple selectors for TOI
        selectors = [
            '.top-newslist li a',
            '.news-item a',
            '.story-link',
            'a[data-title]',
            '.headline a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements[:15]:  # Get more as some might be filtered
                    title = element.get_text(strip=True)
                    # Clean up title
                    if title and len(title) > 15 and not title.lower().startswith('advertisement'):
                        url = element.get('href', '')
                        
                        # Make relative URLs absolute
                        if url and url.startswith('/'):
                            url = f"https://timesofindia.indiatimes.com{url}"
                        elif url and not url.startswith('http'):
                            continue  # Skip invalid URLs
                        
                        headlines.append({
                            'title': title,
                            'url': url
                        })
                        
                        if len(headlines) >= 10:
                            break
                
                if headlines:
                    break
        
        return headlines[:10]