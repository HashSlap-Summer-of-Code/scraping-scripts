# Wikipedia Summary Extractor

A Python script that fetches the first 2 paragraphs of any Wikipedia article and saves it to `summary.txt`.

## Features
- Uses Wikipedia REST API for reliable data fetching
- Sanitizes markup and references
- Extracts exactly 2 paragraphs
- Saves to formatted text file
- Error handling and user feedback

## Usage

### Command Line
```bash
python main.py "Artificial Intelligence"
python main.py "Python programming language"