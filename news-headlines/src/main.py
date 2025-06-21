import json
import os
import sys
from typing import List, Dict

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from scrapers.bbc_scraper import BBCScraper
from scrapers.times_of_india_scraper import TimesOfIndiaScraper
from scrapers.aljazeera_scraper import AlJazeeraScraper
from utils.logger import setup_logger

class NewsAggregator:
    """Main class to aggregate news from multiple sources"""
    
    def __init__(self):
        self.logger = setup_logger()
        self.scrapers = [
            BBCScraper(),
            TimesOfIndiaScraper(),
            AlJazeeraScraper()
        ]
    
    def fetch_all_headlines(self) -> Dict:
        """Fetch headlines from all news sources"""
        self.logger.info("Starting news aggregation...")
        
        results = {
            'timestamp': None,
            'sources': [],
            'total_headlines': 0,
            'successful_sources': 0,
            'failed_sources': 0
        }
        
        for scraper in self.scrapers:
            self.logger.info(f"Fetching headlines from {scraper.name}...")
            
            try:
                source_data = scraper.get_headlines_with_metadata()
                results['sources'].append(source_data)
                
                if source_data['status'] == 'success':
                    results['successful_sources'] += 1
                    results['total_headlines'] += source_data['count']
                    self.logger.info(f"✓ {scraper.name}: {source_data['count']} headlines")
                else:
                    results['failed_sources'] += 1
                    self.logger.error(f"✗ {scraper.name}: {source_data.get('error', 'Unknown error')}")
                    
            except Exception as e:
                results['failed_sources'] += 1
                self.logger.error(f"✗ {scraper.name}: Unexpected error - {str(e)}")
                results['sources'].append({
                    'source': scraper.name,
                    'status': 'error',
                    'error': str(e),
                    'headlines': [],
                    'count': 0
                })
        
        # Set timestamp to the first successful scrape timestamp or current time
        successful_sources = [s for s in results['sources'] if s['status'] == 'success']
        if successful_sources:
            results['timestamp'] = successful_sources[0]['timestamp']
        else:
            import time
            results['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        return results
    
    def save_to_json(self, data: Dict, filepath: str = 'output/headlines.json'):
        """Save headlines to JSON file"""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Headlines saved to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save headlines: {str(e)}")
            return False

def main():
    """Main function"""
    aggregator = NewsAggregator()
    
    # Fetch headlines
    headlines_data = aggregator.fetch_all_headlines()
    
    # Save to JSON
    aggregator.save_to_json(headlines_data)
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"Total headlines: {headlines_data['total_headlines']}")
    print(f"Successful sources: {headlines_data['successful_sources']}")
    print(f"Failed sources: {headlines_data['failed_sources']}")
    
    return headlines_data

if __name__ == "__main__":
    main()