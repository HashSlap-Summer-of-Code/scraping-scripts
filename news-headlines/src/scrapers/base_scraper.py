from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict

class BaseScraper(ABC):
    """Base class for news scrapers"""
    
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_page(self, url: str, timeout: int = 10) -> BeautifulSoup:
        """Fetch and parse a web page"""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch {url}: {str(e)}")
    
    @abstractmethod
    def scrape_headlines(self) -> List[Dict[str, str]]:
        """Abstract method to scrape headlines"""
        pass
    
    def get_headlines_with_metadata(self) -> Dict:
        """Get headlines with metadata"""
        try:
            headlines = self.scrape_headlines()
            return {
                'source': self.name,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'count': len(headlines),
                'headlines': headlines,
                'status': 'success'
            }
        except Exception as e:
            return {
                'source': self.name,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'count': 0,
                'headlines': [],
                'status': 'error',
                'error': str(e)
            }