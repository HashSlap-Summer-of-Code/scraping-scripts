import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from scrapers.base_scraper import BaseScraper
from typing import List, Dict

class BBCScraper(BaseScraper):
    """BBC News scraper"""
    
    def __init__(self):
        super().__init__("BBC News", "https://www.bbc.com/news")
    
    def scrape_headlines(self) -> List[Dict[str, str]]:
        """Scrape BBC headlines"""
        soup = self.fetch_page(self.base_url)
        headlines = []
        
        # Try multiple selectors as BBC structure may vary
        selectors = [
            'h3[data-testid="card-headline"]',
            'h3.gs-c-promo-heading__title',
            'h2[data-testid="card-headline"]',
            'a[data-testid="internal-link"] h3',
            '.media__content h3 a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements[:10]:  # Limit to top 10
                    title = element.get_text(strip=True)
                    if title and len(title) > 10:  # Filter out short/empty titles
                        # Try to get the link
                        link = ""
                        if element.name == 'a':
                            link = element.get('href', '')
                        else:
                            parent_link = element.find_parent('a')
                            if parent_link:
                                link = parent_link.get('href', '')
                        
                        # Make relative URLs absolute
                        if link and link.startswith('/'):
                            link = f"https://www.bbc.com{link}"
                        
                        headlines.append({
                            'title': title,
                            'url': link
                        })
                
                if headlines:
                    break
        
        return headlines[:10]  # Return top 10 headlines