#!/usr/bin/env python3
"""
Email Provider Abstraction Layer
Unified interface for multiple email providers (SendGrid, Mailchimp, etc.)
"""

import os
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailProvider(ABC):
    """Abstract base class for email providers"""
    
    @abstractmethod
    def send_email(self, to_email: str, to_name: str, subject: str, 
                   html_content: str, **kwargs) -> Dict:
        """Send a single email"""
        pass
    
    @abstractmethod
    def send_campaign(self, recipients: List[Dict], subject: str, 
                     html_template: str, campaign_name: str, **kwargs) -> Dict:
        """Send email campaign to multiple recipients"""
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict:
        """Get email sending statistics"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Test provider connection"""
        pass

class UnifiedEmailSender:
    """
    Unified email sender that can use multiple providers
    Provides consistent interface regardless of backend provider
    """
    
    SUPPORTED_PROVIDERS = {
        'mailchimp': 'MailchimpEmailSender',
        'sendgrid': 'SendGridEmailSender',
        'smtp': 'SMTPEmailSender'  # Future implementation
    }
    
    def __init__(self, provider: str = 'mailchimp', daily_limit: int = 100, **provider_kwargs):
        """
        Initialize unified email sender
        
        Args:
            provider: Email provider to use ('mailchimp', 'sendgrid', 'smtp')
            daily_limit: Maximum emails per day
            **provider_kwargs: Provider-specific configuration
        """
        
        self.provider_name = provider.lower()
        self.daily_limit = daily_limit
        self.provider_kwargs = provider_kwargs
        
        # Validate provider
        if self.provider_name not in self.SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}. Supported: {list(self.SUPPORTED_PROVIDERS.keys())}")
        
        # Initialize provider
        self.provider = self._initialize_provider()
        
        # Common configuration
        self.sender_email = "promo@csoaf.org"
        self.sender_name = "Community School of the Arts Foundation"
        self.organization = "CSOAF"
        
        logger.info(f"📧 Unified Email Sender initialized with {self.provider_name.title()} provider")
    
    def _initialize_provider(self):
        """Initialize the selected email provider"""
        
        if self.provider_name == 'mailchimp':
            from .mailchimp_email_sender import MailchimpEmailSender
            return MailchimpEmailSender(daily_limit=self.daily_limit, **self.provider_kwargs)
        
        elif self.provider_name == 'sendgrid':
            from .sendgrid_email_sender import SendGridEmailSender
            return SendGridEmailSender(**self.provider_kwargs)
        
        elif self.provider_name == 'smtp':
            # Future implementation for generic SMTP
            raise NotImplementedError("SMTP provider not yet implemented")
        
        else:
            raise ValueError(f"Provider {self.provider_name} not implemented")
    
    def send_email(self, to_email: str, to_name: str, subject: str, 
                   html_content: str, **kwargs) -> Dict:
        """
        Send a single email using the configured provider
        
        Returns consistent format regardless of provider:
        {
            'success': bool,
            'email_id': str,
            'provider': str,
            'sent_at': str,
            'error': str (if failed)
        }
        """
        
        try:
            # Call provider-specific method
            if hasattr(self.provider, 'send_transactional_email'):
                result = self.provider.send_transactional_email(
                    to_email=to_email,
                    to_name=to_name,
                    subject=subject,
                    html_content=html_content,
                    **kwargs
                )
            elif hasattr(self.provider, 'send_team_email'):
                # SendGrid method signature
                result = self.provider.send_team_email(
                    to_email=to_email,
                    to_name=to_name,
                    subject=subject,
                    html_content=html_content,
                    **kwargs
                )
            else:
                raise AttributeError(f"Provider {self.provider_name} missing send method")
            
            # Normalize response format
            if isinstance(result, dict) and 'success' in result:
                result['provider'] = self.provider_name
                return result
            else:
                # Handle different return formats
                return {
                    'success': True,
                    'email_id': result.get('id', f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
                    'provider': self.provider_name,
                    'sent_at': datetime.now().isoformat(),
                    'to_email': to_email,
                    'to_name': to_name
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to send email via {self.provider_name}: {e}")
            return {
                'success': False,
                'error': str(e),
                'provider': self.provider_name,
                'to_email': to_email,
                'to_name': to_name
            }
    
    def send_campaign(self, recipients: List[Dict], subject: str, html_template: str, 
                     campaign_name: str, **kwargs) -> Dict:
        """
        Send email campaign using the configured provider
        
        Returns consistent format:
        {
            'success': bool,
            'campaign_id': str,
            'provider': str,
            'total_recipients': int,
            'sent_successfully': int,
            'failed': int,
            'details': List[Dict]
        }
        """
        
        try:
            # Call provider-specific campaign method
            if hasattr(self.provider, 'send_campaign_batch'):
                result = self.provider.send_campaign_batch(
                    recipients=recipients,
                    subject=subject,
                    html_template=html_template,
                    campaign_name=campaign_name,
                    **kwargs
                )
            else:
                # Fallback: send individual emails
                result = self._send_campaign_individually(
                    recipients=recipients,
                    subject=subject,
                    html_template=html_template,
                    campaign_name=campaign_name,
                    **kwargs
                )
            
            # Normalize response
            result['provider'] = self.provider_name
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to send campaign via {self.provider_name}: {e}")
            return {
                'success': False,
                'error': str(e),
                'provider': self.provider_name,
                'campaign_name': campaign_name,
                'total_recipients': len(recipients)
            }
    
    def _send_campaign_individually(self, recipients: List[Dict], subject: str, 
                                  html_template: str, campaign_name: str, **kwargs) -> Dict:
        """Fallback method to send campaign as individual emails"""
        
        campaign_id = f"unified_campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        results = {
            'campaign_id': campaign_id,
            'campaign_name': campaign_name,
            'total_recipients': len(recipients),
            'sent_successfully': 0,
            'failed': 0,
            'details': []
        }
        
        logger.info(f"🚀 Sending campaign individually: {campaign_name}")
        
        for recipient in recipients:
            # Personalize template
            personalized_content = self._personalize_template(html_template, recipient)
            
            # Send individual email
            send_result = self.send_email(
                to_email=recipient.get('email', ''),
                to_name=recipient.get('name', ''),
                subject=subject,
                html_content=personalized_content,
                campaign_id=campaign_id
            )
            
            if send_result['success']:
                results['sent_successfully'] += 1
                results['details'].append({
                    'recipient': recipient.get('email', ''),
                    'status': 'sent',
                    'email_id': send_result.get('email_id', '')
                })
            else:
                results['failed'] += 1
                results['details'].append({
                    'recipient': recipient.get('email', ''),
                    'status': 'failed',
                    'error': send_result.get('error', 'Unknown error')
                })
        
        return results
    
    def _personalize_template(self, template: str, recipient: Dict) -> str:
        """Basic template personalization"""
        
        personalized = template
        
        # Common personalizations
        replacements = {
            '{organization_name}': recipient.get('organization_name', 'Your Organization'),
            '{contact_name}': recipient.get('contact_name', recipient.get('name', 'Dear Colleague')),
            '{city}': recipient.get('city', ''),
            '{state}': recipient.get('state', ''),
            '{industry}': recipient.get('industry_sector', ''),
            '{website}': recipient.get('website', '')
        }
        
        for placeholder, value in replacements.items():
            personalized = personalized.replace(placeholder, str(value))
        
        return personalized
    
    def get_stats(self) -> Dict:
        """Get email statistics from the provider"""
        
        try:
            if hasattr(self.provider, 'get_campaign_stats'):
                stats = self.provider.get_campaign_stats()
            elif hasattr(self.provider, 'get_stats'):
                stats = self.provider.get_stats()
            else:
                stats = {'error': 'Provider does not support statistics'}
            
            stats['provider'] = self.provider_name
            return stats
            
        except Exception as e:
            return {
                'error': str(e),
                'provider': self.provider_name
            }
    
    def test_connection(self) -> Dict:
        """Test connection to the email provider"""
        
        try:
            if hasattr(self.provider, 'test_connection'):
                success = self.provider.test_connection()
            elif hasattr(self.provider, '_test_connection'):
                self.provider._test_connection()
                success = True
            else:
                # Basic test by trying to initialize
                success = True
            
            return {
                'success': success,
                'provider': self.provider_name,
                'sender_email': self.sender_email,
                'daily_limit': self.daily_limit
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': self.provider_name
            }
    
    def switch_provider(self, new_provider: str, **new_kwargs):
        """Switch to a different email provider"""
        
        logger.info(f"🔄 Switching from {self.provider_name} to {new_provider}")
        
        # Backup current stats if possible
        current_stats = self.get_stats()
        
        # Switch provider
        self.provider_name = new_provider.lower()
        self.provider_kwargs = new_kwargs
        self.provider = self._initialize_provider()
        
        logger.info(f"✅ Successfully switched to {new_provider}")
        
        return {
            'previous_provider': self.provider_name,
            'new_provider': new_provider,
            'previous_stats': current_stats
        }
    
    def get_provider_config(self) -> Dict:
        """Get current provider configuration"""
        
        return {
            'provider': self.provider_name,
            'sender_email': self.sender_email,
            'sender_name': self.sender_name,
            'daily_limit': self.daily_limit,
            'provider_kwargs': self.provider_kwargs
        }

# Convenience functions for quick setup

def create_mailchimp_sender(api_key: str = None, daily_limit: int = 100) -> UnifiedEmailSender:
    """Create Mailchimp email sender"""
    return UnifiedEmailSender(provider='mailchimp', api_key=api_key, daily_limit=daily_limit)

def create_sendgrid_sender(api_key: str = None, daily_limit: int = 100) -> UnifiedEmailSender:
    """Create SendGrid email sender"""
    return UnifiedEmailSender(provider='sendgrid', api_key=api_key, daily_limit=daily_limit)

def auto_detect_provider() -> UnifiedEmailSender:
    """Auto-detect available email provider based on environment variables"""
    
    # Check for API keys in environment
    if os.environ.get('MAILCHIMP_API_KEY'):
        logger.info("🔍 Detected Mailchimp API key, using Mailchimp provider")
        return create_mailchimp_sender()
    elif os.environ.get('SENDGRID_API_KEY'):
        logger.info("🔍 Detected SendGrid API key, using SendGrid provider")
        return create_sendgrid_sender()
    else:
        logger.warning("⚠️ No email provider API keys found in environment")
        logger.info("📋 Please set MAILCHIMP_API_KEY or SENDGRID_API_KEY environment variable")
        raise ValueError("No email provider API keys found. Please configure MAILCHIMP_API_KEY or SENDGRID_API_KEY")

def main():
    """Test the unified email sender"""
    print("🧪 Testing Unified Email Sender")
    print("="*50)
    
    try:
        # Try to auto-detect provider
        sender = auto_detect_provider()
        
        # Test connection
        connection_test = sender.test_connection()
        print(f"📧 Provider: {connection_test['provider']}")
        print(f"✅ Connection: {'Success' if connection_test['success'] else 'Failed'}")
        
        # Get configuration
        config = sender.get_provider_config()
        print(f"📋 Configuration: {config}")
        
        # Get stats
        stats = sender.get_stats()
        print(f"📊 Stats: {stats}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📋 SETUP INSTRUCTIONS:")
        print("Set one of these environment variables:")
        print("- MAILCHIMP_API_KEY=your_mailchimp_key")
        print("- SENDGRID_API_KEY=your_sendgrid_key")

if __name__ == "__main__":
    main()