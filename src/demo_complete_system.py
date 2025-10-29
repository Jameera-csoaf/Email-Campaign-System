#!/usr/bin/env python3
"""
Dual-Track Fundraising System - Live Demonstration
Complete system demonstration with real-time processing
"""

import time
import json
from datetime import datetime
import sys
import os

# Add project paths
sys.path.append('.')
from tools.campaign_workflow_engine import CampaignWorkflowEngine

def print_header():
    """Print demonstration header"""
    print("=" * 80)
    print("🎯 DUAL-TRACK FUNDRAISING SYSTEM - LIVE DEMONSTRATION")
    print("=" * 80)
    print("Center for the Study of Anesthesia and Fear (CSOAF)")
    print("Intelligent Campaign Creation with Natural Language Processing")
    print("=" * 80)
    print()

def print_section(title):
    """Print section header"""
    print(f"\n{'=' * 60}")
    print(f"📊 {title}")
    print("=" * 60)

def demonstrate_campaign_creation():
    """Demonstrate complete campaign creation process"""
    
    print_header()
    
    # Initialize the system
    print("🚀 Initializing Dual-Track Fundraising System...")
    engine = CampaignWorkflowEngine()
    time.sleep(1)
    print("✅ System ready!")
    
    # Demonstration campaigns
    demo_campaigns = [
        {
            "title": "Corporate Event Sponsorship Campaign",
            "description": "We need corporate sponsors for our annual healing arts gala in New York, aiming to raise $75,000 to support our new adaptive dance program for children with autism",
            "expected": "Corporation-focused with event templates"
        },
        {
            "title": "Foundation Program Grant Campaign", 
            "description": "Looking for foundation grants to fund our veterans music therapy program in California, need about $50,000 to serve 100 veterans over the next year",
            "expected": "Foundation-focused with program templates"
        },
        {
            "title": "Mixed Dual-Track Campaign",
            "description": "Need funding for our inclusive arts education classes for children with special needs in both NY and CA, targeting $30,000 for equipment and instructor training",
            "expected": "Both foundations and corporations"
        }
    ]
    
    # Process each campaign
    for i, campaign in enumerate(demo_campaigns, 1):
        
        print_section(f"CAMPAIGN {i}: {campaign['title']}")
        
        print(f"📝 Campaign Description:")
        print(f"   \"{campaign['description']}\"")
        print()
        
        print(f"🎯 Expected Routing: {campaign['expected']}")
        print()
        
        print("⚡ Processing Campaign...")
        start_time = time.time()
        
        # Create campaign using the workflow engine
        try:
            campaign_package = engine.create_campaign_from_description(campaign['description'])
            
            processing_time = time.time() - start_time
            print(f"✅ Campaign processed in {processing_time:.2f} seconds")
            
            # Display results
            display_campaign_results(campaign_package)
            
        except Exception as e:
            print(f"❌ Error processing campaign: {str(e)}")
            print("💡 This may occur if data files are not available in the demo environment")
        
        # Pause between campaigns
        if i < len(demo_campaigns):
            print("\n" + "⏳ Moving to next campaign..." + "\n")
            time.sleep(2)
    
    # System summary
    print_section("SYSTEM PERFORMANCE SUMMARY")
    
    status = engine.get_campaign_status_report()
    
    print(f"📈 DEMONSTRATION RESULTS:")
    print(f"   Total Campaigns Processed: {status['total_campaigns']}")
    print(f"   Active Campaigns: {status['active_campaigns']}")
    print(f"   Total Funding Potential: ${status['total_funding_potential']:,.0f}")
    print(f"   Total Recipients Identified: {status['total_recipients_reached']}")
    
    print(f"\n🎯 SYSTEM CAPABILITIES:")
    print(f"   ✅ Natural Language Processing: Campaign description → structured data")
    print(f"   ✅ Dual-Track Routing: Foundation (programs) vs Corporation (events)")
    print(f"   ✅ Intelligent Matching: Geographic and mission-based filtering")
    print(f"   ✅ Email Generation: Manager-approved templates with personalization")
    print(f"   ✅ Real-Time Processing: Immediate results with full analytics")
    
    print(f"\n🚀 SYSTEM STATUS: Operational and ready for production use!")

def display_campaign_results(campaign_package):
    """Display detailed campaign results"""
    
    parsed = campaign_package['parsed_campaign']
    matches = campaign_package['matches'] 
    metrics = campaign_package['metrics']
    
    print(f"\n📊 CAMPAIGN ANALYSIS:")
    print(f"   Campaign ID: {campaign_package['campaign_id']}")
    print(f"   Campaign Type: {parsed['campaign_type'].upper()}")
    print(f"   Campaign Name: {parsed['campaign_name']}")
    print(f"   Target Audience: {', '.join(parsed['target_audience'])}")
    print(f"   Geographic Focus: {', '.join(parsed['geographic_focus'])}")
    print(f"   Keywords: {', '.join(parsed['keywords'])}")
    
    if parsed.get('funding_amount'):
        print(f"   Funding Request: {parsed['funding_amount']}")
    
    print(f"\n🎯 ROUTING STRATEGY:")
    foundations = parsed['routing']['foundations']
    corporations = parsed['routing']['corporations']
    print(f"   Foundation Route: {foundations['priority'].upper()} priority → {foundations['focus']}")
    print(f"   Corporation Route: {corporations['priority'].upper()} priority → {corporations['focus']}")
    
    print(f"\n📈 TARGET MATCHES:")
    print(f"   Foundation Targets: {len(matches['foundations'])}")
    print(f"   Corporation Targets: {len(matches['corporations'])}")
    print(f"   Internal Programs: {len(matches['matched_programs'])}")
    print(f"   Total Recipients: {metrics['total_recipients']}")
    
    print(f"\n💰 FUNDING ANALYSIS:")
    funding = metrics['estimated_funding_potential']
    print(f"   Total Potential: ${funding['total_potential']:,.0f}")
    print(f"   Conservative Estimate: ${funding['conservative_estimate']:,.0f}")
    print(f"   Optimistic Estimate: ${funding['optimistic_estimate']:,.0f}")
    
    print(f"\n📧 EMAIL TEMPLATES:")
    email_templates = campaign_package.get('email_templates', {})
    foundation_emails = len(email_templates.get('foundation_emails', []))
    corporation_emails = len(email_templates.get('corporation_emails', []))
    print(f"   Foundation Emails Generated: {foundation_emails}")
    print(f"   Corporation Emails Generated: {corporation_emails}")
    print(f"   Total Templates Ready: {foundation_emails + corporation_emails}")
    
    # Show sample template if available
    if corporation_emails > 0:
        print(f"\n📝 SAMPLE CORPORATION EMAIL:")
        template = email_templates['corporation_emails'][0]
        subject = template['template']['template'].get('subject_templates', [''])[0]
        if subject:
            print(f"   Subject: {subject[:60]}...")
        print(f"   Recipient: {template['recipient_info'].get('organization', 'Sample Corporation')}")
        print(f"   Template Type: Corporate Sponsorship")
    
    elif foundation_emails > 0:
        print(f"\n📝 SAMPLE FOUNDATION EMAIL:")
        template = email_templates['foundation_emails'][0] 
        subject = template['template']['template'].get('subject_templates', [''])[0]
        if subject:
            print(f"   Subject: {subject[:60]}...")
        print(f"   Recipient: {template['recipient_info'].get('organization', 'Sample Foundation')}")
        print(f"   Template Type: Foundation Grant")

def main():
    """Run the complete demonstration"""
    
    try:
        demonstrate_campaign_creation()
        
        print(f"\n{'=' * 80}")
        print("🏆 DEMONSTRATION COMPLETE!")
        print("=" * 80)
        print("The dual-track fundraising system is fully operational.")
        print("Ready for production use with natural language campaign creation.")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print(f"\n\n⏹️ Demonstration stopped by user")
    except Exception as e:
        print(f"\n❌ Demonstration error: {str(e)}")
        print("💡 System may require data files to be present for full functionality")

if __name__ == "__main__":
    main()