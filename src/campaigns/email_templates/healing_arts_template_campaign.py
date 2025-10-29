#!/usr/bin/env python3
"""
Enhanced Healing Through Arts Email Campaign Generator
Uses 5 specific templates based on donor history and contact information
"""

import pandas as pd
import logging
from datetime import datetime
import os
import re
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class HealingArtsTemplateEngine:
    def __init__(self):
        # Template 1 - Has Name + Past Donor
        self.template_1 = {
            'subject': '{first_name}, Healing Through Arts: NYC Schools',
            'content': """Hi {first_name},

We're excited to invite you to join us as a sponsor of Healing Through Arts: NYC Schools, an unforgettable evening where art, music, and community come together to create lasting impact for NYC students.

[Insert banner image here]
"Students performing arts in NYC schools"

🎯 **Mission Connection:** We've identified a strong alignment between your organization's focus on {program_areas} and our commitment to accessible arts education for NYC students with disabilities and diverse learning needs.

Why sponsor this event?

Direct community impact: Every sponsorship dollar funds arts healing programs in underserved NYC schools, particularly supporting students with disabilities through creative educational pathways.

Exclusive engagement: Connect with city leaders, artists, and philanthropists at a vibrant evening of performances, wine tasting, and conversations.

🎭 Healing Through Arts: NYC Schools Benefit
📅 Monday, November 18, 2025 | 7:00 PM – 9:00 PM (doors open 6:30 PM)
📍 Rake Wine Bar (45 1st Ave, NYC)
🎟️ $35 per ticket
✨ Arts displays & live performances
🥂 Wine tasting & hors d'oeuvres
🤝 Meet fellow changemakers

Every ticket funds arts healing programs—attend to see how you can support further.

👉 [Get Your Ticket]

Corporate sponsors: Companies can also support, attend to learn more.

With gratitude,
Jameera Mahima Gujjarlapudi
Community School of Arts Foundation
🌐 Website: csoaf.org
📞 Phone: 917 216-5176"""
        }

        # Template 2 - Has Name + Never Donated
        self.template_2 = {
            'subject': '{first_name}, Healing Through Arts: NYC Schools',
            'content': """Hi {first_name},

We're excited to invite you to join us as a sponsor of Healing Through Arts: NYC Schools, an unforgettable evening where art, music, and community come together to create lasting impact for NYC students.

[Insert banner image here]
"Students performing arts in NYC schools"

🎯 **Shared Vision:** Your organization's work in {program_areas} aligns beautifully with our mission to provide creative educational pathways for NYC students, especially those with disabilities and diverse learning needs.

Why sponsor this event?

Direct community impact: Every sponsorship dollar funds arts healing programs in underserved NYC schools, creating accessible opportunities for students who benefit most from alternative learning approaches.

Exclusive engagement: Connect with city leaders, artists, and philanthropists at a vibrant evening of performances, wine tasting, and conversations.

🎭 Healing Through Arts: NYC Schools Benefit
📅 Monday, November 18, 2025 | 7:00 PM – 9:00 PM (doors open 6:30 PM)
📍 Rake Wine Bar (45 1st Ave, NYC)
🎟️ $35 per ticket
✨ Arts displays & live performances
🥂 Wine tasting & hors d'oeuvres
🤝 Meet fellow changemakers

Every ticket funds arts healing programs—attend to see how you can support further.

👉 [Get Your Ticket]

Corporate sponsors: Companies can also support, attend to learn more.

With gratitude,
Jameera Mahima Gujjarlapudi
Community School of Arts Foundation
🌐 Website: csoaf.org
📞 Phone: 917 216-5176"""
        }

        # Template 3 - No Name + Past Donor
        self.template_3 = {
            'subject': 'Healing Through Arts: NYC Schools',
            'content': """Hello,

We're excited to invite you to join us as a sponsor of Healing Through Arts: NYC Schools, an unforgettable evening where art, music, and community come together to create lasting impact for NYC students.

[Insert banner image here]
"Students performing arts in NYC schools"

🎯 **Partnership Opportunity:** Given your organization's commitment to {program_areas}, we believe you'll appreciate our innovative approach to arts education that serves NYC students with disabilities and creates inclusive community school environments.

Why sponsor this event?

Direct community impact: Every sponsorship dollar funds arts healing programs in underserved NYC schools, specifically supporting accessible arts education and creative pathways for students with diverse learning needs.

Exclusive engagement: Connect with city leaders, artists, and philanthropists at a vibrant evening of performances, wine tasting, and conversations.

🎭 Healing Through Arts: NYC Schools Benefit
📅 Monday, November 18, 2025 | 7:00 PM – 9:00 PM (doors open 6:30 PM)
📍 Rake Wine Bar (45 1st Ave, NYC)
🎟️ $35 per ticket
✨ Arts displays & live performances
🥂 Wine tasting & hors d'oeuvres
🤝 Meet fellow changemakers

Every ticket funds arts healing programs—attend to see how you can support further.

👉 [Get Your Ticket]

Corporate sponsors: Companies can also support, attend to learn more.

With gratitude,
Jameera Mahima Gujjarlapudi
Community School of Arts Foundation
🌐 Website: csoaf.org
📞 Phone: 917 216-5176"""
        }

        # Template 4 - No Name + Never Donated
        self.template_4 = {
            'subject': 'Healing Through Arts: NYC Schools',
            'content': """Hello,

We're excited to invite you to join us as a sponsor of Healing Through Arts: NYC Schools, an unforgettable evening where art, music, and community come together to create lasting impact for NYC students.

[Insert banner image here]
"Students performing arts in NYC schools"

🎯 **Aligned Impact:** We've identified your organization's focus on {program_areas} as perfectly complementing our mission to provide accessible arts education and creative learning opportunities for NYC students, particularly those with disabilities.

Why sponsor this event?

Direct community impact: Every sponsorship dollar funds arts healing programs in underserved NYC schools, creating inclusive environments where all students can thrive through creative expression.

Exclusive engagement: Connect with city leaders, artists, and philanthropists at a vibrant evening of performances, wine tasting, and conversations.

🎭 Healing Through Arts: NYC Schools Benefit
📅 Monday, November 18, 2025 | 7:00 PM – 9:00 PM (doors open 6:30 PM)
📍 Rake Wine Bar (45 1st Ave, NYC)
🎟️ $35 per ticket
✨ Arts displays & live performances
🥂 Wine tasting & hors d'oeuvres
🤝 Meet fellow changemakers

Every ticket funds arts healing programs—attend to see how you can support further.

👉 [Get Your Ticket]

Corporate sponsors: Companies can also support, attend to learn more.

With gratitude,
Jameera Mahima Gujjarlapudi
Community School of Arts Foundation
🌐 Website: csoaf.org
📞 Phone: 917 216-5176"""
        }

        # Template 5 - Internal Team (@csoaf.org)
        self.template_5 = {
            'subject': 'TEAM: Healing Through Arts — Let\'s Fill Rake Wine Bar! 🎉',
            'content': """Hi Team,

We're excited to invite you to join us as a sponsor of Healing Through Arts: NYC Schools, an unforgettable evening where art, music, and community come together to create lasting impact for NYC students.

[Insert banner image here]
"Students performing arts in NYC schools"

🎯 **Our Mission in Action:** This event perfectly showcases our commitment to accessible arts education, creative pathways for students with disabilities, and building inclusive community school environments.

Why sponsor this event?

Direct community impact: Every sponsorship dollar funds arts healing programs in underserved NYC schools, directly supporting our mission of providing accessible arts education for students with diverse learning needs.

Exclusive engagement: Connect with city leaders, artists, and philanthropists at a vibrant evening of performances, wine tasting, and conversations.

🎭 Healing Through Arts: NYC Schools Benefit
📅 Monday, November 18, 2025 | 7:00 PM – 9:00 PM (doors open 6:30 PM)
📍 Rake Wine Bar (45 1st Ave, NYC)
🎟️ $35 per ticket
✨ Arts displays & live performances
🥂 Wine tasting & hors d'oeuvres
🤝 Meet fellow changemakers

Every ticket funds arts healing programs—let's spread the word and fill the room!

👉 [Get Your Ticket]

With gratitude,
Jameera Mahima Gujjarlapudi
Community School of Arts Foundation
🌐 Website: csoaf.org
📞 Phone: 917 216-5176"""
        }

    def extract_first_name(self, full_name):
        """Extract first name from full name or organization name"""
        if not full_name or pd.isna(full_name):
            return None
        
        name = str(full_name).strip()
        
        # Skip if it's clearly an organization (contains org words)
        org_indicators = ['foundation', 'fund', 'trust', 'inc', 'corp', 'llc', 'organization', 
                         'institute', 'association', 'center', 'society', 'company', 'enterprises']
        
        if any(indicator in name.lower() for indicator in org_indicators):
            return None
        
        # Try to extract first name
        parts = name.split()
        if len(parts) >= 1:
            first_part = parts[0]
            # Check if it looks like a real first name (not title, etc.)
            if first_part.lower() not in ['mr', 'mrs', 'ms', 'dr', 'prof', 'president', 'director']:
                return first_part.title()
        
        return None

    def determine_donor_history(self, sponsor_data):
        """Determine if this is a past donor based on available data"""
        # Check for donation history indicators
        donation_indicators = [
            'sponsorship_amount', 'last_donation', 'donation_history', 
            'previous_support', 'past_donor', 'total_donated'
        ]
        
        for indicator in donation_indicators:
            if indicator in sponsor_data and sponsor_data[indicator]:
                try:
                    # If it's a number and > 0, they're a past donor
                    value = float(sponsor_data[indicator])
                    if value > 0:
                        return True
                except:
                    # If it's text indicating past support
                    if str(sponsor_data[indicator]).lower() in ['yes', 'true', 'past', 'previous']:
                        return True
        
        # Check response_received field
        if 'response_received' in sponsor_data:
            if str(sponsor_data['response_received']).lower() == 'yes':
                return True
        
        # Default: assume new donor for conservative approach
        return False

    def is_internal_email(self, email):
        """Check if email is internal (@csoaf.org)"""
        if not email or pd.isna(email):
            return False
        return '@csoaf.org' in str(email).lower()

    def select_template(self, sponsor_data):
        """Select appropriate template based on name availability and donor history"""
        
        # Check if internal email
        email = sponsor_data.get('email', '')
        if self.is_internal_email(email):
            return 5, self.template_5
        
        # Extract first name
        sponsor_name = sponsor_data.get('sponsor_name', '')
        first_name = self.extract_first_name(sponsor_name)
        
        # Determine donor history
        is_past_donor = self.determine_donor_history(sponsor_data)
        
        # Select template based on logic
        if first_name and is_past_donor:
            return 1, self.template_1  # Has Name + Past Donor
        elif first_name and not is_past_donor:
            return 2, self.template_2  # Has Name + Never Donated
        elif not first_name and is_past_donor:
            return 3, self.template_3  # No Name + Past Donor
        else:
            return 4, self.template_4  # No Name + Never Donated

    def generate_email(self, sponsor_data):
        """Generate personalized email using appropriate template"""
        
        template_num, template = self.select_template(sponsor_data)
        
        # Get variables for personalization
        sponsor_name = sponsor_data.get('sponsor_name', 'Friend')
        first_name = self.extract_first_name(sponsor_name)
        
        # Generate subject line
        if first_name and template_num in [1, 2]:
            subject = template['subject'].format(first_name=first_name)
        else:
            subject = template['subject']
        
        # Get program areas for mission alignment personalization
        program_areas = sponsor_data.get('program_areas', 'community impact and education')
        if pd.isna(program_areas) or not program_areas:
            program_areas = 'community impact and education'
        
        # Generate email content
        if first_name and template_num in [1, 2]:
            content = template['content'].format(first_name=first_name, program_areas=program_areas)
        else:
            content = template['content'].format(program_areas=program_areas)
        
        return {
            'template_number': template_num,
            'email_subject': subject,
            'email_content': content,
            'first_name_used': first_name if template_num in [1, 2] else None,
            'template_type': self.get_template_description(template_num)
        }

    def get_template_description(self, template_num):
        """Get description of template type"""
        descriptions = {
            1: "Has Name + Past Donor",
            2: "Has Name + Never Donated", 
            3: "No Name + Past Donor",
            4: "No Name + Never Donated",
            5: "Internal Team (@csoaf.org)"
        }
        return descriptions.get(template_num, "Unknown")

    def generate_campaign(self, input_csv, output_dir='data/results', max_emails=200):
        """Generate personalized email campaign using the 5 templates"""
        
        logger.info(f"Loading sponsors from: {input_csv}")
        df = pd.read_csv(input_csv)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Process sponsors
        campaign_data = []
        template_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        # Limit to max_emails for efficiency
        df_subset = df.head(max_emails)
        logger.info(f"Generating emails for {len(df_subset)} sponsors...")
        
        for index, row in df_subset.iterrows():
            sponsor_name = row.get('sponsor_name', f'Sponsor_{index}')
            
            # Generate personalized email
            email_data = self.generate_email(row)
            template_counts[email_data['template_number']] += 1
            
            # Combine with original sponsor data
            campaign_record = {
                'sponsor_name': sponsor_name,
                'city': row.get('city', ''),
                'state': row.get('state', ''),
                'email': row.get('email', ''),
                'website': row.get('website', ''),
                'template_number': email_data['template_number'],
                'template_type': email_data['template_type'],
                'first_name_used': email_data['first_name_used'],
                'email_subject': email_data['email_subject'],
                'email_content': email_data['email_content'],
                'campaign_status': 'ready_to_send',
                'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            campaign_data.append(campaign_record)
            
            # Log progress
            if (index + 1) % 50 == 0:
                logger.info(f"Generated {index + 1} emails...")

        # Save campaign data
        campaign_df = pd.DataFrame(campaign_data)
        
        # Create timestamped filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        campaign_file = os.path.join(output_dir, f'healing_arts_template_campaign_{timestamp}.csv')
        
        # Save complete campaign
        campaign_df.to_csv(campaign_file, index=False)
        logger.info(f"Campaign saved: {campaign_file}")
        
        # Create template-specific files
        template_files = {}
        for template_num in range(1, 6):
            template_df = campaign_df[campaign_df['template_number'] == template_num]
            if len(template_df) > 0:
                template_name = template_df.iloc[0]['template_type'].lower().replace(' ', '_').replace('+', '').replace('(', '').replace(')', '').replace('@', 'at').replace('.', '')
                template_file = os.path.join(output_dir, f'template_{template_num}_{template_name}_{timestamp}.csv')
                template_df.to_csv(template_file, index=False)
                template_files[template_num] = template_file
                logger.info(f"Saved {len(template_df)} Template {template_num} emails to: {template_file}")

        # Generate summary report
        self.create_template_summary(campaign_df, template_counts, output_dir, timestamp)
        
        return campaign_file, template_files, template_counts

    def create_template_summary(self, campaign_df, template_counts, output_dir, timestamp):
        """Create campaign summary report"""
        
        summary_file = os.path.join(output_dir, f'template_campaign_summary_{timestamp}.md')
        
        with open(summary_file, 'w') as f:
            f.write("# Healing Through Arts: Template-Based Campaign Summary\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall stats
            total_sponsors = len(campaign_df)
            with_emails = len(campaign_df[campaign_df['email'].notna() & (campaign_df['email'] != '')])
            with_first_names = len(campaign_df[campaign_df['first_name_used'].notna()])
            
            f.write(f"## Campaign Statistics\n")
            f.write(f"- **Total Sponsors**: {total_sponsors}\n")
            f.write(f"- **With Email Addresses**: {with_emails} ({with_emails/total_sponsors*100:.1f}%)\n")
            f.write(f"- **With First Names**: {with_first_names} ({with_first_names/total_sponsors*100:.1f}%)\n\n")
            
            # Template breakdown
            f.write("## Template Distribution\n")
            for template_num, count in template_counts.items():
                if count > 0:
                    template_desc = self.get_template_description(template_num)
                    percentage = (count / total_sponsors) * 100
                    f.write(f"- **Template {template_num}** ({template_desc}): {count} emails ({percentage:.1f}%)\n")
            
            f.write("\n## Template Details\n")
            f.write("- **Template 1**: Personalized with first name, past donor recognition\n")
            f.write("- **Template 2**: Personalized with first name, new prospect approach\n")  
            f.write("- **Template 3**: General greeting, past donor recognition\n")
            f.write("- **Template 4**: General greeting, new prospect approach\n")
            f.write("- **Template 5**: Internal team communication style\n")
            
            f.write("\n## Geographic Distribution\n")
            state_counts = campaign_df['state'].value_counts().head(10)
            for state, count in state_counts.items():
                f.write(f"- **{state}**: {count} sponsors\n")

        logger.info(f"Template campaign summary saved: {summary_file}")

def main():
    print("=" * 80)
    print("HEALING THROUGH ARTS: 5-TEMPLATE EMAIL CAMPAIGN GENERATOR")
    print("=" * 80)
    print("Templates:")
    print("1. Has Name + Past Donor")
    print("2. Has Name + Never Donated")
    print("3. No Name + Past Donor") 
    print("4. No Name + Never Donated")
    print("5. Internal Team (@csoaf.org)")
    print("=" * 80)
    
    template_engine = HealingArtsTemplateEngine()
    
    # Check for command line argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        max_emails = 200  # Default for command line usage
        print(f"Using command line file: {input_file}")
        campaign_file, template_files, counts = template_engine.generate_campaign(input_file, max_emails=max_emails)
        
        print(f"\n🎭 5-Template Campaign Generated!")
        print(f"📧 Main campaign file: {campaign_file}")
        print(f"\n📊 Template Distribution:")
        for template_num, count in counts.items():
            if count > 0:
                template_desc = template_engine.get_template_description(template_num)
                print(f"  • Template {template_num} ({template_desc}): {count} emails")
        
        print(f"\n📁 Template-specific files:")
        for template_num, file_path in template_files.items():
            template_desc = template_engine.get_template_description(template_num)
            print(f"  • Template {template_num}: {file_path}")
        
        print(f"\n✅ Ready for outreach! Load template files into your email system.")
        return
    
    print("Campaign Options:")
    print("1. Generate from high-priority sponsors")
    print("2. Generate from all campaign sponsors")
    print("3. Custom file campaign generation")
    print("=" * 80)
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == '1':
        input_file = 'data/input/high_priority_sponsors.csv'
        campaign_file, template_files, counts = template_engine.generate_campaign(input_file, max_emails=100)
        
    elif choice == '2':
        input_file = 'data/input/sponsors_enhanced_for_campaign.csv'
        campaign_file, template_files, counts = template_engine.generate_campaign(input_file, max_emails=200)
        
    elif choice == '3':
        input_file = input("Enter input CSV file path: ").strip()
        max_emails = int(input("Enter max emails to generate: "))
        campaign_file, template_files, counts = template_engine.generate_campaign(input_file, max_emails=max_emails)
        
    else:
        print("Invalid choice")
        return
    
    print(f"\n🎭 5-Template Campaign Generated!")
    print(f"📧 Main campaign file: {campaign_file}")
    print(f"\n📊 Template Distribution:")
    for template_num, count in counts.items():
        if count > 0:
            template_desc = template_engine.get_template_description(template_num)
            print(f"  • Template {template_num} ({template_desc}): {count} emails")
    
    print(f"\n📁 Template-specific files:")
    for template_num, file_path in template_files.items():
        template_desc = template_engine.get_template_description(template_num)
        print(f"  • Template {template_num}: {file_path}")
    
    print(f"\n✅ Ready for outreach! Load template files into your email system.")

if __name__ == "__main__":
    main()