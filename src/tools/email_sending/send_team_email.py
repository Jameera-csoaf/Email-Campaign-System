from sendgrid_email_sender import SendGridEmailSender

# Send team appreciation email
sender = SendGridEmailSender()

# Team email addresses (add more as needed)
team_emails = [
    'jameera@csoaf.org'  # Add other team member emails here
]

print("Sending team appreciation email from Anthony Villacis...")
sent, failed = sender.send_team_email(team_emails)

print(f"Team email results:")
print(f"Successfully sent: {len(sent)} emails")
print(f"Failed: {len(failed)} emails")

for email in sent:
    print(f"✅ Sent to: {email['email']} at {email['sent_time']}")

for email in failed:
    print(f"❌ Failed: {email['email']} - {email.get('error', 'Unknown error')}")