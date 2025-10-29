#!/usr/bin/env python3
"""
Test Mission Alignment with Education Fund
"""

import pandas as pd
import sys
sys.path.append('tools/contact_enhancement')
from enhanced_contact_discovery import ContactEnhancementPipeline

def test_education_org():
    # Test with Arts Equity & Education Fund
    df = pd.read_csv('campaigns/sponsor_data/intelligent_campaign_20251022_154639.csv')
    arts_ed_fund = df[df['sponsor_name'] == 'Arts Equity & Education Fund']

    print('Testing mission alignment with Arts Education organization:')
    print(arts_ed_fund[['sponsor_name', 'city', 'state']].to_string())

    # Run enhanced pipeline
    pipeline = ContactEnhancementPipeline()
    enhanced_df = pipeline.enhance_contact_data(arts_ed_fund, max_records=1)

    print('\nResults:')
    for idx, row in enhanced_df.iterrows():
        print(f'Organization: {row["sponsor_name"]}')
        print(f'Website: {row.get("website", "Not found")}')
        
        mission_score = row.get('mission_alignment_score', 0)
        mission_score = mission_score if not pd.isna(mission_score) else 0
        print(f'Mission Alignment Score: {mission_score:.1f}/100')
        
        print(f'Program Areas: {row.get("program_areas", "None")}')
        print(f'Alignment Factors: {row.get("alignment_factors", "None")}')

if __name__ == "__main__":
    test_education_org()