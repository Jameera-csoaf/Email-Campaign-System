#!/usr/bin/env python3
"""
Run Mission Alignment Analysis on High Priority Sponsors
Process all 1,076 high priority sponsors with enhanced contact discovery and mission alignment
"""

import pandas as pd
import sys
import os
from datetime import datetime
sys.path.append('tools/contact_enhancement')
from enhanced_contact_discovery import ContactEnhancementPipeline

def process_high_priority_sponsors():
    """Process high priority sponsors with mission alignment analysis"""
    
    print("🎯 MISSION ALIGNMENT ANALYSIS - HIGH PRIORITY SPONSORS")
    print("=" * 70)
    
    # Load high priority sponsors
    input_file = 'campaigns/sponsor_data/high_priority_sponsors.csv'
    df = pd.read_csv(input_file)
    
    print(f"📊 Loaded {len(df)} high priority sponsors")
    print(f"📁 Input file: {input_file}")
    
    # Show sample of data
    print("\n📋 Sample organizations to process:")
    sample_orgs = df[['sponsor_name', 'city', 'state']].head(5)
    print(sample_orgs.to_string())
    
    # Ask for confirmation before processing (this will take time)
    print(f"\n⚠️  WARNING: This will process {len(df)} organizations")
    print("⏱️  Estimated time: 2-3 hours (3-5 seconds per organization)")
    print("🌐 Will scrape websites for mission alignment analysis")
    
    response = input("\n🤔 Continue with full processing? (y/n): ")
    if response.lower() != 'y':
        print("❌ Processing cancelled by user")
        
        # Process just a small sample for testing
        print("\n🔬 Processing first 10 organizations as test...")
        df_sample = df.head(10)
        pipeline = ContactEnhancementPipeline()
        enhanced_df = pipeline.enhance_contact_data(df_sample, max_records=10)
        
        # Save sample results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'campaigns/sponsor_data/high_priority_mission_aligned_sample_{timestamp}.csv'
        enhanced_df.to_csv(output_file, index=False)
        
        print(f"✅ Sample results saved to: {output_file}")
        print_sample_results(enhanced_df)
        return
    
    # Run full processing
    print("\n🚀 Starting full mission alignment analysis...")
    pipeline = ContactEnhancementPipeline()
    
    # Process in batches to avoid timeouts
    batch_size = 100
    all_enhanced = []
    
    for i in range(0, len(df), batch_size):
        batch_num = (i // batch_size) + 1
        batch_df = df.iloc[i:i+batch_size]
        
        print(f"\n📦 Processing batch {batch_num}/{(len(df) + batch_size - 1) // batch_size}")
        print(f"   Organizations {i+1} to {min(i+batch_size, len(df))}")
        
        try:
            enhanced_batch = pipeline.enhance_contact_data(batch_df)
            all_enhanced.append(enhanced_batch)
            
            # Save progress after each batch
            if all_enhanced:
                progress_df = pd.concat(all_enhanced, ignore_index=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                progress_file = f'campaigns/sponsor_data/high_priority_mission_aligned_progress_{timestamp}.csv'
                progress_df.to_csv(progress_file, index=False)
                print(f"💾 Progress saved: {len(progress_df)} organizations processed")
        
        except Exception as e:
            print(f"❌ Error processing batch {batch_num}: {str(e)}")
            continue
    
    # Combine all results
    if all_enhanced:
        final_df = pd.concat(all_enhanced, ignore_index=True)
        
        # Save final results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'campaigns/sponsor_data/high_priority_mission_aligned_{timestamp}.csv'
        final_df.to_csv(output_file, index=False)
        
        print(f"\n✅ MISSION ALIGNMENT ANALYSIS COMPLETE!")
        print(f"📁 Results saved to: {output_file}")
        print(f"📊 Total organizations processed: {len(final_df)}")
        
        print_analysis_summary(final_df)
        
    else:
        print("❌ No data was successfully processed")

def print_sample_results(df):
    """Print sample results from mission alignment analysis"""
    
    print("\n📊 SAMPLE MISSION ALIGNMENT RESULTS")
    print("=" * 50)
    
    for idx, row in df.head(5).iterrows():
        print(f"\n🏢 {row['sponsor_name']}")
        print(f"   📍 Location: {row['city']}, {row['state']}")
        print(f"   🌐 Website: {row.get('website', 'Not found')}")
        print(f"   📧 Email: {row.get('email', 'Not found')}")
        
        mission_score = row.get('mission_alignment_score', 0)
        mission_score = mission_score if not pd.isna(mission_score) else 0
        print(f"   🎯 Mission Alignment: {mission_score:.1f}/100")
        
        program_areas = row.get('program_areas', '')
        if program_areas:
            print(f"   📋 Program Areas: {program_areas}")

def print_analysis_summary(df):
    """Print summary statistics of mission alignment analysis"""
    
    print("\n📈 MISSION ALIGNMENT SUMMARY")
    print("=" * 40)
    
    # Basic stats
    total_orgs = len(df)
    websites_found = df['website'].notna().sum()
    emails_found = df['email'].notna().sum()
    
    print(f"📊 Total Organizations: {total_orgs}")
    print(f"🌐 Websites Found: {websites_found} ({websites_found/total_orgs*100:.1f}%)")
    print(f"📧 Emails Found: {emails_found} ({emails_found/total_orgs*100:.1f}%)")
    
    # Mission alignment stats
    mission_scores = df['mission_alignment_score'].fillna(0)
    print(f"\n🎯 Mission Alignment Scores:")
    print(f"   Average Score: {mission_scores.mean():.1f}/100")
    print(f"   High Alignment (70+): {(mission_scores >= 70).sum()} organizations")
    print(f"   Medium Alignment (30-69): {((mission_scores >= 30) & (mission_scores < 70)).sum()} organizations")
    print(f"   Low Alignment (0-29): {(mission_scores < 30).sum()} organizations")
    
    # Top aligned organizations
    top_aligned = df.nlargest(5, 'mission_alignment_score')
    if len(top_aligned) > 0:
        print(f"\n🏆 TOP MISSION-ALIGNED ORGANIZATIONS:")
        for idx, row in top_aligned.iterrows():
            score = row.get('mission_alignment_score', 0)
            print(f"   • {row['sponsor_name']} ({score:.1f}/100)")

if __name__ == "__main__":
    process_high_priority_sponsors()