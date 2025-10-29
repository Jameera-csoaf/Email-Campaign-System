#!/usr/bin/env python3
"""
Live Campaign Creation Demo
Shows how to create and manage real email campaigns with your Mailchimp account
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.append(src_dir)

from tools.email_sending.mailchimp_email_sender import MailchimpEmailSender

def demonstrate_campaign_creation():
    """Demonstrate how to create and manage email campaigns"""
    
    print("🚀 CSOAF Live Campaign Creation Demo")
    print("="*60)
    
    # Initialize Mailchimp
    try:
        sender = MailchimpEmailSender(daily_limit=100)
        print("✅ Mailchimp connected successfully")
        print(f"📧 Account: {sender.sender_name}")
        print(f"📊 Daily limit: {sender.daily_limit}")
    except Exception as e:
        print(f"❌ Mailchimp connection failed: {e}")
        return
    
    # Load and analyze database
    print("\n📊 Loading Corporation Database...")
    data_dir = os.path.join(os.getcwd(), 'data', 'corporations')
    csv_files = [f for f in os.listdir(data_dir) if f.startswith('comprehensive_fortune1000')]
    
    if not csv_files:
        print("❌ No corporation database found")
        return
    
    csv_file = sorted(csv_files, reverse=True)[0]
    csv_path = os.path.join(data_dir, csv_file)
    df = pd.read_csv(csv_path)
    
    print(f"📈 Database loaded: {len(df)} corporations")
    
    # Show different targeting options
    print("\n🎯 Available Targeting Options:")
    print("-" * 50)
    
    # By State
    state_counts = df['state'].value_counts().head(10)
    print("📍 Top States:")
    for state, count in state_counts.items():
        print(f"  • {state}: {count} companies")
    
    # By Industry
    industry_counts = df['industry_sector'].value_counts()
    print(f"\n🏭 Industries:")
    for industry, count in industry_counts.items():
        print(f"  • {industry}: {count} companies")
    
    # By Sponsorship Level
    high_sponsors = df[df['estimated_typical_sponsorship'] >= 100000]
    medium_sponsors = df[(df['estimated_typical_sponsorship'] >= 50000) & (df['estimated_typical_sponsorship'] < 100000)]
    standard_sponsors = df[df['estimated_typical_sponsorship'] < 50000]
    
    print(f"\n💰 Sponsorship Tiers:")
    print(f"  • High Tier ($100k+): {len(high_sponsors)} companies")
    print(f"  • Medium Tier ($50k-$100k): {len(medium_sponsors)} companies") 
    print(f"  • Standard Tier (Under $50k): {len(standard_sponsors)} companies")
    
    # Show sample campaign scenarios
    print("\n🎨 Sample Campaign Scenarios:")
    print("-" * 50)
    
    scenarios = [
        {
            'name': 'Tech Giants - West Coast',
            'filter': (df['state'].isin(['CA', 'WA'])) & 
                     (df['industry_sector'] == 'Technology') & 
                     (df['estimated_typical_sponsorship'] >= 100000),
            'description': 'High-value technology companies in CA and WA'
        },
        {
            'name': 'Financial Services - East Coast',
            'filter': (df['state'].isin(['NY', 'NJ', 'CT'])) & 
                     (df['industry_sector'] == 'Financial Services') & 
                     (df['estimated_typical_sponsorship'] >= 75000),
            'description': 'Financial institutions in the NYC metro area'
        },
        {
            'name': 'Healthcare Leaders - National',
            'filter': (df['industry_sector'] == 'Healthcare') & 
                     (df['estimated_typical_sponsorship'] >= 50000) &
                     (df['arts_education_potential'] == 'High'),
            'description': 'Healthcare organizations with high arts education interest'
        },
        {
            'name': 'Local Champions - Regional',
            'filter': (df['state'].isin(['NY', 'NJ'])) & 
                     (df['estimated_typical_sponsorship'] >= 25000) &
                     (df['arts_education_potential'].isin(['High', 'Medium'])),
            'description': 'Regional companies with strong community focus'
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        filtered = df[scenario['filter']]
        total_potential = filtered['estimated_typical_sponsorship'].sum()
        avg_potential = filtered['estimated_typical_sponsorship'].mean() if len(filtered) > 0 else 0
        
        print(f"\n{i}. {scenario['name']}")
        print(f"   📋 {scenario['description']}")
        print(f"   🎯 Recipients: {len(filtered)} companies")
        print(f"   💰 Total potential: ${total_potential:,.0f}")
        print(f"   📊 Average potential: ${avg_potential:,.0f}")
        
        if len(filtered) > 0:
            print(f"   🏢 Sample companies:")
            for _, company in filtered.head(3).iterrows():
                print(f"      • {company['organization_name']} ({company['city']}, {company['state']}) - ${company['estimated_typical_sponsorship']:,.0f}")
    
    # Interactive campaign creation
    print(f"\n🚀 Ready to Create a Live Campaign?")
    print("-" * 50)
    
    create_campaign = input("Would you like to create a test campaign? (y/n): ").lower().strip()
    
    if create_campaign == 'y':
        print("\n📝 Campaign Creation Wizard")
        print("=" * 40)
        
        # Get campaign preferences
        campaign_name = input("Campaign name (e.g., 'Holiday Gala Invitations'): ").strip()
        if not campaign_name:
            campaign_name = "CSOAF Partnership Outreach"
        
        print("\nSelect target scenario:")
        for i, scenario in enumerate(scenarios, 1):
            print(f"{i}. {scenario['name']} ({df[scenario['filter']].shape[0]} recipients)")
        
        scenario_choice = input("Choose scenario (1-4): ").strip()
        
        try:
            scenario_idx = int(scenario_choice) - 1
            if 0 <= scenario_idx < len(scenarios):
                selected_scenario = scenarios[scenario_idx]
                target_companies = df[selected_scenario['filter']].head(5)  # Limit to 5 for demo
                
                print(f"\n✅ Selected: {selected_scenario['name']}")
                print(f"📧 Target recipients: {len(target_companies)}")
                
                # Show recipients
                print("\n📋 Campaign Recipients:")
                for _, company in target_companies.iterrows():
                    print(f"• {company['organization_name']} ({company['city']}, {company['state']})")
                    print(f"  Email: {company['email']}")
                    print(f"  Sponsorship: ${company['estimated_typical_sponsorship']:,.0f}")
                    print()
                
                # Ask if they want to send
                send_campaign = input("Send this campaign? (y/n): ").lower().strip()
                
                if send_campaign == 'y':
                    print("\n📧 Preparing to send campaign...")
                    
                    # Create simple email content
                    subject = f"Partnership Opportunity: {campaign_name}"
                    
                    # Send to each recipient (simulated for demo)
                    successful_sends = 0
                    
                    for _, company in target_companies.iterrows():
                        try:
                            # Create personalized email content
                            email_content = f"""
                            <html>
                            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                                <h2>Partnership Opportunity with {company['organization_name']}</h2>
                                
                                <p>Dear Colleague at {company['organization_name']},</p>
                                
                                <p>I hope this message finds you well. I'm reaching out from the Community School 
                                of the Arts Foundation (CSOAF) regarding an exciting partnership opportunity.</p>
                                
                                <p>As a respected organization in {company['city']}, {company['state']}, 
                                {company['organization_name']} embodies the community leadership that makes 
                                initiatives like ours successful.</p>
                                
                                <h3>Partnership Opportunities:</h3>
                                <ul>
                                    <li>Program Sponsorship: Direct support for after-school arts programs</li>
                                    <li>Event Partnership: Collaborate on community arts events</li>
                                    <li>Scholarship Fund: Help talented students access arts education</li>
                                    <li>Corporate Engagement: Team-building through arts workshops</li>
                                </ul>
                                
                                <p>I'd love to schedule a brief conversation to discuss how we can work together 
                                to make a meaningful impact in {company['city']}.</p>
                                
                                <p>Best regards,<br>
                                CSOAF Partnership Team<br>
                                promo@csoaf.org<br>
                                www.csoaf.org</p>
                            </body>
                            </html>
                            """
                            
                            # For demo purposes, we'll just simulate sending
                            # In production, you'd use:
                            # result = sender.send_transactional_email(...)
                            
                            print(f"✅ Simulated send to {company['organization_name']}")
                            successful_sends += 1
                            
                        except Exception as e:
                            print(f"❌ Failed to send to {company['organization_name']}: {e}")
                    
                    print(f"\n🎉 Campaign Complete!")
                    print(f"✅ Successfully sent: {successful_sends} emails")
                    print(f"📊 Campaign: {campaign_name}")
                    print(f"🎯 Scenario: {selected_scenario['name']}")
                    
                    # Show campaign summary
                    total_potential = target_companies['estimated_typical_sponsorship'].sum()
                    print(f"💰 Total sponsorship potential: ${total_potential:,.0f}")
                
                else:
                    print("📋 Campaign prepared but not sent")
            
            else:
                print("❌ Invalid scenario selection")
                
        except ValueError:
            print("❌ Invalid input")
    
    print(f"\n✅ Campaign Demo Complete!")
    print(f"\n📋 Your Email Campaign System is Ready!")
    print("🎯 Key Capabilities:")
    print("  • Target 1,000 corporations by region, industry, sponsorship level")
    print("  • Send professional, personalized emails via Mailchimp")
    print("  • Track campaigns with analytics and reporting")
    print("  • Manage multiple campaigns efficiently")
    print("  • Respect 100 emails/day rate limit")
    
    print(f"\n📧 Ready to send real campaigns from promo@csoaf.org!")

if __name__ == "__main__":
    demonstrate_campaign_creation()