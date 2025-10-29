#!/usr/bin/env python3
"""
Campaign Workflow Engine
Integrates interactive campaign creation with existing email template and tracking systems
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Import existing systems
import sys
sys.path.append('.')
sys.path.append('src/tools')
from interactive_campaign_creator import CampaignParser, DataMatcher

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailTemplateSelector:
    """Select appropriate email templates based on campaign analysis"""
    
    def __init__(self):
        self.manager_templates = {
            'foundation_grant': {
                'subject_templates': [
                    "Partnership Opportunity: Supporting {program_name} at CSOAF",
                    "Grant Proposal: {program_name} - Serving {target_audience} in {location}",
                    "Foundation Partnership: Expanding {program_type} Access"
                ],
                'body_template': """Dear {foundation_name} Foundation,

I hope this message finds you well. I'm reaching out from the Center for the Study of Anesthesia and Fear (CSOAF) to explore a meaningful partnership opportunity that aligns with your foundation's commitment to {mission_alignment}.

**About Our Organization:**
CSOAF is a pioneering non-profit dedicated to advancing healing arts and accessible therapy programs. We serve {target_audience} through innovative, evidence-based approaches that integrate mindfulness, creative arts, and therapeutic interventions.

**The Opportunity - {campaign_name}:**
We are seeking foundation support for {program_description}. This program addresses critical needs in our community by {program_impact}.

**Funding Request: {funding_amount}**
Your foundation's support would enable us to:
• {benefit_1}
• {benefit_2}
• {benefit_3}

**Why Partner with CSOAF:**
✓ Proven track record with {success_metric}
✓ Evidence-based approach with measurable outcomes
✓ Strong community partnerships in {geographic_area}
✓ Commitment to accessibility and inclusion

I would welcome the opportunity to discuss how this partnership could advance your foundation's goals while creating lasting impact in our community.

Thank you for considering this proposal. I look forward to hearing from you.

Best regards,

{manager_name}
{manager_title}
Center for the Study of Anesthesia and Fear (CSOAF)
{contact_information}"""
            },
            
            'corporate_sponsor': {
                'subject_templates': [
                    "Corporate Partnership: {event_name} - Premium Sponsorship Opportunity",
                    "Exclusive Sponsorship: {event_name} in {location}",
                    "Community Impact Partnership: {event_name} Sponsorship"
                ],
                'body_template': """Dear {company_name} Team,

I hope this email finds you well. I'm writing to present an exclusive corporate sponsorship opportunity for {event_name}, hosted by the Center for the Study of Anesthesia and Fear (CSOAF).

**About the Event - {event_name}:**
{event_description}

**Sponsorship Investment: {sponsorship_level}**
Your sponsorship will provide significant visibility and community impact:

**Visibility Benefits:**
• Company logo prominently displayed at event venue
• Recognition in all promotional materials and social media
• Speaking opportunity for company representative
• Professional networking with {attendee_count} expected attendees

**Community Impact:**
• Direct support for {program_beneficiaries}
• Measurable outcomes in {impact_area}
• Partnership with respected non-profit organization
• Tax-deductible contribution supporting local community

**Why Partner with CSOAF:**
✓ Established presence in {geographic_area}
✓ Strong community reputation and media relationships
✓ Professional event management with proven results
✓ Meaningful cause that resonates with employees and customers

**Available Sponsorship Levels:**
• Presenting Sponsor: {presenting_amount} - Maximum visibility and exclusivity
• Supporting Sponsor: {supporting_amount} - Significant recognition package
• Community Partner: {community_amount} - Essential support acknowledgment

I would love to schedule a brief call to discuss how this partnership can benefit {company_name} while creating lasting community impact.

Thank you for your consideration.

Best regards,

{manager_name}
{manager_title}
Center for the Study of Anesthesia and Fear (CSOAF)
{contact_information}"""
            }
        }

    def select_template(self, campaign_data: Dict, recipient_type: str, recipient_info: Dict) -> Dict:
        """Select and personalize appropriate template"""
        
        # Determine template type
        if recipient_type == 'foundation':
            template_key = 'foundation_grant'
        elif recipient_type == 'corporation':
            template_key = 'corporate_sponsor'
        else:
            template_key = 'foundation_grant'  # Default
        
        template = self.manager_templates[template_key].copy()
        
        # Personalize template
        personalized = self._personalize_template(template, campaign_data, recipient_info)
        
        return personalized

    def _personalize_template(self, template: Dict, campaign_data: Dict, recipient_info: Dict) -> Dict:
        """Personalize template with campaign and recipient data"""
        
        # Extract campaign information
        campaign_name = campaign_data.get('campaign_name', 'CSOAF Campaign')
        campaign_type = campaign_data.get('campaign_type', 'program')
        target_audience = ', '.join(campaign_data.get('target_audience', ['community members']))
        geographic_focus = ', '.join(campaign_data.get('geographic_focus', ['NY', 'CA']))
        keywords = campaign_data.get('keywords', [])
        
        # Build personalization data
        personalization = {
            'campaign_name': campaign_name,
            'program_name': campaign_name,
            'event_name': campaign_name,
            'program_type': campaign_type,
            'target_audience': target_audience,
            'location': geographic_focus,
            'geographic_area': geographic_focus,
            'manager_name': 'Dr. Sarah Chen',  # Manager name from templates
            'manager_title': 'Executive Director',
            'contact_information': 'schen@csoaf.org | (555) 123-4567',
            
            # Recipient-specific
            'foundation_name': recipient_info.get('organization', '').replace(' Foundation', ''),
            'company_name': recipient_info.get('organization', ''),
            
            # Campaign-specific content
            'program_description': self._generate_program_description(campaign_data),
            'event_description': self._generate_event_description(campaign_data),
            'program_impact': self._generate_impact_statement(campaign_data),
            'funding_amount': campaign_data.get('funding_amount', 'To be discussed'),
            'sponsorship_level': self._determine_sponsorship_level(recipient_info),
            
            # Benefits and outcomes
            'benefit_1': self._generate_benefit(keywords, 1),
            'benefit_2': self._generate_benefit(keywords, 2),
            'benefit_3': self._generate_benefit(keywords, 3),
            
            # Metrics
            'success_metric': self._generate_success_metric(campaign_data),
            'attendee_count': '150-200',
            'program_beneficiaries': target_audience,
            'impact_area': ', '.join(keywords[:2]) if keywords else 'community wellness',
            
            # Mission alignment
            'mission_alignment': self._generate_mission_alignment(recipient_info, keywords),
            
            # Sponsorship amounts
            'presenting_amount': '$25,000',
            'supporting_amount': '$15,000',
            'community_amount': '$5,000'
        }
        
        # Apply personalization to templates
        personalized_template = {}
        for key, value in template.items():
            if isinstance(value, str):
                try:
                    personalized_template[key] = value.format(**personalization)
                except KeyError as e:
                    # Handle missing personalization keys gracefully
                    personalized_template[key] = value.replace(f'{{{e.args[0]}}}', f'[{e.args[0]}]')
            elif isinstance(value, list):
                personalized_list = []
                for item in value:
                    try:
                        personalized_list.append(item.format(**personalization))
                    except KeyError as e:
                        # Handle missing personalization keys gracefully
                        personalized_list.append(item.replace(f'{{{e.args[0]}}}', f'[{e.args[0]}]'))
                personalized_template[key] = personalized_list
            else:
                personalized_template[key] = value
        
        return {
            'template': personalized_template,
            'personalization_data': personalization,
            'recipient_info': recipient_info,
            'campaign_data': campaign_data
        }

    def _generate_program_description(self, campaign_data: Dict) -> str:
        """Generate program description based on campaign data"""
        program_type = campaign_data.get('campaign_type', 'program')
        keywords = campaign_data.get('keywords', [])
        target_audience = campaign_data.get('target_audience', ['community members'])
        
        if 'therapy' in keywords:
            return f"our innovative {program_type} combining therapeutic arts and mindfulness practices for {', '.join(target_audience)}"
        elif 'education' in keywords:
            return f"our comprehensive arts education {program_type} designed to serve {', '.join(target_audience)}"
        elif 'healing' in keywords:
            return f"our healing arts {program_type} providing accessible therapeutic interventions for {', '.join(target_audience)}"
        else:
            return f"our community-based {program_type} serving {', '.join(target_audience)} through creative arts integration"

    def _generate_event_description(self, campaign_data: Dict) -> str:
        """Generate event description"""
        keywords = campaign_data.get('keywords', [])
        target_audience = campaign_data.get('target_audience', ['community members'])
        
        return f"This fundraising event will bring together community leaders, healthcare professionals, and supporters to advance healing arts accessibility for {', '.join(target_audience)}. Featuring live performances, silent auction, and networking opportunities."

    def _generate_impact_statement(self, campaign_data: Dict) -> str:
        """Generate impact statement"""
        keywords = campaign_data.get('keywords', [])
        
        if 'disability' in keywords or 'autism' in keywords:
            return "removing barriers and creating inclusive therapeutic opportunities for individuals with diverse abilities"
        elif 'veterans' in keywords:
            return "addressing trauma and supporting healing for our veteran community through evidence-based arts therapies"
        elif 'children' in keywords:
            return "fostering emotional resilience and creative expression in young people through accessible arts programming"
        else:
            return "expanding access to transformative healing arts experiences in our community"

    def _generate_benefit(self, keywords: List[str], benefit_number: int) -> str:
        """Generate specific benefits based on keywords"""
        benefits = {
            1: {
                'therapy': 'Provide 200+ hours of individual therapy sessions',
                'education': 'Serve 150+ students through expanded programming',
                'veterans': 'Support 75+ veterans through specialized programming',
                'children': 'Reach 100+ children with accessible arts education',
                'default': 'Expand program capacity by 50% to serve more community members'
            },
            2: {
                'therapy': 'Train 15+ healthcare professionals in arts-based interventions',
                'education': 'Develop new curriculum for underserved populations',
                'veterans': 'Create peer support networks and group programming',
                'children': 'Establish family engagement and parent education components',
                'default': 'Enhance program quality through staff development and training'
            },
            3: {
                'therapy': 'Conduct research on therapeutic outcomes and best practices',
                'education': 'Create scholarship fund for low-income participants',
                'veterans': 'Document best practices for veteran-focused arts therapies',
                'children': 'Develop sustainable programming for long-term impact',
                'default': 'Measure and document program outcomes for continuous improvement'
            }
        }
        
        for keyword in keywords:
            if keyword in benefits[benefit_number]:
                return benefits[benefit_number][keyword]
        
        return benefits[benefit_number]['default']

    def _generate_success_metric(self, campaign_data: Dict) -> str:
        """Generate success metrics"""
        keywords = campaign_data.get('keywords', [])
        
        if 'therapy' in keywords:
            return "95% participant satisfaction and measurable therapeutic outcomes"
        elif 'education' in keywords:
            return "87% program completion rates and skill development achievements"
        else:
            return "strong community partnerships and participant engagement"

    def _generate_mission_alignment(self, recipient_info: Dict, keywords: List[str]) -> str:
        """Generate mission alignment statement"""
        if 'healthcare' in str(recipient_info.get('industry', '')).lower():
            return "advancing health and wellness through innovative therapeutic approaches"
        elif 'education' in str(recipient_info.get('organization', '')).lower():
            return "expanding educational opportunities and accessibility"
        elif keywords and 'disability' in keywords:
            return "supporting individuals with diverse abilities and promoting inclusion"
        else:
            return "strengthening communities through arts and healing"

    def _determine_sponsorship_level(self, recipient_info: Dict) -> str:
        """Determine appropriate sponsorship level"""
        if recipient_info.get('type') == 'corporation':
            capacity = recipient_info.get('sponsorship_capacity', {})
            typical = capacity.get('typical', 0)
            
            if typical >= 20000:
                return 'Presenting Sponsor ($25,000)'
            elif typical >= 10000:
                return 'Supporting Sponsor ($15,000)'
            else:
                return 'Community Partner ($5,000)'
        else:
            return 'Foundation Partnership'


class CampaignWorkflowEngine:
    """Complete workflow engine for campaign creation and execution"""
    
    def __init__(self):
        self.parser = CampaignParser()
        self.matcher = DataMatcher()
        self.template_selector = EmailTemplateSelector()
        
        # Initialize tracking
        self.campaign_history = []
        self.email_queue = []
        
    def create_campaign_from_description(self, description: str) -> Dict:
        """Complete workflow: description → parsed → matched → templated"""
        
        logger.info(f"Creating campaign from description: {description[:100]}...")
        
        # Step 1: Parse natural language description
        parsed_campaign = self.parser.parse_campaign_description(description)
        logger.info(f"Parsed campaign type: {parsed_campaign['campaign_type']}")
        
        # Step 2: Match to available data
        matches = self.matcher.match_campaign_to_data(parsed_campaign)
        logger.info(f"Found {len(matches['foundations'])} foundation matches, {len(matches['corporations'])} corporation matches")
        
        # Step 3: Generate email templates for top matches
        email_templates = self._generate_email_templates(parsed_campaign, matches)
        
        # Step 4: Create campaign package
        campaign_package = {
            'campaign_id': f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'created_at': datetime.now().isoformat(),
            'description': description,
            'parsed_campaign': parsed_campaign,
            'matches': matches,
            'email_templates': email_templates,
            'status': 'ready_for_review',
            'metrics': {
                'total_recipients': len(matches['foundations']) + len(matches['corporations']),
                'foundation_recipients': len(matches['foundations']),
                'corporation_recipients': len(matches['corporations']),
                'estimated_reach': self._calculate_estimated_reach(matches),
                'estimated_funding_potential': self._calculate_funding_potential(matches)
            }
        }
        
        # Add to campaign history
        self.campaign_history.append(campaign_package)
        
        return campaign_package

    def _generate_email_templates(self, campaign: Dict, matches: Dict) -> Dict:
        """Generate personalized email templates for all matches"""
        
        templates = {
            'foundation_emails': [],
            'corporation_emails': []
        }
        
        # Generate foundation emails
        for foundation in matches['foundations'][:10]:  # Top 10 foundations
            template = self.template_selector.select_template(
                campaign_data=campaign,
                recipient_type='foundation',
                recipient_info=foundation
            )
            templates['foundation_emails'].append(template)
        
        # Generate corporation emails
        for corporation in matches['corporations'][:8]:  # Top 8 corporations
            template = self.template_selector.select_template(
                campaign_data=campaign,
                recipient_type='corporation',
                recipient_info=corporation
            )
            templates['corporation_emails'].append(template)
        
        return templates

    def _calculate_estimated_reach(self, matches: Dict) -> int:
        """Calculate estimated audience reach"""
        base_reach = len(matches['foundations']) * 500  # Estimated foundation network reach
        corp_reach = len(matches['corporations']) * 1000  # Estimated corporate network reach
        return base_reach + corp_reach

    def _calculate_funding_potential(self, matches: Dict) -> Dict:
        """Calculate estimated funding potential"""
        foundation_potential = len(matches['foundations']) * 15000  # Average foundation grant
        
        corp_potential = 0
        for corp in matches['corporations']:
            capacity = corp.get('sponsorship_capacity', {})
            corp_potential += capacity.get('typical', 10000)
        
        return {
            'foundation_potential': foundation_potential,
            'corporation_potential': corp_potential,
            'total_potential': foundation_potential + corp_potential,
            'conservative_estimate': (foundation_potential + corp_potential) * 0.15,  # 15% success rate
            'optimistic_estimate': (foundation_potential + corp_potential) * 0.35   # 35% success rate
        }

    def export_campaign_summary(self, campaign_package: Dict, output_file: str = None) -> str:
        """Export campaign summary to file"""
        
        if not output_file:
            campaign_id = campaign_package['campaign_id']
            output_file = f"campaigns/campaign_summaries/{campaign_id}_summary.json"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save campaign package
        with open(output_file, 'w') as f:
            json.dump(campaign_package, f, indent=2, default=str)
        
        logger.info(f"Campaign summary exported to {output_file}")
        return output_file

    def get_campaign_status_report(self) -> Dict:
        """Get status report of all campaigns"""
        
        total_campaigns = len(self.campaign_history)
        active_campaigns = len([c for c in self.campaign_history if c['status'] in ['ready_for_review', 'in_progress']])
        
        total_potential = sum(c['metrics']['estimated_funding_potential']['total_potential'] for c in self.campaign_history)
        
        return {
            'total_campaigns': total_campaigns,
            'active_campaigns': active_campaigns,
            'total_funding_potential': total_potential,
            'total_recipients_reached': sum(c['metrics']['total_recipients'] for c in self.campaign_history),
            'campaigns': self.campaign_history
        }


def main():
    """Test the complete workflow"""
    
    print("🚀 CAMPAIGN WORKFLOW ENGINE - Testing Complete System")
    print("=" * 70)
    
    # Initialize workflow engine
    engine = CampaignWorkflowEngine()
    
    # Test campaigns
    test_descriptions = [
        "We need corporate sponsors for our annual healing arts gala in New York, aiming to raise $75,000 to support our new adaptive dance program for children with autism",
        
        "Looking for foundation grants to fund our veterans music therapy program in California, need about $50,000 to serve 100 veterans over the next year"
    ]
    
    for i, description in enumerate(test_descriptions, 1):
        print(f"\n🎯 Campaign {i}: Processing...")
        print(f"Description: {description}")
        
        # Create complete campaign
        campaign = engine.create_campaign_from_description(description)
        
        # Display results
        print(f"\n📊 Campaign Results:")
        print(f"  Campaign ID: {campaign['campaign_id']}")
        print(f"  Type: {campaign['parsed_campaign']['campaign_type']}")
        print(f"  Name: {campaign['parsed_campaign']['campaign_name']}")
        
        metrics = campaign['metrics']
        print(f"\n📈 Campaign Metrics:")
        print(f"  Total Recipients: {metrics['total_recipients']}")
        print(f"  Foundation Targets: {metrics['foundation_recipients']}")
        print(f"  Corporation Targets: {metrics['corporation_recipients']}")
        print(f"  Funding Potential: ${metrics['estimated_funding_potential']['total_potential']:,}")
        print(f"  Conservative Est: ${metrics['estimated_funding_potential']['conservative_estimate']:,}")
        
        print(f"\n📧 Email Templates Generated:")
        print(f"  Foundation Emails: {len(campaign['email_templates']['foundation_emails'])}")
        print(f"  Corporation Emails: {len(campaign['email_templates']['corporation_emails'])}")
        
        # Export campaign summary
        summary_file = engine.export_campaign_summary(campaign)
        print(f"  Summary Exported: {summary_file}")
        
        print("-" * 70)
    
    # Overall status report
    status = engine.get_campaign_status_report()
    print(f"\n📋 OVERALL STATUS REPORT:")
    print(f"  Total Campaigns Created: {status['total_campaigns']}")
    print(f"  Active Campaigns: {status['active_campaigns']}")
    print(f"  Total Funding Potential: ${status['total_funding_potential']:,}")
    print(f"  Total Recipients: {status['total_recipients_reached']}")
    
    print("\n✅ Campaign Workflow Engine - Ready for Production!")

if __name__ == "__main__":
    main()