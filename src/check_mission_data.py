#!/usr/bin/env python3
"""
Check Available Mission-Aligned Data
"""

import pandas as pd
import os

def check_mission_data():
    # List all mission-aligned files
    files = [f for f in os.listdir('campaigns/sponsor_data') if 'mission_aligned' in f]
    print('Available mission-aligned files:')
    for f in sorted(files):
        print(f'- {f}')
    
    # Check latest file
    if files:
        latest = sorted(files)[-1]
        print(f'\nLatest file: {latest}')
        
        df = pd.read_csv(f'campaigns/sponsor_data/{latest}')
        print(f'Records: {len(df)}')
        print('\nColumns available:')
        for col in df.columns:
            print(f'- {col}')
        
        # Check if we have mission alignment scores
        if 'mission_alignment_score' in df.columns:
            scores = df['mission_alignment_score'].dropna()
            print(f'\nMission Alignment Data:')
            print(f'- Records with scores: {len(scores)}')
            print(f'- Average score: {scores.mean():.1f}')
            print(f'- Max score: {scores.max():.1f}')
            print(f'- Records with score > 50: {len(scores[scores > 50])}')
            
            # Show top scoring organizations
            print('\nTop 5 Mission-Aligned Organizations:')
            top_orgs = df.nlargest(5, 'mission_alignment_score')[['sponsor_name', 'mission_alignment_score', 'program_areas']]
            print(top_orgs.to_string(index=False))

if __name__ == "__main__":
    check_mission_data()