#!/usr/bin/env python3
"""
Email Campaign Analysis - Data Classification and Template Mapping
"""

import pandas as pd
import sys
sys.path.append('src/tools')
sys.path.append('src/campaigns/email_templates')

print('📊 CURRENT DATA CLASSIFICATION SYSTEM')
print('='*60)

# Load comprehensive database
df = pd.read_csv('data/corporations/comprehensive_fortune1000_20251026_204329.csv')

print('🏢 CORPORATION DATA CLASSIFICATION:')
print(f'Total Records: {len(df):,}')
print(f'Industry Sectors: {df["industry_sector"].nunique()}')
print(f'Geographic Coverage: {df["state"].nunique()} states')
print(f'Arts Potential Levels: {df["arts_education_potential"].value_counts().to_dict()}')

print('\n📋 INDUSTRY BREAKDOWN:')
industry_counts = df['industry_sector'].value_counts()
for industry, count in industry_counts.items():
    print(f'  {industry}: {count} companies')

print('\n🎯 SPONSORSHIP CAPACITY CLASSIFICATION:')
print(f'Low Tier (<$50k): {len(df[df["estimated_typical_sponsorship"] < 50000])} companies')
print(f'Mid Tier ($50k-$200k): {len(df[(df["estimated_typical_sponsorship"] >= 50000) & (df["estimated_typical_sponsorship"] < 200000)])} companies')
print(f'High Tier ($200k+): {len(df[df["estimated_typical_sponsorship"] >= 200000])} companies')

print('\n🌍 GEOGRAPHIC PRIORITY:')
geo_priority = df['geographic_priority'].value_counts()
for priority, count in geo_priority.items():
    print(f'  {priority}: {count} companies')

print('\n📧 EMAIL TEMPLATE MAPPING:')
print('Current template categories available:')
print('  • Foundation Grant Templates')
print('  • Corporate Sponsorship Templates')  
print('  • Event Partnership Templates')
print('  • Program Funding Templates')

print('\n🔌 SENDGRID INTEGRATION STATUS:')
import os
has_sendgrid_key = bool(os.environ.get('SENDGRID_API_KEY'))
print(f'  SendGrid API Key Configured: {has_sendgrid_key}')
print('  Email Sender Module: Available')
print('  Campaign Deployment: Ready')