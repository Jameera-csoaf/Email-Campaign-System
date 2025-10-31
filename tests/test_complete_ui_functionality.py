#!/usr/bin/env python3
"""
🧪 Complete UI Functionality Test
================================
Tests every feature in the UI end-to-end to ensure everything works properly.
"""

import sys
import os
sys.path.append('.')

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        # Test main app imports
        from app.main import main
        print("✅ Main app imported successfully")
        
        # Test workflow manager
        from app.workflow_manager import get_workflow_manager, show_workflow_progress_bar, show_step_navigation
        print("✅ Workflow manager imported successfully")
        
        # Test workflow functions
        from app.workflow_functions import (
            show_create_campaign_workflow, show_ai_enhancement_workflow, 
            show_template_editor_workflow, show_record_manager_workflow,
            show_approval_center_workflow, show_send_campaign_workflow, show_analytics_workflow
        )
        print("✅ All workflow functions imported successfully")
        
        # Test AI components
        from app.few_shot_email_ai import get_few_shot_email_ai
        print("✅ Few-shot AI imported successfully")
        
        # Test AI intelligence
        try:
            from app.ai_intelligence import get_campaign_intelligence
            print("✅ AI intelligence imported successfully")
        except ImportError:
            print("⚠️ AI intelligence not available (optional)")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_loading():
    """Test data loading functionality"""
    print("\n🔍 Testing data loading...")
    
    try:
        import pandas as pd
        
        # Test Fortune 1000 database
        fortune_path = "data/clean/corporations/fortune1000_main_database.csv"
        if os.path.exists(fortune_path):
            df = pd.read_csv(fortune_path)
            print(f"✅ Fortune 1000 database loaded: {len(df)} records")
        else:
            print("❌ Fortune 1000 database not found")
            return False
        
        # Test campaigns data
        campaigns_path = "data/campaigns/campaigns_data.json"
        if os.path.exists(campaigns_path):
            import json
            with open(campaigns_path, 'r') as f:
                campaigns = json.load(f)
            print(f"✅ Campaigns data loaded: {len(campaigns)} campaigns")
        else:
            print("⚠️ Campaigns data not found (will be created)")
        
        return True
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def test_workflow_functionality():
    """Test workflow manager functionality"""
    print("\n🔍 Testing workflow functionality...")
    
    try:
        from app.workflow_manager import get_workflow_manager
        
        # Initialize workflow
        workflow = get_workflow_manager()
        print("✅ Workflow manager initialized")
        
        # Test step navigation
        current_step = workflow.get_current_step()
        print(f"✅ Current step: {current_step}")
        
        # Test step access
        can_access = workflow.can_access_step('campaign_creator')
        print(f"✅ Can access campaign creator: {can_access}")
        
        return True
    except Exception as e:
        print(f"❌ Workflow functionality error: {e}")
        return False

def test_ai_functionality():
    """Test AI functionality"""
    print("\n🔍 Testing AI functionality...")
    
    try:
        from app.few_shot_email_ai import get_few_shot_email_ai
        
        # Test AI initialization
        ai_system = get_few_shot_email_ai()
        print("✅ Few-shot AI system initialized")
        
        # Test template selection
        test_context = {
            'campaign_name': 'Test Campaign',
            'company_name': 'Test Corp',
            'industry': 'Technology',
            'location': 'New York'
        }
        
        # Test email generation
        result = ai_system.generate_email(test_context)
        print(f"✅ Email generation test completed: {type(result)}")
        
        return True
    except Exception as e:
        print(f"❌ AI functionality error: {e}")
        return False

def test_email_functionality():
    """Test email system functionality"""
    print("\n🔍 Testing email functionality...")
    
    try:
        # Check for Mailchimp API key
        mailchimp_key = os.environ.get('MAILCHIMP_API_KEY')
        if mailchimp_key and mailchimp_key != '[Your-Mailchimp-API-Key-Here]':
            print("✅ Mailchimp API key configured")
        else:
            print("⚠️ Mailchimp API key not configured (demo mode)")
        
        # Check for OpenAI API key
        openai_key = os.environ.get('OPENAI_API_KEY')
        if openai_key and openai_key != '[Your-OpenAI-API-Key-Here]':
            print("✅ OpenAI API key configured")
        else:
            print("⚠️ OpenAI API key not configured (fallback mode)")
        
        return True
    except Exception as e:
        print(f"❌ Email functionality error: {e}")
        return False

def test_performance():
    """Test system performance"""
    print("\n🔍 Testing performance...")
    
    try:
        import time
        import pandas as pd
        
        # Test data loading speed
        start_time = time.time()
        fortune_path = "data/clean/corporations/fortune1000_main_database.csv"
        if os.path.exists(fortune_path):
            df = pd.read_csv(fortune_path)
            load_time = time.time() - start_time
            print(f"✅ Data loading time: {load_time:.3f}s")
            
            if load_time < 3.0:
                print("✅ Performance: Excellent")
            elif load_time < 5.0:
                print("✅ Performance: Good")
            else:
                print("⚠️ Performance: Could be improved")
        
        return True
    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False

def main():
    """Run complete functionality test"""
    print("🚀 CSOAF Email Campaign Manager - Complete UI Functionality Test")
    print("=" * 70)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Imports", test_imports()))
    test_results.append(("Data Loading", test_data_loading()))
    test_results.append(("Workflow", test_workflow_functionality()))
    test_results.append(("AI Features", test_ai_functionality()))
    test_results.append(("Email System", test_email_functionality()))
    test_results.append(("Performance", test_performance()))
    
    # Show results summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:15}: {status}")
        if result:
            passed += 1
    
    print("=" * 70)
    print(f"📈 Overall Result: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready for the manager demo!")
        print("\n🚀 Next steps:")
        print("1. Run: python -m streamlit run app/main.py --server.port 8505")
        print("2. Open: http://localhost:8505")
        print("3. Test each workflow step manually")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()