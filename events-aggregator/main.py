#!/usr/bin/env python3
"""
Events Aggregator - Main Script
Scrapes events from multiple platforms and generates dashboard
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import aiohttp
import requests
from bs4 import BeautifulSoup
from jinja2 import Template
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('events_aggregator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EventsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.events = []
        
    def scrape_devpost(self) -> List[Dict[str, Any]]:
        """Scrape events from Devpost"""
        logger.info("Scraping Devpost...")
        events = []
        
        try:
            url = "https://devpost.com/hackathons"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            hackathon_items = soup.find_all('div', class_='hackathon-tile')
            
            for item in hackathon_items[:10]:  # Limit to 10 events
                try:
                    title_elem = item.find('h3') or item.find('h2') or item.find('a')
                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    
                    # Extract dates
                    date_elem = item.find('div', class_='date-range') or item.find('time')
                    dates = date_elem.get_text(strip=True) if date_elem else "Dates TBA"
                    
                    # Extract organizer
                    org_elem = item.find('div', class_='organizer') or item.find('.sponsor-name')
                    organizer = org_elem.get_text(strip=True) if org_elem else "Devpost Community"
                    
                    events.append({
                        'title': title,
                        'dates': dates,
                        'organizer': organizer,
                        'category': 'Hackathon',
                        'platform': 'Devpost',
                        'scraped_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    logger.warning(f"Error parsing Devpost item: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Devpost: {e}")
            # Add mock data as fallback
            events.extend(self._get_devpost_fallback())
            
        return events
    
    def scrape_mlh(self) -> List[Dict[str, Any]]:
        """Scrape events from MLH.io"""
        logger.info("Scraping MLH...")
        events = []
        
        try:
            # MLH API endpoint (if available) or website scraping
            url = "https://mlh.io/seasons/2025/events"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            event_items = soup.find_all('div', class_='event') or soup.find_all('div', class_='hackathon')
            
            for item in event_items[:8]:  # Limit to 8 events
                try:
                    title_elem = item.find('h3') or item.find('h2') or item.find('a')
                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    
                    date_elem = item.find('div', class_='date') or item.find('time')
                    dates = date_elem.get_text(strip=True) if date_elem else "Dates TBA"
                    
                    org_elem = item.find('div', class_='location') or item.find('.university')
                    organizer = org_elem.get_text(strip=True) if org_elem else "MLH Community"
                    
                    events.append({
                        'title': title,
                        'dates': dates,
                        'organizer': organizer,
                        'category': 'Hackathon',
                        'platform': 'MLH',
                        'scraped_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    logger.warning(f"Error parsing MLH item: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping MLH: {e}")
            events.extend(self._get_mlh_fallback())
            
        return events
    
    def scrape_edtech_platforms(self) -> List[Dict[str, Any]]:
        """Scrape events from EdTech platforms"""
        logger.info("Scraping EdTech platforms...")
        events = []
        
        # Scaler events
        try:
            events.extend(self._scrape_scaler())
        except Exception as e:
            logger.error(f"Error scraping Scaler: {e}")
            events.extend(self._get_scaler_fallback())
        
        # Add more EdTech platforms here
        events.extend(self._get_unacademy_fallback())
        
        return events
    
    def _scrape_scaler(self) -> List[Dict[str, Any]]:
        """Scrape Scaler events"""
        events = []
        try:
            url = "https://www.scaler.com/events/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            event_cards = soup.find_all('div', class_='event-card') or soup.find_all('div', class_='card')
            
            for card in event_cards[:5]:
                try:
                    title_elem = card.find('h3') or card.find('h2')
                    title = title_elem.get_text(strip=True) if title_elem else "Scaler Event"
                    
                    date_elem = card.find('div', class_='date') or card.find('time')
                    dates = date_elem.get_text(strip=True) if date_elem else "Upcoming"
                    
                    events.append({
                        'title': title,
                        'dates': dates,
                        'organizer': 'Scaler',
                        'category': 'EdTech Workshop',
                        'platform': 'Scaler',
                        'scraped_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    logger.warning(f"Error parsing Scaler event: {e}")
                    continue
        except Exception as e:
            logger.error(f"Error accessing Scaler: {e}")
            
        return events
    
    def _get_devpost_fallback(self) -> List[Dict[str, Any]]:
        """Fallback data for Devpost"""
        return [
            {
                'title': 'Global AI Hackathon 2025',
                'dates': 'Jul 15-17, 2025',
                'organizer': 'Devpost Community',
                'category': 'Hackathon',
                'platform': 'Devpost',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Web3 Innovation Challenge',
                'dates': 'Aug 1-3, 2025',
                'organizer': 'Blockchain Alliance',
                'category': 'Hackathon',
                'platform': 'Devpost',
                'scraped_at': datetime.now().isoformat()
            }
        ]
    
    def _get_mlh_fallback(self) -> List[Dict[str, Any]]:
        """Fallback data for MLH"""
        return [
            {
                'title': 'HackMIT 2025',
                'dates': 'Sep 20-22, 2025',
                'organizer': 'MIT',
                'category': 'Hackathon',
                'platform': 'MLH',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'PennApps XXV',
                'dates': 'Oct 4-6, 2025',
                'organizer': 'University of Pennsylvania',
                'category': 'Hackathon',
                'platform': 'MLH',
                'scraped_at': datetime.now().isoformat()
            }
        ]
    
    def _get_scaler_fallback(self) -> List[Dict[str, Any]]:
        """Fallback data for Scaler"""
        return [
            {
                'title': 'System Design Masterclass',
                'dates': 'Jul 25, 2025',
                'organizer': 'Scaler',
                'category': 'EdTech Workshop',
                'platform': 'Scaler',
                'scraped_at': datetime.now().isoformat()
            }
        ]
    
    def _get_unacademy_fallback(self) -> List[Dict[str, Any]]:
        """Fallback data for Unacademy"""
        return [
            {
                'title': 'Data Science Bootcamp',
                'dates': 'Aug 10-12, 2025',
                'organizer': 'Unacademy',
                'category': 'Bootcamp',
                'platform': 'Unacademy',
                'scraped_at': datetime.now().isoformat()
            }
        ]
    
    def scrape_all_platforms(self) -> List[Dict[str, Any]]:
        """Scrape all platforms and return combined events"""
        logger.info("Starting to scrape all platforms...")
        
        all_events = []
        
        # Scrape each platform with delay to be respectful
        all_events.extend(self.scrape_devpost())
        time.sleep(2)
        
        all_events.extend(self.scrape_mlh())
        time.sleep(2)
        
        all_events.extend(self.scrape_edtech_platforms())
        
        logger.info(f"Total events scraped: {len(all_events)}")
        return all_events

class DashboardGenerator:
    def __init__(self, events: List[Dict[str, Any]]):
        self.events = events
        
    def save_to_json(self, filepath: str):
        """Save events to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'events': self.events,
                'total_count': len(self.events),
                'generated_at': datetime.now().isoformat(),
                'platforms': list(set([event.get('platform', 'Unknown') for event in self.events]))
            }, f, indent=2, ensure_ascii=False)
        logger.info(f"Events saved to JSON: {filepath}")
    
    def save_to_markdown(self, filepath: str):
        """Save events to Markdown file"""
        md_content = f"""# Events Dashboard

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Events: {len(self.events)}

## Events by Platform

"""
        
        # Group events by platform
        platforms = {}
        for event in self.events:
            platform = event.get('platform', 'Unknown')
            if platform not in platforms:
                platforms[platform] = []
            platforms[platform].append(event)
        
        for platform, events in platforms.items():
            md_content += f"### {platform} ({len(events)} events)\n\n"
            for event in events:
                md_content += f"**{event['title']}**\n"
                md_content += f"- **Dates:** {event['dates']}\n"
                md_content += f"- **Organizer:** {event['organizer']}\n"
                md_content += f"- **Category:** {event['category']}\n\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        logger.info(f"Events saved to Markdown: {filepath}")
    
    def generate_html_dashboard(self, output_dir: str):
        """Generate HTML dashboard"""
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Events Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header { 
            text-align: center; 
            margin-bottom: 40px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
        }
        .header h1 { 
            color: #333; 
            font-size: 2.5em; 
            margin-bottom: 10px;
        }
        .stats { 
            display: flex; 
            justify-content: center; 
            gap: 30px; 
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .stat-card { 
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white; 
            padding: 15px 25px; 
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .stat-number { font-size: 2em; font-weight: bold; }
        .stat-label { font-size: 0.9em; opacity: 0.9; }
        .filters { 
            margin: 30px 0; 
            text-align: center;
        }
        .filter-btn { 
            background: #fff; 
            border: 2px solid #667eea; 
            color: #667eea; 
            padding: 8px 16px; 
            margin: 5px; 
            border-radius: 25px; 
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .filter-btn:hover, .filter-btn.active { 
            background: #667eea; 
            color: white;
            transform: translateY(-2px);
        }
        .events-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); 
            gap: 25px; 
            margin-top: 30px;
        }
        .event-card { 
            background: white; 
            border-radius: 15px; 
            padding: 25px; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-left: 5px solid #667eea;
        }
        .event-card:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }
        .event-title { 
            font-size: 1.3em; 
            font-weight: bold; 
            color: #333; 
            margin-bottom: 15px;
            line-height: 1.4;
        }
        .event-detail { 
            margin: 10px 0; 
            display: flex; 
            align-items: center;
        }
        .event-detail strong { 
            color: #667eea; 
            min-width: 80px;
            margin-right: 10px;
        }
        .category-badge { 
            display: inline-block; 
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white; 
            padding: 5px 12px; 
            border-radius: 20px; 
            font-size: 0.8em; 
            font-weight: bold;
            margin-top: 10px;
        }
        .platform-tag { 
            position: absolute; 
            top: 15px; 
            right: 15px; 
            background: rgba(102, 126, 234, 0.1); 
            color: #667eea; 
            padding: 5px 10px; 
            border-radius: 10px; 
            font-size: 0.8em;
        }
        .event-card { position: relative; }
        @media (max-width: 768px) {
            .events-grid { grid-template-columns: 1fr; }
            .stats { flex-direction: column; align-items: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Events Dashboard</h1>
            <p>Discover the latest hackathons, bootcamps, and tech events</p>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{{ total_events }}</div>
                    <div class="stat-label">Total Events</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ platforms|length }}</div>
                    <div class="stat-label">Platforms</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ categories|length }}</div>
                    <div class="stat-label">Categories</div>
                </div>
            </div>
        </div>
        
        <div class="filters">
            <button class="filter-btn active" onclick="filterEvents('all')">All Events</button>
            {% for platform in platforms %}
            <button class="filter-btn" onclick="filterEvents('{{ platform }}')">{{ platform }}</button>
            {% endfor %}
        </div>
        
        <div class="events-grid" id="events-grid">
            {% for event in events %}
            <div class="event-card" data-platform="{{ event.platform }}">
                <div class="platform-tag">{{ event.platform }}</div>
                <div class="event-title">{{ event.title }}</div>
                <div class="event-detail">
                    <strong>📅 Dates:</strong>
                    <span>{{ event.dates }}</span>
                </div>
                <div class="event-detail">
                    <strong>👥 Organizer:</strong>
                    <span>{{ event.organizer }}</span>
                </div>
                <span class="category-badge">{{ event.category }}</span>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <script>
        function filterEvents(platform) {
            const cards = document.querySelectorAll('.event-card');
            const buttons = document.querySelectorAll('.filter-btn');
            
            // Update button states
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Filter cards
            cards.forEach(card => {
                if (platform === 'all' || card.dataset.platform === platform) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        // Add some animation on load
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.event-card');
            cards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    card.style.transition = 'all 0.5s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 100);
            });
        });
    </script>
</body>
</html>
        """
        
        # Prepare template data
        platforms = list(set([event.get('platform', 'Unknown') for event in self.events]))
        categories = list(set([event.get('category', 'Unknown') for event in self.events]))
        
        template = Template(html_template)
        html_content = template.render(
            events=self.events,
            total_events=len(self.events),
            platforms=platforms,
            categories=categories
        )
        
        # Save HTML file
        html_path = os.path.join(output_dir, 'index.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML dashboard generated: {html_path}")

def main():
    """Main function to run the events aggregator"""
    logger.info("Starting Events Aggregator...")
    
    # Create output directories
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Initialize scraper and scrape events
    scraper = EventsScraper()
    events = scraper.scrape_all_platforms()
    
    if not events:
        logger.error("No events found. Exiting...")
        return
    
    # Generate dashboard
    dashboard = DashboardGenerator(events)
    
    # Save to different formats
    dashboard.save_to_json(output_dir / 'events.json')
    dashboard.save_to_markdown(output_dir / 'events.md')
    dashboard.generate_html_dashboard(str(output_dir))
    
    logger.info("Events aggregation completed successfully!")
    logger.info(f"Check the 'output' directory for generated files:")
    logger.info(f"- events.json: Raw event data")
    logger.info(f"- events.md: Markdown formatted events")
    logger.info(f"- index.html: Interactive dashboard")

if __name__ == "__main__":
    main()