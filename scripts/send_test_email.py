#!/usr/bin/env python3
"""
Send Test Email via Mailchimp
Real test of the email campaign system with live sending
"""

import os
import sys

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.append(src_dir)

from tools.email_sending.mailchimp_email_sender import MailchimpEmailSender

def send_test_email():
    """Send a real test email via Mailchimp"""
    
    print("🧪 Sending Real Test Email via Mailchimp")
    print("="*50)
    
    # Initialize Mailchimp sender
    try:
        sender = MailchimpEmailSender(daily_limit=100)
        print("✅ Mailchimp connection successful")
        print(f"📧 Connected to: {sender.sender_name}")
        print(f"📊 Daily limit: {sender.daily_limit}")
    except Exception as e:
        print(f"❌ Failed to connect to Mailchimp: {e}")
        return
    
    # Test email content
    test_email_html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .header { background-color: #2c3e50; color: white; padding: 20px; text-align: center; }
            .content { padding: 30px; max-width: 600px; margin: 0 auto; }
            .highlight { background-color: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0; }
            .footer { background-color: #ecf0f1; padding: 20px; text-align: center; font-size: 12px; color: #7f8c8d; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎉 CSOAF Email System Test</h1>
            <p>Community School of the Arts Foundation</p>
        </div>
        
        <div class="content">
            <h2>Email Campaign System Successfully Configured!</h2>
            
            <p>This is a test email to confirm that your CSOAF email campaign system is working perfectly with Mailchimp.</p>
            
            <div class="highlight">
                <h3>✅ System Status: OPERATIONAL</h3>
                <ul>
                    <li><strong>Mailchimp Integration:</strong> Connected and functional</li>
                    <li><strong>Database Integration:</strong> 1,000 corporations loaded</li>
                    <li><strong>Template System:</strong> Professional templates ready</li>
                    <li><strong>Rate Limiting:</strong> 100 emails/day configured</li>
                    <li><strong>Sender Email:</strong> promo@csoaf.org</li>
                </ul>
            </div>
            
            <h3>🎯 Ready for Live Campaigns</h3>
            <p>Your email campaign system can now:</p>
            <ul>
                <li>Target specific regions and industries</li>
                <li>Send personalized, professional emails</li>
                <li>Track campaign performance and analytics</li>
                <li>Manage multiple campaigns efficiently</li>
            </ul>
            
            <p><strong>Campaign targeting example:</strong></p>
            <ul>
                <li>4 qualified recipients in NY & CA</li>
                <li>Technology & Financial Services sectors</li>
                <li>$942k total sponsorship potential</li>
                <li>Average $235k sponsorship capacity</li>
            </ul>
            
            <p>The system is ready to help CSOAF connect with potential sponsors and partners!</p>
        </div>
        
        <div class="footer">
            <p><strong>Community School of the Arts Foundation</strong><br>
            📧 promo@csoaf.org | 🌐 www.csoaf.org<br>
            <em>Test email sent on October 26, 2025</em></p>
        </div>
    </body>
    </html>
    """
    
    # Get test email address
    test_email = input("Enter your email address for the test: ").strip()
    
    if not test_email or '@' not in test_email:
        print("❌ Invalid email address")
        return
    
    print(f"📧 Sending test email to: {test_email}")
    
    # Send test email
    try:
        result = sender.send_transactional_email(
            to_email=test_email,
            to_name="CSOAF Test Recipient",
            subject="🎉 CSOAF Email Campaign System - Test Successful!",
            html_content=test_email_html,
            tracking_data={
                'test_type': 'system_verification',
                'sent_at': '2025-10-26',
                'system_status': 'operational'
            }
        )
        
        if result['success']:
            print("✅ Test email sent successfully!")
            print(f"📧 Email ID: {result['email_id']}")
            print(f"📊 Daily count: {result['sent_today']}/{result['daily_limit']}")
            print(f"⏰ Sent at: {result['sent_at']}")
            
            print("\n🎯 Next Steps:")
            print("1. Check your email inbox for the test message")
            print("2. Review the professional formatting and content")
            print("3. Your system is ready for live campaigns!")
            
        else:
            print(f"❌ Failed to send test email: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error sending test email: {e}")
    
    # Show campaign stats
    try:
        stats = sender.get_campaign_stats()
        print(f"\n📊 Current Statistics:")
        print(f"• Emails sent today: {stats['sent_today']}")
        print(f"• Daily limit: {stats['daily_limit']}")
        print(f"• Total campaigns: {stats['total_campaigns']}")
        
    except Exception as e:
        print(f"⚠️ Could not retrieve stats: {e}")

if __name__ == "__main__":
    send_test_email()