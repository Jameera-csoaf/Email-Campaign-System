#!/usr/bin/env python3
"""
SMS Message Generator for Isabel Valencia Zuniga
Personal thank you message for supporting Healing Through Arts event
"""

def generate_isabel_sms():
    """Generate SMS message for Isabel Valencia Zuniga"""
    
    sms_message = """Hi Isabel! This is Jameera from Community School of Arts Foundation. Thank you so much for supporting our Healing Through Arts: NYC Schools event on Oct 13th at Rake Wine Bar! 🎭 

As an event organizer and artist, your energy really made the evening special. We raised important funds for arts healing programs in NYC schools thanks to supporters like you.

We're planning our upcoming Healing Through Arts event and would love to keep you updated! Can I add you to our event updates? 

Best regards,
Jameera (917) 216-5176
csoaf.org"""

    # SMS version (shorter for text limits)
    sms_short = """Hi Isabel! Jameera from CSOAF here. Thank you for supporting our Healing Through Arts event on Oct 13th! 🎭 Your energy as an event organizer & artist made it special. We raised funds for NYC school arts programs thanks to you! Planning our next event - can I keep you updated? Best, Jameera (917) 216-5176"""

    return sms_message, sms_short

def main():
    print("SMS MESSAGE FOR ISABEL VALENCIA ZUNIGA")
    print("=" * 80)
    print("Phone: 347-463-1193")
    print("Occupation: Event Organizer; Artist")
    print()
    
    full_message, short_message = generate_isabel_sms()
    
    print("FULL SMS MESSAGE:")
    print("-" * 40)
    print(full_message)
    print(f"Character count: {len(full_message)}")
    print()
    
    print("SHORT SMS MESSAGE (for character limits):")
    print("-" * 40)
    print(short_message)
    print(f"Character count: {len(short_message)}")
    print()
    
    print("📱 Ready to send to: 347-463-1193")

if __name__ == "__main__":
    main()