#!/usr/bin/env python3
"""
Demo: AI-Powered Campaign Creation
Test the natural language campaign intelligence
"""

import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from ai_campaign_intelligence import CampaignIntelligence
import pandas as pd

def demo_ai_campaign_creation():
    """Demonstrate AI-powered campaign creation"""
    
    print("🤖 AI-Powered Campaign Creation Demo")
    print("=" * 50)
    
    # Initialize AI
    ai = CampaignIntelligence()
    
    # Test scenarios
    test_campaigns = [
        "I want to reach tech companies in California for a $50k sponsorship",
        "Looking for financial services partners in New York for our gala event",
        "Need healthcare companies with strong arts education interest",
        "Target manufacturing companies in Texas for partnership opportunities",
        "Reach out to major corporations for holiday event sponsorship"
    ]
    
    for i, campaign_desc in enumerate(test_campaigns, 1):
        print(f"\n📝 Test {i}: {campaign_desc}")
        print("-" * 40)
        
        # Extract keywords and parameters
        extracted = ai.extract_keywords_with_ai(campaign_desc)
        
        print("🎯 Extracted Parameters:")
        for key, value in extracted.items():
            if value:  # Only show non-empty values
                print(f"  {key}: {value}")
        
        # Generate suggestions
        suggestions = ai.generate_campaign_suggestions(extracted)
        
        print("\n💡 AI Suggestions:")
        print(f"  Subject: {suggestions['subject_line']}")
        print(f"  Focus: {suggestions['campaign_focus']}")
        if suggestions['key_messages']:
            print("  Messages:")
            for msg in suggestions['key_messages']:
                print(f"    • {msg}")
        
        print(f"  CTA: {suggestions['call_to_action']}")
    
    print("\n" + "=" * 50)
    print("✅ AI Campaign Demo Complete!")
    print("🌐 Visit http://localhost:8523 to try the interactive version")

if __name__ == "__main__":
    demo_ai_campaign_creation()