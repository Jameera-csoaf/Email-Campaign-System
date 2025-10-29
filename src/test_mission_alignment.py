#!/usr/bin/env python3
"""
Test Enhanced Contact Discovery with Mission Alignment
"""

import pandas as pd
import sys
import os
sys.path.append('tools/contact_enhancement')
from enhanced_contact_discovery import ContactEnhancementPipeline

def test_enhanced_system():
    # Load sample data (first 3 records for testing)
    df = pd.read_csv('campaigns/sponsor_data/intelligent_campaign_20251022_154639.csv').head(3)
    print('Testing enhanced contact discovery with mission alignment on 3 organizations:')
    print(df[['sponsor_name', 'city', 'state']].to_string())

    # Run enhanced pipeline
    pipeline = ContactEnhancementPipeline()
    enhanced_df = pipeline.enhance_contact_data(df, max_records=3)

    # Show results
    print('\nEnhancement Results:')
    print('='*80)
    for idx, row in enhanced_df.iterrows():
        print(f'Organization: {row["sponsor_name"]}')
        print(f'Website: {row.get("website", "Not found")}')
        print(f'Email: {row.get("email", "Not found")}')
        mission_score = row.get('mission_alignment_score', 0)
        mission_score = mission_score if not pd.isna(mission_score) else 0
        print(f'Mission Alignment Score: {mission_score:.1f}/100')
        mission_text = row.get('mission_text', 'Not available')
        mission_text = mission_text if isinstance(mission_text, str) else 'Not available'
        print(f'Mission Text: {mission_text[:100]}...')
        print(f'Program Areas: {row.get("program_areas", "None identified")}')
        print('-'*40)
    
    # Save results to file
    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'campaigns/sponsor_data/mission_aligned_test_{timestamp}.csv'
    enhanced_df.to_csv(output_file, index=False)
    print(f'\nResults saved to: {output_file}')

if __name__ == "__main__":
    test_enhanced_system()