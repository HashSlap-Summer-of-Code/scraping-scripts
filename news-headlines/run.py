#!/usr/bin/env python3
"""
News Headlines Scraper - Entry Point
Run this script to fetch latest headlines from major news sources
"""

import sys
import os

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

from main import main

if __name__ == "__main__":
    try:
        print("🗞️  News Headlines Scraper")
        print("=" * 40)
        main()
        print("\n✅ Scraping completed successfully!")
        print("📄 Check output/headlines.json for results")
        
    except KeyboardInterrupt:
        print("\n❌ Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)