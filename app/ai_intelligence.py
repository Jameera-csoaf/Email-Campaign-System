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
    
    def generate_intelligent_template_suggestions(self, targeting_options: Dict) -> Dict:
        """
        🎯 Generate Smart Template & Subject Line Suggestions
        ====================================================
        Analyzes your targeting criteria and suggests the most effective 
        email templates and subject lines for maximum engagement.
        
        Args:
            targeting_options: Dictionary containing:
                - target_states: List of states
                - target_industries: List of industries  
                - min_sponsorship: Minimum sponsorship amount
                - campaign_description: Description of campaign
                - arts_interest: Level of arts education interest
        
        Returns:
            Dictionary with suggested templates and subject lines
        """
        
        # Extract targeting criteria
        industries = targeting_options.get('target_industries', [])
        states = targeting_options.get('target_states', [])
        min_sponsorship = targeting_options.get('min_sponsorship', 50000)
        description = targeting_options.get('campaign_description', '')
        arts_interest = targeting_options.get('arts_interest', ['High'])
        
        suggestions = {
            "recommended_templates": [],
            "subject_lines": [],
            "email_approaches": [],
            "personalization_tips": []
        }
        
        # 🎨 Template Selection Logic Based on Industry
        if any(industry in industries for industry in ['Technology', 'Financial Services', 'Consulting']):
            suggestions["recommended_templates"].append({
                "name": "Innovation Partnership",
                "description": "Emphasizes cutting-edge arts education and technology integration",
                "best_for": "Tech companies and financial services",
                "subject_template": "Innovation in Arts Education: Partnership with {organization_name}"
            })
            suggestions["subject_lines"].append("Transforming Education Through Arts & Technology Partnership")
            suggestions["email_approaches"].append("Focus on innovation, measurable outcomes, and competitive advantage")
        
        if any(industry in industries for industry in ['Healthcare', 'Education', 'Non-Profit']):
            suggestions["recommended_templates"].append({
                "name": "Community Impact Partnership", 
                "description": "Highlights community benefits and social responsibility",
                "best_for": "Healthcare, education, and mission-driven organizations",
                "subject_template": "Community Impact: {organization_name} x CSOAF Partnership"
            })
            suggestions["subject_lines"].append("Making a Difference: Arts Education Partnership Opportunity")
            suggestions["email_approaches"].append("Emphasize community impact, student outcomes, and shared values")
        
        if any(industry in industries for industry in ['Manufacturing', 'Energy', 'Retail']):
            suggestions["recommended_templates"].append({
                "name": "Workforce Development Partnership",
                "description": "Connects arts education to workforce development and employee engagement", 
                "best_for": "Large corporations with workforce development focus",
                "subject_template": "Workforce Development Through Arts: {organization_name} Partnership"
            })
            suggestions["subject_lines"].append("Building Tomorrow's Workforce Through Arts Education")
            suggestions["email_approaches"].append("Link arts education to creativity, problem-solving, and employee development")
        
        # 💰 Sponsorship Level Considerations
        if min_sponsorship >= 100000:
            suggestions["recommended_templates"].append({
                "name": "Premium Strategic Alliance",
                "description": "High-value partnership with executive-level positioning",
                "best_for": "Major sponsorship opportunities ($100K+)",
                "subject_template": "Strategic Alliance Opportunity: {organization_name} Leadership"
            })
            suggestions["subject_lines"].append("Exclusive Partnership: CSOAF Strategic Alliance Invitation")
            suggestions["personalization_tips"].append("Target C-suite executives and decision makers")
            suggestions["email_approaches"].append("Focus on strategic value, brand alignment, and exclusive benefits")
        
        elif min_sponsorship >= 50000:
            suggestions["recommended_templates"].append({
                "name": "Professional Partnership",
                "description": "Mid-tier professional engagement with concrete benefits",
                "best_for": "Standard corporate partnerships ($50K-$100K)",
                "subject_template": "Partnership Opportunity: {organization_name} & CSOAF"
            })
            suggestions["subject_lines"].append("Professional Partnership: Arts Education Initiative")
            suggestions["personalization_tips"].append("Target department heads and senior managers")
        
        else:
            suggestions["recommended_templates"].append({
                "name": "Community Engagement",
                "description": "Accessible partnership focusing on local community impact",
                "best_for": "Smaller partnerships and local engagement",
                "subject_template": "Community Partnership: {organization_name} & Local Arts"
            })
            suggestions["subject_lines"].append("Community Arts Education Partnership")
            suggestions["personalization_tips"].append("Target community relations and local managers")
        
        # 🗺️ Geographic Personalization
        if any(state in states for state in ['CA', 'NY', 'WA']):
            suggestions["subject_lines"].append("West Coast Arts Innovation Partnership")
            suggestions["personalization_tips"].append("Emphasize innovation, creativity, and progressive values")
        
        if any(state in states for state in ['TX', 'FL', 'AZ']):
            suggestions["subject_lines"].append("Expanding Arts Education Across Growing Markets")
            suggestions["personalization_tips"].append("Focus on growth, opportunity, and market expansion")
        
        # 🎭 Arts Interest Level Adaptations
        if 'High' in arts_interest:
            suggestions["email_approaches"].append("Lead with arts passion and detailed program benefits")
            suggestions["subject_lines"].append("Exclusive Arts Education Partnership for Arts Advocates")
        elif 'Medium' in arts_interest:
            suggestions["email_approaches"].append("Balance arts benefits with broader educational and business value")
            suggestions["subject_lines"].append("Education Partnership with Strong Arts Component")
        else:
            suggestions["email_approaches"].append("Focus on business value, workforce development, and general education benefits")
            suggestions["subject_lines"].append("Strategic Education Partnership Opportunity")
        
        # 📝 Campaign Description Analysis
        if description:
            description_lower = description.lower()
            if any(word in description_lower for word in ['innovation', 'technology', 'digital', 'modern']):
                suggestions["subject_lines"].append("Innovation-Driven Arts Education Partnership")
                suggestions["email_approaches"].append("Emphasize cutting-edge educational technology and modern teaching methods")
            
            if any(word in description_lower for word in ['community', 'local', 'neighborhood', 'region']):
                suggestions["subject_lines"].append("Strengthening Our Community Through Arts Education")
                suggestions["email_approaches"].append("Focus on local community impact and regional development")
            
            if any(word in description_lower for word in ['equity', 'inclusion', 'diversity', 'access']):
                suggestions["subject_lines"].append("Expanding Access to Quality Arts Education")
                suggestions["email_approaches"].append("Highlight equity, inclusion, and expanding educational access")
        
        # 🏆 Add general best practices
        suggestions["personalization_tips"].extend([
            "Research recent company news and initiatives",
            "Reference specific company values or mission alignment",
            "Include relevant local or industry statistics",
            "Mention specific arts programs that align with company interests"
        ])
        
        # Limit to top 5 suggestions for each category
        for key in suggestions:
            if isinstance(suggestions[key], list) and len(suggestions[key]) > 5:
                suggestions[key] = suggestions[key][:5]
        
        return suggestions

def get_campaign_intelligence():
    """Get campaign intelligence instance"""
    if 'campaign_ai' not in st.session_state:
        st.session_state.campaign_ai = CampaignIntelligence()
    return st.session_state.campaign_ai