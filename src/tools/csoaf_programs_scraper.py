#!/usr/bin/env python3
"""
CSOAF Programs Data Scraper
Extracts current programs, events, and funding needs from CSOAF.org
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from datetime import datetime
import json
import re
from urllib.parse import urljoin

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class CSOAFProgramsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://csoaf.org"
        
    def scrape_programs_page(self):
        """Scrape main programs page"""
        programs = []
        
        try:
            url = f"{self.base_url}/programs"
            response = self.session.get(url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract program information
                program_sections = soup.find_all(['div', 'section'], class_=lambda x: x and any(
                    keyword in str(x).lower() for keyword in ['program', 'class', 'course', 'workshop']
                ))
                
                for section in program_sections:
                    program_info = self.extract_program_info(section)
                    if program_info:
                        programs.append(program_info)
                        
                # Also look for text-based program mentions
                text_programs = self.extract_programs_from_text(soup)
                programs.extend(text_programs)
                
        except Exception as e:
            logger.error(f"Error scraping programs page: {e}")
            
        return programs
        
    def scrape_events_page(self):
        """Scrape events and workshops"""
        events = []
        
        try:
            event_urls = [
                f"{self.base_url}/events",
                f"{self.base_url}/calendar",
                f"{self.base_url}/workshops",
                f"{self.base_url}/classes"
            ]
            
            for url in event_urls:
                try:
                    response = self.session.get(url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extract event information
                        event_elements = soup.find_all(['div', 'article', 'li'], class_=lambda x: x and any(
                            keyword in str(x).lower() for keyword in ['event', 'workshop', 'class', 'performance']
                        ))
                        
                        for element in event_elements:
                            event_info = self.extract_event_info(element)
                            if event_info:
                                events.append(event_info)
                                
                except Exception as e:
                    logger.debug(f"Error accessing {url}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping events: {e}")
            
        return events
        
    def scrape_about_mission(self):
        """Scrape about page for mission and program details"""
        mission_data = {}
        
        try:
            about_urls = [
                f"{self.base_url}/about",
                f"{self.base_url}/mission",
                f"{self.base_url}/about-us"
            ]
            
            for url in about_urls:
                try:
                    response = self.session.get(url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extract mission statement
                        mission_text = self.extract_mission_text(soup)
                        if mission_text:
                            mission_data['mission_statement'] = mission_text
                            
                        # Extract program descriptions
                        program_descriptions = self.extract_program_descriptions(soup)
                        mission_data['program_descriptions'] = program_descriptions
                        
                        # Extract impact data
                        impact_data = self.extract_impact_data(soup)
                        mission_data['impact_metrics'] = impact_data
                        
                        break  # Use first successful page
                        
                except Exception as e:
                    logger.debug(f"Error accessing {url}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping about/mission: {e}")
            
        return mission_data
        
    def extract_program_info(self, section):
        """Extract program information from a page section"""
        try:
            program = {}
            
            # Look for program title
            title_elem = section.find(['h1', 'h2', 'h3', 'h4', 'strong'])
            if title_elem:
                program['title'] = title_elem.get_text().strip()
            else:
                return None
                
            # Extract description
            description_text = section.get_text().strip()
            if len(description_text) > 50:
                program['description'] = description_text[:300]
                
            # Look for program type/category
            program['category'] = self.classify_program_type(description_text)
            
            # Look for target audience
            program['target_audience'] = self.extract_target_audience(description_text)
            
            # Look for schedule/frequency
            program['schedule'] = self.extract_schedule_info(description_text)
            
            return program
            
        except Exception as e:
            logger.debug(f"Error extracting program info: {e}")
            return None
            
    def extract_event_info(self, element):
        """Extract event information from an element"""
        try:
            event = {}
            
            # Extract event title
            title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'strong', 'a'])
            if title_elem:
                event['title'] = title_elem.get_text().strip()
            else:
                return None
                
            # Extract date if available
            event_text = element.get_text()
            date_match = re.search(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', event_text)
            if date_match:
                event['date'] = date_match.group()
                
            # Extract description
            event['description'] = event_text[:200].strip()
            
            # Classify event type
            event['event_type'] = self.classify_event_type(event_text)
            
            return event
            
        except Exception as e:
            logger.debug(f"Error extracting event info: {e}")
            return None
            
    def extract_programs_from_text(self, soup):
        """Extract program mentions from general text content"""
        programs = []
        
        # Common program-related keywords
        program_keywords = [
            'art class', 'dance class', 'music class', 'theater class',
            'workshop', 'program', 'course', 'lesson', 'training',
            'healing arts', 'creative arts', 'visual arts', 'performing arts'
        ]
        
        text_content = soup.get_text().lower()
        
        for keyword in program_keywords:
            if keyword in text_content:
                # Find sentences containing the keyword
                sentences = self.find_sentences_with_keyword(soup, keyword)
                for sentence in sentences:
                    program = {
                        'title': f"{keyword.title()} Program",
                        'description': sentence,
                        'category': self.classify_program_type(sentence),
                        'source': 'text_extraction'
                    }
                    programs.append(program)
                    
        return programs[:10]  # Limit to avoid duplicates
        
    def find_sentences_with_keyword(self, soup, keyword):
        """Find sentences containing specific keywords"""
        sentences = []
        
        paragraphs = soup.find_all(['p', 'div', 'li'])
        for p in paragraphs:
            text = p.get_text().strip()
            if keyword in text.lower() and len(text) > 30:
                sentences.append(text[:200])
                
        return sentences[:3]  # Limit to 3 sentences per keyword
        
    def classify_program_type(self, text):
        """Classify program type based on content"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['dance', 'movement', 'choreography']):
            return 'Dance'
        elif any(word in text_lower for word in ['music', 'singing', 'instrument', 'song']):
            return 'Music'
        elif any(word in text_lower for word in ['theater', 'drama', 'acting', 'performance']):
            return 'Theater'
        elif any(word in text_lower for word in ['visual', 'painting', 'drawing', 'art therapy']):
            return 'Visual Arts'
        elif any(word in text_lower for word in ['healing', 'therapy', 'wellness', 'mindfulness']):
            return 'Healing Arts'
        elif any(word in text_lower for word in ['disability', 'accessible', 'inclusive', 'adaptive']):
            return 'Accessible Arts'
        else:
            return 'General Arts'
            
    def classify_event_type(self, text):
        """Classify event type"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['performance', 'show', 'concert', 'recital']):
            return 'Performance'
        elif any(word in text_lower for word in ['workshop', 'class', 'lesson']):
            return 'Educational'
        elif any(word in text_lower for word in ['fundraiser', 'gala', 'benefit']):
            return 'Fundraising'
        elif any(word in text_lower for word in ['community', 'outreach', 'volunteer']):
            return 'Community'
        else:
            return 'General Event'
            
    def extract_target_audience(self, text):
        """Extract target audience from text"""
        text_lower = text.lower()
        
        audiences = []
        if any(word in text_lower for word in ['children', 'kids', 'youth', 'young']):
            audiences.append('Children/Youth')
        if any(word in text_lower for word in ['adult', 'senior', 'elderly']):
            audiences.append('Adults')
        if any(word in text_lower for word in ['disability', 'disabled', 'special needs']):
            audiences.append('People with Disabilities')
        if any(word in text_lower for word in ['veteran', 'military']):
            audiences.append('Veterans')
        if any(word in text_lower for word in ['family', 'parent', 'caregiver']):
            audiences.append('Families')
            
        return ', '.join(audiences) if audiences else 'General Public'
        
    def extract_schedule_info(self, text):
        """Extract schedule/frequency information"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['weekly', 'every week']):
            return 'Weekly'
        elif any(word in text_lower for word in ['monthly', 'every month']):
            return 'Monthly'
        elif any(word in text_lower for word in ['daily', 'every day']):
            return 'Daily'
        elif any(word in text_lower for word in ['ongoing', 'continuous']):
            return 'Ongoing'
        else:
            return 'Variable'
            
    def extract_mission_text(self, soup):
        """Extract mission statement"""
        # Look for mission-related content
        mission_indicators = ['mission', 'purpose', 'about', 'who we are', 'what we do']
        
        for indicator in mission_indicators:
            # Find headings with mission-related text
            headings = soup.find_all(['h1', 'h2', 'h3'], string=re.compile(indicator, re.IGNORECASE))
            
            for heading in headings:
                # Get following paragraph
                next_elem = heading.find_next(['p', 'div'])
                if next_elem:
                    text = next_elem.get_text().strip()
                    if len(text) > 50:
                        return text[:500]
                        
        # Fallback: get first substantial paragraph
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 100:
                return text[:500]
                
        return None
        
    def extract_program_descriptions(self, soup):
        """Extract detailed program descriptions"""
        descriptions = []
        
        # Look for sections that describe programs
        program_sections = soup.find_all(['div', 'section'], string=re.compile('program|class|workshop', re.IGNORECASE))
        
        for section in program_sections:
            text = section.get_text().strip()
            if len(text) > 100:
                descriptions.append(text[:300])
                
        return descriptions[:5]  # Limit to 5 descriptions
        
    def extract_impact_data(self, soup):
        """Extract impact metrics and success stories"""
        impact_data = []
        
        # Look for numbers that might be impact metrics
        text_content = soup.get_text()
        
        # Find patterns like "X people served", "X years", "X% improvement"
        impact_patterns = [
            r'\d+\s*(?:people|students|participants|individuals|families)',
            r'\d+\s*(?:years|months)\s*(?:of|providing|serving)',
            r'\d+%\s*(?:improvement|increase|success|completion)',
            r'\$\d+(?:,\d{3})*\s*(?:raised|donated|funded)'
        ]
        
        for pattern in impact_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            impact_data.extend(matches)
            
        return impact_data[:10]  # Limit to 10 metrics
        
    def estimate_funding_needs(self, programs, events):
        """Estimate funding needs based on programs and events"""
        funding_estimates = []
        
        # Base estimates per program type
        program_costs = {
            'Dance': {'per_session': 150, 'equipment': 500, 'annual': 5000},
            'Music': {'per_session': 200, 'equipment': 1000, 'annual': 8000},
            'Theater': {'per_session': 175, 'equipment': 750, 'annual': 6000},
            'Visual Arts': {'per_session': 125, 'equipment': 800, 'annual': 4500},
            'Healing Arts': {'per_session': 100, 'equipment': 300, 'annual': 3500},
            'General Arts': {'per_session': 100, 'equipment': 400, 'annual': 3000}
        }
        
        total_estimated_need = 0
        
        for program in programs:
            category = program.get('category', 'General Arts')
            if category in program_costs:
                costs = program_costs[category]
                
                # Estimate sessions per year based on schedule
                schedule = program.get('schedule', 'Variable')
                if schedule == 'Weekly':
                    sessions_per_year = 50
                elif schedule == 'Monthly':
                    sessions_per_year = 12
                elif schedule == 'Daily':
                    sessions_per_year = 200
                else:
                    sessions_per_year = 24  # Default
                    
                program_annual_cost = (costs['per_session'] * sessions_per_year) + costs['equipment']
                total_estimated_need += program_annual_cost
                
                funding_estimates.append({
                    'program': program.get('title', 'Unnamed Program'),
                    'category': category,
                    'estimated_annual_cost': program_annual_cost,
                    'sessions_per_year': sessions_per_year,
                    'cost_per_session': costs['per_session']
                })
                
        return funding_estimates, total_estimated_need
        
    def run_full_scrape(self):
        """Run complete CSOAF scraping process"""
        logger.info("Starting CSOAF.org programs and events scraping")
        
        results = {
            'programs': [],
            'events': [],
            'mission_data': {},
            'funding_estimates': [],
            'total_estimated_funding_need': 0
        }
        
        try:
            # Scrape programs
            logger.info("Scraping programs...")
            results['programs'] = self.scrape_programs_page()
            
            # Scrape events
            logger.info("Scraping events...")
            results['events'] = self.scrape_events_page()
            
            # Scrape mission/about
            logger.info("Scraping mission and about information...")
            results['mission_data'] = self.scrape_about_mission()
            
            # Estimate funding needs
            logger.info("Calculating funding estimates...")
            funding_estimates, total_need = self.estimate_funding_needs(
                results['programs'], results['events']
            )
            results['funding_estimates'] = funding_estimates
            results['total_estimated_funding_need'] = total_need
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save programs as CSV
            if results['programs']:
                programs_df = pd.DataFrame(results['programs'])
                programs_df.to_csv(f'csoaf_programs_{timestamp}.csv', index=False)
                
            # Save events as CSV
            if results['events']:
                events_df = pd.DataFrame(results['events'])
                events_df.to_csv(f'csoaf_events_{timestamp}.csv', index=False)
                
            # Save funding estimates
            if results['funding_estimates']:
                funding_df = pd.DataFrame(results['funding_estimates'])
                funding_df.to_csv(f'csoaf_funding_estimates_{timestamp}.csv', index=False)
                
            # Save complete results as JSON
            with open(f'csoaf_complete_data_{timestamp}.json', 'w') as f:
                json.dump(results, f, indent=2, default=str)
                
            logger.info(f"CSOAF scraping complete!")
            logger.info(f"Found {len(results['programs'])} programs")
            logger.info(f"Found {len(results['events'])} events")
            logger.info(f"Estimated total funding need: ${results['total_estimated_funding_need']:,}")
            
        except Exception as e:
            logger.error(f"Error in full scrape: {e}")
            
        return results

if __name__ == "__main__":
    scraper = CSOAFProgramsScraper()
    results = scraper.run_full_scrape()
    
    print(f"Scraped CSOAF data:")
    print(f"- Programs: {len(results['programs'])}")
    print(f"- Events: {len(results['events'])}")
    print(f"- Estimated funding need: ${results['total_estimated_funding_need']:,}")