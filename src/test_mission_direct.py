#!/usr/bin/env python3
"""
Test Mission Analysis Directly
"""

import sys
sys.path.append('tools/contact_enhancement')
from enhanced_contact_discovery import WebsiteDiscoveryEngine

def test_mission_analysis():
    # Test mission analysis directly
    website_engine = WebsiteDiscoveryEngine()
    mission_data = website_engine.analyze_mission_alignment('https://imagineperformingarts.com', 'Imagine Performing Arts Fund')

    print('Mission Analysis Results:')
    print(f'Mission Score: {mission_data["mission_score"]}')
    print(f'Mission Text: {mission_data["mission_text"][:200]}...')
    print(f'Alignment Factors: {mission_data["alignment_factors"]}')
    print(f'Pages Analyzed: {mission_data["pages_analyzed"]}')
    print(f'Program Areas: {mission_data["program_areas"]}')
    
    # Let's also test our keyword matching
    print('\nKeyword Categories:')
    for category, keywords in website_engine.mission_keywords.items():
        print(f'{category}: {list(keywords.keys())[:5]}...')

if __name__ == "__main__":
    test_mission_analysis()