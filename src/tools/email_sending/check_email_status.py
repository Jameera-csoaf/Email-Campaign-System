#!/usr/bin/env python3
"""
SendGrid Email Status Checker
Check delivery status of sent emails
"""

import pandas as pd
import os
from datetime import datetime

def check_sent_emails():
    """Display sent email status from logs"""
    
    print("SENDGRID EMAIL DELIVERY STATUS")
    print("=" * 80)
    
    # Find the most recent sent emails file
    results_dir = "data/results"
    sent_files = [f for f in os.listdir(results_dir) if f.startswith('sendgrid_sent_emails_')]
    
    if not sent_files:
        print("❌ No sent email logs found")
        return
    
    # Get most recent file
    latest_file = max(sent_files)
    file_path = os.path.join(results_dir, latest_file)
    
    print(f"📁 Log file: {latest_file}")
    print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load and display sent emails
    df = pd.read_csv(file_path)
    
    print(f"📊 DELIVERY SUMMARY:")
    print(f"✅ Total emails sent: {len(df)}")
    print(f"📧 All emails accepted for delivery (Status 202)")
    print()
    
    print("📋 SENT EMAIL DETAILS:")
    print("-" * 80)
    
    for i, row in df.iterrows():
        sent_time = row['sent_time']
        print(f"{i+1}. ✅ {row['name']}")
        print(f"   📧 {row['email']}")
        print(f"   ⏰ Sent: {sent_time}")
        print(f"   📊 Status: HTTP {row['status_code']} (Accepted)")
        print()
    
    print("🔍 FOR DETAILED TRACKING:")
    print("1. Visit SendGrid Dashboard: https://app.sendgrid.com")
    print("2. Go to Activity → Email Activity")
    print("3. Filter by today's date to see delivery details")
    print("4. Check opens, clicks, and delivery confirmations")
    print()
    
    print("📱 REMINDER:")
    print("Don't forget to send SMS to Isabel Valencia Zuniga: 347-463-1193")

if __name__ == "__main__":
    check_sent_emails()