#!/usr/bin/env python3
"""
Web Scraper Tool for AI Agent Toolkit
Fetches URL content and converts it to Markdown for LLM consumption.
"""
import sys
import argparse
import requests
import html2text
from urllib.parse import urlparse

def fetch_light(url):
    """Fetch using Requests (lightweight)"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AI-Toolkit/1.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Scrape URL to Markdown")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--out", help="Output file (optional)")
    
    args = parser.parse_args()
    
    # 1. Fetch
    print(f"🌐 Fetching {args.url}...", file=sys.stderr)
    html = fetch_light(args.url)
    
    if not html:
        sys.exit(1)
        
    # 2. Convert to MD
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0 # No wrapping
    
    markdown = h.handle(html)
    
    # 3. Output
    if args.out:
        try:
            with open(args.out, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"✅ Saved to {args.out}", file=sys.stderr)
        except Exception as e:
            print(f"❌ Error saving file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(markdown)

if __name__ == "__main__":
    main()
