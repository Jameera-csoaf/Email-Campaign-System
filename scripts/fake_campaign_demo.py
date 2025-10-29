#!/usr/bin/env python3
"""
Detailed Fake Campaign Demo
Shows exactly what emails would look like without sending them
"""

import os
import sys
import pandas as pd
from datetime import datetime

def run_fake_campaign_demo():
    """Run a detailed fake campaign to show email content"""
    
    print("🎭 FAKE CAMPAIGN DEMO - No Real Emails Sent")
    print("="*60)
    
    # Load database
    data_dir = os.path.join(os.getcwd(), 'data', 'corporations')
    csv_files = [f for f in os.listdir(data_dir) if f.startswith('comprehensive_fortune1000')]
    
    if not csv_files:
        print("❌ No corporation database found")
        return
    
    csv_file = sorted(csv_files, reverse=True)[0]
    csv_path = os.path.join(data_dir, csv_file)
    df = pd.read_csv(csv_path)
    
    print(f"📊 Database: {len(df)} corporations loaded")
    
    # Select some high-value targets for demo
    demo_targets = df[
        (df['state'].isin(['NY', 'CA', 'TX'])) &
        (df['estimated_typical_sponsorship'] >= 100000) &
        (df['arts_education_potential'].isin(['High', 'Medium']))
    ].head(5)
    
    print(f"🎯 Demo Campaign: '{len(demo_targets)} High-Value Prospects'")
    print(f"📧 Campaign Type: Partnership Outreach")
    print(f"📅 Campaign Date: {datetime.now().strftime('%B %d, %Y')}")
    
    print(f"\n📋 Target Recipients:")
    print("-" * 80)
    
    total_potential = 0
    
    for idx, company in demo_targets.iterrows():
        total_potential += company['estimated_typical_sponsorship']
        
        print(f"\n{idx+1}. {company['organization_name']}")
        print(f"   📍 Location: {company['city']}, {company['state']}")
        print(f"   🏭 Industry: {company['industry_sector']}")
        print(f"   💰 Sponsorship Potential: ${company['estimated_typical_sponsorship']:,.0f}")
        print(f"   🎨 Arts Interest: {company['arts_education_potential']}")
        print(f"   📧 Email: {company['email']}")
        print(f"   🌐 Website: {company['website']}")
    
    print(f"\n💰 Campaign Summary:")
    print(f"   • Total Recipients: {len(demo_targets)}")
    print(f"   • Total Sponsorship Potential: ${total_potential:,.0f}")
    print(f"   • Average Potential: ${total_potential/len(demo_targets):,.0f}")
    
    # Show sample email for first company
    if len(demo_targets) > 0:
        sample_company = demo_targets.iloc[0]
        
        print(f"\n📧 SAMPLE EMAIL PREVIEW")
        print("="*60)
        
        subject = f"Partnership Opportunity: {sample_company['organization_name']} x CSOAF Arts Initiative"
        print(f"📨 Subject: {subject}")
        print(f"📤 From: Community School of the Arts Foundation <promo@csoaf.org>")
        print(f"📬 To: {sample_company['email']}")
        
        print(f"\n📄 Email Content:")
        print("-" * 60)
        
        email_body = f"""
Dear Colleague at {sample_company['organization_name']},

I hope this message finds you well. I'm reaching out from the Community School 
of the Arts Foundation (CSOAF) regarding an exciting partnership opportunity 
that aligns perfectly with {sample_company['organization_name']}'s commitment 
to community development.

As a distinguished leader in {sample_company['industry_sector'].lower()}, 
{sample_company['organization_name']} understands the profound impact that 
strategic community investments can have on both social good and business outcomes.

PARTNERSHIP OPPORTUNITY HIGHLIGHTS:

🎓 Educational Excellence
   Students in our programs show 40% improvement in academic performance 
   and 95% graduation rates.

🤝 Community Building  
   Our programs bring together diverse communities in {sample_company['city']}, 
   fostering understanding and collaboration.

💼 Workforce Development
   Arts education develops critical thinking, creativity, and communication 
   skills essential for 21st-century careers.

🏆 Brand Recognition
   Partner organizations receive extensive community recognition and positive 
   brand association.

PARTNERSHIP INVESTMENT TIERS:

🥇 Platinum Partner ($50,000+): Program naming rights, executive board seat
🥈 Gold Partner ($25,000+): Scholarship fund establishment, quarterly reports  
🥉 Silver Partner ($10,000+): Workshop sponsorship, community recognition
🎨 Creative Partner ($5,000+): Event collaboration, volunteer opportunities

LOCAL IMPACT IN {sample_company['city'].upper()}, {sample_company['state']}:

With your support, we can reach an additional 200+ students in the 
{sample_company['city']} area, providing them with transformative arts 
education that builds confidence, creativity, and community connections.

NEXT STEPS:

I'd love to schedule a personalized 15-minute presentation to explore how 
{sample_company['organization_name']} can become a cornerstone partner in 
our mission to transform lives through arts education.

Thank you for your commitment to community excellence. I look forward to 
discussing how we can create lasting impact together.

Best regards,

CSOAF Partnership Development Team
Community School of the Arts Foundation
📧 promo@csoaf.org
📞 (555) 123-ARTS  
🌐 www.csoaf.org

---
This invitation was sent to {sample_company['organization_name']} due to your 
reputation for community leadership and social impact.
        """
        
        print(email_body)
        
        # Show campaign metrics
        print(f"\n📊 CAMPAIGN METRICS")
        print("="*60)
        print(f"📧 Emails to Send: {len(demo_targets)}")
        print(f"⏱️ Estimated Send Time: {len(demo_targets) * 2} minutes")
        print(f"📈 Expected Response Rate: 8-12% (industry average)")
        print(f"💬 Expected Responses: {int(len(demo_targets) * 0.1)} conversations")
        print(f"🤝 Expected Partnerships: {int(len(demo_targets) * 0.03)} partnerships")
        print(f"💰 Potential Partnership Value: ${total_potential * 0.03:,.0f}")
        
        # Show industry breakdown
        industry_counts = demo_targets['industry_sector'].value_counts()
        print(f"\n🏭 INDUSTRY TARGETING:")
        for industry, count in industry_counts.items():
            print(f"   • {industry}: {count} companies")
        
        # Show geographic breakdown  
        state_counts = demo_targets['state'].value_counts()
        print(f"\n📍 GEOGRAPHIC TARGETING:")
        for state, count in state_counts.items():
            print(f"   • {state}: {count} companies")
    
    print(f"\n🎭 FAKE CAMPAIGN COMPLETE!")
    print(f"✅ No real emails were sent - this was a demonstration")
    print(f"📋 To send real campaigns:")
    print(f"   1. Use: python src/campaigns/email_campaign_manager.py")
    print(f"   2. Or: python send_test_email.py (for individual test)")
    print(f"   3. System respects 100 emails/day limit automatically")
    
    return demo_targets

if __name__ == "__main__":
    run_fake_campaign_demo()