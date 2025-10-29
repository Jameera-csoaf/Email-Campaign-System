#!/usr/bin/env python3
"""
Comprehensive Email Campaign Management System
Complete solution for creating, managing, and tracking email campaigns
"""

import os
import json
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple
import uuid

# Import our custom modules
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

# Now import our modules
UnifiedEmailSender = None
auto_detect_provider = None
CSPAFEmailTemplates = None

try:
    from tools.email_sending.unified_email_sender import UnifiedEmailSender, auto_detect_provider
    print("✅ Unified email sender imported successfully")
except ImportError as e:
    print(f"⚠️ Could not import unified email sender: {e}")

try:
    from campaigns.email_templates.enhanced_email_templates import CSPAFEmailTemplates
    print("✅ Enhanced email templates imported successfully")
except ImportError as e:
    print(f"⚠️ Could not import enhanced email templates: {e}")

# Try importing the Mailchimp sender directly if needed
try:
    from tools.email_sending.mailchimp_email_sender import MailchimpEmailSender
    print("✅ Mailchimp email sender imported successfully")
except ImportError as e:
    print(f"⚠️ Could not import Mailchimp email sender: {e}")
    MailchimpEmailSender = None

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailCampaignManager:
    """
    Complete email campaign management system for CSOAF
    Features: Campaign creation, template management, scheduling, tracking, analytics
    """
    
    def __init__(self, email_provider: str = 'mailchimp', data_directory: str = None):
        """
        Initialize Email Campaign Manager
        
        Args:
            email_provider: Email provider to use ('mailchimp', 'sendgrid')
            data_directory: Directory for storing campaign data
        """
        
        # Set up directories
        self.data_directory = data_directory or os.path.join(os.getcwd(), 'data')
        self.campaigns_dir = os.path.join(self.data_directory, 'campaigns')
        self.reports_dir = os.path.join(self.data_directory, 'reports')
        self.corporations_dir = os.path.join(self.data_directory, 'corporations')
        
        # Create directories if they don't exist
        for directory in [self.campaigns_dir, self.reports_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Initialize email sender
        try:
            if UnifiedEmailSender is None:
                # Fallback to Mailchimp directly if unified sender not available
                if MailchimpEmailSender:
                    self.email_sender = MailchimpEmailSender(daily_limit=100)
                    logger.info("✅ Email sender initialized: Mailchimp (direct)")
                else:
                    raise ImportError("No email sender available")
            elif email_provider == 'auto':
                self.email_sender = auto_detect_provider()
            else:
                self.email_sender = UnifiedEmailSender(provider=email_provider)
            logger.info(f"✅ Email sender initialized: {email_provider}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize email sender: {e}")
            self.email_sender = None
        
        # Initialize template system
        if CSPAFEmailTemplates:
            self.templates = CSPAFEmailTemplates()
        else:
            logger.error("❌ Template system not available")
            self.templates = None
        
        # Campaign tracking
        self.active_campaigns = {}
        self.campaign_history = []
        
        # Load existing campaign data
        self._load_campaign_data()
        
        logger.info("🚀 Email Campaign Manager initialized successfully")
    
    def _load_campaign_data(self):
        """Load existing campaign data from files"""
        
        campaigns_file = os.path.join(self.campaigns_dir, 'campaigns_data.json')
        if os.path.exists(campaigns_file):
            try:
                with open(campaigns_file, 'r') as f:
                    data = json.load(f)
                    self.active_campaigns = data.get('active_campaigns', {})
                    self.campaign_history = data.get('campaign_history', [])
                logger.info(f"📂 Loaded {len(self.active_campaigns)} active campaigns and {len(self.campaign_history)} historical campaigns")
            except Exception as e:
                logger.warning(f"⚠️ Could not load campaign data: {e}")
    
    def _save_campaign_data(self):
        """Save campaign data to files"""
        
        campaigns_file = os.path.join(self.campaigns_dir, 'campaigns_data.json')
        try:
            data = {
                'active_campaigns': self.active_campaigns,
                'campaign_history': self.campaign_history,
                'last_updated': datetime.now().isoformat()
            }
            with open(campaigns_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info("💾 Campaign data saved successfully")
        except Exception as e:
            logger.error(f"❌ Failed to save campaign data: {e}")
    
    def load_corporation_database(self, filename: str = None) -> pd.DataFrame:
        """Load corporation database for targeting"""
        
        if filename:
            file_path = os.path.join(self.corporations_dir, filename)
        else:
            # Look for the most recent comprehensive database
            files = [f for f in os.listdir(self.corporations_dir) if f.startswith('comprehensive_fortune1000')]
            if files:
                files.sort(reverse=True)  # Get most recent
                file_path = os.path.join(self.corporations_dir, files[0])
                logger.info(f"📊 Auto-selected database: {files[0]}")
            else:
                logger.error("❌ No corporation database found")
                return pd.DataFrame()
        
        try:
            df = pd.read_csv(file_path)
            logger.info(f"📈 Loaded {len(df)} corporations from database")
            return df
        except Exception as e:
            logger.error(f"❌ Failed to load corporation database: {e}")
            return pd.DataFrame()
    
    def create_campaign(self, campaign_name: str, campaign_type: str, 
                       template_type: str, template_name: str,
                       target_criteria: Dict = None, 
                       schedule_date: str = None,
                       custom_data: Dict = None) -> str:
        """
        Create a new email campaign
        
        Args:
            campaign_name: Name of the campaign
            campaign_type: Type ('sponsorship', 'event', 'partnership', 'follow_up')
            template_type: Template category
            template_name: Specific template
            target_criteria: Criteria for selecting recipients
            schedule_date: When to send (ISO format) or 'immediate'
            custom_data: Additional campaign data
            
        Returns:
            Campaign ID
        """
        
        campaign_id = str(uuid.uuid4())[:8]
        
        campaign_data = {
            'campaign_id': campaign_id,
            'campaign_name': campaign_name,
            'campaign_type': campaign_type,
            'template_type': template_type,
            'template_name': template_name,
            'target_criteria': target_criteria or {},
            'schedule_date': schedule_date,
            'custom_data': custom_data or {},
            'created_at': datetime.now().isoformat(),
            'status': 'draft',
            'recipients': [],
            'sent_count': 0,
            'failed_count': 0,
            'open_rate': 0,
            'click_rate': 0
        }
        
        self.active_campaigns[campaign_id] = campaign_data
        self._save_campaign_data()
        
        logger.info(f"📝 Campaign created: {campaign_name} (ID: {campaign_id})")
        return campaign_id
    
    def add_recipients_to_campaign(self, campaign_id: str, 
                                 target_criteria: Dict = None,
                                 custom_recipients: List[Dict] = None) -> int:
        """
        Add recipients to a campaign based on criteria or custom list
        
        Args:
            campaign_id: Campaign to add recipients to
            target_criteria: Criteria for selecting from database
            custom_recipients: Manual list of recipients
            
        Returns:
            Number of recipients added
        """
        
        if campaign_id not in self.active_campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        recipients = []
        
        if custom_recipients:
            recipients = custom_recipients
            logger.info(f"📋 Using {len(custom_recipients)} custom recipients")
        
        elif target_criteria:
            # Load and filter corporation database
            df = self.load_corporation_database()
            if df.empty:
                logger.error("❌ No corporation database available")
                return 0
            
            # Apply filtering criteria
            filtered_df = self._filter_database(df, target_criteria)
            
            # Convert to recipient format
            recipients = []
            for _, row in filtered_df.iterrows():
                recipient = {
                    'email': row.get('email', ''),
                    'name': row.get('contact_name', ''),
                    'organization_name': row.get('organization_name', ''),
                    'city': row.get('city', ''),
                    'state': row.get('state', ''),
                    'industry_sector': row.get('industry_sector', ''),
                    'website': row.get('website', ''),
                    'sponsorship_capacity': row.get('estimated_typical_sponsorship', ''),
                    'arts_program_interest': row.get('arts_education_potential', '')
                }
                recipients.append(recipient)
            
            logger.info(f"🎯 Filtered to {len(recipients)} recipients based on criteria")
        
        # Update campaign with recipients
        self.active_campaigns[campaign_id]['recipients'] = recipients
        self.active_campaigns[campaign_id]['target_count'] = len(recipients)
        self._save_campaign_data()
        
        return len(recipients)
    
    def _filter_database(self, df: pd.DataFrame, criteria: Dict) -> pd.DataFrame:
        """Filter corporation database based on criteria"""
        
        filtered_df = df.copy()
        
        # State filtering
        if 'states' in criteria and criteria['states']:
            filtered_df = filtered_df[filtered_df['state'].isin(criteria['states'])]
            logger.info(f"🗺️ Filtered by states: {criteria['states']}")
        
        # Industry filtering
        if 'industries' in criteria and criteria['industries']:
            filtered_df = filtered_df[filtered_df['industry_sector'].isin(criteria['industries'])]
            logger.info(f"🏭 Filtered by industries: {criteria['industries']}")
        
        # Sponsorship capacity filtering
        if 'min_sponsorship' in criteria:
            # Use the correct field name from our database
            if 'estimated_typical_sponsorship' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['estimated_typical_sponsorship'] >= criteria['min_sponsorship']]
            else:
                logger.warning("⚠️ Sponsorship capacity field not found, skipping filter")
            logger.info(f"💰 Filtered by minimum sponsorship: ${criteria['min_sponsorship']:,}")
        
        # Arts interest filtering  
        if 'arts_interest' in criteria and criteria['arts_interest']:
            # Use the correct field name from our database
            if 'arts_education_potential' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['arts_education_potential'].isin(criteria['arts_interest'])]
            else:
                logger.warning("⚠️ Arts interest field not found, skipping filter")
            logger.info(f"🎨 Filtered by arts interest: {criteria['arts_interest']}")
        
        # Limit results if specified
        if 'max_recipients' in criteria and criteria['max_recipients']:
            filtered_df = filtered_df.head(criteria['max_recipients'])
            logger.info(f"📊 Limited to {criteria['max_recipients']} recipients")
        
        return filtered_df
    
    def preview_campaign(self, campaign_id: str, recipient_index: int = 0) -> Dict:
        """
        Preview how the campaign email will look for a specific recipient
        
        Args:
            campaign_id: Campaign to preview
            recipient_index: Index of recipient to use for preview (default: 0)
            
        Returns:
            Dict with preview data including subject and html content
        """
        
        if campaign_id not in self.active_campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        campaign = self.active_campaigns[campaign_id]
        recipients = campaign.get('recipients', [])
        
        if not recipients:
            raise ValueError("No recipients in campaign for preview")
        
        if recipient_index >= len(recipients):
            recipient_index = 0
        
        recipient = recipients[recipient_index]
        
        # Generate personalized email
        if self.templates:
            email_content = self.templates.get_template(
                template_type=campaign['template_type'],
                template_name=campaign['template_name'],
                recipient_data=recipient,
                campaign_data=campaign.get('custom_data', {})
            )
        else:
            # Fallback if templates not available
            email_content = {
                'subject': f"Partnership Opportunity with {recipient.get('organization_name', 'Your Organization')}",
                'html': f"<h1>Hello {recipient.get('name', 'Friend')}</h1><p>Preview email content for {recipient.get('organization_name', 'your organization')}.</p>"
            }
        
        preview_data = {
            'campaign_id': campaign_id,
            'campaign_name': campaign['campaign_name'],
            'recipient_preview': recipient,
            'subject': email_content['subject'],
            'html_content': email_content['html'],
            'preview_index': recipient_index,
            'total_recipients': len(recipients)
        }
        
        return preview_data
    
    def send_campaign(self, campaign_id: str, send_immediately: bool = True,
                     test_send: bool = False, test_email: str = None) -> Dict:
        """
        Send email campaign
        
        Args:
            campaign_id: Campaign to send
            send_immediately: Send now or schedule for later
            test_send: Send only to test email
            test_email: Email address for test sending
            
        Returns:
            Campaign sending results
        """
        
        if campaign_id not in self.active_campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        if not self.email_sender:
            raise ValueError("Email sender not initialized. Please check your API keys.")
        
        campaign = self.active_campaigns[campaign_id]
        recipients = campaign.get('recipients', [])
        
        if not recipients:
            raise ValueError("No recipients in campaign")
        
        # Test send to single email
        if test_send and test_email:
            test_recipient = recipients[0].copy()
            test_recipient['email'] = test_email
            test_recipient['name'] = 'Test Recipient'
            recipients = [test_recipient]
            logger.info(f"🧪 Test sending to {test_email}")
        
        # Generate subject and template
        sample_recipient = recipients[0]
        if self.templates:
            email_content = self.templates.get_template(
                template_type=campaign['template_type'],
                template_name=campaign['template_name'],
                recipient_data=sample_recipient,
                campaign_data=campaign.get('custom_data', {})
            )
        else:
            # Fallback if templates not available
            email_content = {
                'subject': f"Partnership Opportunity: {campaign['campaign_name']}",
                'html': f"<h1>Hello {sample_recipient.get('name', 'Friend')}</h1><p>We'd like to discuss a partnership opportunity with {sample_recipient.get('organization_name', 'your organization')}.</p>"
            }
        
        # Send campaign
        send_results = self.email_sender.send_campaign(
            recipients=recipients,
            subject=email_content['subject'],
            html_template=email_content['html'],
            campaign_name=campaign['campaign_name']
        )
        
        # Update campaign status
        campaign['status'] = 'sent' if send_results.get('success', True) else 'failed'
        campaign['sent_at'] = datetime.now().isoformat()
        campaign['sent_count'] = send_results.get('sent_successfully', 0)
        campaign['failed_count'] = send_results.get('failed', 0)
        campaign['send_results'] = send_results
        
        # Save updated campaign data
        self._save_campaign_data()
        
        logger.info(f"📧 Campaign sent: {campaign['campaign_name']}")
        logger.info(f"✅ Successful: {send_results.get('sent_successfully', 0)}")
        logger.info(f"❌ Failed: {send_results.get('failed', 0)}")
        
        return send_results
    
    def get_campaign_analytics(self, campaign_id: str = None) -> Dict:
        """Get analytics for a specific campaign or all campaigns"""
        
        if campaign_id:
            if campaign_id not in self.active_campaigns:
                raise ValueError(f"Campaign {campaign_id} not found")
            
            campaign = self.active_campaigns[campaign_id]
            return {
                'campaign_id': campaign_id,
                'campaign_name': campaign['campaign_name'],
                'status': campaign['status'],
                'recipients_count': len(campaign.get('recipients', [])),
                'sent_count': campaign.get('sent_count', 0),
                'failed_count': campaign.get('failed_count', 0),
                'success_rate': (campaign.get('sent_count', 0) / max(len(campaign.get('recipients', [])), 1)) * 100,
                'created_at': campaign['created_at'],
                'sent_at': campaign.get('sent_at', 'Not sent')
            }
        else:
            # Overall analytics
            total_campaigns = len(self.active_campaigns)
            total_sent = sum(c.get('sent_count', 0) for c in self.active_campaigns.values())
            total_failed = sum(c.get('failed_count', 0) for c in self.active_campaigns.values())
            
            return {
                'total_campaigns': total_campaigns,
                'total_emails_sent': total_sent,
                'total_failed': total_failed,
                'overall_success_rate': (total_sent / max(total_sent + total_failed, 1)) * 100,
                'campaigns': [self.get_campaign_analytics(cid) for cid in self.active_campaigns.keys()]
            }
    
    def export_campaign_report(self, campaign_id: str, filename: str = None) -> str:
        """Export detailed campaign report to CSV"""
        
        if campaign_id not in self.active_campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        campaign = self.active_campaigns[campaign_id]
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"campaign_report_{campaign_id}_{timestamp}.csv"
        
        filepath = os.path.join(self.reports_dir, filename)
        
        # Prepare report data
        report_data = []
        recipients = campaign.get('recipients', [])
        send_results = campaign.get('send_results', {})
        details = send_results.get('details', [])
        
        for i, recipient in enumerate(recipients):
            # Find sending result for this recipient
            result = next((d for d in details if d.get('recipient') == recipient.get('email')), {})
            
            report_data.append({
                'campaign_id': campaign_id,
                'campaign_name': campaign['campaign_name'],
                'recipient_email': recipient.get('email', ''),
                'recipient_name': recipient.get('name', ''),
                'organization_name': recipient.get('organization_name', ''),
                'city': recipient.get('city', ''),
                'state': recipient.get('state', ''),
                'industry_sector': recipient.get('industry_sector', ''),
                'sponsorship_capacity': recipient.get('sponsorship_capacity', ''),
                'send_status': result.get('status', 'unknown'),
                'email_id': result.get('email_id', ''),
                'campaign_sent_at': campaign.get('sent_at', '')
            })
        
        # Save to CSV
        df = pd.DataFrame(report_data)
        df.to_csv(filepath, index=False)
        
        logger.info(f"📊 Campaign report exported: {filepath}")
        return filepath
    
    def list_campaigns(self) -> List[Dict]:
        """List all campaigns with basic info"""
        
        campaigns = []
        for campaign_id, campaign in self.active_campaigns.items():
            campaigns.append({
                'campaign_id': campaign_id,
                'campaign_name': campaign['campaign_name'],
                'status': campaign['status'],
                'created_at': campaign['created_at'],
                'recipients_count': len(campaign.get('recipients', [])),
                'sent_count': campaign.get('sent_count', 0)
            })
        
        return sorted(campaigns, key=lambda x: x['created_at'], reverse=True)
    
    def delete_campaign(self, campaign_id: str) -> bool:
        """Delete a campaign"""
        
        if campaign_id not in self.active_campaigns:
            return False
        
        # Move to history before deleting
        campaign = self.active_campaigns[campaign_id]
        campaign['deleted_at'] = datetime.now().isoformat()
        self.campaign_history.append(campaign)
        
        # Remove from active campaigns
        del self.active_campaigns[campaign_id]
        self._save_campaign_data()
        
        logger.info(f"🗑️ Campaign deleted: {campaign_id}")
        return True

def create_sample_campaign():
    """Create a sample campaign for demonstration"""
    
    print("🧪 Creating Sample Email Campaign")
    print("="*50)
    
    # Initialize campaign manager
    try:
        manager = EmailCampaignManager(email_provider='auto')
        if not manager.email_sender:
            print("⚠️ Email sender not initialized, continuing with demo mode")
        if not manager.templates:
            print("⚠️ Template system not initialized, using basic templates")
    except Exception as e:
        print(f"❌ Failed to initialize campaign manager: {e}")
        print("Creating campaign manager in demo mode...")
        manager = EmailCampaignManager.__new__(EmailCampaignManager)
        manager.data_directory = os.path.join(os.getcwd(), 'data')
        manager.campaigns_dir = os.path.join(manager.data_directory, 'campaigns')
        manager.reports_dir = os.path.join(manager.data_directory, 'reports')
        manager.corporations_dir = os.path.join(manager.data_directory, 'corporations')
        for directory in [manager.campaigns_dir, manager.reports_dir]:
            os.makedirs(directory, exist_ok=True)
        manager.email_sender = None
        manager.templates = None
        manager.active_campaigns = {}
        manager.campaign_history = []
    
    # Create a new campaign
    campaign_id = manager.create_campaign(
        campaign_name="CSOAF Partnership Outreach - Tech Companies",
        campaign_type="sponsorship",
        template_type="sponsorship_request",
        template_name="standard",
        custom_data={
            'event_date': 'November 15, 2024',
            'venue_name': 'Downtown Arts Center',
            'venue_address': '123 Arts Street, New York, NY'
        }
    )
    
    print(f"✅ Campaign created: {campaign_id}")
    
    # Add recipients based on criteria
    target_criteria = {
        'states': ['NY', 'CA'],
        'industries': ['Technology', 'Financial Services'],
        'min_sponsorship': 25000,
        'arts_interest': ['High', 'Medium'],
        'max_recipients': 50
    }
    
    recipient_count = manager.add_recipients_to_campaign(campaign_id, target_criteria)
    print(f"📧 Added {recipient_count} recipients")
    
    # Preview campaign
    if recipient_count > 0:
        preview = manager.preview_campaign(campaign_id)
        print(f"📋 Preview Subject: {preview['subject']}")
        print(f"👤 Preview Recipient: {preview['recipient_preview']['organization_name']}")
    
    # Show campaign analytics
    analytics = manager.get_campaign_analytics(campaign_id)
    print(f"📊 Campaign Analytics: {analytics}")
    
    # List all campaigns
    campaigns = manager.list_campaigns()
    print(f"📝 Total Campaigns: {len(campaigns)}")
    
    return manager, campaign_id

def main():
    """Main demonstration function"""
    
    print("🚀 CSOAF Email Campaign Management System")
    print("="*50)
    
    try:
        manager, campaign_id = create_sample_campaign()
        
        print(f"\n🎯 Sample campaign ready for sending!")
        print(f"Campaign ID: {campaign_id}")
        print("\n📋 Next steps:")
        print("1. Test send: manager.send_campaign(campaign_id, test_send=True, test_email='test@example.com')")
        print("2. Live send: manager.send_campaign(campaign_id)")
        print("3. Analytics: manager.get_campaign_analytics(campaign_id)")
        print("4. Export report: manager.export_campaign_report(campaign_id)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📋 Setup Requirements:")
        print("1. Set MAILCHIMP_API_KEY or SENDGRID_API_KEY environment variable")
        print("2. Ensure corporation database exists in data/corporations/")
        print("3. Run from the correct directory structure")

if __name__ == "__main__":
    main()