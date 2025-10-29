#!/usr/bin/env python3
"""
Analyze Mission-Aligned Data for UI Display
"""

import pandas as pd

def analyze_ui_data():
    # Load the latest high priority mission-aligned data
    df = pd.read_csv('campaigns/sponsor_data/high_priority_mission_aligned_progress_20251022_230326.csv')
    
    print('=== DATA SUMMARY FOR UI ===')
    print(f'Total records: {len(df)}')
    print(f'Records with websites: {df["website"].notna().sum()}')
    print(f'Records with emails: {df["email"].notna().sum()}')
    print(f'Records with mission scores > 0: {(df["mission_alignment_score"] > 0).sum()}')
    print(f'Records with mission scores > 20: {(df["mission_alignment_score"] > 20).sum()}')
    print(f'Records with mission scores > 50: {(df["mission_alignment_score"] > 50).sum()}')
    
    print('\n=== TOP 10 MISSION-ALIGNED ORGANIZATIONS ===')
    top = df.nlargest(10, 'mission_alignment_score')[['sponsor_name', 'mission_alignment_score', 'website', 'email', 'program_areas']]
    print(top.to_string(index=False))
    
    print('\n=== MISSION SCORE DISTRIBUTION ===')
    scores = df['mission_alignment_score'].dropna()
    print(f'Average score: {scores.mean():.1f}')
    print(f'Median score: {scores.median():.1f}')
    print(f'Max score: {scores.max():.1f}')
    print(f'Min score: {scores.min():.1f}')
    
    # Score ranges
    print('\nScore Distribution:')
    print(f'0-10: {len(scores[(scores >= 0) & (scores <= 10)])} organizations')
    print(f'10-20: {len(scores[(scores > 10) & (scores <= 20)])} organizations')
    print(f'20-30: {len(scores[(scores > 20) & (scores <= 30)])} organizations')
    print(f'30-50: {len(scores[(scores > 30) & (scores <= 50)])} organizations')
    print(f'50+: {len(scores[scores > 50])} organizations')
    
    # Program areas analysis
    print('\n=== PROGRAM AREAS ANALYSIS ===')
    program_counts = {}
    for areas in df['program_areas'].dropna():
        if areas and isinstance(areas, str):
            for area in areas.split(','):
                area = area.strip()
                program_counts[area] = program_counts.get(area, 0) + 1
    
    print('Most common program areas:')
    for area, count in sorted(program_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f'- {area}: {count} organizations')

if __name__ == "__main__":
    analyze_ui_data()