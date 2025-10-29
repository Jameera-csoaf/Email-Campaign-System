#!/usr/bin/env python3
"""
Debug Website Content Scraping
"""

import sys
sys.path.append('tools/contact_enhancement')
from enhanced_contact_discovery import WebsiteDiscoveryEngine

def debug_content_scraping():
    website_engine = WebsiteDiscoveryEngine()
    
    # Test content scraping directly
    content = website_engine._scrape_mission_page('https://imagineperformingarts.com')
    
    print('Raw Website Content Sample:')
    print('='*60)
    if content:
        print(f'Content length: {len(content)} characters')
        print(f'First 500 characters: {content[:500]}')
        print('\nLooking for key terms:')
        test_terms = ['arts', 'education', 'program', 'creative', 'learn', 'children', 'youth']
        for term in test_terms:
            if term in content:
                print(f'✓ Found: {term}')
            else:
                print(f'✗ Missing: {term}')
    else:
        print('No content scraped - website might be blocking or error occurred')

if __name__ == "__main__":
    debug_content_scraping()