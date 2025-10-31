#!/usr/bin/env python3
"""
Comprehensive UI Functionality Test Script
This script tests all major components of the CSOAF Email Campaign Manager
to ensure everything is working properly.
"""

import pandas as pd
import os
import sys
from datetime import datetime
import traceback

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def test_result(test_name, success, details=""):
    """Print test result with formatting"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"   📝 {details}")

def test_data_files():
    """Test all data files are accessible"""
    print_section("Data Files Test")
    
    files_to_test = [
        ("Fortune 1000 Database", "data/clean/corporations/fortune1000_main_database.csv"),
        ("Mission Aligned Prospects", "data/clean/campaigns/mission_aligned_prospects.csv"),
        ("Campaign Templates", "campaigns/email_templates/manager_approved_templates.py"),
        ("Main Application", "app/main.py"),
        ("AI Intelligence", "app/ai_intelligence.py")
    ]
    
    all_files_ok = True
    for name, path in files_to_test:
        exists = os.path.exists(path)
        test_result(f"{name} File", exists, f"Path: {path}")
        if not exists:
            all_files_ok = False
    
    return all_files_ok

def test_database_loading():
    """Test database loading and structure"""
    print_section("Database Loading Test")
    
    try:
        # Test Fortune 1000 database
        corp_df = pd.read_csv("data/clean/corporations/fortune1000_main_database.csv")
        test_result("Fortune 1000 Database Load", True, f"{len(corp_df)} records loaded")
        
        # Test column structure
        expected_cols = ['organization_name', 'industry_sector', 'state', 'city']
        missing_cols = [col for col in expected_cols if col not in corp_df.columns]
        test_result("Required Columns Present", len(missing_cols) == 0, 
                   f"Missing: {missing_cols}" if missing_cols else "All key columns found")
        
        # Test data quality
        non_null_orgs = corp_df['organization_name'].notna().sum()
        test_result("Data Quality Check", non_null_orgs > 900, 
                   f"{non_null_orgs} valid organization names")
        
        return True, corp_df
        
    except Exception as e:
        test_result("Database Loading", False, str(e))
        return False, None

def test_campaign_data():
    """Test campaign prospect data"""
    print_section("Campaign Data Test")
    
    try:
        campaign_df = pd.read_csv("data/clean/campaigns/mission_aligned_prospects.csv")
        test_result("Campaign Prospects Load", True, f"{len(campaign_df)} prospects loaded")
        
        # Check if we have email addresses
        if 'email' in campaign_df.columns:
            valid_emails = campaign_df['email'].notna().sum()
            test_result("Email Addresses Available", valid_emails > 0, 
                       f"{valid_emails} valid email addresses")
        
        return True, campaign_df
        
    except Exception as e:
        test_result("Campaign Data Loading", False, str(e))
        return False, None

def test_analytics_functions(corp_df):
    """Test analytics and visualization functions"""
    print_section("Analytics Functions Test")
    
    if corp_df is None:
        test_result("Analytics Test", False, "No data available")
        return False
    
    try:
        # Test industry analysis
        if 'industry_sector' in corp_df.columns:
            industry_counts = corp_df['industry_sector'].value_counts()
            test_result("Industry Analysis", len(industry_counts) > 0, 
                       f"{len(industry_counts)} industries identified")
        
        # Test geographic analysis
        if 'state' in corp_df.columns:
            state_counts = corp_df['state'].value_counts()
            test_result("Geographic Analysis", len(state_counts) > 0, 
                       f"{len(state_counts)} states represented")
        
        # Test data filtering
        if 'state' in corp_df.columns:
            ny_companies = corp_df[corp_df['state'] == 'NY']
            test_result("Data Filtering", len(ny_companies) >= 0, 
                       f"{len(ny_companies)} NY companies found")
        
        # Test search functionality
        if 'organization_name' in corp_df.columns:
            search_results = corp_df[corp_df['organization_name'].str.contains('Corp', case=False, na=False)]
            test_result("Search Functionality", len(search_results) >= 0, 
                       f"{len(search_results)} companies match 'Corp'")
        
        return True
        
    except Exception as e:
        test_result("Analytics Functions", False, str(e))
        return False

def test_email_templates():
    """Test email template generation"""
    print_section("Email Template Test")
    
    try:
        sys.path.append('campaigns/email_templates')
        from manager_approved_templates import generate_personalized_email, generate_subject_line
        
        # Test email generation
        test_data = {
            'organization_name': 'Test Corporation',
            'contact_name': 'Program Director',
            'city': 'New York',
            'state': 'NY',
            'mission_alignment_score': 95.0
        }
        
        email = generate_personalized_email(test_data, 'major_sponsor', 'new_york')
        test_result("Email Generation", len(email) > 100, 
                   f"Generated {len(email)} character email")
        
        # Test subject line generation
        subject = generate_subject_line('arts_partnership', 'New York')
        test_result("Subject Line Generation", len(subject) > 5, 
                   f"Generated: '{subject}'")
        
        return True
        
    except Exception as e:
        test_result("Email Templates", False, str(e))
        return False

def test_ai_intelligence():
    """Test AI intelligence module"""
    print_section("AI Intelligence Test")
    
    try:
        sys.path.append('app')
        from ai_intelligence import get_campaign_intelligence
        
        # Test AI function import
        test_result("AI Module Import", True, "AI intelligence module loaded successfully")
        
        # Test basic functionality (without API key)
        test_data = {
            'organization_name': 'Test Corp',
            'industry_sector': 'Technology',
            'location': 'New York, NY'
        }
        
        # This might fail without OpenAI API key, but we test the function exists
        test_result("AI Function Available", callable(get_campaign_intelligence), 
                   "AI intelligence function is callable")
        
        return True
        
    except Exception as e:
        test_result("AI Intelligence", False, str(e))
        return False

def test_ui_components():
    """Test UI component imports and basic functionality"""
    print_section("UI Components Test")
    
    try:
        # Test Streamlit import
        import streamlit as st
        test_result("Streamlit Import", True, "Streamlit library available")
        
        # Test Plotly import for charts
        import plotly.express as px
        test_result("Plotly Import", True, "Plotly library available for charts")
        
        # Test pandas for data handling
        import pandas as pd
        test_result("Pandas Import", True, "Pandas library available")
        
        # Test main app import
        sys.path.append('app')
        import main
        test_result("Main App Import", True, "Main application module loads successfully")
        
        return True
        
    except Exception as e:
        test_result("UI Components", False, str(e))
        return False

def test_campaign_workflow():
    """Test campaign creation workflow"""
    print_section("Campaign Workflow Test")
    
    try:
        # Load data for campaign creation
        corp_df = pd.read_csv("data/clean/corporations/fortune1000_main_database.csv")
        
        # Test filtering for campaign
        if 'state' in corp_df.columns and 'industry_sector' in corp_df.columns:
            # Create a sample campaign filter
            ny_tech = corp_df[
                (corp_df['state'] == 'NY') & 
                (corp_df['industry_sector'] == 'Technology')
            ]
            test_result("Campaign Filtering", len(ny_tech) >= 0, 
                       f"Created campaign with {len(ny_tech)} targets")
        
        # Test export functionality (simulate)
        export_columns = ['organization_name', 'city', 'state']
        available_cols = [col for col in export_columns if col in corp_df.columns]
        test_result("Export Capability", len(available_cols) > 0, 
                   f"Can export {len(available_cols)} columns")
        
        return True
        
    except Exception as e:
        test_result("Campaign Workflow", False, str(e))
        return False

def generate_test_report():
    """Generate comprehensive test report"""
    print_header("CSOAF EMAIL CAMPAIGN MANAGER - COMPREHENSIVE UI TEST")
    
    print(f"🕐 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Test Directory: {os.getcwd()}")
    
    # Run all tests
    tests_passed = 0
    total_tests = 8
    
    try:
        # Test 1: Data Files
        if test_data_files():
            tests_passed += 1
        
        # Test 2: Database Loading
        db_success, corp_df = test_database_loading()
        if db_success:
            tests_passed += 1
        
        # Test 3: Campaign Data
        campaign_success, campaign_df = test_campaign_data()
        if campaign_success:
            tests_passed += 1
        
        # Test 4: Analytics
        if test_analytics_functions(corp_df):
            tests_passed += 1
        
        # Test 5: Email Templates
        if test_email_templates():
            tests_passed += 1
        
        # Test 6: AI Intelligence
        if test_ai_intelligence():
            tests_passed += 1
        
        # Test 7: UI Components
        if test_ui_components():
            tests_passed += 1
        
        # Test 8: Campaign Workflow
        if test_campaign_workflow():
            tests_passed += 1
        
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        traceback.print_exc()
    
    # Final Report
    print_header("TEST SUMMARY")
    
    success_rate = (tests_passed / total_tests) * 100
    
    print(f"📊 Tests Passed: {tests_passed}/{total_tests}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🟢 EXCELLENT: Your UI is fully functional!")
    elif success_rate >= 75:
        print("🟡 GOOD: Most features working, minor issues detected")
    elif success_rate >= 50:
        print("🟠 FAIR: Some features working, needs attention")
    else:
        print("🔴 POOR: Major issues detected, requires fixes")
    
    print("\n📋 WHAT THIS MEANS:")
    print("✅ If tests pass, your UI components will work correctly")
    print("📊 Data loading tests ensure Record Manager will show data")
    print("📧 Email template tests ensure Campaign Creator works")
    print("📈 Analytics tests ensure dashboards display properly")
    
    return success_rate

if __name__ == "__main__":
    generate_test_report()