#!/usr/bin/env python3
"""
Interactive Campaign Creation System
Natural language processing for dual-track fundraising campaigns
"""

import re
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class CampaignParser:
    """Parse natural language campaign descriptions into structured data"""
    
    def __init__(self):
        # Keywords for different campaign types
        self.event_keywords = [
            'gala', 'event', 'fundraiser', 'benefit', 'reception', 'dinner',
            'auction', 'performance', 'show', 'concert', 'exhibition',
            'wine tasting', 'art gallery', 'showcase', 'celebration'
        ]
        
        self.program_keywords = [
            'class', 'program', 'course', 'lesson', 'workshop', 'training',
            'education', 'curriculum', 'instruction', 'teaching', 'learning',
            'therapy', 'session', 'studio', 'arts education'
        ]
        
        # CSOAF specific programs from database
        self.csoaf_programs = [
            'adaptive dance', 'music therapy', 'art therapy', 'theater workshop',
            'mindfulness', 'meditation', 'visual arts', 'family healing',
            'creative writing', 'sensory integration', 'professional development'
        ]
        
        # Geographic keywords
        self.geo_keywords = {
            'ny': ['new york', 'ny', 'nyc', 'manhattan', 'brooklyn', 'queens', 'bronx'],
            'ca': ['california', 'ca', 'los angeles', 'san francisco', 'san diego']
        }
        
        # Amount keywords
        self.amount_patterns = [
            r'\$[\d,]+',  # $1,000
            r'[\d,]+\s*dollars?',  # 1000 dollars
            r'[\d,]+k',  # 50k
            r'[\d,]+\s*thousand',  # 50 thousand
        ]

    def parse_campaign_description(self, description: str) -> Dict:
        """Parse campaign description into structured requirements"""
        description_lower = description.lower()
        
        result = {
            'campaign_type': self._determine_campaign_type(description_lower),
            'target_audience': self._extract_target_audience(description_lower),
            'geographic_focus': self._extract_geographic_focus(description_lower),
            'funding_amount': self._extract_funding_amount(description_lower),
            'specific_programs': self._extract_specific_programs(description_lower),
            'keywords': self._extract_keywords(description_lower),
            'urgency': self._extract_urgency(description_lower),
            'campaign_name': self._extract_campaign_name(description)
        }
        
        # Determine dual-track routing
        result['routing'] = self._determine_routing(result)
        
        return result

    def _determine_campaign_type(self, description: str) -> str:
        """Determine if this is an event or program campaign"""
        event_score = sum(1 for keyword in self.event_keywords if keyword in description)
        program_score = sum(1 for keyword in self.program_keywords if keyword in description)
        
        if event_score > program_score:
            return 'event'
        elif program_score > event_score:
            return 'program'
        else:
            # Default based on specific indicators
            if any(word in description for word in ['gala', 'fundraiser', 'benefit']):
                return 'event'
            elif any(word in description for word in ['class', 'education', 'therapy']):
                return 'program'
            else:
                return 'mixed'  # Both types

    def _extract_target_audience(self, description: str) -> List[str]:
        """Extract target audience from description"""
        audiences = []
        
        audience_keywords = {
            'children': ['children', 'kids', 'youth', 'young people', 'students'],
            'adults': ['adults', 'grown-ups', 'parents', 'caregivers'],
            'disabilities': ['disabilities', 'disabled', 'special needs', 'autism', 'inclusive'],
            'veterans': ['veterans', 'military', 'service members'],
            'families': ['families', 'family', 'parents and children'],
            'seniors': ['seniors', 'elderly', 'older adults']
        }
        
        for audience, keywords in audience_keywords.items():
            if any(keyword in description for keyword in keywords):
                audiences.append(audience)
        
        return audiences if audiences else ['general public']

    def _extract_geographic_focus(self, description: str) -> List[str]:
        """Extract geographic focus"""
        locations = []
        
        for region, keywords in self.geo_keywords.items():
            if any(keyword in description for keyword in keywords):
                locations.append(region.upper())
        
        return locations if locations else ['NY', 'CA']  # Default to both

    def _extract_funding_amount(self, description: str) -> Optional[str]:
        """Extract funding amount if mentioned"""
        for pattern in self.amount_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group()
        return None

    def _extract_specific_programs(self, description: str) -> List[str]:
        """Extract specific CSOAF programs mentioned"""
        programs = []
        
        for program in self.csoaf_programs:
            if program in description:
                programs.append(program)
        
        # Also check for general program types
        program_types = ['dance', 'music', 'art', 'theater', 'writing', 'therapy']
        for ptype in program_types:
            if ptype in description and ptype not in [p.split()[0] for p in programs]:
                programs.append(f"{ptype} program")
        
        return programs

    def _extract_keywords(self, description: str) -> List[str]:
        """Extract relevant keywords for database matching"""
        # Common arts/education keywords
        relevant_keywords = [
            'arts', 'education', 'healing', 'therapy', 'creative', 'inclusive',
            'accessibility', 'community', 'wellness', 'mental health', 'trauma',
            'disability', 'autism', 'special needs', 'veterans', 'children',
            'youth', 'family', 'dance', 'music', 'visual arts', 'theater'
        ]
        
        found_keywords = []
        for keyword in relevant_keywords:
            if keyword in description:
                found_keywords.append(keyword)
        
        return found_keywords

    def _extract_urgency(self, description: str) -> str:
        """Extract urgency level"""
        urgent_words = ['urgent', 'asap', 'immediately', 'emergency', 'critical']
        high_words = ['soon', 'quickly', 'fast', 'high priority']
        
        if any(word in description for word in urgent_words):
            return 'urgent'
        elif any(word in description for word in high_words):
            return 'high'
        else:
            return 'normal'

    def _extract_campaign_name(self, description: str) -> str:
        """Extract or generate campaign name"""
        # Look for quoted campaign names
        quotes_match = re.search(r'"([^"]+)"', description)
        if quotes_match:
            return quotes_match.group(1)
        
        # Look for "for X" or "campaign for X"
        for_match = re.search(r'(?:campaign )?for (.+?)(?:\s|$|,)', description.lower())
        if for_match:
            name = for_match.group(1).strip()
            if len(name) > 3:
                return name.title()
        
        # Generate based on content
        if 'healing' in description.lower():
            return "Healing Arts Campaign"
        elif 'gala' in description.lower():
            return "Fundraising Gala"
        elif 'education' in description.lower():
            return "Arts Education Campaign"
        else:
            return "CSOAF Campaign"

    def _determine_routing(self, parsed_data: Dict) -> Dict:
        """Determine foundation vs corporation routing"""
        campaign_type = parsed_data['campaign_type']
        
        routing = {
            'foundations': {
                'priority': 'high' if campaign_type in ['program', 'mixed'] else 'low',
                'focus': 'program_funding',
                'templates': ['foundation_grant', 'program_partner']
            },
            'corporations': {
                'priority': 'high' if campaign_type in ['event', 'mixed'] else 'low',
                'focus': 'event_sponsorship',
                'templates': ['corporate_sponsor', 'event_partner']
            }
        }
        
        return routing


class DataMatcher:
    """Match parsed campaign requirements to database records"""
    
    def __init__(self):
        self.foundation_data = None
        self.corporation_data = None
        self.csoaf_programs = None
        
    def load_databases(self):
        """Load all relevant databases"""
        try:
            # Load foundation data
            foundation_files = [f for f in ['data/foundations/integrated_sponsor_database_20251026_195246.csv']]
            if foundation_files:
                self.foundation_data = pd.read_csv(foundation_files[0])
                logger.info(f"Loaded {len(self.foundation_data)} foundation records")
            
            # Load corporation data - prioritize comprehensive Fortune 1000, then enhanced, then others
            import os
            
            # First try comprehensive Fortune 1000 database
            comprehensive_files = [f for f in os.listdir('data/corporations/') if f.startswith('comprehensive_fortune1000_')]
            if comprehensive_files:
                latest_corp_file = max([f'data/corporations/{f}' for f in comprehensive_files], key=os.path.getctime)
                self.corporation_data = pd.read_csv(latest_corp_file)
                logger.info(f"Loaded {len(self.corporation_data)} Comprehensive Fortune 1000 corporation records from {latest_corp_file}")
            else:
                # Fallback to enhanced Fortune 1000
                enhanced_corp_files = [f for f in os.listdir('data/corporations/') if f.startswith('enhanced_fortune1000_ny_ca_')]
                if enhanced_corp_files:
                    latest_corp_file = max([f'data/corporations/{f}' for f in enhanced_corp_files], key=os.path.getctime)
                    self.corporation_data = pd.read_csv(latest_corp_file)
                    logger.info(f"Loaded {len(self.corporation_data)} Enhanced Fortune 1000 corporation records from {latest_corp_file}")
                else:
                    # Fallback to regular Fortune 1000, then Fortune 100
                    fortune1000_files = [f for f in os.listdir('data/corporations/') if f.startswith('fortune1000_ny_ca_')]
                    if fortune1000_files:
                        latest_corp_file = max([f'data/corporations/{f}' for f in fortune1000_files], key=os.path.getctime)
                        self.corporation_data = pd.read_csv(latest_corp_file)
                        logger.info(f"Loaded {len(self.corporation_data)} Fortune 1000 corporation records from {latest_corp_file}")
            
            # Load CSOAF programs - prioritize enhanced version
            enhanced_program_files = [f for f in os.listdir('data/programs/') if f.startswith('enhanced_csoaf_programs_')]
            if enhanced_program_files:
                latest_program_file = max([f'data/programs/{f}' for f in enhanced_program_files], key=os.path.getctime)
                self.csoaf_programs = pd.read_csv(latest_program_file)
                logger.info(f"Loaded {len(self.csoaf_programs)} Enhanced CSOAF programs from {latest_program_file}")
            else:
                # Fallback to regular CSOAF data
                program_files = [f for f in os.listdir('data/programs/') if f.startswith('csoaf_programs_')]
                if program_files:
                    latest_program_file = max([f'data/programs/{f}' for f in program_files], key=os.path.getctime)
                    self.csoaf_programs = pd.read_csv(latest_program_file)
                    logger.info(f"Loaded {len(self.csoaf_programs)} CSOAF programs from {latest_program_file}")
                    
        except Exception as e:
            logger.error(f"Error loading databases: {e}")

    def match_campaign_to_data(self, parsed_campaign: Dict) -> Dict:
        """Match campaign requirements to available data"""
        if not self.foundation_data is not None:
            self.load_databases()
        
        results = {
            'foundations': [],
            'corporations': [],
            'matched_programs': [],
            'campaign_summary': parsed_campaign
        }
        
        # Match foundations for program funding
        if parsed_campaign['routing']['foundations']['priority'] == 'high':
            results['foundations'] = self._match_foundations(parsed_campaign)
        
        # Match corporations for event sponsorship
        if parsed_campaign['routing']['corporations']['priority'] == 'high':
            results['corporations'] = self._match_corporations(parsed_campaign)
        
        # Match internal programs
        results['matched_programs'] = self._match_programs(parsed_campaign)
        
        return results

    def _match_foundations(self, campaign: Dict) -> List[Dict]:
        """Match foundations based on campaign requirements"""
        if self.foundation_data is None:
            return []
        
        matched = []
        keywords = campaign['keywords']
        geo_focus = campaign['geographic_focus']
        
        for _, foundation in self.foundation_data.iterrows():
            score = 0
            
            # Geographic match
            if foundation.get('state') in geo_focus:
                score += 20
            
            # Mission alignment score
            if 'mission_alignment_score' in foundation:
                score += foundation['mission_alignment_score'] * 0.5
            
            # Keyword matching in program areas
            program_areas = str(foundation.get('program_areas', '')).lower()
            keyword_matches = sum(1 for keyword in keywords if keyword in program_areas)
            score += keyword_matches * 5
            
            # Additional mission text analysis
            mission_text = str(foundation.get('mission_text', foundation.get('mission_statement', ''))).lower()
            mission_keyword_matches = sum(1 for keyword in keywords if keyword in mission_text)
            score += mission_keyword_matches * 3
            
            # Priority level bonus
            if foundation.get('priority_level') == 'high':
                score += 10
            
            if score > 15:  # Minimum threshold
                matched.append({
                    'organization': foundation.get('sponsor_name', ''),
                    'score': score,
                    'type': 'foundation',
                    'contact_info': {
                        'email': foundation.get('email', ''),
                        'website': foundation.get('website', ''),
                        'city': foundation.get('city', ''),
                        'state': foundation.get('state', ''),
                        'mission': foundation.get('mission_text', foundation.get('mission_statement', '')),
                        'contact_person': foundation.get('contact_person', ''),
                        'phone': foundation.get('phone', ''),
                        'program_areas': foundation.get('program_areas', ''),
                        'annual_revenue': foundation.get('annual_revenue', ''),
                        'priority_level': foundation.get('priority_level', '')
                    },
                    'alignment_reason': f"Keywords: {keyword_matches + mission_keyword_matches}, Mission Score: {foundation.get('mission_alignment_score', 0)}, Priority: {foundation.get('priority_level', 'standard')}"
                })
        
        # Sort by score and return top matches
        matched.sort(key=lambda x: x['score'], reverse=True)
        return matched[:20]  # Top 20 matches

    def _match_corporations(self, campaign: Dict) -> List[Dict]:
        """Match corporations based on campaign requirements"""
        if self.corporation_data is None:
            return []
        
        matched = []
        geo_focus = campaign['geographic_focus']
        keywords = campaign.get('keywords', [])
        
        for _, corp in self.corporation_data.iterrows():
            score = 0
            
            # Geographic match
            if corp.get('state') in geo_focus:
                score += 25
            
            # Enhanced arts sponsorship scoring
            arts_potential = str(corp.get('arts_education_potential', corp.get('arts_sponsorship_history', ''))).lower()
            if 'very high' in arts_potential:
                score += 30
            elif 'high' in arts_potential:
                score += 20
            elif 'medium' in arts_potential:
                score += 10
            
            # Sponsorship likelihood score (if available from enhanced data)
            if 'sponsorship_likelihood_score' in corp:
                score += corp['sponsorship_likelihood_score'] * 0.3
            
            # Industry relevance with enhanced scoring
            industry = str(corp.get('industry_sector', '')).lower()
            if any(word in industry for word in ['technology', 'financial', 'media', 'entertainment']):
                score += 15
            
            # Mission alignment for enhanced data
            mission = str(corp.get('mission', corp.get('sponsorship_focus', ''))).lower()
            keyword_matches = sum(1 for keyword in keywords if keyword in mission)
            score += keyword_matches * 3
            
            if score > 20:  # Minimum threshold
                matched.append({
                    'organization': corp.get('organization_name', ''),
                    'score': score,
                    'type': 'corporation',
                    'contact_info': {
                        'email': corp.get('email', ''),
                        'website': corp.get('website', ''),
                        'city': corp.get('city', ''),
                        'state': corp.get('state', ''),
                        'industry': corp.get('industry_sector', ''),
                        'mission': corp.get('mission', ''),
                        'contact_department': corp.get('contact_department', ''),
                        'sponsorship_focus': corp.get('sponsorship_focus', ''),
                        'donation_range': corp.get('donation_range', ''),
                        'linkedin': corp.get('linkedin', '')
                    },
                    'sponsorship_capacity': {
                        'min': corp.get('estimated_min_sponsorship', 0),
                        'max': corp.get('estimated_max_sponsorship', 0),
                        'typical': corp.get('estimated_typical_sponsorship', 0)
                    },
                    'alignment_reason': f"Arts potential: {arts_potential}, Industry: {industry}, Keywords: {keyword_matches}"
                })
        
        # Sort by score and return top matches
        matched.sort(key=lambda x: x['score'], reverse=True)
        return matched[:20]  # Top 20 matches
        matched.sort(key=lambda x: x['score'], reverse=True)
        return matched[:15]  # Top 15 matches

    def _match_programs(self, campaign: Dict) -> List[Dict]:
        """Match CSOAF programs to campaign requirements"""
        if self.csoaf_programs is None:
            return []
        
        matched = []
        specific_programs = campaign['specific_programs']
        target_audience = campaign['target_audience']
        
        for _, program in self.csoaf_programs.iterrows():
            score = 0
            
            # Specific program match
            program_title = str(program.get('title', '')).lower()
            for spec_prog in specific_programs:
                if any(word in program_title for word in spec_prog.split()):
                    score += 30
            
            # Target audience match
            prog_audience = str(program.get('target_audience', '')).lower()
            for audience in target_audience:
                if audience.replace('_', ' ') in prog_audience:
                    score += 20
            
            # Category relevance
            category = str(program.get('category', '')).lower()
            if any(keyword in category for keyword in campaign['keywords']):
                score += 15
            
            if score > 10:  # Minimum threshold
                matched.append({
                    'program': program.get('title', ''),
                    'category': program.get('category', ''),
                    'score': score,
                    'cost': program.get('estimated_annual_cost', 0),
                    'description': program.get('description', ''),
                    'target_audience': program.get('target_audience', ''),
                    'funding_need': program.get('estimated_annual_cost', 0)
                })
        
        # Sort by score
        matched.sort(key=lambda x: x['score'], reverse=True)
        return matched

def main():
    """Test the campaign parsing system"""
    
    # Test cases
    test_campaigns = [
        "I want to run a campaign for our upcoming healing arts gala to support our new adaptive dance program for children with disabilities",
        "We need funding for our art therapy classes for veterans in New York",
        "Looking for corporate sponsors for our annual fundraising event in California, need about $50,000",
        "Need foundation grants for our inclusive music therapy program serving autistic children"
    ]
    
    parser = CampaignParser()
    matcher = DataMatcher()
    
    print("🎯 INTERACTIVE CAMPAIGN CREATION SYSTEM")
    print("=" * 60)
    
    for i, campaign_desc in enumerate(test_campaigns, 1):
        print(f"\n📝 Test Campaign {i}:")
        print(f"Description: {campaign_desc}")
        
        # Parse campaign
        parsed = parser.parse_campaign_description(campaign_desc)
        print(f"\n📊 Parsed Results:")
        print(f"  Campaign Type: {parsed['campaign_type']}")
        print(f"  Target Audience: {', '.join(parsed['target_audience'])}")
        print(f"  Geographic Focus: {', '.join(parsed['geographic_focus'])}")
        print(f"  Keywords: {', '.join(parsed['keywords'])}")
        print(f"  Campaign Name: {parsed['campaign_name']}")
        
        # Show routing
        print(f"\n🎯 Routing Strategy:")
        foundations = parsed['routing']['foundations']
        corporations = parsed['routing']['corporations']
        print(f"  Foundations: {foundations['priority']} priority - {foundations['focus']}")
        print(f"  Corporations: {corporations['priority']} priority - {corporations['focus']}")
        
        # Match to data
        matches = matcher.match_campaign_to_data(parsed)
        print(f"\n📈 Data Matches:")
        print(f"  Foundations: {len(matches['foundations'])} matches")
        print(f"  Corporations: {len(matches['corporations'])} matches")
        print(f"  Programs: {len(matches['matched_programs'])} matches")
        
        print("-" * 60)

if __name__ == "__main__":
    main()