import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from scrapers.base_scraper import BaseScraper
from typing import List, Dict

class AlJazeeraScraper(BaseScraper):
    """Al Jazeera scraper"""
    
    def __init__(self):
        super().__init__("Al Jazeera", "https://www.aljazeera.com/")
    
    def scrape_headlines(self) -> List[Dict[str, str]]:
        """Scrape Al Jazeera headlines"""
        soup = self.fetch_page(self.base_url)
        headlines = []
        
        # Multiple selectors for Al Jazeera
        selectors = [
            'article h3 a',
            '.featured-articles-list article h3 a',
            '.top-news-item h3 a',
            'h3.article-card__title a',
            '.news-item h3 a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements[:15]:
                    title = element.get_text(strip=True)
                    if title and len(title) > 10:
                        url = element.get('href', '')
                        
                        # Make relative URLs absolute
                        if url and url.startswith('/'):
                            url = f"https://www.aljazeera.com{url}"
                        
                        headlines.append({
                            'title': title,
                            'url': url
                        })
                        
                        if len(headlines) >= 10:
                            break
                
                if headlines:
                    break
        
        return headlines[:10]