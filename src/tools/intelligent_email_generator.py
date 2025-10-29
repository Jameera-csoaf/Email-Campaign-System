#!/usr/bin/env python3
"""
Intelligent Email Generator - Manager-Approved Template System
Uses manager's approved template with AI-powered personalization
"""

import sys
import os
import pandas as pd
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from campaigns.email_templates.healing_arts_template_campaign import HealingArtsTemplateEngine
from campaigns.email_templates.manager_approved_templates import (
    generate_personalized_email, 
    get_available_templates,
    get_available_locations,
    generate_subject_line
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'intelligent_email_generation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

def generate_emails_from_intelligent_campaign(campaign_file):
    """Generate emails from intelligent campaign categorization"""
    
    print("🎯 INTELLIGENT EMAIL GENERATOR")
    print("=" * 60)
    
    # Load intelligent campaign data
    logger.info(f"Loading intelligent campaign data from: {campaign_file}")
    
    if not os.path.exists(campaign_file):
        logger.error(f"Campaign file not found: {campaign_file}")
        return None
    
    campaign_data = pd.read_csv(campaign_file)
    logger.info(f"Loaded {len(campaign_data)} categorized contacts")
    
    # Initialize email generator
    email_generator = HealingArtsTemplateEngine()
    
    # Generate emails based on template assignments
    generated_emails = []
    
    for idx, contact in campaign_data.iterrows():
        sponsor_name = contact['sponsor_name']
        alignment_score = contact.get('mission_alignment_score', contact.get('alignment_score', 0))
        
        logger.info(f"Generating email for {sponsor_name} (Score: {alignment_score:.1f})")
        
        # Prepare contact data for manager's template system
        sponsor_data = {
            'organization_name': sponsor_name,
            'contact_name': contact.get('contact_person', 'Valued Partner'),
            'program_areas': contact.get('program_areas', ''),
            'mission_alignment_score': alignment_score,
            'city': contact.get('city', ''),
            'state': contact.get('state', ''),
            'website': contact.get('website', ''),
            'email': contact.get('email', '')
        }
        
        # Determine sponsorship type based on alignment score and organization type
        if alignment_score >= 80:
            template_type = 'major_sponsor'
        elif 'corporation' in contact.get('organization_type', '').lower():
            template_type = 'corporate_sponsor'
        elif alignment_score >= 50:
            template_type = 'foundation_grant'
        else:
            template_type = 'standard'
        
        # Generate email using manager's approved template
        try:
            email_content = generate_personalized_email(
                sponsor_data=sponsor_data,
                template_type=template_type,
                location='new_york'
            )
            
            subject_line = generate_subject_line('arts_partnership', 'New York')
            
        except Exception as e:
            logger.warning(f"Error generating email for {sponsor_name}: {str(e)}")
            continue
        
        # Add email to collection
        email_data = {
            'sponsor_name': sponsor_name,
            'email_address': sponsor_data['email'],
            'template_used': template_type,
            'alignment_score': alignment_score,
            'subject': subject_line,
            'content': email_content,
            'template_type': 'manager_approved',
            'contact_name': sponsor_data['contact_name'],
            'program_areas': sponsor_data['program_areas']
        }
        
        generated_emails.append(email_data)
    
    # Save generated emails
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"campaigns/email_templates/intelligent_emails_{timestamp}.csv"
    
    emails_df = pd.DataFrame(generated_emails)
    emails_df.to_csv(output_file, index=False)
    
    logger.info(f"Generated {len(generated_emails)} emails")
    logger.info(f"Emails saved to: {output_file}")
    
    # Print summary
    print(f"\\n✅ EMAIL GENERATION COMPLETE!")
    print(f"📊 Generated {len(generated_emails)} personalized emails")
    print(f"📁 Saved to: {output_file}")
    print(f"\\n📈 Template Distribution:")
    template_counts = emails_df['template_used'].value_counts().sort_index()
    for template, count in template_counts.items():
        print(f"   Template {template}: {count} emails")
    
    print(f"\\n🎯 Potential Level Distribution:")
    potential_counts = emails_df['potential_level'].value_counts()
    for level, count in potential_counts.items():
        print(f"   {level}: {count} emails")
    
    print(f"\\n🚀 Ready for SendGrid deployment!")
    print(f"💡 Use: python tools/email_sending/sendgrid_email_sender.py")
    
    return output_file

def main():
    """Main execution function"""
    
    # Find the most recent intelligent campaign file
    campaign_dir = "campaigns/sponsor_data"
    
    # Look for intelligent campaign files
    campaign_files = [f for f in os.listdir(campaign_dir) if f.startswith('intelligent_campaign_') and f.endswith('.csv')]
    
    if not campaign_files:
        logger.error("No intelligent campaign files found! Run intelligent_campaign_agent.py first.")
        return
    
    # Use the most recent campaign file
    latest_campaign = sorted(campaign_files)[-1]
    campaign_file = os.path.join(campaign_dir, latest_campaign)
    
    logger.info(f"Using latest campaign file: {latest_campaign}")
    
    # Generate emails
    generate_emails_from_intelligent_campaign(campaign_file)

if __name__ == "__main__":
    main()