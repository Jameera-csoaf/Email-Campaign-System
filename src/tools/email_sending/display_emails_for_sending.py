#!/usr/bin/env python3
"""
Display Thank You Emails Ready for Sending
Formatted for easy copy/paste into email client
"""

import pandas as pd

def display_emails_for_sending():
    # Load the generated emails
    df = pd.read_csv('data/results/healing_arts_thank_you_emails_20251022_115129.csv')
    
    # Filter contacts with email addresses
    email_contacts = df[df['email'].str.contains('@', na=False)]
    
    print("THANK YOU EMAILS - READY TO SEND")
    print("=" * 80)
    print(f"Send from: jameera@csoaf.org")
    print(f"Total emails to send: {len(email_contacts)}")
    print("=" * 80)
    
    for i, row in email_contacts.iterrows():
        print(f"\nEMAIL #{i+1}")
        print("-" * 50)
        print(f"TO: {row['email']}")
        print(f"SUBJECT: {row['email_subject']}")
        print()
        print("EMAIL CONTENT:")
        print("-" * 30)
        # Remove the duplicate subject line from content
        content = row['email_content']
        if content.startswith('Subject:'):
            content = content.split('\n', 2)[2]  # Skip subject line
        print(content)
        print("\n" + "="*80)
    
    print(f"\n✅ Copy each email above and send from jameera@csoaf.org")
    print(f"📱 Also send SMS to Isabel Valencia Zuniga: 347-463-1193")

if __name__ == "__main__":
    display_emails_for_sending()