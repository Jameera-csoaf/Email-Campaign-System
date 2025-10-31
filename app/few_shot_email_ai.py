#!/usr/bin/env python3
"""
🤖 Few-Shot Learning Email Template AI
====================================
Uses your proven email templates as examples to generate new, 
personalized emails that follow the same successful patterns.

This AI learns from your best-performing templates and creates
new emails that maintain the same tone, structure, and effectiveness.
"""

import openai
import os
import re
from typing import Dict, List, Any
import streamlit as st

class FewShotEmailAI:
    """
    🧠 Few-Shot Learning Email Generator
    ===================================
    Uses your existing successful email templates as training examples
    to generate new, personalized emails that follow proven patterns.
    """
    
    def __init__(self):
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Your proven email templates (few-shot examples)
        self.email_examples = self._load_proven_templates()
        
    def _load_proven_templates(self) -> List[Dict]:
        """Load your successful email templates as few-shot examples"""
        
        return [
            {
                "category": "Premium Partnership",
                "context": "Major corporate sponsor, technology industry, high sponsorship level ($25,000+), New York location",
                "template": {
                    "subject": "Exclusive Partnership: {organization_name} x CSOAF Arts Initiative",
                    "body": """Dear {contact_name},

As a distinguished leader at {organization_name}, you understand the profound impact that strategic community investments can have on both social good and business outcomes.

At the Community School of the Arts Foundation (CSOAF), we're pioneering a new approach to arts education that aligns perfectly with your company's forward-thinking vision. Our programs integrate cutting-edge technology with creative expression, developing the kind of innovative thinking that drives business success.

🌟 Exclusive Partnership Opportunity
We're inviting {organization_name} to join an exclusive circle of visionary partners who are transforming communities through arts education.

Given your organization's commitment to innovation, you're uniquely positioned to make a transformative impact in our community.

📊 Proven Impact:
• Students show 40% improvement in academic performance
• 95% graduation rates in our programs
• Enhanced workforce development through creativity and innovation
• Extensive community recognition and positive brand association

🎯 Strategic Partnership Tiers:
🥇 Platinum Partner ($50,000+): Program naming rights, executive board seat, premium event access
🥈 Gold Partner ($25,000+): Scholarship fund establishment, quarterly impact reports, VIP events
🥉 Silver Partner ($10,000+): Workshop sponsorship, bi-annual meetings, community recognition

Ready to Make a Transformative Impact?
Let's schedule a personalized presentation to explore how {organization_name} can become a cornerstone partner in our mission.

Thank you for your commitment to community excellence. I look forward to discussing how we can create lasting impact together.

Best regards,
{sender_name}
Partnership Development Director
Community School of the Arts Foundation"""
                }
            },
            
            {
                "category": "Community Partnership",
                "context": "Healthcare/community focus organization, medium sponsorship level ($10,000-$50,000), community impact emphasis",
                "template": {
                    "subject": "Partner with Us to Bring Arts Education to Local Schools",
                    "body": """Dear {contact_name},

I hope this message finds you well.

The Community School of the Arts Foundation (CSOAF) is reaching out to invite your organization to become a sponsor in support of implementing our arts curriculum at local schools.

Our mission is to make high-quality arts education accessible to every child, especially in underserved public schools. Your sponsorship will help us deliver a comprehensive arts curriculum that includes visual arts, dance, music, and theater, giving students the opportunity to explore creativity, build confidence, and express their unique voices.

We noticed your organization's commitment to supporting community health and wellbeing, which aligns perfectly with our inclusive arts programs designed to serve students of all abilities.

As a valued partner, your organization will:
• Help us implement and sustain the arts curriculum at local public schools
• Receive recognition on school materials, program flyers, and social media campaigns
• Be associated with a trusted 501(c)(3) nonprofit that has provided arts programs across New York public schools since 2003
• Gain positive community visibility through direct engagement with students, teachers, and families

Partnership benefits include:
• Quarterly impact reports showing student progress
• Invitation to student showcase performances
• Recognition in our annual report and website
• Tax-deductible contribution with full documentation

Thank you for your consideration. I would love to discuss this opportunity with you further and answer any questions you may have.

Best regards,
{sender_name}
Community Partnership Coordinator
Community School of the Arts Foundation"""
                }
            },
            
            {
                "category": "Event Invitation",
                "context": "Healing arts event, individual tickets, community fundraiser, intimate setting",
                "template": {
                    "subject": "Healing Through Arts: NYC Schools - Join Us Nov 18th",
                    "body": """Hi {contact_name},

We're excited to invite you to join us as a sponsor of Healing Through Arts: NYC Schools, an unforgettable evening where art, music, and community come together to create lasting impact for NYC students.

🎯 Mission Connection: We've identified a strong alignment between your organization's focus on community support and our commitment to accessible arts education for NYC students with disabilities and diverse learning needs.

Why sponsor this event?

Direct community impact: Every sponsorship dollar funds arts healing programs in underserved NYC schools, particularly supporting students with disabilities through creative educational pathways.

Exclusive engagement: Connect with city leaders, artists, and philanthropists at a vibrant evening of performances, wine tasting, and conversations.

🎭 Healing Through Arts: NYC Schools Benefit
📅 Monday, November 18, 2025 | 7:00 PM – 9:00 PM (doors open 6:30 PM)
📍 Rake Wine Bar (45 1st Ave, NYC)
🎟️ $35 per ticket
✨ Arts displays & live performances
🥂 Wine tasting & hors d'oeuvres
🤝 Meet fellow changemakers

Every ticket funds arts healing programs—attend to see how you can support further.

👉 [Get Your Ticket]

Corporate sponsors: Companies can also support, attend to learn more.

With gratitude,
{sender_name}
Community School of Arts Foundation"""
                }
            },
            
            {
                "category": "Gala Invitation",
                "context": "Gala invitation, formal event, corporate table sales, annual fundraiser",
                "template": {
                    "subject": "You're Invited: CSOAF Annual Arts Gala",
                    "body": """Dear {contact_name},

You are cordially invited to join us for an extraordinary evening celebrating the transformative power of arts education in our community.

🎭 Annual Arts Gala
A Night of Inspiration & Impact
Community School of the Arts Foundation

📅 Event Details:
Date: November 15, 2025
Time: 6:00 PM - 10:00 PM
Venue: Metropolitan Arts Center
Dress Code: Cocktail Attire

This year's gala will feature:
🎵 Performances by our talented students
🍷 Cocktail reception and gourmet dinner
🎨 Silent auction featuring local artist works
🏆 Recognition of community champions
💝 Inspiring stories of student transformation

As a valued member of our business community, {organization_name} embodies the spirit of giving that makes events like this possible.

Reserve Your Table Today
Individual tickets: $150 | Corporate table (10 guests): $1,200

We hope to see you there as we celebrate another year of changing lives through arts education.

With warm regards,
{sender_name}
Event Coordination Team
Community School of the Arts Foundation"""
                }
            },
            
            {
                "category": "Strategic Partnership",
                "context": "Follow-up email, partnership proposal, strategic collaboration focus",
                "template": {
                    "subject": "Strategic Partnership Proposal: {organization_name} & CSOAF",
                    "body": """Dear {contact_name},

Following our recent conversation about {organization_name}'s commitment to community development, I wanted to formally present a strategic partnership opportunity with the Community School of the Arts Foundation.

🤝 Strategic Partnership Proposal

Our research shows that {organization_name}'s values align perfectly with CSOAF's mission to transform communities through accessible arts education. We believe a partnership between our organizations could create significant impact while advancing both of our strategic objectives.

Partnership Opportunities:
• Program Co-Development: Collaborate on innovative arts education initiatives
• Community Engagement: Joint events and workshops that serve both our audiences
• Thought Leadership: Co-authored content and speaking opportunities
• Corporate Social Responsibility: Measurable community impact for your CSR goals

Mutual Benefits:
✅ Enhanced community presence and brand recognition
✅ Access to diverse networks and partnership opportunities
✅ Quantifiable social impact metrics for reporting
✅ Unique employee engagement and team-building opportunities

Next Steps:
I'd welcome the opportunity to present a customized partnership proposal that aligns with {organization_name}'s specific goals and timeline. Would you be available for a 30-minute meeting next week?

Thank you for your consideration. I look forward to exploring how we can create meaningful impact together.

Best regards,
{sender_name}
Strategic Partnerships Director
Community School of the Arts Foundation"""
                }
            }
        ]
    
    def generate_email(self, context: Dict) -> Dict:
        """
        🎯 Generate Email (Compatibility Method)
        =======================================
        Wrapper method for compatibility with the main application.
        Converts the context format and calls generate_few_shot_email.
        """
        
        # Convert context to target_info format
        target_info = {
            'organization_name': context.get('campaign_name', 'Target Organization'),
            'industry': ', '.join(context.get('selected_industries', [])),
            'location': context.get('location_focus', ''),
            'sponsorship_amount': context.get('sponsorship_tiers', [''])[0] if context.get('sponsorship_tiers') else '',
            'description': context.get('user_description', ''),
            'targeting': context.get('targeting_description', '')
        }
        
        # Determine email type from context
        email_type = "sponsorship"  # Default
        if any(keyword in target_info['description'].lower() for keyword in ['event', 'gala', 'celebration']):
            email_type = "event"
        elif any(keyword in target_info['description'].lower() for keyword in ['partnership', 'strategic', 'alliance']):
            email_type = "partnership"
        
        # Generate the email
        result = self.generate_few_shot_email(target_info, email_type)
        
        # Add template information for consistency
        if result['success']:
            result['template_used'] = f"Few-shot AI ({email_type})"
        
        return result
    
    @property
    def template_examples(self) -> List[Dict]:
        """
        📚 Template Examples (Compatibility Property)
        ==========================================
        Returns the email examples for compatibility with demo scripts.
        """
        return self.email_examples

    def generate_few_shot_email(self, target_info: Dict, email_type: str = "sponsorship") -> Dict:
        """
        🎯 Generate Few-Shot Email
        ========================
        Uses proven templates to generate personalized emails.
        
        Args:
            target_info: Dictionary with organization details
            email_type: Type of email ("sponsorship", "event", "partnership")
            
        Returns:
            Dictionary with success status, subject, content, and metadata
        """
        
        try:
            # Select relevant templates based on email type
            relevant_templates = self._select_relevant_templates(target_info, email_type)
            
            # Try OpenAI generation first
            if self.openai_api_key:
                try:
                    ai_result = self._generate_with_openai(target_info, relevant_templates, email_type)
                    if ai_result['success']:
                        return ai_result
                except Exception as e:
                    # Fall back to template-based generation
                    pass
            
            # Fallback to template-based generation
            return self._generate_with_templates(target_info, relevant_templates, email_type)
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'subject': '',
                'content': ''
            }
    
    def _select_relevant_templates(self, target_info: Dict, email_type: str) -> List[Dict]:
        """Select the most relevant templates based on context"""
        
        relevant_examples = []
        
        # Select based on email type
        if email_type == "event":
            # Event-related templates
            relevant_examples.append(self.email_examples[2])  # Event invitation
            relevant_examples.append(self.email_examples[3])  # Gala invitation
        elif email_type == "partnership":
            # Partnership-focused templates
            relevant_examples.append(self.email_examples[4])  # Strategic partnership
            relevant_examples.append(self.email_examples[0])  # Premium partnership
        else:
            # Default sponsorship templates
            if "$" in target_info.get('sponsorship_amount', '') or "high" in target_info.get('description', '').lower():
                relevant_examples.append(self.email_examples[0])  # Premium partnership
            else:
                relevant_examples.append(self.email_examples[1])  # Community partnership
            
            # Add complementary templates
            for example in self.email_examples[:3]:
                if example not in relevant_examples:
                    relevant_examples.append(example)
                    
        return relevant_examples[:3]  # Limit to 3 most relevant
    
    def _generate_with_openai(self, target_info: Dict, templates: List[Dict], email_type: str) -> Dict:
        """Generate email using OpenAI with few-shot learning"""
        
        # Create few-shot prompt
        prompt = self._create_few_shot_prompt(target_info, templates, email_type)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert fundraising email writer for arts education organizations. Generate professional, compelling emails that follow proven templates and maintain consistent tone and structure."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # Parse the response
        generated_text = response.choices[0].message.content.strip()
        subject, content = self._parse_generated_email(generated_text)
        
        return {
            'success': True,
            'subject': subject,
            'content': content,
            'method': 'openai',
            'reasoning': f"Generated using {len(templates)} proven templates as examples"
        }
    
    def _generate_with_templates(self, target_info: Dict, templates: List[Dict], email_type: str) -> Dict:
        """Generate email using template-based approach (fallback)"""
        
        # Select the best template
        if templates:
            selected_template = templates[0]  # Use the first (most relevant) template
        else:
            # Fallback to default
            selected_template = self.email_examples[0] if self.email_examples else None
            
        if not selected_template:
            return {
                'success': False,
                'error': 'No templates available',
                'subject': '',
                'content': ''
            }
        
        # Personalize the template
        subject = selected_template['template']['subject']
        content = selected_template['template']['body']
        
        # Simple variable replacement
        replacements = {
            '{organization_name}': target_info.get('organization_name', 'Your Organization'),
            '{contact_name}': 'Dear Team',
            '{sender_name}': 'CSOAF Partnership Team'
        }
        
        for placeholder, value in replacements.items():
            subject = subject.replace(placeholder, value)
            content = content.replace(placeholder, value)
        
        return {
            'success': True,
            'subject': subject,
            'content': content,
            'method': 'template',
            'reasoning': f"Used template: {selected_template['category']}"
        }
    
    def _create_few_shot_prompt(self, target_info: Dict, templates: List[Dict], email_type: str) -> str:
        """Create a few-shot learning prompt for OpenAI"""
        
        prompt = f"""
Generate a fundraising email for the Community School of the Arts Foundation (CSOAF) based on these proven successful examples:

TARGET INFORMATION:
- Organization: {target_info.get('organization_name', 'Target Organization')}
- Industry: {target_info.get('industry', 'Various')}
- Location: {target_info.get('location', 'General')}
- Sponsorship Level: {target_info.get('sponsorship_amount', 'Standard')}
- Campaign Description: {target_info.get('description', 'Arts education partnership')}
- Email Type: {email_type}

PROVEN SUCCESSFUL EXAMPLES:
"""
        
        for i, template in enumerate(templates[:2], 1):  # Use top 2 examples
            prompt += f"""
Example {i} - {template['category']}:
Context: {template['context']}
Subject: {template['template']['subject']}
Body: {template['template']['body'][:500]}...

"""
        
        prompt += f"""
Based on these proven examples, generate a new email that:
1. Matches the tone and structure of the examples
2. Is personalized for the target organization
3. Includes specific details relevant to the {email_type} context
4. Maintains CSOAF's mission focus on arts education
5. Includes a clear call to action

Format your response as:
SUBJECT: [subject line]
BODY: [email content]
"""
        
        return prompt
    
    def _parse_generated_email(self, generated_text: str) -> tuple:
        """Parse OpenAI response to extract subject and body"""
        
        lines = generated_text.strip().split('\n')
        subject = ""
        content = ""
        
        for i, line in enumerate(lines):
            if line.startswith('SUBJECT:'):
                subject = line.replace('SUBJECT:', '').strip()
            elif line.startswith('BODY:'):
                content = '\n'.join(lines[i:]).replace('BODY:', '').strip()
                break
        
        # Fallback parsing
        if not subject and not content:
            if len(lines) > 1:
                subject = lines[0].strip()
                content = '\n'.join(lines[1:]).strip()
            else:
                subject = "Partnership Opportunity with CSOAF"
                content = generated_text
        
        return subject, content


def get_few_shot_email_ai() -> FewShotEmailAI:
    """
    🎯 Get Few-Shot Email AI Instance
    ===============================
    Returns a cached instance of the FewShotEmailAI for use in Streamlit.
    This ensures we don't reload templates on every interaction.
    """
    
    if 'few_shot_ai' not in st.session_state:
        st.session_state.few_shot_ai = FewShotEmailAI()
    
    return st.session_state.few_shot_ai