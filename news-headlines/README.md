# 🗞️ News Headlines Scraper

A Python script that fetches top headlines from major news websites and outputs them in a clean JSON format.

## 🌟 Features

- **Multi-source scraping**: Fetches headlines from BBC, Times of India, and Al Jazeera
- **Error handling**: Robust error handling with fallback selectors
- **Clean JSON output**: Well-structured JSON with metadata
- **Logging**: Comprehensive logging for debugging
- **Modular design**: Easy to add new news sources

## 🏗️ Project Structure

```
news-headlines/
├── src/
│   ├── main.py              # Main aggregation logic
│   ├── scrapers/            # News source scrapers
│   │   ├── base_scraper.py  # Base scraper class
│   │   ├── bbc_scraper.py   # BBC News scraper
│   │   ├── times_of_india_scraper.py  # TOI scraper
│   │   └── aljazeera_scraper.py       # Al Jazeera scraper
│   └── utils/
│       └── logger.py        # Logging utilities
├── output/
│   └── headlines.json       # Generated headlines file
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── run.py                  # Main entry point
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd news-headlines
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the scraper**
   ```bash
   python run.py
   ```

### Alternative Installation (Virtual Environment)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## 📊 Output Format

The script generates a JSON file (`output/headlines.json`) with the following structure:

```json
{
  "timestamp": "2025-06-20 14:30:25",
  "sources": [
    {
      "source": "BBC News",
      "timestamp": "2025-06-20 14:30:25",
      "count": 10,
      "status": "success",
      "headlines": [
        {
          "title": "Breaking: Major News Event",
          "url": "https://www.bbc.com/news/example"
        }
      ]
    }
  ],
  "total_headlines": 30,
  "successful_sources": 3,
  "failed_sources": 0
}
```

## 🔧 Configuration

### Adding New News Sources

1. Create a new scraper in `src/scrapers/`
2. Inherit from `BaseScraper`
3. Implement the `scrape_headlines()` method
4. Add the scraper to `src/scrapers/__init__.py`
5. Add it to the scrapers list in `src/main.py`

Example:
```python
from .base_scraper import BaseScraper

class YourNewsScraper(BaseScraper):
    def __init__(self):
        super().__init__("Your News Site", "https://example.com")
    
    def scrape_headlines(self):
        soup = self.fetch_page(self.base_url)
        # Your scraping logic here
        return headlines
```

### Customizing Output

- **Output location**: Modify the `filepath` parameter in `main.py`
- **Number of headlines**: Change the limit in individual scrapers
- **Timeout settings**: Adjust timeout in `BaseScraper.fetch_page()`

## 🛠️ Troubleshooting

### Common Issues

1. **No headlines found**
   - News sites frequently change their HTML structure
   - The script includes multiple fallback selectors
   - Check logs for specific error messages

2. **Connection errors**
   - Ensure internet connectivity
   - Some sites may block automated requests
   - The script includes retry logic and user-agent headers

3. **Permission errors**
   - Ensure write permissions for the `output/` directory
   - Run with appropriate permissions if needed

### Debug Mode

Enable detailed logging by modifying the logger level in `src/utils/logger.py`:
```python
logger.setLevel(logging.DEBUG)
```

## 📝 Dependencies

- **requests**: HTTP library for making web requests
- **beautifulsoup4**: HTML parsing library
- **lxml**: Fast XML and HTML parser

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please respect the terms of service of the news websites and implement appropriate rate limiting for production use.

## 🔄 Version History

- **v1.0.0**: Initial release with BBC, Times of India, and Al Jazeera support
- Multi-source scraping with error handling
- Clean JSON output format