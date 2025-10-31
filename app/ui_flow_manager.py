#!/usr/bin/env python3
"""
🎯 Comprehensive UI Flow Validation & Fix System
===============================================
This ensures the entire UI works with proper features and functionality flow.
"""

import streamlit as st
import os
import sys

class UIFlowManager:
    """
    🔄 Comprehensive UI Flow Management
    ==================================
    Ensures proper navigation, state management, and data flow throughout the UI.
    """
    
    def __init__(self):
        self.flow_steps = [
            'dashboard',
            'campaign_creator', 
            'ai_enhancement',
            'template_editor',
            'record_manager',
            'approval_center',
            'send_campaign',
            'analytics'
        ]
        
        # Initialize flow state
        self.init_flow_state()
    
    def init_flow_state(self):
        """Initialize comprehensive flow state management"""
        if 'ui_flow_state' not in st.session_state:
            st.session_state.ui_flow_state = {
                'current_page': 'dashboard',
                'navigation_history': [],
                'button_clicks': {},
                'form_submissions': {},
                'data_flow': {},
                'validation_status': {},
                'flow_errors': []
            }
    
    def handle_navigation(self, target_page: str, trigger: str = 'manual'):
        """
        Handle all navigation with proper state management
        
        Args:
            target_page: The page to navigate to
            trigger: How navigation was triggered (button, selectbox, form, etc.)
        """
        flow_state = st.session_state.ui_flow_state
        
        # Record navigation
        flow_state['navigation_history'].append({
            'from': flow_state['current_page'],
            'to': target_page,
            'trigger': trigger,
            'timestamp': st.session_state.get('timestamp', 'unknown')
        })
        
        # Update current page
        flow_state['current_page'] = target_page
        
        # Log for debugging
        st.write(f"🔄 Navigation: {target_page} (via {trigger})")
    
    def handle_button_click(self, button_id: str, action: str, target_page: str = None):
        """Handle button clicks with proper state management"""
        flow_state = st.session_state.ui_flow_state
        
        # Record button click
        flow_state['button_clicks'][button_id] = {
            'action': action,
            'target_page': target_page,
            'timestamp': st.session_state.get('timestamp', 'unknown')
        }
        
        # Navigate if target specified
        if target_page:
            self.handle_navigation(target_page, f'button:{button_id}')
        
        # Force page update
        if target_page:
            st.session_state.force_page = target_page
    
    def handle_form_submission(self, form_id: str, form_data: dict, next_step: str = None):
        """Handle form submissions with data flow validation"""
        flow_state = st.session_state.ui_flow_state
        
        # Record form submission
        flow_state['form_submissions'][form_id] = {
            'data': form_data,
            'next_step': next_step,
            'timestamp': st.session_state.get('timestamp', 'unknown')
        }
        
        # Store data for next step
        if next_step:
            flow_state['data_flow'][next_step] = form_data
        
        # Navigate to next step
        if next_step:
            self.handle_navigation(next_step, f'form:{form_id}')
    
    def validate_flow_integrity(self):
        """Validate the entire UI flow integrity"""
        flow_state = st.session_state.ui_flow_state
        
        issues = []
        
        # Check navigation consistency
        if not flow_state.get('current_page'):
            issues.append("No current page set")
        
        # Check data flow
        for step in self.flow_steps[1:]:  # Skip dashboard
            if step in flow_state.get('navigation_history', []):
                prev_step_idx = self.flow_steps.index(step) - 1
                prev_step = self.flow_steps[prev_step_idx]
                
                if step not in flow_state.get('data_flow', {}):
                    issues.append(f"Missing data flow from {prev_step} to {step}")
        
        flow_state['validation_status'] = {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'timestamp': st.session_state.get('timestamp', 'unknown')
        }
        
        return len(issues) == 0, issues

def create_enhanced_navigation_system():
    """Create an enhanced navigation system that actually works"""
    
    # Initialize flow manager
    flow_manager = UIFlowManager()
    
    # Navigation section with proper state management
    st.sidebar.markdown("## 🎯 Enhanced Navigation")
    
    # Get current page from flow state or session state
    current_page = st.session_state.get('force_page') or \
                   st.session_state.ui_flow_state.get('current_page', 'dashboard')
    
    # Clear forced page after use
    if 'force_page' in st.session_state:
        del st.session_state.force_page
    
    navigation_options = [
        "📊 Dashboard",
        "🚀 Campaign Creator", 
        "🤖 AI Enhancement",
        "📝 Template Editor",
        "📋 Record Manager",
        "✅ Approval Center",
        "📧 Send Campaign",
        "📈 Analytics"
    ]
    
    # Map page names to navigation options
    page_mapping = {
        'dashboard': "📊 Dashboard",
        'campaign_creator': "🚀 Campaign Creator",
        'ai_enhancement': "🤖 AI Enhancement",
        'template_editor': "📝 Template Editor",
        'record_manager': "📋 Record Manager",
        'approval_center': "✅ Approval Center",
        'send_campaign': "📧 Send Campaign",
        'analytics': "📈 Analytics"
    }
    
    # Get current index
    current_option = page_mapping.get(current_page, "📊 Dashboard")
    current_index = navigation_options.index(current_option) if current_option in navigation_options else 0
    
    # Navigation selectbox
    selected_option = st.sidebar.selectbox(
        "Choose your step:",
        navigation_options,
        index=current_index,
        key="enhanced_navigation"
    )
    
    # Convert back to page id
    reverse_mapping = {v: k for k, v in page_mapping.items()}
    selected_page = reverse_mapping.get(selected_option, 'dashboard')
    
    # Update flow state
    if selected_page != current_page:
        flow_manager.handle_navigation(selected_page, 'selectbox')
    
    return selected_page, flow_manager

def create_enhanced_dashboard_button():
    """Create an enhanced dashboard button that actually works"""
    
    st.markdown("### 🚀 Start New Campaign")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🎯 Create New Campaign", type="primary", use_container_width=True, key="enhanced_create_campaign"):
            # Multiple strategies to ensure navigation works
            
            # Strategy 1: Session state
            st.session_state.force_page = 'campaign_creator'
            
            # Strategy 2: Direct workflow advancement
            if 'workflow_state' in st.session_state:
                st.session_state.workflow_state['current_step'] = 'campaign_creator'
            
            # Strategy 3: UI flow state
            if 'ui_flow_state' in st.session_state:
                st.session_state.ui_flow_state['current_page'] = 'campaign_creator'
                st.session_state.ui_flow_state['button_clicks']['create_campaign'] = {
                    'target': 'campaign_creator',
                    'timestamp': 'now'
                }
            
            # Strategy 4: Success feedback
            st.success("✅ Navigating to Campaign Creator...")
            
            # Strategy 5: Force rerun
            st.rerun()

# Export functions for use in main app
__all__ = ['UIFlowManager', 'create_enhanced_navigation_system', 'create_enhanced_dashboard_button']