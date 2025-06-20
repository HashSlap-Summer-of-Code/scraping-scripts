#!/usr/bin/env python3
"""
Wikipedia Summary Extractor
Fetches the first 2 paragraphs of a Wikipedia article and saves to summary.txt
"""

import requests
import re
import sys
import os
from urllib.parse import quote


class WikipediaSummaryExtractor:
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WikipediaSummaryExtractor/1.0 (Educational Purpose)'
        })

    def fetch_summary(self, topic):
        """
        Fetch Wikipedia summary using the REST API
        """
        try:
            # URL encode the topic to handle special characters
            encoded_topic = quote(topic.replace(' ', '_'))
            url = f"{self.base_url}{encoded_topic}"
            
            print(f"Fetching summary for: {topic}")
            print(f"API URL: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'extract' not in data:
                raise ValueError(f"No summary found for topic: {topic}")
            
            return data['extract']
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching data from Wikipedia: {e}")
        except ValueError as e:
            raise Exception(str(e))

    def sanitize_text(self, text):
        """
        Clean up the text by removing markup and references
        """
        if not text:
            return ""
        
        # Remove citation references like [1], [2], [citation needed], etc.
        text = re.sub(r'\[[\d\w\s,]+\]', '', text)
        
        # Remove HTML tags if any
        text = re.sub(r'<[^>]+>', '', text)
        
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    def extract_paragraphs(self, text, num_paragraphs=2):
        """
        Extract the first N paragraphs from the text
        """
        if not text:
            return ""
        
        # Split by double newlines or periods followed by space and capital letter
        # This helps identify paragraph boundaries
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        
        if len(sentences) <= num_paragraphs:
            return text
        
        # Take first num_paragraphs sentences and join them
        paragraphs = '. '.join(sentences[:num_paragraphs])
        
        # Ensure it ends with proper punctuation
        if not paragraphs.endswith(('.', '!', '?')):
            paragraphs += '.'
            
        return paragraphs

    def save_to_file(self, content, filename="summary.txt"):
        """
        Save content to a text file
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Summary saved to: {filename}")
            return True
        except IOError as e:
            print(f"Error saving file: {e}")
            return False

    def process_topic(self, topic, output_file="summary.txt"):
        """
        Main method to process a topic and save summary
        """
        try:
            # Fetch raw summary
            raw_summary = self.fetch_summary(topic)
            
            # Sanitize the text
            clean_summary = self.sanitize_text(raw_summary)
            
            # Extract first 2 paragraphs
            final_summary = self.extract_paragraphs(clean_summary, 2)
            
            if not final_summary:
                raise Exception("No content extracted from the summary")
            
            # Prepare final content with header
            content = f"Wikipedia Summary: {topic}\n"
            content += "=" * (len(content) - 1) + "\n\n"
            content += final_summary + "\n"
            
            # Save to file
            success = self.save_to_file(content, output_file)
            
            if success:
                print(f"\n✅ Successfully extracted summary for '{topic}'")
                print(f"📁 Saved to: {output_file}")
                print(f"📊 Content length: {len(final_summary)} characters")
            
            return success
            
        except Exception as e:
            print(f"❌ Error processing topic '{topic}': {e}")
            return False


def main():
    """
    Main function to run the extractor
    """
    extractor = WikipediaSummaryExtractor()
    
    if len(sys.argv) > 1:
        # Topic provided as command line argument
        topic = ' '.join(sys.argv[1:])
    else:
        # Interactive mode
        topic = input("Enter Wikipedia topic: ").strip()
    
    if not topic:
        print("❌ No topic provided!")
        sys.exit(1)
    
    # Process the topic
    success = extractor.process_topic(topic)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()