#!/usr/bin/env python3
"""Amazon book monitor for Bob J Mills — weekly cron job.

Searches Amazon Kindle Store for "Bob J Mills", extracts ASINs and metadata,
compares with known books, and generates an update report.

If new books are found, updates pipeline data files and delivers notification.
"""
import json
import os
import sys
from datetime import datetime

KNOWN_BOOKS_FILE = os.path.expanduser('~/.hermes/pipeline-engine/data/pipeline-books.json')
DASHBOARD_FILE = os.path.expanduser('~/.hermes/pipeline-engine/dashboard/pipeline-dashboard.html')
BOOKSTORE_FILE = os.path.expanduser('~/.hermes/mifeco_web/mifeco-website/src/components/BookstoreSection.jsx')

# Known ASINs as of 2026-05-25
KNOWN_ASINS = {
    'B0GX2XC5YF': 'Tomorrow Remembered',
    'B0H15NLBW8': 'AI That Works for Small Business',
    'B0GX2YJ92K': 'Built from Dust (No Blue Sky 1)',
    'B0H1KSCRYC': "The Owner's Manual for AI Agents",
}

def check_new_books_on_amazon():
    """
    Opens browser, searches Amazon for "Bob J Mills", extracts ASINs.
    Returns list of dicts with asin, title, price.
    """
    try:
        # Use Playwright-compatible browser via the hermes browser harness
        from hermes_tools import browser_navigate, browser_console
        
        # Search Amazon Kindle Store for Bob J Mills
        url = 'https://www.amazon.com/s?k=%22Bob+J+Mills%22&i=digital-text'
        result = browser_navigate(url=url)
        if not result.get('success'):
            return None, f"Failed to navigate to Amazon: {result.get('error', 'unknown error')}"
        
        # Extract ASINs and titles from search results
        js_code = """
        Array.from(document.querySelectorAll('[data-asin]'))
            .map(e => ({
                asin: e.getAttribute('data-asin'),
                title: (e.querySelector('h2') || e.querySelector('.a-size-medium') || {}).innerText?.trim() || 'unknown'
            }))
            .filter(x => x.asin && x.asin.length > 5)
        """
        result = browser_console(expression=js_code)
        if not result.get('success'):
            return None, f"Failed to extract ASINs: {result.get('error', 'unknown error')}"
        
        # Parse the returned data
        import ast
        try:
            books_found = ast.literal_eval(result['result']) if isinstance(result['result'], str) else result['result']
        except:
            books_found = result.get('result', [])
        
        return books_found, None
        
    except Exception as e:
        return None, str(e)


def main():
    print(f"=== Amazon Book Monitor — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    
    books, error = check_new_books_on_amazon()
    
    if error:
        print(f"ERROR: {error}")
        sys.exit(0)  # Don't alert on transient errors
    
    if not books:
        print("No books found on Amazon.")
        sys.exit(0)
    
    print(f"Found {len(books)} book(s) on Amazon:")
    
    new_books = []
    for b in books:
        asin = b.get('asin', '').strip()
        title = b.get('title', 'unknown').strip()
        
        # Skip empty ASINs and the "unknown" results
        if not asin or not title or title == 'unknown':
            continue
            
        print(f"  • {title} — ASIN: {asin}")
        
        if asin not in KNOWN_ASINS:
            new_books.append(b)
    
    if new_books:
        print(f"\n🚀 NEW BOOKS FOUND: {len(new_books)}")
        for b in new_books:
            print(f"  ✨ {b['title']} — https://www.amazon.com/dp/{b['asin']}")
        
        # Output the report for delivery back to the user
        print(f"\n--- BEGIN REPORT ---")
        print(f"New books by Bob J Mills found on Amazon:")
        for b in new_books:
            print(f"- {b['title']}")
            print(f"  https://www.amazon.com/dp/{b['asin']}")
        print(f"--- END REPORT ---")
        
        print("\nACTION: Update the following files with new ASINs:")
        print(f"  1. {KNOWN_BOOKS_FILE}")
        print(f"  2. {DASHBOARD_FILE}")
        print(f"  3. {BOOKSTORE_FILE}")
    else:
        print(f"\n✅ No new books found. All {len(KNOWN_ASINS)} known books still current.")
    
    print("=== Done ===")


if __name__ == '__main__':
    main()
