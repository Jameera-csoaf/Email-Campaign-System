#!/usr/bin/env python3
"""
Thank You Email Generator for Healing Through Arts Event Attendees
Personalized emails for 7 creative professionals who attended the previous event
"""

import pandas as pd
import logging
from datetime import datetime
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class ThankYouEmailGenerator:
    def __init__(self):
        self.sender_email = "jameera@csoaf.org"
        self.sender_name = "Jameera Mahima Gujjarlapudi"
        self.organization = "Community School of Arts Foundation"
        self.website = "csoaf.org"
        
        # Event details
        self.previous_event_name = "Healing Through Arts: NYC Schools"
        self.previous_event_date = "Monday, October 13, 2025"
        self.previous_venue = "Rake Wine Bar (45 1st Ave, NYC)"
        
        # Thank you email template
        self.email_template = """Subject: Thank you for supporting Healing Through Arts: NYC Schools! 🎭

Dear {name},

Thank you so much for supporting Healing Through Arts: NYC Schools on {event_date}! It was wonderful to have you join us at {venue} for an evening celebrating the power of arts in education.

As a talented {occupation_summary}, your presence added so much to the vibrant community of artists, educators, and changemakers who came together that evening. The energy you brought to our wine tasting, performances, and conversations truly made the event special.

Thanks to supporters like you, we raised important funds for arts healing programs in underserved NYC schools. Your participation helps us continue empowering students through creative expression and healing arts education.

🎨 **Stay Connected for What's Next**
We're planning our upcoming Healing Through Arts: NYC Schools event! We'd love to keep you in the loop about:
- Upcoming arts healing events and performances
- Opportunities to get involved with NYC school programs  
- Ways to support creative education in underserved communities
- Networking with fellow artists and changemakers

Follow us and stay updated:
🌐 Website: {website}
📧 Email: {sender_email}

We hope to see you at our next gathering! Thank you again for being part of this meaningful community working to heal and inspire through the arts.

With deep gratitude,

{sender_name}
{organization}
🌐 {website}
📞 917 216-5176

P.S. If you have any photos or reflections from the event you'd like to share, we'd love to feature them in our community updates!"""

    def format_occupation(self, occupation_text):
        """Format occupation text to be more readable"""
        if not occupation_text:
            return "creative professional"
        
        # Clean up the occupation text
        occupations = [occ.strip() for occ in occupation_text.split(';')]
        
        if len(occupations) == 1:
            return occupations[0].lower()
        elif len(occupations) == 2:
            return f"{occupations[0].lower()} and {occupations[1].lower()}"
        else:
            # For multiple occupations, group them nicely
            return f"{', '.join(occupations[:-1]).lower()}, and {occupations[-1].lower()}"

    def generate_thank_you_email(self, contact_data):
        """Generate personalized thank you email for a contact"""
        
        name = contact_data.get('name', 'Friend')
        occupation = contact_data.get('occupation', '')
        occupation_summary = self.format_occupation(occupation)
        
        # Generate email content
        email_content = self.email_template.format(
            name=name,
            event_date=self.previous_event_date,
            venue=self.previous_venue,
            occupation_summary=occupation_summary,
            website=self.website,
            sender_email=self.sender_email,
            sender_name=self.sender_name,
            organization=self.organization
        )
        
        return {
            'name': name,
            'email': contact_data.get('email', ''),
            'phone': contact_data.get('phone', ''),
            'occupation': occupation,
            'occupation_summary': occupation_summary,
            'email_subject': f"Thank you for supporting Healing Through Arts: NYC Schools! 🎭",
            'email_content': email_content,
            'sender_email': self.sender_email,
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def generate_all_thank_you_emails(self, contacts_data, output_dir='data/results'):
        """Generate thank you emails for all contacts"""
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"Generating thank you emails for {len(contacts_data)} contacts...")
        
        thank_you_emails = []
        
        for i, contact in enumerate(contacts_data, 1):
            logger.info(f"Generating email {i}: {contact['name']}")
            email_data = self.generate_thank_you_email(contact)
            thank_you_emails.append(email_data)
        
        # Save to CSV
        df = pd.DataFrame(thank_you_emails)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(output_dir, f'healing_arts_thank_you_emails_{timestamp}.csv')
        
        df.to_csv(output_file, index=False)
        logger.info(f"Thank you emails saved: {output_file}")
        
        # Generate summary
        self.create_thank_you_summary(df, output_dir, timestamp)
        
        return output_file, thank_you_emails

    def create_thank_you_summary(self, df, output_dir, timestamp):
        """Create summary report for thank you emails"""
        
        summary_file = os.path.join(output_dir, f'thank_you_emails_summary_{timestamp}.md')
        
        with open(summary_file, 'w') as f:
            f.write("# Healing Through Arts: Thank You Emails Summary\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall stats
            total_contacts = len(df)
            with_emails = len(df[df['email'].notna() & (df['email'] != '')])
            
            f.write(f"## Campaign Statistics\n")
            f.write(f"- **Total Contacts**: {total_contacts}\n")
            f.write(f"- **With Email Addresses**: {with_emails} ({with_emails/total_contacts*100:.1f}%)\n")
            f.write(f"- **Ready to Send**: {with_emails} emails\n\n")
            
            # Contact details
            f.write("## Contact List\n")
            for _, row in df.iterrows():
                f.write(f"### {row['name']}\n")
                f.write(f"- **Email**: {row['email'] if row['email'] else 'No email provided'}\n")
                f.write(f"- **Phone**: {row['phone']}\n")
                f.write(f"- **Occupation**: {row['occupation']}\n")
                f.write(f"- **Email Status**: {'Ready to Send' if row['email'] else 'Phone Contact Only'}\n\n")
            
            # Event details
            f.write("## Event Details\n")
            f.write(f"- **Previous Event**: {self.previous_event_name}\n")
            f.write(f"- **Date**: {self.previous_event_date}\n")
            f.write(f"- **Venue**: {self.previous_venue}\n")
            f.write(f"- **Upcoming Event**: Same event, venue TBD\n\n")
            
            f.write("## Next Steps\n")
            f.write("1. **Review generated emails** in the CSV file\n")
            f.write("2. **Send emails** to contacts with email addresses\n")
            f.write("3. **Follow up by phone** with contacts without emails\n")
            f.write("4. **Track responses** and engagement\n")
            f.write("5. **Update contact database** with any new information\n")

        logger.info(f"Thank you emails summary saved: {summary_file}")

def main():
    print("=" * 80)
    print("HEALING THROUGH ARTS: THANK YOU EMAIL GENERATOR")
    print("=" * 80)
    
    # Define the 7 contacts
    contacts = [
        {
            'name': 'Isabel Valencia Zuniga',
            'phone': '3474631193',
            'occupation': 'Event Organizer; Artist',
            'email': ''
        },
        {
            'name': 'Jonathan Frnch Folly',
            'phone': '9178086263',
            'occupation': 'Artist; Teacher',
            'email': 'frnch@familiapacti.com'
        },
        {
            'name': 'Elizabeth Yurovskaya(z)',
            'phone': '2158802732',
            'occupation': 'Curator; Painter; Production; Designer',
            'email': 'zilfutura@gmail.com'
        },
        {
            'name': 'Gabriela Garcia Belisario',
            'phone': '8137688645',
            'occupation': 'Filmmaker; Photographer; Video editor; Light tech',
            'email': 'gabrielagbelisario@gmail.com'
        },
        {
            'name': 'Belein Orsini',
            'phone': '6193139588',
            'occupation': 'Filmmaker; Theater; Visual arts',
            'email': 'orsini7@gmail.com'
        },
        {
            'name': 'Alexandra Alvarez',
            'phone': '5516975753',
            'occupation': '',  # Not specified
            'email': 'alexillustra@gmail.com'
        },
        {
            'name': 'Tory Grossman',
            'phone': '9148066556',
            'occupation': '',  # Not specified
            'email': 'tory@betternow.nyc'
        }
    ]
    
    generator = ThankYouEmailGenerator()
    output_file, emails = generator.generate_all_thank_you_emails(contacts)
    
    print(f"\n🎭 Thank You Emails Generated!")
    print(f"📧 Output file: {output_file}")
    print(f"📊 Total contacts: {len(emails)}")
    
    # Show contacts with/without emails
    with_email = [e for e in emails if e['email']]
    without_email = [e for e in emails if not e['email']]
    
    print(f"✅ Ready to send: {len(with_email)} emails")
    print(f"📞 Phone follow-up needed: {len(without_email)} contacts")
    
    if without_email:
        print(f"\nContacts needing phone follow-up:")
        for contact in without_email:
            print(f"  • {contact['name']} - {contact['phone']}")
    
    print(f"\n🚀 Ready for deployment!")

if __name__ == "__main__":
    main()