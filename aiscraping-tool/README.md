# aiscraping-tool
A CLI tool that scrapes news articles from The New York Times using their API.

## Overview
The aiscraping-tool is a command-line interface (CLI) application designed to scrape news articles from The New York Times using their API. It provides an easy-to-use interface for users to fetch and parse news articles, making it a valuable tool for developers, researchers, and anyone interested in accessing NYT's content programmatically.

## Prerequisites
- Python 3.8 or higher

## Installation
To install the aiscraping-tool, run the following commands:
```bash
git clone https://github.com/yourusername/aiscraping-tool.git
cd aiscraping-tool
pip install -r requirements.txt
```

## Configuration
The tool requires the `OPENAI_API_KEY` environment variable to be set. This key is used for authentication purposes.

- `OPENAI_API_KEY`: The OpenAI API key required for authentication.
  Example value: `your_openai_api_key_here`

## Usage
To use the aiscraping-tool, run the following command with the desired search parameters:
```bash
python main.py --query "topic:politics" --limit 10
```
This will fetch and print the first 10 news articles related to politics from The New York Times.

Alternatively, you can use `curl` to test the API endpoint:
```bash
curl -X GET \
  https://api.nytimes.com/svc/search/v2/articles.json?query=topic%3Apolitics&limit=10 \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer your_openai_api_key_here'
```
This will output the same data as the `--query` option.

## License
The aiscraping-tool is licensed under the MIT license.