#!/usr/bin/env python3
"""
Simple Website and Email Discovery for Sponsors
Direct approach using Google search and email extraction
"""

import pandas as pd
import requests
import time
import re
from urllib.parse import urlparse
import logging

class SimpleContactFinder:
    """
    Simple contact finder using direct search approaches
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def find_website_simple(self, org_name, city="", state=""):
        """
        Simple website discovery using known patterns
        """
        try:
            # Try common website patterns first
            org_clean = re.sub(r'[^a-zA-Z0-9\s]', '', org_name.lower())
            org_words = org_clean.split()
            
            # Common foundation website patterns
            possible_domains = []
            
            if len(org_words) >= 2:
                # Try: firstwordlastword.org, firstword-lastword.org, etc.
                possible_domains.extend([
                    f"{org_words[0]}{org_words[-1]}.org",
                    f"{org_words[0]}-{org_words[-1]}.org", 
                    f"{org_words[0]}{org_words[-1]}.com",
                    f"{''.join(org_words[:2])}.org",
                    f"{org_words[0]}foundation.org"
                ])
            
            # Test each possible domain
            for domain in possible_domains:
                url = f"https://{domain}"
                try:
                    response = self.session.head(url, timeout=5)
                    if response.status_code == 200:
                        self.logger.info(f"✅ Found website: {url}")
                        return url
                except:
                    continue
            
            # If direct patterns fail, try a simple Google search approach
            return self._google_search_website(org_name, city, state)
            
        except Exception as e:
            self.logger.error(f"Website search error: {e}")
            return ""
    
    def _google_search_website(self, org_name, city, state):
        """
        Simple Google search for organization website
        """
        try:
            # Use Google search via requests
            query = f'"{org_name}" official website {state}'
            url = "https://www.google.com/search"
            params = {
                'q': query,
                'num': 5
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                # Simple pattern matching for URLs in Google results
                url_pattern = r'https?://[^\s<>"]+(?:\.org|\.com|\.net)[^\s<>"]*'
                urls = re.findall(url_pattern, response.text)
                
                for url in urls[:5]:
                    if self._is_likely_official_site(url, org_name):
                        self.logger.info(f"🔍 Found via Google: {url}")
                        return url
            
            return ""
            
        except Exception as e:
            self.logger.error(f"Google search error: {e}")
            return ""
    
    def _is_likely_official_site(self, url, org_name):
        """
        Check if URL looks like official organization site
        """
        try:
            domain = urlparse(url).netloc.lower()
            org_words = org_name.lower().split()
            
            # Filter out social media and directory sites
            bad_sites = ['facebook', 'twitter', 'linkedin', 'youtube', 'wikipedia', 
                        'guidestar', 'charitynavigator', 'google', 'bing']
            
            if any(bad in domain for bad in bad_sites):
                return False
            
            # Check if org name appears in domain
            org_keywords = [word for word in org_words if len(word) > 3 and 
                           word not in ['foundation', 'fund', 'trust', 'inc', 'corp']]
            
            if org_keywords and any(keyword in domain for keyword in org_keywords):
                return True
            
            # Prefer .org domains for nonprofits
            if '.org' in domain and len(domain.split('.')) <= 3:
                return True
                
            return False
            
        except:
            return False
    
    def extract_emails_simple(self, url):
        """
        Extract emails from website using simple patterns
        """
        if not url:
            return []
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                # Find emails with regex
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, response.text, re.IGNORECASE)
                
                # Filter and prioritize
                good_emails = []
                for email in emails:
                    email = email.lower()
                    
                    # Skip unwanted emails
                    if any(bad in email for bad in ['noreply', 'webmaster', 'example', 'test']):
                        continue
                    
                    # Prefer contact/info emails
                    if any(good in email for good in ['contact', 'info', 'director', 'grants']):
                        good_emails.insert(0, email)  # Add to front
                    else:
                        good_emails.append(email)
                    
                    if len(good_emails) >= 3:
                        break
                
                # Remove duplicates while preserving order
                unique_emails = list(dict.fromkeys(good_emails))
                return unique_emails[:3]
        
        except Exception as e:
            self.logger.error(f"Email extraction error: {e}")
        
        return []
    
    def enhance_sponsors_simple(self, csv_file, max_records=10):
        """
        Simple enhancement of sponsor data
        """
        self.logger.info(f"📁 Reading: {csv_file}")
        df = pd.read_csv(csv_file)
        
        if max_records:
            df = df.head(max_records)
        
        enhanced_count = 0
        
        for index, row in df.iterrows():
            org_name = row.get('sponsor_name', '')
            city = row.get('city', '')
            state = row.get('state', '')
            
            self.logger.info(f"🔍 [{index+1}] {org_name}")
            
            # Find website
            website = self.find_website_simple(org_name, city, state)
            
            # Find emails
            emails = []
            if website:
                time.sleep(1)  # Be polite
                emails = self.extract_emails_simple(website)
            
            # Update data
            df.at[index, 'website'] = website
            df.at[index, 'email'] = emails[0] if emails else ''
            df.at[index, 'all_emails'] = '; '.join(emails) if emails else ''
            
            if website or emails:
                enhanced_count += 1
                self.logger.info(f"✅ Found: Website={bool(website)}, Emails={len(emails)}")
            else:
                self.logger.info(f"⚠️ No contacts found")
        
        # Save enhanced data
        output_file = csv_file.replace('.csv', '_with_contacts.csv')
        df.to_csv(output_file, index=False)
        
        self.logger.info(f"\n🎉 Enhanced {enhanced_count}/{len(df)} records")
        self.logger.info(f"💾 Saved to: {output_file}")
        
        return output_file

def main():
    """Test the simple contact finder"""
    finder = SimpleContactFinder()
    
    # Test with our ProPublica data
    output_file = finder.enhance_sponsors_simple(
        'data/input/test_propublica_sponsors.csv', 
        max_records=5
    )
    
    print(f"\n✅ Contact enhancement complete!")
    print(f"📧 Enhanced file: {output_file}")
    
    # Show results
    df = pd.read_csv(output_file)
    print("\n📋 Results sample:")
    for _, row in df.head(3).iterrows():
        print(f"• {row['sponsor_name']}: {row.get('website', 'No website')} | {row.get('email', 'No email')}")

if __name__ == "__main__":
    main()