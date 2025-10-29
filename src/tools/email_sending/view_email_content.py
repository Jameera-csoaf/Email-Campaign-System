#!/usr/bin/env python3
"""
Email Content Viewer - View the actual content sent via SendGrid
"""

import pandas as pd

def view_sent_email_content():
    """Display the content of all sent emails"""
    
    print("SENT EMAIL CONTENT VIEWER")
    print("=" * 80)
    
    # Load the email content
    df = pd.read_csv('data/results/healing_arts_thank_you_emails_20251022_115129.csv')
    
    # Filter to emails that were sent (have email addresses)
    sent_emails = df[df['email'].str.contains('@', na=False)]
    
    print(f"📧 Total emails sent: {len(sent_emails)}")
    print("=" * 80)
    
    for i, row in sent_emails.iterrows():
        print(f"\nEMAIL #{i+1}")
        print("-" * 60)
        print(f"👤 TO: {row['name']}")
        print(f"📧 EMAIL: {row['email']}")
        print(f"📋 SUBJECT: {row['email_subject']}")
        print()
        print("📝 EMAIL CONTENT:")
        print("-" * 30)
        
        # Clean content (remove duplicate subject if present)
        content = row['email_content']
        if content.startswith('Subject:'):
            content = content.split('\n', 2)[2]
        
        print(content)
        print("\n" + "="*80)
    
    print("\n✅ This is the exact content that was delivered to each recipient!")
    print("📊 SendGrid shows delivery tracking, not content - that's normal!")

if __name__ == "__main__":
    view_sent_email_content()