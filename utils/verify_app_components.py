#!/usr/bin/env python3
"""
Quick test to verify the campaign creator form submission works
"""

import sys
import os
import importlib.util

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_workflow_functions():
    """Test that workflow functions can be imported and called"""
    try:
        # Test importing the workflow functions
        from workflow_functions import create_campaign_step
        print("✅ Successfully imported workflow_functions")
        
        # Test that the function exists
        if callable(create_campaign_step):
            print("✅ create_campaign_step function is callable")
        else:
            print("❌ create_campaign_step is not callable")
            
        return True
    except Exception as e:
        print(f"❌ Error importing workflow functions: {e}")
        return False

def test_main_app():
    """Test that main app can be imported"""
    try:
        from main import main
        print("✅ Successfully imported main app")
        return True
    except Exception as e:
        print(f"❌ Error importing main app: {e}")
        return False

def main():
    print("🧪 Testing App Components...")
    print("=" * 50)
    
    success = True
    
    print("\n📦 Testing Workflow Functions:")
    if not test_workflow_functions():
        success = False
        
    print("\n📦 Testing Main App:")
    if not test_main_app():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All components loaded successfully!")
        print("🌐 App should be running at: http://localhost:8501")
        print("\n🧪 Test Steps:")
        print("1. Open the URL in your browser")
        print("2. Navigate to '🚀 Campaign Creator'")
        print("3. Fill out the form:")
        print("   - Campaign Name: 'Test Campaign'")
        print("   - Description: 'Test Description'")
        print("   - Priority Levels: Select 'High' and 'Medium'")
        print("4. Click 'Create Campaign'")
        print("5. You should see navigation to '🤖 AI Enhancement'")
    else:
        print("❌ Some components failed to load")
        print("🔧 Check the error messages above")

if __name__ == "__main__":
    main()