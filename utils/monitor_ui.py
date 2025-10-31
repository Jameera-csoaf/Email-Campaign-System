#!/usr/bin/env python3
"""
🔍 Live UI Monitoring Tool
=========================
Monitor what's happening in the Streamlit UI in real-time
"""

import time
import os

def monitor_ui_logs():
    """Monitor Streamlit logs for debugging"""
    print("🔍 UI MONITORING STARTED")
    print("=" * 50)
    print("📍 Application URL: http://localhost:8507")
    print("📋 What to test:")
    print("   1. Open the dashboard")
    print("   2. Check the debug panels (sidebar and main area)")
    print("   3. Click 'Create New Campaign' button")
    print("   4. Navigate to Campaign Creator from sidebar")
    print("   5. Check debug info in Campaign Creator")
    print("=" * 50)
    
    print("\n🎯 EXPECTED DEBUG OUTPUT IN UI:")
    print("Dashboard Debug Info should show:")
    print("   - Current Workflow Step: dashboard")
    print("   - WORKFLOW_ENABLED: True") 
    print("   - Session State Exists: True")
    
    print("\nCampaign Creator Debug Info should show:")
    print("   - Campaign Creator function called successfully!")
    print("   - Workflow Manager Initialized: ✅")
    print("   - Current Step: campaign_creator")
    print("   - Input Data and Campaign Data")
    
    print("\n🔧 DEBUGGING INSTRUCTIONS:")
    print("1. Open http://localhost:8507 in your browser")
    print("2. Look for debug information in:")
    print("   - Sidebar 'Live Debug Panel'")
    print("   - Main area debug sections")
    print("   - Campaign Creator debug info")
    print("3. Try navigation: Dashboard → Campaign Creator")
    print("4. Report what you see in each debug panel")
    
    print("\n✅ WHAT SHOULD WORK NOW:")
    print("- Dashboard loads with debug info")
    print("- 'Create New Campaign' button works")
    print("- Campaign Creator shows debug details")
    print("- Sidebar shows live workflow state")
    
    print("\n❌ REPORT IF YOU SEE:")
    print("- Error messages in any debug panel")
    print("- 'WORKFLOW_ENABLED: False'")
    print("- 'Session State Exists: False'") 
    print("- Empty or missing debug information")
    print("- Navigation not working between pages")
    
    print(f"\n🚀 Ready for testing! Application running at: http://localhost:8507")

if __name__ == "__main__":
    monitor_ui_logs()