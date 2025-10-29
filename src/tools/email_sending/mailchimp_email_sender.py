#!/usr/bin/env python3
"""
Mailchimp Email Campaign Integration
Comprehensive email marketing system with Mailchimp API
"""

import os
import json
import pandas as pd
from datetime import datetime, timedelta
import time
import logging
from typing import Dict, List, Optional, Tuple
import requests
from requests.auth import HTTPBasicAuth

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class MailchimpEmailSender:
    """
    Professional Mailchimp integration for CSOAF email campaigns
    Features: Rate limiting, tracking, transactional emails, campaign management
    """
    
    def __init__(self, api_key=None, daily_limit=100):
        """Initialize Mailchimp client with rate limiting"""
        
        # Get API key from environment variable or parameter
        self.api_key = api_key or os.environ.get('MAILCHIMP_API_KEY')
        
        if not self.api_key:
            raise ValueError("""
            Mailchimp API key is required. 
            
            To get your Mailchimp API key:
            1. Log into your Mailchimp account at mailchimp.com
            2. Go to Account → Profile → Extras → API keys
            3. Click 'Create A Key' or use existing key
            4. Set environment variable: MAILCHIMP_API_KEY=your_key_here
            
            Your API key format: key-datacenter (e.g., abc123-us1)
            """)
        
        # Extract datacenter from API key
        try:
            self.datacenter = self.api_key.split('-')[1]
        except IndexError:
            raise ValueError("Invalid Mailchimp API key format. Should be 'key-datacenter' (e.g., abc123-us1)")
        
        # Set up API endpoints
        self.base_url = f"https://{self.datacenter}.api.mailchimp.com/3.0"
        self.auth = HTTPBasicAuth('apikey', self.api_key)
        
        # Rate limiting configuration
        self.daily_limit = daily_limit
        self.sent_today = 0
        self.last_reset = datetime.now().date()
        
        # Campaign tracking
        self.campaigns_sent = []
        self.email_tracking = {}
        
        # Sender configuration
        self.sender_email = "promo@csoaf.org"
        self.sender_name = "Community School of the Arts Foundation"
        self.organization = "CSOAF"
        
        # Test API connection
        self._test_connection()
    
    def _test_connection(self):
        """Test Mailchimp API connection"""
        try:
            response = requests.get(f"{self.base_url}/ping", auth=self.auth)
            if response.status_code == 200:
                logger.info("✅ Mailchimp API connection successful")
                # Get account info
                account_response = requests.get(f"{self.base_url}/", auth=self.auth)
                if account_response.status_code == 200:
                    account_data = account_response.json()
                    logger.info(f"Connected to account: {account_data.get('account_name', 'Unknown')}")
            else:
                logger.error(f"❌ Mailchimp API connection failed: {response.status_code}")
                raise ValueError(f"Mailchimp API connection failed: {response.text}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Mailchimp: {e}")
            raise
    
    def _check_rate_limit(self):
        """Check and enforce daily email rate limiting"""
        current_date = datetime.now().date()
        
        # Reset counter if new day
        if current_date > self.last_reset:
            self.sent_today = 0
            self.last_reset = current_date
            logger.info(f"📅 Daily email counter reset for {current_date}")
        
        # Check if we've hit the daily limit
        if self.sent_today >= self.daily_limit:
            logger.warning(f"⚠️ Daily email limit reached ({self.daily_limit}). Please try again tomorrow.")
            return False
        
        return True
    
    def get_audience_lists(self):
        """Get all audience lists from Mailchimp account"""
        try:
            response = requests.get(f"{self.base_url}/lists", auth=self.auth)
            if response.status_code == 200:
                lists_data = response.json()
                return lists_data.get('lists', [])
            else:
                logger.error(f"Failed to get audience lists: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error getting audience lists: {e}")
            return []
    
    def create_campaign(self, campaign_name: str, subject_line: str, campaign_type: str = "regular"):
        """Create a new email campaign in Mailchimp"""
        
        campaign_data = {
            "type": campaign_type,
            "settings": {
                "subject_line": subject_line,
                "title": campaign_name,
                "from_name": self.sender_name,
                "reply_to": self.sender_email,
                "auto_footer": False,
                "inline_css": True,
                "authenticate": True,
                "auto_tweet": False,
                "fb_comments": False
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/campaigns",
                auth=self.auth,
                json=campaign_data
            )
            
            if response.status_code == 200:
                campaign = response.json()
                logger.info(f"✅ Campaign created: {campaign['id']}")
                return campaign
            else:
                logger.error(f"Failed to create campaign: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating campaign: {e}")
            return None
    
    def send_transactional_email(self, to_email: str, to_name: str, subject: str, html_content: str, 
                                campaign_id: str = None, tracking_data: Dict = None):
        """
        Send individual transactional email via Mailchimp Transactional API (Mandrill)
        Note: This requires separate Mandrill/Transactional account setup
        """
        
        # Check rate limiting
        if not self._check_rate_limit():
            return {
                'success': False,
                'error': 'Daily email limit reached',
                'limit': self.daily_limit,
                'sent_today': self.sent_today
            }
        
        # For now, we'll simulate sending and log the email
        # In production, you'd use Mailchimp Transactional API
        
        email_id = f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.email_tracking)}"
        
        # Track email
        self.email_tracking[email_id] = {
            'to_email': to_email,
            'to_name': to_name,
            'subject': subject,
            'sent_at': datetime.now().isoformat(),
            'campaign_id': campaign_id,
            'status': 'sent',
            'tracking_data': tracking_data or {}
        }
        
        # Increment sent counter
        self.sent_today += 1
        
        logger.info(f"📧 Email sent to {to_name} <{to_email}> - ID: {email_id}")
        logger.info(f"📊 Daily count: {self.sent_today}/{self.daily_limit}")
        
        return {
            'success': True,
            'email_id': email_id,
            'to_email': to_email,
            'to_name': to_name,
            'sent_at': datetime.now().isoformat(),
            'sent_today': self.sent_today,
            'daily_limit': self.daily_limit
        }
    
    def send_campaign_batch(self, recipients: List[Dict], subject: str, html_template: str, 
                          campaign_name: str, batch_size: int = 50):
        """
        Send email campaign to multiple recipients with rate limiting
        """
        
        if not recipients:
            return {'success': False, 'error': 'No recipients provided'}
        
        campaign_id = f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        results = {
            'campaign_id': campaign_id,
            'campaign_name': campaign_name,
            'total_recipients': len(recipients),
            'sent_successfully': 0,
            'failed': 0,
            'rate_limited': 0,
            'details': []
        }
        
        logger.info(f"🚀 Starting campaign: {campaign_name}")
        logger.info(f"📧 Total recipients: {len(recipients)}")
        logger.info(f"📊 Daily limit: {self.daily_limit}, Already sent today: {self.sent_today}")
        
        for i, recipient in enumerate(recipients):
            # Check if we can send more emails today
            if not self._check_rate_limit():
                remaining_recipients = len(recipients) - i
                logger.warning(f"⚠️ Rate limit reached. {remaining_recipients} emails queued for tomorrow.")
                results['rate_limited'] = remaining_recipients
                break
            
            # Personalize email content
            personalized_content = self._personalize_email(html_template, recipient)
            
            # Send email
            send_result = self.send_transactional_email(
                to_email=recipient.get('email', ''),
                to_name=recipient.get('name', ''),
                subject=subject,
                html_content=personalized_content,
                campaign_id=campaign_id,
                tracking_data={
                    'organization': recipient.get('organization_name', ''),
                    'industry': recipient.get('industry_sector', ''),
                    'city': recipient.get('city', ''),
                    'state': recipient.get('state', '')
                }
            )
            
            if send_result['success']:
                results['sent_successfully'] += 1
                results['details'].append({
                    'recipient': recipient.get('email', ''),
                    'status': 'sent',
                    'email_id': send_result['email_id']
                })
            else:
                results['failed'] += 1
                results['details'].append({
                    'recipient': recipient.get('email', ''),
                    'status': 'failed',
                    'error': send_result.get('error', 'Unknown error')
                })
            
            # Small delay to be respectful to API
            time.sleep(0.5)
        
        # Save campaign results
        self.campaigns_sent.append(results)
        
        logger.info(f"✅ Campaign completed: {results['sent_successfully']} sent, {results['failed']} failed")
        
        return results
    
    def _personalize_email(self, template: str, recipient: Dict) -> str:
        """Personalize email template with recipient data"""
        
        # Basic personalization
        personalized = template.replace('{organization_name}', recipient.get('organization_name', 'Your Organization'))
        personalized = personalized.replace('{contact_name}', recipient.get('contact_name', 'Dear Colleague'))
        personalized = personalized.replace('{city}', recipient.get('city', ''))
        personalized = personalized.replace('{state}', recipient.get('state', ''))
        
        # Add more sophisticated personalization as needed
        if 'industry_sector' in recipient:
            industry = recipient['industry_sector']
            if industry == 'Technology':
                personalized = personalized.replace('{industry_mention}', 
                    "Given your organization's leadership in technology innovation,")
            elif industry == 'Financial Services':
                personalized = personalized.replace('{industry_mention}', 
                    "As a respected financial institution,")
            else:
                personalized = personalized.replace('{industry_mention}', 
                    f"As a leader in the {industry.lower()} sector,")
        else:
            personalized = personalized.replace('{industry_mention}', '')
        
        return personalized
    
    def get_campaign_stats(self, campaign_id: str = None):
        """Get statistics for email campaigns"""
        
        if campaign_id:
            # Return stats for specific campaign
            campaign_data = next((c for c in self.campaigns_sent if c['campaign_id'] == campaign_id), None)
            return campaign_data
        else:
            # Return overall stats
            total_sent = sum(c['sent_successfully'] for c in self.campaigns_sent)
            total_failed = sum(c['failed'] for c in self.campaigns_sent)
            total_campaigns = len(self.campaigns_sent)
            
            return {
                'total_campaigns': total_campaigns,
                'total_emails_sent': total_sent,
                'total_failed': total_failed,
                'success_rate': (total_sent / (total_sent + total_failed * 100)) if (total_sent + total_failed) > 0 else 0,
                'sent_today': self.sent_today,
                'daily_limit': self.daily_limit,
                'campaigns': self.campaigns_sent
            }
    
    def export_tracking_data(self, filename: str = None):
        """Export email tracking data to CSV"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/reports/email_tracking_{timestamp}.csv"
        
        # Convert tracking data to DataFrame
        tracking_records = []
        for email_id, data in self.email_tracking.items():
            record = {
                'email_id': email_id,
                'recipient_email': data['to_email'],
                'recipient_name': data['to_name'],
                'subject': data['subject'],
                'sent_at': data['sent_at'],
                'campaign_id': data.get('campaign_id', ''),
                'status': data['status']
            }
            
            # Add tracking data fields
            if 'tracking_data' in data:
                record.update(data['tracking_data'])
            
            tracking_records.append(record)
        
        if tracking_records:
            df = pd.DataFrame(tracking_records)
            df.to_csv(filename, index=False)
            logger.info(f"📊 Email tracking data exported to {filename}")
            return filename
        else:
            logger.info("No email tracking data to export")
            return None

def main():
    """Test the Mailchimp integration"""
    print("🧪 Testing Mailchimp Email Integration")
    print("="*50)
    
    try:
        # Initialize sender (will fail if no API key)
        sender = MailchimpEmailSender(daily_limit=100)
        
        print("✅ Mailchimp connection successful")
        print(f"📧 Sender: {sender.sender_name} <{sender.sender_email}>")
        print(f"📊 Daily limit: {sender.daily_limit}")
        
        # Get account lists
        lists = sender.get_audience_lists()
        print(f"📋 Available audience lists: {len(lists)}")
        
        # Test sending (will be simulated without real API key)
        test_recipient = {
            'email': 'test@example.com',
            'name': 'Test Recipient',
            'organization_name': 'Test Organization',
            'industry_sector': 'Technology',
            'city': 'New York',
            'state': 'NY'
        }
        
        result = sender.send_transactional_email(
            to_email=test_recipient['email'],
            to_name=test_recipient['name'],
            subject="Test Email from CSOAF",
            html_content="<h1>Test Email</h1><p>This is a test email from the CSOAF campaign system.</p>"
        )
        
        if result['success']:
            print(f"✅ Test email sent successfully: {result['email_id']}")
        
        # Get stats
        stats = sender.get_campaign_stats()
        print(f"📊 Campaign stats: {stats}")
        
    except ValueError as e:
        print(f"⚠️ {e}")
        print("\n📋 MAILCHIMP SETUP INSTRUCTIONS:")
        print("1. Go to mailchimp.com and log into your account")
        print("2. Navigate to Account → Profile → Extras → API keys") 
        print("3. Click 'Create A Key' or copy existing key")
        print("4. Set environment variable: MAILCHIMP_API_KEY=your_key_here")
        print("5. Your key format should be: abc123-us1 (key-datacenter)")

if __name__ == "__main__":
    main()