#!/usr/bin/env python3
"""
🤖 Few-Shot AI Email Generation Demo
===================================
Demonstration of the advanced AI email generation system using proven templates.

This script shows how the few-shot learning system works and provides examples
of AI-generated emails based on existing successful templates.
"""

import sys
import os

# Add the app directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, 'app')
sys.path.append(app_dir)

from few_shot_email_ai import get_few_shot_email_ai

def demo_few_shot_email_generation():
    """Demonstrate the few-shot AI email generation with various scenarios"""
    
    print("🤖 Few-Shot AI Email Generation Demo")
    print("=" * 50)
    
    # Initialize the AI system
    try:
        few_shot_ai = get_few_shot_email_ai()
        print("✅ Few-shot AI system initialized successfully")
        print(f"📚 Loaded {len(few_shot_ai.template_examples)} proven template examples")
        print()
    except Exception as e:
        print(f"❌ Error initializing AI system: {e}")
        return
    
    # Test scenarios
    test_scenarios = [
        {
            'name': 'Technology Partnership - Fortune 500',
            'context': {
                'campaign_name': 'Tech Innovation Partnership',
                'targeting_description': 'Fortune 500 technology companies',
                'selected_industries': ['Technology', 'Software'],
                'location_focus': 'San Francisco Bay Area',
                'sponsorship_tiers': ['$100,000+'],
                'user_description': 'Looking for strategic partnerships with major tech companies to support our STEM-arts fusion programs. We want to develop the next generation of creative technologists.'
            }
        },
        {
            'name': 'Community Partnership - Healthcare',
            'context': {
                'campaign_name': 'Healing Arts Initiative',
                'targeting_description': 'Healthcare organizations and hospitals',
                'selected_industries': ['Healthcare', 'Medical'],
                'location_focus': 'New York City',
                'sponsorship_tiers': ['$25,000-$50,000'],
                'user_description': 'Seeking partnerships with healthcare organizations to bring arts therapy and creative wellness programs to patients and communities.'
            }
        },
        {
            'name': 'Foundation Grant - Education',
            'context': {
                'campaign_name': 'Arts Education Access Fund',
                'targeting_description': 'Education-focused foundations',
                'selected_industries': ['Non-profit', 'Education'],
                'location_focus': 'National',
                'sponsorship_tiers': ['$50,000-$100,000'],
                'user_description': 'Requesting foundation support to expand arts education access in underserved communities across the country.'
            }
        },
        {
            'name': 'Event Partnership - Finance',
            'context': {
                'campaign_name': 'Annual Gala Sponsorship',
                'targeting_description': 'Financial services companies',
                'selected_industries': ['Finance', 'Banking'],
                'location_focus': 'Manhattan',
                'sponsorship_tiers': ['$10,000-$25,000'],
                'user_description': 'Inviting financial sector leaders to sponsor our annual gala celebrating student achievements and community impact.'
            }
        }
    ]
    
    # Generate emails for each scenario
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"📧 Scenario {i}: {scenario['name']}")
        print("-" * 40)
        
        try:
            result = few_shot_ai.generate_email(scenario['context'])
            
            if result['success']:
                print(f"✨ AI Generation: SUCCESS")
                print(f"📋 Template Used: {result['template_used']}")
                print()
                print(f"📌 Subject: {result['subject']}")
                print()
                print("📝 Email Content:")
                print(result['content'])
                print()
                print(f"🔍 Reasoning: {result.get('reasoning', 'N/A')}")
                
            else:
                print(f"❌ AI Generation: FAILED")
                print(f"Error: {result['error']}")
                
        except Exception as e:
            print(f"❌ Error generating email: {e}")
        
        print("\n" + "="*60 + "\n")
    
    # Show template statistics
    print("📊 Template Usage Statistics:")
    print("-" * 30)
    template_categories = [example['category'] for example in few_shot_ai.template_examples]
    for category in set(template_categories):
        count = template_categories.count(category)
        print(f"• {category}: {count} templates")
    
    print(f"\n🎯 Total Templates Available: {len(few_shot_ai.template_examples)}")
    print("✅ Demo completed successfully!")

def test_ai_availability():
    """Test if OpenAI API is available and working"""
    
    print("\n🔧 Testing AI Availability")
    print("-" * 25)
    
    try:
        few_shot_ai = get_few_shot_email_ai()
        
        # Test with simple context
        test_context = {
            'campaign_name': 'Test Campaign',
            'user_description': 'Simple test to check if AI is working'
        }
        
        result = few_shot_ai.generate_email(test_context)
        
        if result['success']:
            print("✅ OpenAI API: WORKING")
            print("✅ Email Generation: FUNCTIONAL")
        else:
            print("⚠️  OpenAI API: LIMITED (using fallback)")
            print(f"Fallback reason: {result.get('error', 'Unknown')}")
            
    except Exception as e:
        print(f"❌ AI System: ERROR - {e}")

if __name__ == "__main__":
    print("🚀 Starting Few-Shot AI Email Demo...\n")
    
    # Test AI availability first
    test_ai_availability()
    
    print("\n" + "="*60)
    
    # Run the main demo
    demo_few_shot_email_generation()
    
    print("\n🎉 Demo finished! Visit http://localhost:8502 to try the live system.")