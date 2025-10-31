#!/usr/bin/env python3
"""
🔧 Workflow Debug Tool
=====================
Debugging the workflow data flow issues
"""

import streamlit as st
import sys
import os

# Add the app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def debug_workflow_state():
    """Debug the current workflow state"""
    print("🔍 DEBUGGING WORKFLOW STATE")
    print("=" * 50)
    
    try:
        from app.workflow_manager import get_workflow_manager
        
        # Initialize workflow manager (this should create session state)
        workflow = get_workflow_manager()
        print("✅ Workflow manager initialized")
        
        # Try to access session state (this will fail outside Streamlit)
        try:
            if hasattr(st, 'session_state') and hasattr(st.session_state, 'workflow_state'):
                print("✅ Session state exists")
                workflow_state = st.session_state.workflow_state
                print(f"📊 Current step: {workflow_state.get('current_step', 'NONE')}")
                print(f"📊 Campaign data keys: {list(workflow_state.get('campaign_data', {}).keys())}")
                print(f"📊 Completed steps: {workflow_state.get('completed_steps', set())}")
            else:
                print("⚠️ Session state not available (running outside Streamlit)")
        except Exception as e:
            print(f"⚠️ Session state access error: {e}")
        
        # Test step requirements
        print("\n🔍 TESTING STEP REQUIREMENTS")
        print("=" * 30)
        
        for step in workflow.workflow_steps:
            requirements = workflow.get_step_requirements(step)
            print(f"📋 {step}: {requirements}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_campaign_creator_data():
    """Test what data the campaign creator should produce"""
    print("\n🔍 TESTING CAMPAIGN CREATOR DATA STRUCTURE")
    print("=" * 50)
    
    # Simulate the data that campaign creator should produce
    test_campaign_data = {
        'campaign_name': 'Test Campaign',
        'campaign_type': 'Sponsorship Request',
        'priority_level': 'High',
        'target_funding': 50000,
        'deadline': '2025-12-31',
        'expected_recipients': 25,
        'campaign_description': 'Test campaign description for debugging',
        'created_at': '2025-10-30T22:30:00',
        'status': 'foundation_created'
    }
    
    print("📊 Expected campaign data structure:")
    for key, value in test_campaign_data.items():
        print(f"   {key}: {value}")
    
    # Test what AI Enhancement needs
    ai_requirements = ['campaign_name', 'campaign_description']
    print(f"\n📋 AI Enhancement requirements: {ai_requirements}")
    
    missing = []
    for req in ai_requirements:
        if req not in test_campaign_data:
            missing.append(req)
    
    if missing:
        print(f"❌ Missing requirements: {missing}")
        return False
    else:
        print("✅ All AI Enhancement requirements satisfied")
        return True

def main():
    print("🚀 CSOAF Workflow Debug Tool")
    print("=" * 70)
    
    # Test 1: Basic workflow functionality
    print("\n🧪 TEST 1: Workflow Manager")
    test1_passed = debug_workflow_state()
    
    # Test 2: Campaign data structure
    print("\n🧪 TEST 2: Campaign Data Structure")
    test2_passed = test_campaign_creator_data()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 DEBUG SUMMARY")
    print("=" * 70)
    print(f"Test 1 (Workflow Manager): {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Test 2 (Data Structure): {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎯 DIAGNOSIS: Workflow structure looks correct")
        print("💡 LIKELY ISSUE: Session state not persisting between page navigation")
        print("\n🔧 RECOMMENDED FIX:")
        print("1. Check if session state is being reset")
        print("2. Verify workflow advance_to_step is being called correctly")
        print("3. Test with debug prints in the actual Streamlit app")
    else:
        print("\n❌ ISSUES DETECTED: See failures above")
    
    print("\n🚀 Next: Run the actual app and check session state persistence")

if __name__ == "__main__":
    main()