#!/usr/bin/env python3
"""
Quick Test: Email Campaign System Demo
Simple test of the email campaign functionality
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

def test_email_campaign_demo():
    """Test the email campaign system without requiring API keys"""
    
    print("🚀 Email Campaign System Demo")
    print("="*50)
    
    # Load corporation database
    data_dir = os.path.join(os.getcwd(), 'data', 'corporations')
    csv_files = [f for f in os.listdir(data_dir) if f.startswith('comprehensive_fortune1000')]
    
    if not csv_files:
        print("❌ No corporation database found")
        return
    
    # Load most recent database
    csv_file = sorted(csv_files, reverse=True)[0]
    csv_path = os.path.join(data_dir, csv_file)
    
    print(f"📊 Loading database: {csv_file}")
    df = pd.read_csv(csv_path)
    print(f"📈 Total corporations: {len(df)}")
    
    # Filter for email campaign targets
    # NY and CA, Technology and Financial Services, $25k+ sponsorship
    filtered_df = df[
        (df['state'].isin(['NY', 'CA'])) &
        (df['industry_sector'].isin(['Technology', 'Financial Services'])) &
        (df['estimated_typical_sponsorship'] >= 25000) &
        (df['arts_education_potential'].isin(['High', 'Medium']))
    ].head(10)  # Limit to 10 for demo
    
    print(f"🎯 Filtered recipients: {len(filtered_df)}")
    
    if len(filtered_df) == 0:
        print("❌ No recipients match criteria")
        return
    
    # Show sample recipients
    print("\n📋 Sample Recipients:")
    print("-" * 80)
    for idx, row in filtered_df.iterrows():
        print(f"• {row['organization_name']} ({row['city']}, {row['state']})")
        print(f"  Industry: {row['industry_sector']}")
        print(f"  Sponsorship: ${row['estimated_typical_sponsorship']:,}")
        print(f"  Arts Interest: {row['arts_education_potential']}")
        print(f"  Email: {row['email']}")
        print()
    
    # Generate sample email content
    sample_org = filtered_df.iloc[0]
    
    print("📧 Sample Email Preview:")
    print("-" * 80)
    
    subject = f"Partnership Opportunity: {sample_org['organization_name']} x CSOAF Arts Initiative"
    print(f"Subject: {subject}")
    print()
    
    email_content = f"""
Dear Colleague at {sample_org['organization_name']},

I hope this message finds you well. I'm reaching out from the Community School 
of the Arts Foundation (CSOAF) regarding an exciting partnership opportunity 
that aligns with {sample_org['organization_name']}'s commitment to community 
development.

As a leader in {sample_org['industry_sector'].lower()}, {sample_org['organization_name']} 
understands the importance of creativity and innovation. Arts education develops 
the same creative problem-solving skills that drive success in your industry.

Partnership Opportunities:
• Program Sponsorship: Direct support for after-school arts programs
• Event Partnership: Collaborate on community arts events in {sample_org['city']}
• Scholarship Fund: Help talented students access arts education
• Corporate Engagement: Team-building through arts workshops

With your support, we can reach an additional 200+ students in the {sample_org['city']} 
area, providing them with transformative arts education that builds confidence, 
creativity, and community connections.

I'd love to schedule a brief 15-minute call to discuss how {sample_org['organization_name']} 
can make a meaningful impact in our community while achieving your corporate 
social responsibility goals.

Thank you for your time and consideration.

Best regards,
CSOAF Partnership Team
promo@csoaf.org
www.csoaf.org
"""
    
    print(email_content)
    
    # Campaign statistics
    print("📊 Campaign Statistics:")
    print("-" * 80)
    print(f"Total Database Size: {len(df):,} corporations")
    print(f"Target States: NY, CA")
    print(f"Target Industries: Technology, Financial Services")
    print(f"Minimum Sponsorship: $25,000")
    print(f"Arts Interest: High, Medium")
    print(f"Qualified Recipients: {len(filtered_df)}")
    print(f"Daily Email Limit: 100")
    print(f"Campaign Send Time: ~{len(filtered_df)} minutes")
    
    # Show industry breakdown
    industry_breakdown = filtered_df['industry_sector'].value_counts()
    print(f"\n🏭 Industry Breakdown:")
    for industry, count in industry_breakdown.items():
        print(f"• {industry}: {count} companies")
    
    # Show state breakdown
    state_breakdown = filtered_df['state'].value_counts()
    print(f"\n🗺️ State Breakdown:")
    for state, count in state_breakdown.items():
        print(f"• {state}: {count} companies")
    
    # Show sponsorship capacity breakdown
    avg_sponsorship = filtered_df['estimated_typical_sponsorship'].mean()
    max_sponsorship = filtered_df['estimated_typical_sponsorship'].max()
    total_potential = filtered_df['estimated_typical_sponsorship'].sum()
    
    print(f"\n💰 Sponsorship Potential:")
    print(f"• Average Sponsorship: ${avg_sponsorship:,.0f}")
    print(f"• Maximum Sponsorship: ${max_sponsorship:,.0f}")
    print(f"• Total Potential: ${total_potential:,.0f}")
    
    print("\n✅ Email Campaign System Ready!")
    print("\n📋 To Send Real Campaigns:")
    print("1. Set MAILCHIMP_API_KEY environment variable")
    print("2. Use: manager.send_campaign(campaign_id, test_send=True)")
    print("3. Then: manager.send_campaign(campaign_id) for live sending")
    
    return filtered_df

if __name__ == "__main__":
    test_email_campaign_demo()