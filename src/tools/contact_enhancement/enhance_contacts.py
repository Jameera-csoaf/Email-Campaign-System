#!/usr/bin/env python3
"""
Contact Enhancement Script for ProPublica Sponsor Data
Takes existing CSV data and enhances it with websites and email addresses

This script:
1. Reads existing ProPublica sponsor data
2. Discovers official websites for each organization  
3. Extracts email addresses from websites
4. Updates the CSV with contact information
5. Prepares data for email outreach campaigns
"""

import pandas as pd
import requests
import time
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import logging
from datetime import datetime

class ContactEnhancer:
    """
    Enhance sponsor data with website and email contact information
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.request_delay = 2.0  # Be respectful to websites
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def discover_website(self, org_name, city, state):
        """
        Discover organization's official website using search
        """
        try:
            # Try multiple search strategies
            search_queries = [
                f'"{org_name}" {city} {state} official website',
                f'"{org_name}" {state} foundation contact',
                f'{org_name.replace(" Foundation", "")} {state} org'
            ]
            
            for query in search_queries:
                website = self._search_for_website(query, org_name)
                if website:
                    return website
            
            return ""
            
        except Exception as e:
            self.logger.error(f"Website discovery error for {org_name}: {e}")
            return ""
    
    def _search_for_website(self, query, org_name):
        """
        Search for website using DuckDuckGo
        """
        try:
            search_url = "https://html.duckduckgo.com/html/"
            params = {'q': query}
            
            response = self.session.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find search result links
                result_links = soup.find_all('a', href=True)
                
                for link in result_links[:5]:  # Check first 5 results
                    href = link.get('href')
                    if href and self._is_valid_website(href, org_name):
                        return href
            
            return ""
            
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            return ""
    
    def _is_valid_website(self, url, org_name):
        """
        Check if URL is likely the official website
        """
        try:
            if not url.startswith('http'):
                return False
            
            domain = urlparse(url).netloc.lower()
            org_words = org_name.lower().split()
            
            # Remove common foundation words
            org_words = [word for word in org_words if word not in 
                        ['foundation', 'inc', 'corporation', 'fund', 'trust', 'the', 'and', 'of', 'for', 'llc']]
            
            # Check if organization name appears in domain
            if len(org_words) > 0:
                for word in org_words:
                    if len(word) > 3 and word in domain:
                        return True
            
            # Avoid unwanted sites
            unwanted_sites = ['facebook', 'twitter', 'linkedin', 'instagram', 'youtube', 
                            'guidestar', 'charitynavigator', 'wikipedia', 'amazon', 'ebay']
            
            if any(site in domain for site in unwanted_sites):
                return False
            
            return True
            
        except:
            return False
    
    def extract_emails(self, url):
        """
        Extract email addresses from website
        """
        try:
            if not url:
                return []
            
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                return []
            
            # Look for emails in multiple page sections
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try contact page first
            contact_links = soup.find_all('a', href=True)
            contact_page_url = None
            
            for link in contact_links:
                href = link.get('href', '').lower()
                text = link.get_text().lower()
                
                if any(word in href for word in ['contact', 'about', 'staff']) or \
                   any(word in text for word in ['contact', 'about us', 'staff']):
                    if href.startswith('/'):
                        contact_page_url = urljoin(url, href)
                    elif href.startswith('http'):
                        contact_page_url = href
                    break
            
            # Extract emails from main page and contact page
            all_text = response.text
            
            if contact_page_url:
                try:
                    time.sleep(1)  # Brief delay
                    contact_response = self.session.get(contact_page_url, timeout=10)
                    if contact_response.status_code == 200:
                        all_text += contact_response.text
                except:
                    pass  # If contact page fails, continue with main page
            
            # Extract emails using regex
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, all_text)
            
            # Filter and prioritize emails
            filtered_emails = []
            unwanted = ['noreply', 'no-reply', 'donotreply', 'webmaster', 'admin@example', 
                       'test@', 'support@', 'sales@', 'marketing@', 'spam@', 'abuse@']
            
            # Prioritize certain email types
            priority_emails = []
            regular_emails = []
            
            for email in emails:
                email = email.lower().strip()
                
                # Skip unwanted emails
                if any(pattern in email for pattern in unwanted):
                    continue
                
                # Skip duplicates
                if email in filtered_emails:
                    continue
                
                # Prioritize contact, info, development, grants emails
                if any(word in email for word in ['contact', 'info', 'development', 'grants', 'giving', 'director']):
                    priority_emails.append(email)
                else:
                    regular_emails.append(email)
                
                if len(priority_emails) + len(regular_emails) >= 5:
                    break
            
            # Combine prioritized emails first
            filtered_emails = priority_emails + regular_emails
            
            return filtered_emails[:3]  # Return top 3 emails
            
        except Exception as e:
            self.logger.error(f"Email extraction error for {url}: {e}")
            return []
    
    def enhance_contact_data(self, input_file, output_file=None, max_records=None):
        """
        Enhance existing CSV data with contact information
        """
        if output_file is None:
            output_file = input_file.replace('.csv', '_enhanced.csv')
        
        self.logger.info(f"📁 Reading data from: {input_file}")
        
        # Read existing data
        df = pd.read_csv(input_file)
        
        if max_records:
            df = df.head(max_records)
            self.logger.info(f"🎯 Processing first {max_records} records for testing")
        
        enhanced_count = 0
        total_records = len(df)
        
        self.logger.info(f"🚀 Starting contact enhancement for {total_records} records...")
        
        for index, row in df.iterrows():
            try:
                org_name = row.get('sponsor_name', '')
                city = row.get('city', '')
                state = row.get('state', '')
                
                # Skip if already has contact info
                if pd.notna(row.get('website', '')) and row.get('website', '') != '':
                    continue
                
                self.logger.info(f"🔍 [{index+1}/{total_records}] Processing: {org_name}")
                
                # Discover website
                website = self.discover_website(org_name, city, state)
                df.at[index, 'website'] = website
                
                # Extract emails
                emails = []
                if website:
                    time.sleep(self.request_delay)  # Be respectful
                    emails = self.extract_emails(website)
                
                # Update email fields
                df.at[index, 'email'] = emails[0] if emails else ''
                df.at[index, 'all_emails'] = '; '.join(emails) if emails else ''
                df.at[index, 'contact_discovery_status'] = 'completed'
                df.at[index, 'contact_enhanced_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                if website or emails:
                    enhanced_count += 1
                    self.logger.info(f"✅ Enhanced {org_name}: Website={bool(website)}, Emails={len(emails)}")
                else:
                    self.logger.info(f"⚠️ No contacts found for {org_name}")
                
                # Save progress every 10 records
                if (index + 1) % 10 == 0:
                    df.to_csv(output_file, index=False)
                    self.logger.info(f"💾 Progress saved: {index+1}/{total_records} processed")
                
            except Exception as e:
                self.logger.error(f"❌ Error processing {org_name}: {e}")
                df.at[index, 'contact_discovery_status'] = 'failed'
        
        # Final save
        df.to_csv(output_file, index=False)
        
        self.logger.info(f"\n🎉 ENHANCEMENT COMPLETE!")
        self.logger.info(f"📊 Total records processed: {total_records}")
        self.logger.info(f"✅ Records enhanced: {enhanced_count}")
        self.logger.info(f"💾 Enhanced data saved to: {output_file}")
        
        return output_file

def main():
    """
    Run contact enhancement on ProPublica data
    """
    print("🚀 ProPublica Contact Enhancement Tool")
    print("📧 Discovers websites and email addresses for sponsor outreach")
    print("="*60)
    
    # Get input file
    input_file = input("Enter CSV file path (or press Enter for test file): ").strip()
    if not input_file:
        input_file = "data/input/test_propublica_sponsors.csv"
    
    # Get number of records to process
    max_records_input = input("Max records to process (Enter for all, or number for testing): ").strip()
    max_records = None
    if max_records_input.isdigit():
        max_records = int(max_records_input)
    
    print(f"📁 Processing: {input_file}")
    if max_records:
        print(f"🎯 Limiting to: {max_records} records")
    
    # Initialize enhancer and run
    enhancer = ContactEnhancer()
    output_file = enhancer.enhance_contact_data(input_file, max_records=max_records)
    
    print(f"\n✅ Enhancement complete!")
    print(f"📧 Enhanced data ready for email campaigns: {output_file}")

if __name__ == "__main__":
    main()