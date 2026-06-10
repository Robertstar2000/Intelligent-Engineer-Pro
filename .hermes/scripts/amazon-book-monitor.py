#!/usr/bin/env python3
"""Amazon book monitor for Bob J Mills — weekly cron job.

Searches Amazon Kindle Store for "Bob J Mills", extracts ASINs and metadata,
compares with known books, and generates an update report.

This script outputs JSON to stdout for the agent to parse and act on.
"""
import json
import os
import sys
from datetime import datetime

KNOWN_ASINS = {
    'B0GX2XC5YF': 'Tomorrow Remembered',
    'B0H15NLBW8': 'AI That Works for Small Business',
    'B0GX2YJ92K': 'Built from Dust (No Blue Sky 1)',
    'B0H1KSCRYC': "The Owner's Manual for AI Agents",
}

def main():
    print(f"=== Amazon Book Monitor — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    print(f"KNOWN_ASINS: {json.dumps(KNOWN_ASINS)}")
    print(f"SEARCH_URL: https://www.amazon.com/s?k=%22Bob+J+Mills%22&i=digital-text")
    print("=== Done ===")

if __name__ == '__main__':
    main()
