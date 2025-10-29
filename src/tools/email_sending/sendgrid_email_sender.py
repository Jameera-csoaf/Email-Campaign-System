#!/usr/bin/env python3
"""
SendGrid Email Sender for Thank You Campaign
Automatically sends personalized thank you emails via SendGrid API
"""

import pandas as pd
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Content
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class SendGridEmailSender:
    def __init__(self, api_key=None):
        """Initialize SendGrid client"""
        # Get API key from environment variable or parameter
        self.api_key = api_key or os.environ.get('SENDGRID_API_KEY')
        
        if not self.api_key:
            raise ValueError("SendGrid API key is required. Set SENDGRID_API_KEY environment variable or pass api_key parameter.")
        
        self.sg = SendGridAPIClient(api_key=self.api_key)
        self.sender_email = "jameera@csoaf.org"
        self.sender_name = "Jameera Mahima Gujjarlapudi"
        
    def send_team_email(self, team_email_list):
        """Send team appreciation email from Anthony Villacis"""
        
        team_subject = "Thank You Team - Healing Through Arts Success! 🎭"
        team_content = """Dear Team,

October 13th was truly unforgettable. The Healing Through Arts: NYC Schools Benefit was more than a charity event, it was a powerful celebration of creativity, resilience, and community.

Thanks to each of you — our teachers, artists, volunteers, and coordinators — the evening came alive with meaning and inspiration. From the live performances to the heartfelt conversations, every detail reflected our shared mission to bring healing and hope through the arts to New York City public schools.

Your dedication and teamwork made this event possible, and the impact will continue far beyond that night, in every classroom and every student we serve.

Let's carry this energy forward as we continue building programs that uplift, connect, and transform lives through the arts.

With deep gratitude and pride,

Anthony Villacis
Executive Director
Community School of the Arts Foundation (CSOAF)
📧 info@csoaf.org | 🌐 csoaf.org | 📞 917-216-5176"""

        sender_email = "info@csoaf.org"
        sender_name = "Anthony Villacis"
        
        sent_emails = []
        failed_emails = []
        
        for email_address in team_email_list:
            try:
                message = Mail(
                    from_email=From(sender_email, sender_name),
                    to_emails=To(email_address),
                    subject=team_subject,
                    html_content=Content("text/html", self.format_html_email(team_content))
                )
                
                logger.info(f"Sending team email to {email_address}...")
                response = self.sg.send(message)
                
                if response.status_code in [200, 201, 202]:
                    logger.info(f"✅ Team email sent successfully to {email_address}")
                    sent_emails.append({
                        'email': email_address,
                        'status': 'sent',
                        'status_code': response.status_code,
                        'sent_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                else:
                    logger.error(f"❌ Failed to send team email to {email_address}: Status {response.status_code}")
                    failed_emails.append({
                        'email': email_address,
                        'status': 'failed',
                        'status_code': response.status_code,
                        'error': f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                logger.error(f"❌ Error sending team email to {email_address}: {str(e)}")
                failed_emails.append({
                    'email': email_address,
                    'status': 'error',
                    'error': str(e)
                })
        
        return sent_emails, failed_emails

    def send_thank_you_emails(self, csv_file='data/results/healing_arts_thank_you_emails_20251022_115129.csv'):
        """Send all thank you emails via SendGrid"""
        
        logger.info(f"Loading emails from: {csv_file}")
        df = pd.read_csv(csv_file)
        
        # Filter contacts with email addresses
        email_contacts = df[df['email'].str.contains('@', na=False)]
        
        logger.info(f"Found {len(email_contacts)} emails to send via SendGrid")
        
        sent_emails = []
        failed_emails = []
        
        for i, row in email_contacts.iterrows():
            try:
                # Clean up email content (remove duplicate subject line if present)
                email_content = row['email_content']
                if email_content.startswith('Subject:'):
                    email_content = email_content.split('\n', 2)[2]  # Skip subject line
                
                # Create email
                message = Mail(
                    from_email=From(self.sender_email, self.sender_name),
                    to_emails=To(row['email'], row['name']),
                    subject=row['email_subject'],
                    html_content=Content("text/html", self.format_html_email(email_content))
                )
                
                # Send email
                logger.info(f"Sending email to {row['name']} ({row['email']})...")
                response = self.sg.send(message)
                
                if response.status_code in [200, 201, 202]:
                    logger.info(f"✅ Email sent successfully to {row['name']}")
                    sent_emails.append({
                        'name': row['name'],
                        'email': row['email'],
                        'status': 'sent',
                        'status_code': response.status_code,
                        'sent_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                else:
                    logger.error(f"❌ Failed to send email to {row['name']}: Status {response.status_code}")
                    failed_emails.append({
                        'name': row['name'],
                        'email': row['email'],
                        'status': 'failed',
                        'status_code': response.status_code,
                        'error': f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                logger.error(f"❌ Error sending email to {row['name']}: {str(e)}")
                failed_emails.append({
                    'name': row['name'],
                    'email': row['email'],
                    'status': 'error',
                    'error': str(e)
                })
        
        # Save results
        self.save_send_results(sent_emails, failed_emails)
        
        return sent_emails, failed_emails
    
    def format_html_email(self, text_content):
        """Convert plain text email to HTML format"""
        
        # Replace line breaks with HTML
        html_content = text_content.replace('\n', '<br>')
        
        # Format emojis and special characters
        html_content = html_content.replace('🎨', '🎨')
        html_content = html_content.replace('🌐', '🌐')
        html_content = html_content.replace('📧', '📧')
        html_content = html_content.replace('📞', '📞')
        
        # Format bold sections
        html_content = html_content.replace('**Stay Connected for What\'s Next**', '<strong>Stay Connected for What\'s Next</strong>')
        
        # Create full HTML email
        html_email = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                {html_content}
            </div>
        </body>
        </html>
        """
        
        return html_email
    
    def save_send_results(self, sent_emails, failed_emails):
        """Save email sending results to CSV files"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save sent emails
        if sent_emails:
            sent_df = pd.DataFrame(sent_emails)
            sent_file = f'data/results/sendgrid_sent_emails_{timestamp}.csv'
            sent_df.to_csv(sent_file, index=False)
            logger.info(f"Sent emails log saved: {sent_file}")
        
        # Save failed emails
        if failed_emails:
            failed_df = pd.DataFrame(failed_emails)
            failed_file = f'data/results/sendgrid_failed_emails_{timestamp}.csv'
            failed_df.to_csv(failed_file, index=False)
            logger.info(f"Failed emails log saved: {failed_file}")
        
        # Create summary report
        self.create_send_summary(sent_emails, failed_emails, timestamp)
    
    def create_send_summary(self, sent_emails, failed_emails, timestamp):
        """Create summary report of email sending results"""
        
        summary_file = f'data/results/sendgrid_summary_{timestamp}.md'
        
        with open(summary_file, 'w') as f:
            f.write("# SendGrid Thank You Email Campaign Results\n\n")
            f.write(f"Sent: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall stats
            total_attempted = len(sent_emails) + len(failed_emails)
            success_rate = (len(sent_emails) / total_attempted * 100) if total_attempted > 0 else 0
            
            f.write(f"## Campaign Statistics\n")
            f.write(f"- **Total Emails Attempted**: {total_attempted}\n")
            f.write(f"- **Successfully Sent**: {len(sent_emails)}\n")
            f.write(f"- **Failed**: {len(failed_emails)}\n")
            f.write(f"- **Success Rate**: {success_rate:.1f}%\n\n")
            
            # Sent emails
            if sent_emails:
                f.write("## Successfully Sent Emails\n")
                for email in sent_emails:
                    f.write(f"- ✅ **{email['name']}** ({email['email']}) - {email['sent_time']}\n")
                f.write("\n")
            
            # Failed emails
            if failed_emails:
                f.write("## Failed Emails\n")
                for email in failed_emails:
                    f.write(f"- ❌ **{email['name']}** ({email['email']}) - {email.get('error', 'Unknown error')}\n")
                f.write("\n")
            
            f.write("## Next Steps\n")
            if failed_emails:
                f.write("1. **Review failed emails** and retry if needed\n")
                f.write("2. **Check email addresses** for any typos\n")
                f.write("3. **Verify SendGrid account** status and limits\n")
            else:
                f.write("1. **Monitor email delivery** in SendGrid dashboard\n")
                f.write("2. **Track opens and clicks** in SendGrid analytics\n")
                f.write("3. **Follow up** on any responses received\n")
            
            f.write(f"4. **Send SMS to Isabel** Valencia Zuniga at 347-463-1193\n")
        
        logger.info(f"SendGrid summary saved: {summary_file}")

def main():
    print("=" * 80)
    print("SENDGRID EMAIL SENDER - HEALING THROUGH ARTS")
    print("=" * 80)
    
    print("Email Campaign Options:")
    print("1. Send Thank You Emails (6 attendee emails)")
    print("2. Send Team Appreciation Email (from Anthony Villacis)")
    print("3. Send Both Campaigns")
    print("=" * 80)
    
    # Check for API key
    api_key = os.environ.get('SENDGRID_API_KEY')
    if not api_key:
        print("❌ SendGrid API key not found!")
        print("Please set your SendGrid API key:")
        print("1. Get API key from SendGrid dashboard")
        print("2. Set environment variable: set SENDGRID_API_KEY=your_api_key")
        print("3. Or provide it when prompted")
        print()
        
        api_key = input("Enter your SendGrid API key (or press Enter to set as environment variable): ").strip()
        
        if not api_key:
            print("Please set the SENDGRID_API_KEY environment variable and run again.")
            return
    
    try:
        # Initialize sender
        sender = SendGridEmailSender(api_key)
        
        print(f"✅ SendGrid client initialized")
        print(f"📧 Sender: {sender.sender_email}")
        print()
        
        # Get user choice
        choice = input("Select option (1-3): ").strip()
        
        if choice == '1':
            # Send thank you emails
            sent, failed = sender.send_thank_you_emails()
            print(f"\n🎭 THANK YOU EMAIL CAMPAIGN COMPLETE!")
            
        elif choice == '2':
            # Send team appreciation email
            team_emails = input("Enter team email addresses (comma-separated): ").strip().split(',')
            team_emails = [email.strip() for email in team_emails if email.strip()]
            
            if team_emails:
                sent, failed = sender.send_team_email(team_emails)
                print(f"\n👥 TEAM APPRECIATION EMAIL COMPLETE!")
            else:
                print("No email addresses provided.")
                return
                
        elif choice == '3':
            # Send both campaigns
            sent1, failed1 = sender.send_thank_you_emails()
            
            team_emails = input("Enter team email addresses (comma-separated): ").strip().split(',')
            team_emails = [email.strip() for email in team_emails if email.strip()]
            
            if team_emails:
                sent2, failed2 = sender.send_team_email(team_emails)
                sent = sent1 + sent2
                failed = failed1 + failed2
                print(f"\n🎭 ALL EMAIL CAMPAIGNS COMPLETE!")
            else:
                sent, failed = sent1, failed1
                print(f"\n🎭 THANK YOU EMAIL CAMPAIGN COMPLETE!")
        else:
            print("Invalid option selected.")
            return
        
        print(f"✅ Successfully sent: {len(sent)} emails")
        print(f"❌ Failed: {len(failed)} emails")
        
        if sent:
            print(f"\n📧 Successfully sent to:")
            for email in sent:
                print(f"  • {email['name']} ({email['email']})")
        
        if failed:
            print(f"\n❌ Failed to send to:")
            for email in failed:
                print(f"  • {email['name']} ({email['email']}) - {email.get('error', 'Unknown error')}")
        
        print(f"\n📱 Don't forget to send SMS to Isabel Valencia Zuniga: 347-463-1193")
        print(f"🚀 Campaign deployment complete!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please check your SendGrid API key and try again.")

if __name__ == "__main__":
    main()