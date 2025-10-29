#!/usr/bin/env python3
"""
Intelligent Contact Categorization & Email Automation Agent
Automatically categorizes contacts based on event data and sends targeted emails
"""

import pandas as pd
import re
import logging
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
import time
import random
from typing import Dict, List, Tuple, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class EventKeywordExtractor:
    """Extract keywords from event descriptions for contact matching"""
    
    def __init__(self):
        # Common keyword categories for events
        self.keyword_categories = {
            'causes': ['education', 'arts', 'health', 'children', 'youth', 'seniors', 'environment', 
                      'community', 'social', 'cultural', 'music', 'theater', 'healing', 'therapy',
                      'mental health', 'wellness', 'creativity', 'learning', 'development'],
            
            'beneficiaries': ['students', 'schools', 'children', 'kids', 'youth', 'teens', 'families',
                            'communities', 'teachers', 'artists', 'performers', 'creators'],
            
            'locations': ['nyc', 'new york', 'brooklyn', 'manhattan', 'queens', 'bronx', 'staten island',
                         'local', 'neighborhood', 'community', 'urban', 'underserved'],
            
            'event_types': ['benefit', 'fundraiser', 'gala', 'performance', 'exhibition', 'workshop',
                           'concert', 'theater', 'art show', 'celebration', 'gathering'],
            
            'impact_words': ['healing', 'transforming', 'empowering', 'inspiring', 'supporting',
                           'uplifting', 'connecting', 'building', 'strengthening', 'creating']
        }
    
    def extract_keywords(self, event_text: str) -> Dict[str, List[str]]:
        """Extract relevant keywords from event description"""
        
        event_text_lower = event_text.lower()
        extracted = {}
        
        for category, keywords in self.keyword_categories.items():
            found_keywords = []
            for keyword in keywords:
                if keyword in event_text_lower:
                    found_keywords.append(keyword)
            extracted[category] = found_keywords
        
        # Extract additional keywords using patterns
        extracted['organizations'] = self._extract_organization_types(event_text_lower)
        extracted['monetary'] = self._extract_monetary_keywords(event_text_lower)
        
        return extracted
    
    def _extract_organization_types(self, text: str) -> List[str]:
        """Extract organization type keywords"""
        org_types = ['foundation', 'fund', 'trust', 'nonprofit', 'charity', 'organization',
                    'institute', 'center', 'society', 'association', 'corporation']
        return [org_type for org_type in org_types if org_type in text]
    
    def _extract_monetary_keywords(self, text: str) -> List[str]:
        """Extract monetary and sponsorship keywords"""
        money_words = ['sponsor', 'donate', 'support', 'fund', 'contribute', 'give',
                      'dollars', 'ticket', 'corporate', 'partnership']
        return [word for word in money_words if word in text]

class ContactCategorizer:
    """Categorize contacts based on alignment with event keywords"""
    
    def __init__(self):
        self.event_extractor = EventKeywordExtractor()
        
        # Scoring weights for different alignment factors
        self.weights = {
            'keyword_match': 0.4,
            'location_match': 0.2,
            'organization_type': 0.2,
            'cause_alignment': 0.2
        }
    
    def calculate_alignment_score(self, contact: Dict, event_keywords: Dict) -> float:
        """Calculate alignment score between contact and event"""
        
        score = 0.0
        max_score = 100.0
        
        contact_name = str(contact.get('sponsor_name', '')).lower()
        contact_city = str(contact.get('city', '')).lower()
        contact_state = str(contact.get('state', '')).lower()
        contact_classification = str(contact.get('classification', '')).lower()
        contact_ntee = str(contact.get('ntee_code', '')).lower()
        
        # 1. Keyword matching (40% weight)
        keyword_score = 0
        total_keywords = 0
        
        for category, keywords in event_keywords.items():
            for keyword in keywords:
                total_keywords += 1
                if (keyword in contact_name or 
                    keyword in contact_classification or
                    keyword in contact_ntee):
                    keyword_score += 1
        
        if total_keywords > 0:
            score += (keyword_score / total_keywords) * self.weights['keyword_match'] * max_score
        
        # 2. Location matching (20% weight)
        location_score = 0
        for location in event_keywords.get('locations', []):
            if location in contact_city or location in contact_state:
                location_score += 1
        
        if event_keywords.get('locations'):
            score += min(location_score / len(event_keywords['locations']), 1.0) * self.weights['location_match'] * max_score
        
        # 3. Organization type matching (20% weight)
        org_score = 0
        for org_type in event_keywords.get('organizations', []):
            if org_type in contact_name or org_type in contact_classification:
                org_score += 1
        
        if event_keywords.get('organizations'):
            score += min(org_score / len(event_keywords['organizations']), 1.0) * self.weights['organization_type'] * max_score
        
        # 4. Cause alignment (20% weight)
        cause_score = 0
        for cause in event_keywords.get('causes', []):
            if cause in contact_name or cause in contact_classification or cause in contact_ntee:
                cause_score += 1
        
        if event_keywords.get('causes'):
            score += min(cause_score / len(event_keywords['causes']), 1.0) * self.weights['cause_alignment'] * max_score
        
        return min(score, max_score)
    
    def categorize_contacts(self, contacts_df: pd.DataFrame, event_text: str, 
                          min_score: float = 15.0, max_contacts: int = 200) -> pd.DataFrame:
        """Categorize contacts based on event alignment"""
        
        logger.info("Extracting keywords from event description...")
        event_keywords = self.event_extractor.extract_keywords(event_text)
        
        logger.info(f"Found keywords: {event_keywords}")
        
        # Calculate alignment scores
        logger.info("Calculating alignment scores for all contacts...")
        contacts_df['alignment_score'] = contacts_df.apply(
            lambda row: self.calculate_alignment_score(row.to_dict(), event_keywords), 
            axis=1
        )
        
        # Filter contacts by minimum score
        aligned_contacts = contacts_df[contacts_df['alignment_score'] >= min_score].copy()
        
        # Sort by alignment score (highest first)
        aligned_contacts = aligned_contacts.sort_values('alignment_score', ascending=False)
        
        # Limit number of contacts if specified
        if max_contacts:
            aligned_contacts = aligned_contacts.head(max_contacts)
        
        # Add categorization
        aligned_contacts['potential_level'] = aligned_contacts['alignment_score'].apply(
            lambda score: 'High' if score >= 40 else 'Medium' if score >= 25 else 'Low'
        )
        
        logger.info(f"Found {len(aligned_contacts)} aligned contacts:")
        logger.info(f"  High potential: {len(aligned_contacts[aligned_contacts['potential_level'] == 'High'])}")
        logger.info(f"  Medium potential: {len(aligned_contacts[aligned_contacts['potential_level'] == 'Medium'])}")
        logger.info(f"  Low potential: {len(aligned_contacts[aligned_contacts['potential_level'] == 'Low'])}")
        
        return aligned_contacts

class DonationHistoryChecker:
    """Check if organizations have donation history online"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def check_donation_history(self, organization_name: str, website: str = None) -> Dict:
        """Check if organization has donation/funding history"""
        
        try:
            # Check organization website for donation patterns
            if website and website.strip():
                donation_info = self._check_website_for_donations(website)
                if donation_info['has_donations']:
                    return donation_info
            
            # Search for organization + donation keywords
            search_results = self._search_donation_patterns(organization_name)
            return search_results
            
        except Exception as e:
            logger.warning(f"Error checking donation history for {organization_name}: {str(e)}")
            return {'has_donations': False, 'confidence': 0, 'source': 'error'}
    
    def _check_website_for_donations(self, website: str) -> Dict:
        """Check organization website for donation indicators"""
        
        try:
            if not website.startswith('http'):
                website = 'https://' + website
            
            response = self.session.get(website, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text().lower()
            
            # Look for donation indicators
            donation_keywords = [
                'grants', 'funding', 'donated', 'supported', 'awarded',
                'philanthropic', 'charitable giving', 'beneficiary',
                'recipient', 'grantee', 'sponsor', 'partner'
            ]
            
            donation_score = sum(1 for keyword in donation_keywords if keyword in text_content)
            
            if donation_score >= 3:
                return {
                    'has_donations': True,
                    'confidence': min(donation_score / len(donation_keywords), 1.0),
                    'source': 'website',
                    'indicators': donation_score
                }
            
        except Exception as e:
            logger.debug(f"Website check failed for {website}: {str(e)}")
        
        return {'has_donations': False, 'confidence': 0, 'source': 'website_check_failed'}
    
    def _search_donation_patterns(self, organization_name: str) -> Dict:
        """Search for donation patterns using simple heuristics"""
        
        # Simple heuristic based on organization name patterns
        org_lower = organization_name.lower()
        
        # Organizations likely to have donation history
        donor_indicators = [
            'foundation', 'fund', 'trust', 'charitable', 'philanthropic',
            'giving', 'grant', 'endowment', 'fellowship'
        ]
        
        # Organizations likely to receive donations
        recipient_indicators = [
            'school', 'university', 'college', 'hospital', 'clinic',
            'museum', 'theater', 'arts', 'community', 'center'
        ]
        
        donor_score = sum(1 for indicator in donor_indicators if indicator in org_lower)
        recipient_score = sum(1 for indicator in recipient_indicators if indicator in org_lower)
        
        if donor_score >= 1:
            return {
                'has_donations': True,
                'confidence': 0.7,
                'source': 'donor_pattern',
                'type': 'likely_donor'
            }
        elif recipient_score >= 1:
            return {
                'has_donations': True,
                'confidence': 0.5,
                'source': 'recipient_pattern',
                'type': 'likely_recipient'
            }
        
        return {'has_donations': False, 'confidence': 0, 'source': 'no_pattern'}

class TemplateAssigner:
    """Assign email templates based on contact characteristics"""
    
    def __init__(self):
        self.internal_domains = ['csoaf.org', 'csoaf.mail']
    
    def assign_template(self, contact: Dict) -> Tuple[int, str]:
        """Assign appropriate email template (1-5) based on contact data"""
        
        email = str(contact.get('email', '')).lower()
        sponsor_name = str(contact.get('sponsor_name', ''))
        donation_history = contact.get('donation_history', {})
        
        # Template 5: Internal team
        if any(domain in email for domain in self.internal_domains):
            return 5, "Internal Team (@csoaf.org)"
        
        # Extract first name
        first_name = self._extract_first_name(sponsor_name)
        has_name = bool(first_name)
        
        # Check donation history
        has_donated = False
        if donation_history and donation_history != 'unknown':
            if isinstance(donation_history, str):
                has_donated = 'True' in donation_history or 'has_donations' in donation_history
            else:
                has_donated = donation_history.get('has_donations', False) if donation_history else False
        
        # Template assignment logic
        if has_name and has_donated:
            return 1, "Has Name + Past Donor"
        elif has_name and not has_donated:
            return 2, "Has Name + Never Donated"
        elif not has_name and has_donated:
            return 3, "No Name + Past Donor"
        else:
            return 4, "No Name + Never Donated"
    
    def _extract_first_name(self, full_name: str) -> Optional[str]:
        """Extract first name from full name or organization name"""
        
        if not full_name or pd.isna(full_name):
            return None
        
        name = str(full_name).strip()
        
        # Skip if it's clearly an organization
        org_indicators = [
            'foundation', 'fund', 'trust', 'inc', 'corp', 'llc', 'organization',
            'institute', 'association', 'center', 'society', 'company', 'enterprises'
        ]
        
        if any(indicator in name.lower() for indicator in org_indicators):
            return None
        
        # Try to extract first name
        parts = name.split()
        if len(parts) >= 1:
            first_part = parts[0]
            # Check if it looks like a real first name
            if first_part.lower() not in ['mr', 'mrs', 'ms', 'dr', 'prof', 'president', 'director']:
                return first_part.title()
        
        return None

class IntelligentCampaignAgent:
    """Main agent that orchestrates the entire categorization and email process"""
    
    def __init__(self):
        self.categorizer = ContactCategorizer()
        self.donation_checker = DonationHistoryChecker()
        self.template_assigner = TemplateAssigner()
    
    def run_campaign(self, event_description: str, contacts_file: str, 
                    max_contacts: int = 100, min_score: float = 15.0,
                    check_donations: bool = True) -> str:
        """Run complete intelligent campaign"""
        
        logger.info("=" * 80)
        logger.info("INTELLIGENT CONTACT CATEGORIZATION & EMAIL AGENT")
        logger.info("=" * 80)
        
        # Load contacts
        logger.info(f"Loading contacts from: {contacts_file}")
        contacts_df = pd.read_csv(contacts_file)
        logger.info(f"Loaded {len(contacts_df)} total contacts")
        
        # Categorize contacts
        logger.info("Categorizing contacts based on event alignment...")
        aligned_contacts = self.categorizer.categorize_contacts(
            contacts_df, event_description, min_score, max_contacts
        )
        
        if len(aligned_contacts) == 0:
            logger.warning("No aligned contacts found! Consider lowering min_score threshold.")
            return None
        
        # Check donation history (for top contacts only to save time)
        if check_donations:
            logger.info("Checking donation history for top contacts...")
            top_contacts = aligned_contacts.head(50)  # Check top 50 for efficiency
            
            donation_data = []
            for idx, contact in top_contacts.iterrows():
                logger.info(f"Checking donation history: {contact['sponsor_name']}")
                website = contact.get('website', '')
                if pd.isna(website):
                    website = ''
                donation_info = self.donation_checker.check_donation_history(
                    contact['sponsor_name'], website
                )
                donation_data.append(donation_info)
                time.sleep(0.5)  # Be respectful to websites
            
            # Add donation history to contacts
            aligned_contacts['donation_history'] = 'unknown'
            for i, donation_info in enumerate(donation_data):
                if i < len(aligned_contacts):
                    aligned_contacts.iloc[i, aligned_contacts.columns.get_loc('donation_history')] = str(donation_info)
        
        # Assign email templates
        logger.info("Assigning email templates...")
        template_assignments = []
        template_descriptions = []
        
        for idx, contact in aligned_contacts.iterrows():
            template_num, template_desc = self.template_assigner.assign_template(contact.to_dict())
            template_assignments.append(template_num)
            template_descriptions.append(template_desc)
        
        aligned_contacts['template_number'] = template_assignments
        aligned_contacts['template_type'] = template_descriptions
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'campaigns/sponsor_data/intelligent_campaign_{timestamp}.csv'
        
        aligned_contacts.to_csv(output_file, index=False)
        logger.info(f"Intelligent campaign saved: {output_file}")
        
        # Generate summary
        self._create_campaign_summary(aligned_contacts, event_description, output_file, timestamp)
        
        return output_file
    
    def _create_campaign_summary(self, contacts_df: pd.DataFrame, event_description: str, 
                                output_file: str, timestamp: str):
        """Create campaign summary report"""
        
        summary_file = f'campaigns/sponsor_data/intelligent_summary_{timestamp}.md'
        
        with open(summary_file, 'w') as f:
            f.write("# Intelligent Contact Categorization Campaign\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Event details
            f.write("## Event Description\n")
            f.write(f"```\n{event_description}\n```\n\n")
            
            # Campaign statistics
            f.write("## Campaign Statistics\n")
            f.write(f"- **Total Aligned Contacts**: {len(contacts_df)}\n")
            f.write(f"- **Average Alignment Score**: {contacts_df['alignment_score'].mean():.1f}\n")
            f.write(f"- **Highest Score**: {contacts_df['alignment_score'].max():.1f}\n")
            f.write(f"- **With Email Addresses**: {len(contacts_df[contacts_df['email'].notna()])}\n\n")
            
            # Potential level distribution
            potential_counts = contacts_df['potential_level'].value_counts()
            f.write("## Potential Level Distribution\n")
            for level, count in potential_counts.items():
                percentage = (count / len(contacts_df)) * 100
                f.write(f"- **{level} Potential**: {count} contacts ({percentage:.1f}%)\n")
            f.write("\n")
            
            # Template distribution
            template_counts = contacts_df['template_number'].value_counts().sort_index()
            f.write("## Email Template Distribution\n")
            for template_num, count in template_counts.items():
                template_type = contacts_df[contacts_df['template_number'] == template_num]['template_type'].iloc[0]
                percentage = (count / len(contacts_df)) * 100
                f.write(f"- **Template {template_num}** ({template_type}): {count} contacts ({percentage:.1f}%)\n")
            f.write("\n")
            
            # Top contacts
            f.write("## Top 10 Aligned Contacts\n")
            top_contacts = contacts_df.nlargest(10, 'alignment_score')
            for idx, contact in top_contacts.iterrows():
                f.write(f"1. **{contact['sponsor_name']}** - Score: {contact['alignment_score']:.1f} ")
                f.write(f"({contact['potential_level']} potential, Template {contact['template_number']})\n")
            
            f.write(f"\n## Output Files\n")
            f.write(f"- **Campaign Data**: {output_file}\n")
            f.write(f"- **Summary Report**: {summary_file}\n")
            
            f.write(f"\n## Next Steps\n")
            f.write(f"1. Review aligned contacts and scores\n")
            f.write(f"2. Generate personalized emails using template system\n")
            f.write(f"3. Send emails via SendGrid\n")
            f.write(f"4. Track responses and engagement\n")
        
        logger.info(f"Campaign summary saved: {summary_file}")

def main():
    """Main function to run the intelligent campaign agent"""
    
    print("INTELLIGENT CONTACT CATEGORIZATION AGENT")
    print("=" * 60)
    
    # Example event description (Healing Through Arts)
    event_description = """
    Hi Team,
    We're excited to invite you to join us as a sponsor of Healing Through Arts: NYC Schools, 
    an unforgettable evening where art, music, and community come together to create lasting 
    impact for NYC students.
    
    Why sponsor this event?
    Direct community impact: Every sponsorship dollar funds arts healing programs in underserved NYC schools.
    Exclusive engagement: Connect with city leaders, artists, and philanthropists at a vibrant evening 
    of performances, wine tasting, and conversations.
    
    Healing Through Arts: NYC Schools Benefit
    Monday, November 18, 2025 | 7:00 PM – 9:00 PM (doors open 6:30 PM)
    Rake Wine Bar (45 1st Ave, NYC)
    $35 per ticket
    Arts displays & live performances
    Wine tasting & hors d'oeuvres
    Meet fellow changemakers
    """
    
    # Initialize agent
    agent = IntelligentCampaignAgent()
    
    # Run campaign
    campaign_file = agent.run_campaign(
        event_description=event_description,
        contacts_file='campaigns/sponsor_data/sponsors_enhanced_for_campaign.csv',
        max_contacts=100,
        min_score=15.0,
        check_donations=True
    )
    
    if campaign_file:
        print(f"\n🎯 INTELLIGENT CAMPAIGN COMPLETE!")
        print(f"📁 Campaign file: {campaign_file}")
        print(f"🚀 Ready for email generation and sending!")
    else:
        print(f"\n❌ No aligned contacts found. Try lowering the minimum score threshold.")

if __name__ == "__main__":
    main()