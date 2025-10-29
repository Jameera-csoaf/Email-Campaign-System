#!/usr/bin/env python3
"""
ProPublica Data Harvester - Maximum 24-Hour Collection
Fetches maximum possible nonprofit records from ProPublica API in 24 hours
Stores all data in CSV format for future email outreach campaigns

This script is designed to:
1. Maximize data collection within API limits
2. Store comprehensive nonprofit contact data  
3. Prepare database for sponsorship/donor outreach
4. Run continuously for 24 hours to get maximum records
"""

import pandas as pd
import requests
import time
import os
from datetime import datetime, timedelta
import logging
import sys
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from campaign import ProPublicaConnector

class ProPublicaHarvester:
    """
    Maximum data harvesting from ProPublica Nonprofit Explorer API
    Designed to collect as many nonprofit records as possible in 24 hours
    """
    
    def __init__(self, output_file="data/input/propublica_sponsors.csv"):
        self.output_file = output_file
        self.connector = ProPublicaConnector()
        self.collected_data = []
        self.seen_eins = set()
        self.start_time = datetime.now()
        self.total_api_calls = 0
        self.rate_limit_delay = 1.0  # Start with 1 second delay between calls
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('propublica_harvest.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        self.logger.info("🚀 ProPublica Harvester initialized")
        self.logger.info(f"📁 Output file: {output_file}")
        
        # Web scraping settings for contact discovery
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.request_delay = 2.0  # Delay between requests to be respectful
    
    def discover_website_for_organization(self, org_name, city, state):
        """
        Search for organization's official website using Google search
        Returns the most likely official website URL
        """
        try:
            # Clean organization name for search
            search_query = f'"{org_name}" {city} {state} official website'
            
            # Use DuckDuckGo search (more reliable than Google for automation)
            search_url = "https://html.duckduckgo.com/html/"
            params = {'q': search_query}
            
            response = self.session.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find search result links
                result_links = soup.find_all('a', class_='result__a')
                
                for link in result_links[:3]:  # Check first 3 results
                    href = link.get('href')
                    if href and self._is_likely_official_website(href, org_name):
                        self.logger.info(f"🌐 Found website: {href}")
                        return href
            
            return ""
            
        except Exception as e:
            self.logger.error(f"❌ Website discovery error for {org_name}: {e}")
            return ""
    
    def _is_likely_official_website(self, url, org_name):
        """
        Check if URL is likely the official website for the organization
        """
        try:
            # Parse domain
            domain = urlparse(url).netloc.lower()
            org_words = org_name.lower().split()
            
            # Remove common words
            org_words = [word for word in org_words if word not in ['foundation', 'inc', 'corporation', 'fund', 'trust', 'the', 'and', 'of', 'for']]
            
            # Check if organization name words appear in domain
            if len(org_words) > 0 and any(word in domain for word in org_words if len(word) > 3):
                return True
                
            # Avoid social media, directories, etc.
            if any(site in domain for site in ['facebook', 'twitter', 'linkedin', 'guidestar', 'charitynavigator', 'wikipedia']):
                return False
                
            return True
            
        except:
            return False
    
    def extract_emails_from_website(self, url):
        """
        Extract email addresses from a website
        Returns list of found email addresses
        """
        try:
            if not url:
                return []
            
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return []
            
            # Extract emails using regex
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, response.text)
            
            # Filter out common unwanted emails
            filtered_emails = []
            unwanted_patterns = ['noreply', 'no-reply', 'donotreply', 'webmaster', 'admin@example', 'test@']
            
            for email in emails:
                email = email.lower()
                if not any(pattern in email for pattern in unwanted_patterns):
                    if email not in filtered_emails:  # Remove duplicates
                        filtered_emails.append(email)
                        
                if len(filtered_emails) >= 3:  # Limit to 3 emails per organization
                    break
            
            if filtered_emails:
                self.logger.info(f"📧 Found emails: {', '.join(filtered_emails)}")
            
            return filtered_emails
            
        except Exception as e:
            self.logger.error(f"❌ Email extraction error for {url}: {e}")
            return []
    
    def enhance_organization_with_contacts(self, org_data):
        """
        Enhance organization data with website and email information
        """
        try:
            org_name = org_data.get('sponsor_name', '')
            city = org_data.get('city', '')
            state = org_data.get('state', '')
            
            self.logger.info(f"🔍 Discovering contacts for: {org_name}")
            
            # Discover website
            website = self.discover_website_for_organization(org_name, city, state)
            org_data['website'] = website
            
            # Extract emails from website
            emails = []
            if website:
                time.sleep(self.request_delay)  # Be respectful
                emails = self.extract_emails_from_website(website)
            
            # Store primary email and all emails
            org_data['email'] = emails[0] if emails else ''
            org_data['all_emails'] = '; '.join(emails) if emails else ''
            org_data['contact_discovery_status'] = 'completed'
            
            return org_data
            
        except Exception as e:
            self.logger.error(f"❌ Contact enhancement error: {e}")
            org_data['contact_discovery_status'] = 'failed'
            return org_data
    
    def get_comprehensive_search_terms(self):
        """
        Generate comprehensive search terms to maximize data collection
        Returns list of search terms that will capture different types of sponsors
        """
        return [
            # Foundation types - highest priority for sponsors
            "foundation", "foundations", "charitable foundation", "family foundation",
            "community foundation", "private foundation", "corporate foundation",
            
            # Arts & Culture (CSOAF's domain)
            "arts", "cultural", "music", "theater", "dance", "visual arts",
            "arts education", "cultural arts", "performing arts",
            
            # Education sponsors
            "education", "educational", "school", "schools", "university",
            "college", "learning", "scholarship", "student",
            
            # Community & Social
            "community", "social", "civic", "public", "nonprofit",
            "charity", "charitable", "philanthropy", "giving",
            
            # Corporate & Business
            "corporate", "business", "company", "inc", "corporation",
            "association", "society", "institute",
            
            # Health & Human Services (potential sponsors)
            "health", "healthcare", "medical", "hospital", "wellness",
            "human services", "social services", "youth", "children",
            
            # Geographic terms for broad coverage
            "new york", "california", "national", "american", "united states"
        ]
    
    def get_target_states(self):
        """
        Get states prioritized by sponsor potential
        Focus on high-population states with many nonprofits first
        """
        # High-priority states (large populations, many nonprofits, wealthy donors)
        priority_states = [
            'NY', 'CA', 'TX', 'FL', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI',
            'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI'
        ]
        
        # Secondary states
        other_states = [
            'AL', 'AK', 'AR', 'CO', 'CT', 'DE', 'DC', 'HI', 'ID', 'IA',
            'KS', 'KY', 'LA', 'ME', 'MN', 'MS', 'MT', 'NE', 'NV', 'NH',
            'NM', 'ND', 'OK', 'OR', 'RI', 'SC', 'SD', 'UT', 'VT', 'WV', 'WY'
        ]
        
        return priority_states + other_states
    
    def fetch_organizations_batch(self, search_term, state, limit=100):
        """
        Fetch a batch of organizations for given search term and state
        Includes rate limiting and error handling
        """
        try:
            self.logger.info(f"🔍 Searching: '{search_term}' in {state}")
            
            results = self.connector.search_organizations(
                keywords=search_term,
                state=state,
                limit=limit
            )
            
            self.total_api_calls += 1
            
            if 'organizations' in results:
                new_orgs = 0
                for org in results['organizations']:
                    ein = org.get('ein', '')
                    if ein and ein not in self.seen_eins:
                        self.seen_eins.add(ein)
                        
                        # Format data for outreach database
                        sponsor_record = {
                            'sponsor_name': org.get('name', '').strip(),
                            'ein': ein,
                            'city': org.get('city', '').strip(),
                            'state': state,
                            'ntee_code': org.get('ntee_code', ''),
                            'classification': org.get('subsection', ''),
                            'propublica_url': f"https://projects.propublica.org/nonprofits/organizations/{ein}",
                            'search_term_found': search_term,
                            'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            
                            # Contact fields (will be filled by discovery)
                            'website': '',
                            'email': '',
                            'all_emails': '',
                            'phone': '',
                            'contact_person': '',
                            'mission_statement': '',
                            'annual_revenue': '',
                            'assets': '',
                            'outreach_status': 'not_contacted',
                            'email_sent': 'no',
                            'response_received': 'no',
                            'sponsorship_amount': '',
                            'notes': '',
                            'follow_up_date': '',
                            'priority_level': 'medium',
                            'contact_discovery_status': 'pending'
                        }
                        
                        # Enhance with contact information (for first few records to test)
                        if new_orgs < 5:  # Only enhance first 5 per batch to avoid overwhelming
                            sponsor_record = self.enhance_organization_with_contacts(sponsor_record)
                        
                        self.collected_data.append(sponsor_record)
                        new_orgs += 1
                
                self.logger.info(f"📊 Found {new_orgs} new organizations (Total: {len(self.collected_data)})")
                return new_orgs
            
            return 0
            
        except Exception as e:
            self.logger.error(f"❌ Error fetching {search_term} in {state}: {e}")
            return 0
    
    def save_progress(self):
        """
        Save current progress to CSV file
        Called periodically to avoid data loss
        """
        if not self.collected_data:
            return
        
        df = pd.DataFrame(self.collected_data)
        
        # Remove duplicates based on EIN
        df = df.drop_duplicates(subset=['ein'], keep='first')
        
        df.to_csv(self.output_file, index=False)
        
        self.logger.info(f"💾 Saved {len(df)} unique records to {self.output_file}")
    
    def harvest_maximum_data(self, max_hours=24):
        """
        Run maximum data collection for specified hours
        Systematically searches all combinations to maximize results
        """
        end_time = self.start_time + timedelta(hours=max_hours)
        search_terms = self.get_comprehensive_search_terms()
        states = self.get_target_states()
        
        self.logger.info(f"🎯 Starting {max_hours}-hour harvest")
        self.logger.info(f"📋 {len(search_terms)} search terms × {len(states)} states = {len(search_terms) * len(states)} combinations")
        
        save_interval = 50  # Save every 50 API calls
        api_calls_since_save = 0
        
        try:
            for state in states:
                if datetime.now() >= end_time:
                    break
                    
                self.logger.info(f"\n🗺️ Starting state: {state}")
                
                for search_term in search_terms:
                    if datetime.now() >= end_time:
                        break
                    
                    # Fetch batch of organizations
                    new_orgs = self.fetch_organizations_batch(search_term, state, limit=100)
                    
                    # Rate limiting to be respectful
                    time.sleep(self.rate_limit_delay)
                    
                    # Periodic saving
                    api_calls_since_save += 1
                    if api_calls_since_save >= save_interval:
                        self.save_progress()
                        api_calls_since_save = 0
                        
                        # Progress report
                        elapsed = datetime.now() - self.start_time
                        rate = len(self.collected_data) / max(elapsed.total_seconds() / 3600, 0.1)
                        self.logger.info(f"⏱️ Progress: {len(self.collected_data)} records in {elapsed}, Rate: {rate:.1f} records/hour")
                
                # Save after each state
                self.save_progress()
        
        except KeyboardInterrupt:
            self.logger.info("⚠️ Harvest interrupted by user")
        
        # Final save and summary
        self.save_progress()
        
        elapsed = datetime.now() - self.start_time
        self.logger.info(f"\n🎉 HARVEST COMPLETE!")
        self.logger.info(f"📊 Total records collected: {len(self.collected_data)}")
        self.logger.info(f"⏱️ Time elapsed: {elapsed}")
        self.logger.info(f"📞 Total API calls: {self.total_api_calls}")
        self.logger.info(f"💾 Data saved to: {self.output_file}")
        
        return self.output_file

def quick_test_harvest(minutes=5):
    """
    Quick test harvest for specified minutes to test the system
    """
    print(f"🧪 Running {minutes}-minute test harvest...")
    
    harvester = ProPublicaHarvester(output_file="data/input/test_propublica_sponsors.csv")
    output_file = harvester.harvest_maximum_data(max_hours=minutes/60)
    
    print(f"✅ Test complete! Check {output_file}")
    return output_file

def main():
    """
    Run the ProPublica data harvester
    """
    print("🚀 ProPublica Maximum Data Harvester")
    print("📝 This script will collect nonprofit data for sponsor outreach")
    print("💾 All data will be saved to CSV for future email campaigns")
    print("="*60)
    
    # Ask user for harvest type
    print("Choose harvest type:")
    print("1. Quick test (5 minutes)")
    print("2. Full harvest (24 hours)")
    print("3. Custom duration")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        return quick_test_harvest()
    
    elif choice == "2":
        duration = 24
        
    elif choice == "3":
        duration = float(input("Enter harvest duration in hours: ").strip())
        
    else:
        print("Invalid choice, defaulting to quick test")
        return quick_test_harvest()
    
    print(f"⏱️ Starting {duration}-hour harvest...")
    print("Press Ctrl+C to stop early (data will be saved)")
    
    # Initialize and run harvester
    harvester = ProPublicaHarvester()
    output_file = harvester.harvest_maximum_data(max_hours=duration)
    
    print(f"\n✅ Harvest complete! Data saved to: {output_file}")
    print("💡 This CSV can now be used for email outreach campaigns")
    return output_file

if __name__ == "__main__":
    main()