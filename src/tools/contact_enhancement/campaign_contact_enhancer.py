#!/usr/bin/env python3
"""
Enhanced Contact Discovery for High-Priority Sponsors
Focused tool to enhance contact information for campaign outreach
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(f'contact_enhancement_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CampaignContactEnhancer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.request_delay = 1.0  # Respectful rate limiting
        
    def find_website_patterns(self, org_name, city, state):
        """Try common website patterns for organizations"""
        patterns = [
            f"{org_name.lower().replace(' ', '').replace('foundation', '').replace('trust', '').replace('fund', '')}.org",
            f"{org_name.lower().replace(' ', '').replace('foundation', '').replace('trust', '').replace('fund', '')}.com", 
            f"{org_name.lower().replace(' ', '')}.org",
            f"{org_name.lower().replace(' ', '')}.com",
            f"www.{org_name.lower().replace(' ', '').replace('foundation', '').replace('trust', '').replace('fund', '')}.org"
        ]
        
        for pattern in patterns:
            # Clean up the pattern
            pattern = re.sub(r'[^a-z0-9.-]', '', pattern)
            if len(pattern) > 5:  # Must be reasonable length
                try:
                    url = f"https://{pattern}"
                    response = self.session.head(url, timeout=5, allow_redirects=True)
                    if response.status_code == 200:
                        logger.info(f"Found website via pattern: {url}")
                        return url
                except:
                    continue
        
        return None
    
    def search_duckduckgo(self, query):
        """Search DuckDuckGo for organization website"""
        try:
            search_url = "https://html.duckduckgo.com/html/"
            params = {'q': query}
            
            response = self.session.get(search_url, params=params, timeout=10)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for result links
            for link in soup.find_all('a', class_='result__a'):
                href = link.get('href', '')
                if href and ('foundation' in href.lower() or any(word in href.lower() for word in query.lower().split())):
                    # Extract actual URL from DuckDuckGo redirect
                    if href.startswith('/l/?uddg='):
                        continue
                    if href.startswith('http'):
                        logger.info(f"Found website via search: {href}")
                        return href
            
            return None
        except Exception as e:
            logger.error(f"Search error: {e}")
            return None
    
    def extract_emails_from_website(self, website_url):
        """Extract email addresses from a website"""
        try:
            response = self.session.get(website_url, timeout=10)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            
            # Email regex pattern
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            
            # Filter out common unwanted emails
            filtered_emails = []
            unwanted = ['example.com', 'test.com', 'lorem', 'ipsum', 'noreply', 'no-reply']
            
            for email in emails:
                if not any(word in email.lower() for word in unwanted):
                    if email not in filtered_emails:
                        filtered_emails.append(email)
            
            return filtered_emails[:3]  # Return up to 3 emails
            
        except Exception as e:
            logger.error(f"Email extraction error: {e}")
            return []
    
    def enhance_sponsor_contacts(self, sponsor_name, city, state):
        """Find website and email for a sponsor"""
        logger.info(f"Enhancing: {sponsor_name}")
        
        website = None
        emails = []
        
        # Try pattern matching first (faster)
        website = self.find_website_patterns(sponsor_name, city, state)
        
        # If no pattern match, try search
        if not website:
            search_query = f'"{sponsor_name}" {city} {state} official website'
            website = self.search_duckduckgo(search_query)
        
        # Extract emails from website if found
        if website:
            time.sleep(self.request_delay)
            emails = self.extract_emails_from_website(website)
            logger.info(f"Found: Website={bool(website)}, Emails={len(emails)}")
        else:
            logger.info("No website found")
        
        return {
            'website': website or '',
            'email': emails[0] if emails else '',
            'all_emails': '; '.join(emails) if emails else ''
        }
    
    def enhance_campaign_file(self, input_file, output_file, max_records=50):
        """Enhance contacts for high-priority sponsors"""
        logger.info(f"Loading sponsors from: {input_file}")
        
        df = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df)} sponsors")
        
        # Limit to max_records for efficiency
        df_subset = df.head(max_records)
        logger.info(f"Enhancing top {len(df_subset)} sponsors...")
        
        enhanced_count = 0
        
        # Add contact columns if they don't exist
        for col in ['website', 'email', 'all_emails']:
            if col not in df_subset.columns:
                df_subset[col] = ''
        
        for index, row in df_subset.iterrows():
            sponsor_name = row['sponsor_name']
            city = row.get('city', '')
            state = row.get('state', '')
            
            # Skip if already has meaningful contacts
            existing_website = row.get('website', '')
            existing_email = row.get('email', '')
            
            # Check for meaningful data (not empty, not NaN, not 'nan')
            has_website = existing_website and str(existing_website).lower() not in ['', 'nan', 'none']
            has_email = existing_email and str(existing_email).lower() not in ['', 'nan', 'none']
            
            if has_website and has_email:
                logger.info(f"Skipping {sponsor_name} - already has contacts")
                continue
            
            # Enhance contacts
            contacts = self.enhance_sponsor_contacts(sponsor_name, city, state)
            
            # Update the dataframe
            for field, value in contacts.items():
                df_subset.at[index, field] = value
            
            if contacts['website'] or contacts['email']:
                enhanced_count += 1
            
            # Rate limiting
            time.sleep(self.request_delay)
        
        # Save enhanced data
        df_subset.to_csv(output_file, index=False)
        logger.info(f"Enhanced {enhanced_count}/{len(df_subset)} records")
        logger.info(f"Saved to: {output_file}")
        
        return output_file

def main():
    print("=" * 60)
    print("CAMPAIGN CONTACT ENHANCEMENT")
    print("=" * 60)
    print("1. Enhance high-priority sponsors (top 50)")
    print("2. Enhance all high-priority sponsors")
    print("3. Custom enhancement")
    print("=" * 60)
    
    enhancer = CampaignContactEnhancer()
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == '1':
        input_file = 'data/input/high_priority_sponsors.csv'
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'data/input/high_priority_enhanced_{timestamp}.csv'
        
        enhancer.enhance_campaign_file(input_file, output_file, max_records=50)
        
    elif choice == '2':
        input_file = 'data/input/high_priority_sponsors.csv'
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'data/input/high_priority_enhanced_full_{timestamp}.csv'
        
        enhancer.enhance_campaign_file(input_file, output_file, max_records=200)
        
    elif choice == '3':
        input_file = input("Enter input CSV file path: ").strip()
        output_file = input("Enter output CSV file path: ").strip()
        max_records = int(input("Enter max records to enhance: "))
        
        enhancer.enhance_campaign_file(input_file, output_file, max_records)
    
    else:
        print("Invalid choice")
        return
    
    print(f"\n✅ Contact enhancement complete!")
    print(f"📧 Enhanced file: {output_file}")

if __name__ == "__main__":
    main()