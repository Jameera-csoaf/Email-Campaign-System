#!/usr/bin/env python3
"""
🔄 Campaign Workflow System
==========================
Manages the interconnected flow between all campaign management steps.
Each step takes output from the previous step as input.

Workflow: Dashboard → Campaign Creator → AI Enhancement → Template Editor → 
         Record Manager → Approval Center → Send Campaign → Analytics
"""

import streamlit as st
from typing import Dict, Any, List
import json
from datetime import datetime

class CampaignWorkflow:
    """
    🔄 Campaign Workflow Manager
    ===========================
    Manages the complete campaign lifecycle with interconnected steps.
    """
    
    def __init__(self):
        self.workflow_steps = [
            "dashboard",
            "campaign_creator", 
            "ai_enhancement",
            "template_editor",
            "record_manager",
            "approval_center",
            "send_campaign",
            "analytics"
        ]
        
        # Initialize workflow state if not exists
        if 'workflow_state' not in st.session_state:
            self.initialize_workflow()
    
    def initialize_workflow(self):
        """Initialize the workflow state in session"""
        st.session_state.workflow_state = {
            'current_step': 'dashboard',
            'campaign_data': {},
            'step_outputs': {},
            'workflow_id': f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'step_history': [],
            'completed_steps': set(),
            'validation_status': {}
        }
    
    def get_current_step(self) -> str:
        """Get the current workflow step"""
        return st.session_state.workflow_state.get('current_step', 'dashboard')
    
    def set_current_step(self, step: str):
        """Set the current step without advancing (for navigation only)"""
        st.session_state.workflow_state['current_step'] = step
    
    def advance_to_step(self, step: str, output_data: Dict = None):
        """
        Advance workflow to the next step with output data
        
        Args:
            step: The step to advance to
            output_data: Data to pass to the next step
        """
        current_step = self.get_current_step()
        
        # Store output from current step
        if output_data:
            st.session_state.workflow_state['step_outputs'][current_step] = output_data
            
            # Update campaign data with new information
            if 'campaign_data' in output_data:
                st.session_state.workflow_state['campaign_data'].update(output_data['campaign_data'])
        
        # Mark current step as completed
        st.session_state.workflow_state['completed_steps'].add(current_step)
        
        # Record step transition
        st.session_state.workflow_state['step_history'].append({
            'from_step': current_step,
            'to_step': step,
            'timestamp': datetime.now().isoformat(),
            'data_size': len(str(output_data)) if output_data else 0
        })
        
        # Advance to new step
        st.session_state.workflow_state['current_step'] = step
    
    def get_step_input(self, step: str) -> Dict:
        """Get input data for a specific step from previous step outputs"""
        if step == 'dashboard':
            return {}
        
        step_index = self.workflow_steps.index(step)
        if step_index == 0:
            return {}
        
        previous_step = self.workflow_steps[step_index - 1]
        return st.session_state.workflow_state['step_outputs'].get(previous_step, {})
    
    def get_campaign_data(self) -> Dict:
        """Get the current campaign data accumulated through the workflow"""
        return st.session_state.workflow_state.get('campaign_data', {})
    
    def update_campaign_data(self, updates: Dict):
        """Update campaign data with new information"""
        if 'campaign_data' not in st.session_state.workflow_state:
            st.session_state.workflow_state['campaign_data'] = {}
        
        st.session_state.workflow_state['campaign_data'].update(updates)
    
    def validate_step_requirements(self, step: str) -> tuple[bool, List[str]]:
        """
        Validate if a step has all required input data
        
        Returns:
            (is_valid, missing_requirements)
        """
        requirements = self.get_step_requirements(step)
        campaign_data = self.get_campaign_data()
        
        missing = []
        for req in requirements:
            if req not in campaign_data or not campaign_data[req]:
                missing.append(req)
        
        return len(missing) == 0, missing
    
    def get_step_requirements(self, step: str) -> List[str]:
        """Get required data fields for each step"""
        requirements_map = {
            'dashboard': [],
            'campaign_creator': [],
            'ai_enhancement': ['campaign_name', 'campaign_description'],
            'template_editor': ['campaign_name', 'campaign_description'],
            'record_manager': ['campaign_name', 'campaign_description'],
            'approval_center': ['campaign_name', 'campaign_description'],
            'send_campaign': ['campaign_name', 'campaign_description'],
            'analytics': ['campaign_name']
        }
        
        return requirements_map.get(step, [])
    
    def can_access_step(self, step: str) -> bool:
        """Check if a step can be accessed based on completed steps"""
        if step == 'dashboard':
            return True
        
        step_index = self.workflow_steps.index(step)
        if step_index == 0:
            return True
        
        # Allow access to current step and next step
        current_step = self.get_current_step()
        current_index = self.workflow_steps.index(current_step) if current_step in self.workflow_steps else 0
        
        # Can access current step, previous completed steps, or immediate next step
        if step == current_step:
            return True
        elif step_index <= current_index + 1:  # Allow access to next step
            return True
        else:
            # Check if previous step is completed for steps further ahead
            previous_step = self.workflow_steps[step_index - 1]
            return previous_step in st.session_state.workflow_state.get('completed_steps', set())
    
    def get_workflow_progress(self) -> Dict:
        """Get workflow progress information"""
        completed = st.session_state.workflow_state.get('completed_steps', set())
        current = self.get_current_step()
        
        progress_info = {
            'total_steps': len(self.workflow_steps),
            'completed_count': len(completed),
            'current_step': current,
            'current_step_index': self.workflow_steps.index(current),
            'progress_percentage': (len(completed) / len(self.workflow_steps)) * 100,
            'next_step': self.get_next_step(),
            'can_proceed': self.can_proceed_to_next()
        }
        
        return progress_info
    
    def get_next_step(self) -> str:
        """Get the next step in the workflow"""
        current = self.get_current_step()
        current_index = self.workflow_steps.index(current)
        
        if current_index < len(self.workflow_steps) - 1:
            return self.workflow_steps[current_index + 1]
        
        return current  # Last step
    
    def can_proceed_to_next(self) -> bool:
        """Check if workflow can proceed to next step"""
        current_step = self.get_current_step()
        is_valid, _ = self.validate_step_requirements(current_step)
        return is_valid
    
    def reset_workflow(self):
        """Reset the workflow to start from beginning"""
        self.initialize_workflow()
    
    def export_workflow_data(self) -> Dict:
        """Export complete workflow data for backup/analysis"""
        return {
            'workflow_state': st.session_state.workflow_state,
            'export_timestamp': datetime.now().isoformat(),
            'workflow_version': '1.0'
        }

def show_workflow_progress_bar():
    """Display a visual progress bar for the workflow"""
    if 'workflow' not in st.session_state:
        st.session_state.workflow = CampaignWorkflow()
    
    workflow = st.session_state.workflow
    progress_info = workflow.get_workflow_progress()
    
    # Progress bar
    progress_col1, progress_col2 = st.columns([4, 1])
    
    with progress_col1:
        st.progress(progress_info['progress_percentage'] / 100, 
                   text=f"Step {progress_info['current_step_index'] + 1} of {progress_info['total_steps']}: {progress_info['current_step'].replace('_', ' ').title()}")
    
    with progress_col2:
        st.metric("Progress", f"{progress_info['completed_count']}/{progress_info['total_steps']}")
    
    # Step indicators
    step_cols = st.columns(len(workflow.workflow_steps))
    
    for i, step in enumerate(workflow.workflow_steps):
        with step_cols[i]:
            if step in st.session_state.workflow_state.get('completed_steps', set()):
                st.success(f"✅ {step.replace('_', ' ').title()}")
            elif step == progress_info['current_step']:
                st.info(f"🔄 {step.replace('_', ' ').title()}")
            else:
                st.secondary_container = st.container()
                with st.secondary_container:
                    if workflow.can_access_step(step):
                        st.warning(f"⏳ {step.replace('_', ' ').title()}")
                    else:
                        st.error(f"🔒 {step.replace('_', ' ').title()}")

def show_step_navigation():
    """Show navigation controls for the workflow"""
    if 'workflow' not in st.session_state:
        st.session_state.workflow = CampaignWorkflow()
    
    workflow = st.session_state.workflow
    progress_info = workflow.get_workflow_progress()
    
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 1])
    
    with nav_col1:
        if st.button("🏠 Dashboard", help="Go to Dashboard"):
            workflow.advance_to_step('dashboard')
            st.rerun()
    
    with nav_col2:
        current_index = progress_info['current_step_index']
        if current_index > 0:
            prev_step = workflow.workflow_steps[current_index - 1]
            if st.button(f"⬅️ Back to {prev_step.replace('_', ' ').title()}", help=f"Return to {prev_step}"):
                st.session_state.workflow_state['current_step'] = prev_step
                st.rerun()
    
    with nav_col3:
        if progress_info['can_proceed'] and progress_info['next_step'] != progress_info['current_step']:
            if st.button(f"➡️ Next: {progress_info['next_step'].replace('_', ' ').title()}", 
                        type="primary", help=f"Proceed to {progress_info['next_step']}"):
                workflow.advance_to_step(progress_info['next_step'])
                st.rerun()
        else:
            if not progress_info['can_proceed']:
                st.button("❌ Complete Current Step", disabled=True, 
                         help="Complete required fields in current step to proceed")
    
    with nav_col4:
        if st.button("🔄 Reset Workflow", help="Start over from beginning"):
            workflow.reset_workflow()
            st.rerun()

def get_workflow_manager():
    """Get or create the workflow manager instance"""
    if 'workflow' not in st.session_state:
        st.session_state.workflow = CampaignWorkflow()
    
    return st.session_state.workflow