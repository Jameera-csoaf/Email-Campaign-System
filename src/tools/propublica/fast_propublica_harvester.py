#!/usr/bin/env python3
"""
Fast ProPublica Data Harvester - No Contact Discovery
Optimized for maximum data collection speed from ProPublica Nonprofit Explorer API
"""

import requests
import pandas as pd
import time
import logging
from datetime import datetime, timedelta
import sys
import os

class FastProPublicaHarvester:
    def __init__(self):
        self.base_url = "https://projects.propublica.org/nonprofits/api/v2/search.json"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Set up logging to file only (no console output to avoid Unicode issues)
        self.setup_logging()
        
        # Comprehensive search terms for maximum data collection
        self.search_terms = [
            'foundation', 'fund', 'trust', 'charity', 'nonprofit', 'organization',
            'institute', 'association', 'society', 'center', 'program', 'project',
            'alliance', 'coalition', 'network', 'council', 'committee', 'group',
            'education', 'health', 'medical', 'research', 'social', 'community',
            'arts', 'culture', 'environment', 'human', 'relief', 'development',
            'church', 'temple', 'mosque', 'religious', 'faith', 'mission',
            'school', 'university', 'college', 'academy', 'library', 'museum'
        ]
        
        # All US states for comprehensive coverage
        self.states = [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
        ]
        
        self.collected_data = []
        self.request_delay = 0.5  # Respectful rate limiting
        
    def setup_logging(self):
        """Set up logging to file only"""
        log_filename = f"fast_harvest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def search_propublica(self, query_term, limit=100):
        """Search ProPublica API for organizations"""
        params = {
            'q': query_term,
            'c_code': 'all',
            'limit': limit
        }
        
        # Note: Not using state parameter as it causes 500 errors
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            organizations = data.get('organizations', [])
            
            print(f"Found {len(organizations)} organizations for '{query_term}'")
            self.logger.info(f"Found {len(organizations)} organizations for '{query_term}'")
            
            return organizations
            
        except Exception as e:
            error_msg = f"Error searching for '{query_term}': {e}"
            print(error_msg)
            self.logger.error(error_msg)
            return []
    
    def convert_to_sponsor_record(self, org_data):
        """Convert ProPublica organization data to sponsor record format"""
        return {
            'sponsor_name': org_data.get('name', ''),
            'classification': org_data.get('subsection', ''),
            'city': org_data.get('city', ''),
            'state': org_data.get('state', ''),
            'address': f"{org_data.get('city', '')}, {org_data.get('state', '')}",
            'ein': org_data.get('ein', ''),
            'ruling_date': org_data.get('ruling_date', ''),
            'asset_amount': org_data.get('asset_amount', 0),
            'income_amount': org_data.get('income_amount', 0),
            'revenue_amount': org_data.get('revenue_amount', 0),
            'ntee_code': org_data.get('ntee_code', ''),
            'subsection': org_data.get('subsection', ''),
            'foundation_code': org_data.get('foundation_code', ''),
            'pf_filing_req_cd': org_data.get('pf_filing_req_cd', ''),
            'data_source': 'ProPublica Nonprofit Explorer',
            'website': '',  # To be filled later if needed
            'email': '',    # To be filled later if needed
            'contact_discovery_status': 'pending'
        }
    
    def fetch_organizations_batch(self, search_term, limit=100):
        """Fetch and process a batch of organizations"""
        organizations = self.search_propublica(search_term, limit)
        new_count = 0
        
        for org_data in organizations:
            sponsor_record = self.convert_to_sponsor_record(org_data)
            
            # Check for duplicates by EIN
            ein = sponsor_record.get('ein', '')
            if ein and not any(record.get('ein') == ein for record in self.collected_data):
                self.collected_data.append(sponsor_record)
                new_count += 1
                
        return new_count
    
    def save_progress(self, filename):
        """Save current progress to CSV"""
        if self.collected_data:
            df = pd.DataFrame(self.collected_data)
            df.to_csv(filename, index=False)
            print(f"Progress saved: {len(self.collected_data)} organizations to {filename}")
            self.logger.info(f"Progress saved: {len(self.collected_data)} organizations to {filename}")
            return filename
        return None
    
    def harvest_maximum_data(self, max_hours=24):
        """Harvest maximum data within time limit"""
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=max_hours)
        
        total_terms = len(self.search_terms)
        current_term = 0
        
        print(f"Starting fast harvest for {max_hours} hours")
        print(f"Will search {total_terms} terms")
        self.logger.info(f"Starting fast harvest for {max_hours} hours with {total_terms} terms")
        
        try:
            for search_term in self.search_terms:
                current_term += 1
                
                if datetime.now() >= end_time:
                    print("Time limit reached!")
                    break
                    
                print(f"[{current_term}/{total_terms}] Searching: '{search_term}'")
                
                # Fetch batch
                new_orgs = self.fetch_organizations_batch(search_term, limit=100)
                
                print(f"Added {new_orgs} new organizations (Total: {len(self.collected_data)})")
                
                # Save progress every 10 terms
                if current_term % 10 == 0:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    progress_file = f"fast_harvest_progress_{timestamp}.csv"
                    self.save_progress(progress_file)
                
                # Respectful delay
                time.sleep(self.request_delay)
                    
        except KeyboardInterrupt:
            print("\nHarvest interrupted by user")
            self.logger.info("Harvest interrupted by user")
        
        # Final save
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        final_file = f"propublica_sponsors_fast_harvest_{timestamp}.csv"
        self.save_progress(final_file)
        
        elapsed = datetime.now() - start_time
        print(f"\nFast harvest completed!")
        print(f"Time elapsed: {elapsed}")
        print(f"Total organizations collected: {len(self.collected_data)}")
        print(f"Final file: {final_file}")
        
        self.logger.info(f"Fast harvest completed in {elapsed}")
        self.logger.info(f"Total organizations collected: {len(self.collected_data)}")
        
        return final_file

def main():
    print("=" * 60)
    print("FAST PROPUBLICA SPONSOR HARVESTER")
    print("=" * 60)
    print("1. Test run (5 minutes)")
    print("2. Full harvest (24 hours)")
    print("3. Custom duration")
    print("=" * 60)
    
    try:
        choice = input("Select option (1-3): ").strip()
        
        harvester = FastProPublicaHarvester()
        
        if choice == '1':
            duration = 5/60  # 5 minutes in hours
            print(f"Starting 5-minute test run...")
        elif choice == '2':
            duration = 24
            print(f"Starting 24-hour full harvest...")
        elif choice == '3':
            hours = float(input("Enter duration in hours: "))
            duration = hours
            print(f"Starting {hours}-hour harvest...")
        else:
            print("Invalid choice. Starting 5-minute test...")
            duration = 5/60
        
        output_file = harvester.harvest_maximum_data(max_hours=duration)
        print(f"\nHarvest complete! Data saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        return

if __name__ == "__main__":
    main()