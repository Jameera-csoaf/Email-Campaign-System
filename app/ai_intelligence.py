#!/usr/bin/env python3
"""
🤖 Your AI Campaign Writing Assistant
===================================
Think of this as your personal fundraising copywriter who never gets tired
and always knows the right thing to say to potential sponsors.

This AI helper can:
- Turn your ideas into professional email campaigns
- Understand what you want even when you describe it casually
- Suggest the best companies to contact
- Write compelling subject lines and email content
- Learn from successful campaigns to get better over time
"""

import openai  # The AI brain that understands language
import os      # For reading environment settings
import json    # For handling data files
import re      # For text pattern matching
from typing import Dict, List, Any  # Type hints to keep code clean
import streamlit as st  # For displaying messages to users

class CampaignIntelligence:
    """
    🧠 The Smart Campaign Assistant
    ==============================
    This is like having a fundraising expert who knows:
    - What words work best for different industries
    - Which companies are most likely to respond
    - How to write emails that get opened and read
    - What sponsorship levels make sense for different organizations
    """
    
    def __init__(self):
        """
        🔧 Setting Up Your AI Assistant
        ==============================
        This runs when you first start the AI - it's like waking up your
        assistant and making sure they have access to all their tools.
        """
        # Check if we can connect to OpenAI (the AI service)
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # 📚 Knowledge Base: Categories that help the AI understand your requests
        # Think of these as the AI's "cheat sheets" for different types of organizations
        
        # Industry keywords - helps AI identify what type of companies you want
        self.industry_keywords = {
            'Technology': ['tech', 'software', 'IT', 'digital', 'startup', 'innovation', 'AI', 'machine learning', 'blockchain', 'cybersecurity'],
            'Financial Services': ['bank', 'finance', 'investment', 'insurance', 'lending', 'capital', 'wealth', 'trading'],
            'Healthcare': ['health', 'medical', 'hospital', 'pharmaceutical', 'biotech', 'wellness', 'care'],
            'Manufacturing': ['manufacturing', 'factory', 'production', 'industrial', 'automotive', 'aerospace'],
            'Energy': ['energy', 'oil', 'gas', 'renewable', 'solar', 'wind', 'electric', 'utility'],
            'Retail': ['retail', 'shopping', 'consumer', 'merchandise', 'store', 'ecommerce', 'brand'],
            'Education': ['education', 'school', 'university', 'learning', 'academic', 'student'],
            'Entertainment': ['entertainment', 'media', 'film', 'music', 'gaming', 'sports', 'arts']
        }
        
        # Location keywords - helps AI understand geographic preferences
        self.location_keywords = {
            'NY': ['new york', 'nyc', 'manhattan', 'brooklyn', 'queens'],
            'CA': ['california', 'san francisco', 'los angeles', 'silicon valley', 'bay area'],
            'TX': ['texas', 'houston', 'dallas', 'austin', 'san antonio'],
            'FL': ['florida', 'miami', 'orlando', 'tampa', 'jacksonville'],
            'IL': ['illinois', 'chicago'],
            'PA': ['pennsylvania', 'philadelphia', 'pittsburgh'],
            'OH': ['ohio', 'cleveland', 'columbus', 'cincinnati'],
            'GA': ['georgia', 'atlanta'],
            'NC': ['north carolina', 'charlotte', 'raleigh'],
            'MI': ['michigan', 'detroit']
        }
        
        # Sponsorship level keywords - helps AI understand budget expectations
        self.sponsorship_keywords = {
            'high': ['major', 'large', 'premium', 'substantial', 'significant', 'big', 'top tier'],
            'medium': ['medium', 'moderate', 'standard', 'regular', 'mid-level'],
            'low': ['small', 'minimal', 'basic', 'entry', 'starter']
        }
        
        self.arts_keywords = {
            'high': ['arts', 'creative', 'cultural', 'artistic', 'music', 'theater', 'dance', 'visual arts', 'education'],
            'medium': ['community', 'youth', 'learning', 'development'],
            'low': ['general', 'broad', 'diverse']
        }
    
    def extract_keywords_with_ai(self, user_input: str) -> Dict[str, Any]:
        """Use OpenAI to extract campaign parameters from natural language"""
        
        if not self.openai_api_key:
            return self.extract_keywords_basic(user_input)
        
        try:
            prompt = f"""
            Analyze this campaign description and extract relevant parameters:
            
            "{user_input}"
            
            Please identify and return a JSON object with:
            1. Industries mentioned (Technology, Financial Services, Healthcare, Manufacturing, Energy, Retail, Education, Entertainment)
            2. Locations/States mentioned (use state abbreviations like NY, CA, TX, etc.)
            3. Sponsorship level (high/medium/low based on budget mentions or company size)
            4. Arts education interest level (high/medium/low)
            5. Campaign type (Sponsorship Request, Event Invitation, Partnership Proposal, Thank You, Follow-up)
            6. Target company characteristics
            7. Minimum sponsorship amount (if mentioned)
            
            Return only valid JSON format:
            {{
                "industries": ["list of relevant industries"],
                "states": ["list of state abbreviations"],
                "sponsorship_level": "high/medium/low",
                "arts_interest": ["High", "Medium", "Low"],
                "campaign_type": "campaign type",
                "min_sponsorship": number or null,
                "characteristics": ["list of key characteristics"]
            }}
            """
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                extracted = json.loads(result)
                return extracted
            except json.JSONDecodeError:
                # Fallback to basic extraction
                return self.extract_keywords_basic(user_input)
                
        except Exception as e:
            st.warning(f"AI extraction unavailable: {e}")
            return self.extract_keywords_basic(user_input)
    
    def extract_keywords_basic(self, user_input: str) -> Dict[str, Any]:
        """Basic keyword extraction without AI"""
        
        user_lower = user_input.lower()
        
        # Extract industries
        industries = []
        for industry, keywords in self.industry_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                industries.append(industry)
        
        # Extract locations
        states = []
        for state, keywords in self.location_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                states.append(state)
        
        # Extract sponsorship level
        sponsorship_level = "medium"  # default
        for level, keywords in self.sponsorship_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                sponsorship_level = level
                break
        
        # Extract arts interest
        arts_interest = ["Medium"]  # default
        for level, keywords in self.arts_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                arts_interest = [level.title()]
                break
        
        # Extract sponsorship amount
        min_sponsorship = None
        amount_match = re.search(r'\$?([\d,]+)k?', user_input)
        if amount_match:
            amount = amount_match.group(1).replace(',', '')
            if 'k' in user_input.lower():
                min_sponsorship = int(amount) * 1000
            else:
                min_sponsorship = int(amount)
        
        # Determine campaign type
        campaign_type = "Sponsorship Request"  # default
        if any(word in user_lower for word in ['event', 'gala', 'invitation']):
            campaign_type = "Event Invitation"
        elif any(word in user_lower for word in ['partnership', 'collaborate']):
            campaign_type = "Partnership Proposal"
        elif any(word in user_lower for word in ['thank', 'appreciation']):
            campaign_type = "Thank You"
        
        return {
            "industries": industries,
            "states": states,
            "sponsorship_level": sponsorship_level,
            "arts_interest": arts_interest,
            "campaign_type": campaign_type,
            "min_sponsorship": min_sponsorship,
            "characteristics": []
        }
    
    def generate_campaign_suggestions(self, extracted_params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate campaign suggestions based on extracted parameters"""
        
        suggestions = {
            "subject_line": "",
            "campaign_focus": "",
            "key_messages": [],
            "call_to_action": ""
        }
        
        # Generate subject line
        if extracted_params.get("campaign_type") == "Event Invitation":
            suggestions["subject_line"] = "Exclusive Arts Education Partnership - {organization_name}"
        elif extracted_params.get("campaign_type") == "Partnership Proposal":
            suggestions["subject_line"] = "Strategic Partnership Opportunity: CSOAF x {organization_name}"
        else:
            suggestions["subject_line"] = "Arts Education Sponsorship: {organization_name} Partnership"
        
        # Generate campaign focus
        industries = extracted_params.get("industries", [])
        if industries:
            suggestions["campaign_focus"] = f"Targeting {', '.join(industries)} companies for arts education partnerships"
        else:
            suggestions["campaign_focus"] = "Broad outreach for arts education sponsorship opportunities"
        
        # Generate key messages
        if "Technology" in industries:
            suggestions["key_messages"].append("STEM + Arts integration opportunities")
            suggestions["key_messages"].append("Digital innovation in arts education")
        
        if "Financial Services" in industries:
            suggestions["key_messages"].append("Community investment and social impact")
            suggestions["key_messages"].append("Financial literacy through arts programs")
        
        if extracted_params.get("sponsorship_level") == "high":
            suggestions["key_messages"].append("Premium partnership opportunities")
            suggestions["key_messages"].append("Executive board recognition")
        
        # Generate call to action
        suggestions["call_to_action"] = "Schedule a 15-minute call to explore partnership opportunities"
        
        return suggestions
    
    def estimate_campaign_reach(self, extracted_params: Dict[str, Any], database_df) -> Dict[str, int]:
        """Estimate campaign reach based on parameters"""
        
        try:
            filtered_df = database_df.copy()
            
            # Apply industry filter
            if extracted_params.get("industries"):
                filtered_df = filtered_df[filtered_df['industry_sector'].isin(extracted_params["industries"])]
            
            # Apply state filter
            if extracted_params.get("states"):
                filtered_df = filtered_df[filtered_df['state'].isin(extracted_params["states"])]
            
            # Apply sponsorship filter
            if extracted_params.get("min_sponsorship"):
                filtered_df = filtered_df[filtered_df['estimated_typical_sponsorship'] >= extracted_params["min_sponsorship"]]
            
            # Apply arts interest filter
            if extracted_params.get("arts_interest"):
                filtered_df = filtered_df[filtered_df['arts_education_potential'].isin(extracted_params["arts_interest"])]
            
            return {
                "total_matches": len(filtered_df),
                "high_value": len(filtered_df[filtered_df['estimated_typical_sponsorship'] >= 100000]),
                "total_potential": int(filtered_df['estimated_typical_sponsorship'].sum()),
                "avg_potential": int(filtered_df['estimated_typical_sponsorship'].mean()) if len(filtered_df) > 0 else 0
            }
            
        except Exception as e:
            return {"total_matches": 0, "high_value": 0, "total_potential": 0, "avg_potential": 0}

def get_campaign_intelligence():
    """Get campaign intelligence instance"""
    if 'campaign_ai' not in st.session_state:
        st.session_state.campaign_ai = CampaignIntelligence()
    return st.session_state.campaign_ai