#!/usr/bin/env python3
"""
Enhanced Contact Discovery System
Comprehensive tools to find email addresses, websites, and contact information
for nonprofit organizations from ProPublica data
"""

import requests
import pandas as pd
import re
import time
import logging
from datetime import datetime
from urllib.parse import urljoin, urlparse
import json
from bs4 import BeautifulSoup
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'contact_enhancement_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

class WebsiteDiscoveryEngine:
    """Discovers organization websites and analyzes mission alignment using search engines and pattern matching"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # CSOAF Mission Keywords for Alignment Scoring
        self.mission_keywords = {
            'primary': {
                'arts education': 10,
                'creative education': 9,
                'art education': 10,
                'arts program': 8,
                'creative pathways': 10,
                'artistic enrichment': 9,
                'creative learning': 8,
                'arts access': 8,
                'accessibility': 7,
                'inclusive arts': 9
            },
            'disability_support': {
                'disabilities': 10,
                'special needs': 9,
                'inclusive education': 8,
                'adaptive arts': 9,
                'therapeutic arts': 8,
                'art therapy': 7,
                'special education': 7,
                'accessibility': 8,
                'adaptive learning': 7,
                'sensory learning': 6
            },
            'youth_development': {
                'youth development': 8,
                'children': 7,
                'teens': 6,
                'young minds': 8,
                'student empowerment': 8,
                'self-expression': 7,
                'creative development': 8,
                'cultural awareness': 6,
                'imagination': 6,
                'lifelong learning': 6
            },
            'community_education': {
                'community school': 9,
                'educational pathways': 8,
                'public schools': 7,
                'school partnerships': 7,
                'educational access': 8,
                'quality education': 7,
                'transforming lives': 8,
                'empowering students': 7,
                'community engagement': 6,
                'educational equity': 7
            }
        }
        
    def search_organization_website(self, org_name, city=None, state=None):
        """Search for organization website using multiple strategies"""
        
        try:
            # Strategy 1: Direct domain guessing
            website = self._guess_organization_domain(org_name)
            if website and self._verify_website(website):
                logger.info(f"Found website via domain guess: {website}")
                return website
            
            # Strategy 2: Google search simulation (using DuckDuckGo to avoid blocking)
            website = self._search_duckduckgo(org_name, city, state)
            if website:
                logger.info(f"Found website via search: {website}")
                return website
            
            # Strategy 3: Nonprofit directory search
            website = self._search_nonprofit_directories(org_name, city, state)
            if website:
                logger.info(f"Found website via directory: {website}")
                return website
                
            logger.warning(f"No website found for {org_name}")
            return None
            
        except Exception as e:
            logger.error(f"Error searching website for {org_name}: {str(e)}")
            return None
    
    def _guess_organization_domain(self, org_name):
        """Generate likely domain names for organization"""
        
        # Clean organization name
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', org_name.lower())
        clean_name = re.sub(r'\s+', '', clean_name)
        
        # Remove common words
        remove_words = ['foundation', 'fund', 'inc', 'incorporated', 'organization', 'org', 'company', 'co', 'the']
        for word in remove_words:
            clean_name = clean_name.replace(word, '')
        
        # Generate domain possibilities
        domain_possibilities = [
            f"{clean_name}.org",
            f"{clean_name}.com",
            f"{clean_name}foundation.org",
            f"{clean_name}fund.org",
            f"{org_name.split()[0].lower()}.org",
        ]
        
        # Test each possibility
        for domain in domain_possibilities:
            if len(domain) > 4:  # Minimum reasonable domain length
                test_url = f"https://{domain}"
                if self._verify_website(test_url):
                    return test_url
        
        return None
    
    def _verify_website(self, url):
        """Verify if a website exists and is valid"""
        try:
            response = self.session.head(url, timeout=10, allow_redirects=True)
            return response.status_code == 200
        except:
            return False
    
    def _search_duckduckgo(self, org_name, city, state):
        """Search DuckDuckGo for organization website"""
        try:
            # Build search query
            query = f'"{org_name}"'
            if city:
                query += f' "{city}"'
            if state:
                query += f' "{state}"'
            query += ' site:org OR site:com'
            
            # DuckDuckGo instant answer API (limited but doesn't require API key)
            search_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Check abstract URL
                if 'AbstractURL' in data and data['AbstractURL']:
                    return data['AbstractURL']
                
                # Check related topics
                if 'RelatedTopics' in data:
                    for topic in data['RelatedTopics']:
                        if 'FirstURL' in topic and topic['FirstURL']:
                            domain = urlparse(topic['FirstURL']).netloc
                            if 'org' in domain or 'com' in domain:
                                return topic['FirstURL']
            
            return None
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error for {org_name}: {str(e)}")
            return None
    
    def _search_nonprofit_directories(self, org_name, city, state):
        """Search nonprofit directories for organization info"""
        
        # This could be expanded to search:
        # - Guidestar
        # - CharityNavigator  
        # - Network for Good
        # - Local foundation directories
        
        # For now, we'll focus on the other strategies
        return None
    
    def analyze_mission_alignment(self, website_url, org_name):
        """Analyze mission alignment by scraping mission, vision, and about pages"""
        
        if not website_url:
            return {
                'mission_score': 0,
                'mission_text': '',
                'alignment_factors': [],
                'pages_analyzed': []
            }
        
        try:
            mission_data = {
                'mission_score': 0,
                'mission_text': '',
                'alignment_factors': [],
                'pages_analyzed': [],
                'grant_history': [],
                'program_areas': []
            }
            
            # Pages to check for mission information
            mission_pages = [
                '',  # Homepage
                '/about',
                '/about-us', 
                '/mission',
                '/vision',
                '/our-mission',
                '/what-we-do',
                '/programs',
                '/grants',
                '/giving',
                '/impact'
            ]
            
            total_score = 0
            pages_found = 0
            
            for page_path in mission_pages:
                page_url = urljoin(website_url, page_path)
                page_content = self._scrape_mission_page(page_url)
                
                if page_content:
                    pages_found += 1
                    mission_data['pages_analyzed'].append(page_path or 'homepage')
                    
                    # Analyze mission alignment
                    page_score, factors = self._calculate_mission_score(page_content)
                    total_score += page_score
                    mission_data['alignment_factors'].extend(factors)
                    
                    # Extract mission text (keep first substantial mission statement found)
                    if not mission_data['mission_text']:
                        mission_text = self._extract_mission_statement(page_content)
                        if mission_text:
                            mission_data['mission_text'] = mission_text
                    
                    # Extract grant/program information
                    grants = self._extract_grant_history(page_content)
                    programs = self._extract_program_areas(page_content)
                    
                    mission_data['grant_history'].extend(grants)
                    mission_data['program_areas'].extend(programs)
                
                # Rate limiting
                time.sleep(0.5)
            
            # Calculate final mission score (average across pages, max 100)
            if pages_found > 0:
                mission_data['mission_score'] = min(100, total_score / pages_found)
            
            logger.info(f"Mission analysis for {org_name}: Score {mission_data['mission_score']:.1f}, {pages_found} pages analyzed")
            return mission_data
            
        except Exception as e:
            logger.error(f"Mission alignment analysis error for {org_name}: {str(e)}")
            return {
                'mission_score': 0,
                'mission_text': '',
                'alignment_factors': [],
                'pages_analyzed': [],
                'grant_history': [],
                'program_areas': []
            }
    
    def _scrape_mission_page(self, page_url):
        """Scrape text content from a mission-related page"""
        
        try:
            response = self.session.get(page_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text content
                text = soup.get_text()
                
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return text.lower()  # Convert to lowercase for keyword matching
            
        except Exception as e:
            logger.debug(f"Error scraping {page_url}: {str(e)}")
        
        return None
    
    def _calculate_mission_score(self, page_content):
        """Calculate mission alignment score based on keyword matching"""
        
        total_score = 0
        alignment_factors = []
        
        # Analyze each keyword category
        for category, keywords in self.mission_keywords.items():
            category_score = 0
            found_keywords = []
            
            for keyword, weight in keywords.items():
                # More flexible matching - check for keyword phrases and individual words
                if keyword in page_content:
                    category_score += weight
                    found_keywords.append(keyword)
                else:
                    # Check for partial matches (individual words in phrase)
                    keyword_words = keyword.split()
                    if len(keyword_words) > 1:
                        words_found = sum(1 for word in keyword_words if word in page_content)
                        if words_found >= len(keyword_words) * 0.6:  # At least 60% of words found
                            partial_weight = weight * (words_found / len(keyword_words))
                            category_score += partial_weight
                            found_keywords.append(f"{keyword} (partial: {words_found}/{len(keyword_words)} words)")
            
            if found_keywords:
                alignment_factors.append({
                    'category': category,
                    'keywords_found': found_keywords,
                    'category_score': category_score
                })
                total_score += category_score
        
        return total_score, alignment_factors
    
    def _extract_mission_statement(self, page_content):
        """Extract the organization's mission statement from page content"""
        
        # Look for mission statement patterns
        mission_patterns = [
            r'our mission[:\s]([^.]{50,300}\.)',
            r'mission[:\s]([^.]{50,300}\.)',
            r'we believe[:\s]([^.]{50,300}\.)',
            r'our purpose[:\s]([^.]{50,300}\.)',
            r'we strive to[:\s]([^.]{50,300}\.)',
            r'dedicated to[:\s]([^.]{50,300}\.)',
            r'committed to[:\s]([^.]{50,300}\.)'
        ]
        
        for pattern in mission_patterns:
            match = re.search(pattern, page_content, re.IGNORECASE | re.DOTALL)
            if match:
                mission_text = match.group(1).strip()
                # Clean up and return first reasonable mission statement
                if 30 < len(mission_text) < 500:
                    return mission_text
        
        return ""
    
    def _extract_grant_history(self, page_content):
        """Extract information about grants given or funding areas"""
        
        grants = []
        
        # Look for grant-related keywords and amounts
        grant_patterns = [
            r'grant[s]?\s+of\s+\$([0-9,]+)',
            r'funded\s+\$([0-9,]+)',
            r'awarded\s+\$([0-9,]+)',
            r'support[s]?\s+.*?education',
            r'support[s]?\s+.*?arts',
            r'funding\s+.*?programs',
            r'grants?\s+to\s+.*?schools',
            r'support[s]?\s+.*?disabilities'
        ]
        
        for pattern in grant_patterns:
            matches = re.findall(pattern, page_content, re.IGNORECASE)
            grants.extend(matches)
        
        return list(set(grants))  # Remove duplicates
    
    def _extract_program_areas(self, page_content):
        """Extract program areas and focus sectors"""
        
        programs = []
        
        # Look for program area keywords
        program_keywords = [
            'education', 'arts', 'health', 'community', 'youth', 'children', 
            'disabilities', 'accessibility', 'inclusion', 'learning', 'creative',
            'therapeutic', 'cultural', 'social services', 'mental health',
            'special needs', 'adaptive', 'inclusive', 'empowerment'
        ]
        
        for keyword in program_keywords:
            if keyword in page_content:
                programs.append(keyword)
        
        return programs

class EmailHarvestingEngine:
    """Extracts email addresses from discovered websites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Common email patterns
        self.email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
        ]
        
        # Contact page indicators
        self.contact_indicators = [
            'contact', 'about', 'staff', 'team', 'directory', 'leadership',
            'board', 'management', 'development', 'fundraising', 'grants'
        ]
    
    def harvest_emails_from_website(self, website_url, org_name):
        """Extract email addresses from organization website"""
        
        try:
            emails = set()
            
            # Get main page
            main_emails = self._extract_emails_from_page(website_url)
            emails.update(main_emails)
            
            # Find and check contact pages
            contact_pages = self._find_contact_pages(website_url)
            for page_url in contact_pages:
                page_emails = self._extract_emails_from_page(page_url)
                emails.update(page_emails)
                time.sleep(1)  # Be respectful
            
            # Filter and prioritize emails
            best_email = self._select_best_email(list(emails), org_name)
            
            return {
                'primary_email': best_email,
                'all_emails': list(emails),
                'contact_pages_found': len(contact_pages)
            }
            
        except Exception as e:
            logger.error(f"Error harvesting emails from {website_url}: {str(e)}")
            return {'primary_email': None, 'all_emails': [], 'contact_pages_found': 0}
    
    def _extract_emails_from_page(self, url):
        """Extract emails from a single page"""
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                return []
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text()
            
            # Find emails using patterns
            emails = set()
            for pattern in self.email_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                emails.update(matches)
            
            # Clean and validate emails
            valid_emails = []
            for email in emails:
                if self._is_valid_email(email):
                    valid_emails.append(email.lower())
            
            return valid_emails
            
        except Exception as e:
            logger.error(f"Error extracting emails from {url}: {str(e)}")
            return []
    
    def _find_contact_pages(self, base_url):
        """Find contact/about pages on website"""
        try:
            response = self.session.get(base_url, timeout=15)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            contact_pages = set()
            
            # Find links that might lead to contact pages
            for link in soup.find_all('a', href=True):
                href = link['href'].lower()
                link_text = link.get_text().lower()
                
                # Check if link text or href suggests contact page
                for indicator in self.contact_indicators:
                    if indicator in href or indicator in link_text:
                        full_url = urljoin(base_url, link['href'])
                        contact_pages.add(full_url)
                        break
            
            return list(contact_pages)[:5]  # Limit to 5 pages
            
        except Exception as e:
            logger.error(f"Error finding contact pages for {base_url}: {str(e)}")
            return []
    
    def _is_valid_email(self, email):
        """Validate email format and filter out common false positives"""
        if not email or len(email) < 5:
            return False
        
        # Basic email regex
        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        if not re.match(email_regex, email):
            return False
        
        # Filter out common false positives
        exclude_patterns = [
            r'example\.com', r'test\.com', r'yoursite\.com', r'domain\.com',
            r'email\.com', r'webmaster@', r'admin@', r'noreply@', r'no-reply@'
        ]
        
        for pattern in exclude_patterns:
            if re.search(pattern, email, re.IGNORECASE):
                return False
        
        return True
    
    def _select_best_email(self, emails, org_name):
        """Select the most likely primary contact email"""
        if not emails:
            return None
        
        # Priority order for email prefixes
        priority_prefixes = [
            'info@', 'contact@', 'hello@', 'inquiries@',
            'development@', 'fundraising@', 'grants@',
            'admin@', 'office@', 'mail@'
        ]
        
        # Check for priority emails first
        for prefix in priority_prefixes:
            for email in emails:
                if email.startswith(prefix):
                    return email
        
        # If no priority email found, return the first valid one
        return emails[0]

class EmailEstimationEngine:
    """Generates professional email guesses when harvesting fails"""
    
    def __init__(self):
        self.common_formats = [
            'info@{domain}',
            'contact@{domain}',
            'hello@{domain}',
            'inquiries@{domain}',
            'development@{domain}',
            'admin@{domain}'
        ]
    
    def estimate_emails(self, org_name, website=None):
        """Generate likely email addresses for organization"""
        
        estimated_emails = []
        
        if website:
            # Extract domain from website
            domain = urlparse(website).netloc
            if domain:
                for format_template in self.common_formats:
                    email = format_template.format(domain=domain)
                    estimated_emails.append(email)
        
        # Generate domain-based estimates
        domain_estimates = self._generate_domain_estimates(org_name)
        estimated_emails.extend(domain_estimates)
        
        return {
            'primary_estimate': estimated_emails[0] if estimated_emails else None,
            'all_estimates': estimated_emails[:6]  # Limit to top 6 guesses
        }
    
    def _generate_domain_estimates(self, org_name):
        """Generate domain estimates from organization name"""
        
        # Clean organization name
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', org_name.lower())
        clean_name = re.sub(r'\s+', '', clean_name)
        
        # Remove common words
        remove_words = ['foundation', 'fund', 'inc', 'incorporated', 'organization', 'org', 'company', 'co', 'the']
        for word in remove_words:
            clean_name = clean_name.replace(word, '')
        
        if not clean_name:
            return []
        
        # Generate domain possibilities
        domains = [
            f"{clean_name}.org",
            f"{clean_name}.com",
            f"{clean_name}foundation.org",
            f"{org_name.split()[0].lower()}.org"
        ]
        
        # Generate emails for each domain
        estimated_emails = []
        for domain in domains:
            if len(domain) > 4:
                estimated_emails.append(f"info@{domain}")
                estimated_emails.append(f"contact@{domain}")
        
        return estimated_emails

class ContactEnhancementPipeline:
    """Main pipeline for enhancing contact information"""
    
    def __init__(self):
        self.website_discovery = WebsiteDiscoveryEngine()
        self.email_harvesting = EmailHarvestingEngine()
        self.email_estimation = EmailEstimationEngine()
        
    def enhance_contact_data(self, df, max_records=None):
        """Enhance contact data for DataFrame of organizations"""
        
        logger.info(f"Starting contact enhancement for {len(df)} organizations")
        
        if max_records:
            df = df.head(max_records)
            logger.info(f"Limited to {max_records} records for testing")
        
        enhanced_data = []
        
        for idx, row in df.iterrows():
            org_name = row['sponsor_name']
            city = row.get('city', '')
            state = row.get('state', '')
            
            logger.info(f"Processing {idx+1}/{len(df)}: {org_name}")
            
            try:
                # Step 1: Find website
                website = self.website_discovery.search_organization_website(org_name, city, state)
                
                # Step 2: Harvest emails from website
                email_data = {'primary_email': None, 'all_emails': []}
                if website:
                    email_data = self.email_harvesting.harvest_emails_from_website(website, org_name)
                
                # Step 3: Generate email estimates if harvesting failed
                estimated_emails = {'primary_estimate': None, 'all_estimates': []}
                if not email_data['primary_email']:
                    estimated_emails = self.email_estimation.estimate_emails(org_name, website)
                
                # Step 4: Analyze mission alignment
                mission_data = self.website_discovery.analyze_mission_alignment(website, org_name)
                
                # Compile enhanced record
                enhanced_record = row.to_dict()
                enhanced_record.update({
                    'website': website or '',
                    'email': email_data['primary_email'] or estimated_emails['primary_estimate'] or '',
                    'email_source': 'harvested' if email_data['primary_email'] else 'estimated',
                    'all_emails_found': ','.join(email_data['all_emails']) if email_data['all_emails'] else '',
                    'estimated_emails': ','.join(estimated_emails['all_estimates']) if estimated_emails['all_estimates'] else '',
                    'contact_pages_found': email_data.get('contact_pages_found', 0),
                    'mission_alignment_score': mission_data['mission_score'],
                    'mission_text': mission_data['mission_text'][:500] if mission_data['mission_text'] else '',  # Limit length
                    'alignment_factors': json.dumps(mission_data['alignment_factors']) if mission_data['alignment_factors'] else '',
                    'pages_analyzed': ','.join(mission_data['pages_analyzed']) if mission_data['pages_analyzed'] else '',
                    'grant_history': ','.join(mission_data['grant_history'][:10]) if mission_data['grant_history'] else '',  # Limit to first 10
                    'program_areas': ','.join(mission_data['program_areas']) if mission_data['program_areas'] else '',
                    'enhanced_at': datetime.now().isoformat()
                })
                
                enhanced_data.append(enhanced_record)
                
                # Progress update
                if (idx + 1) % 10 == 0:
                    logger.info(f"Processed {idx + 1}/{len(df)} organizations")
                
                # Be respectful to websites
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error processing {org_name}: {str(e)}")
                
                # Add record with error info
                enhanced_record = row.to_dict()
                enhanced_record.update({
                    'website': '',
                    'email': '',
                    'email_source': 'error',
                    'mission_alignment_score': 0,
                    'mission_text': '',
                    'alignment_factors': '',
                    'pages_analyzed': '',
                    'grant_history': '',
                    'program_areas': '',
                    'error': str(e),
                    'enhanced_at': datetime.now().isoformat()
                })
                enhanced_data.append(enhanced_record)
        
        return pd.DataFrame(enhanced_data)

def main():
    """Main execution function"""
    
    print("🔍 ENHANCED CONTACT DISCOVERY SYSTEM")
    print("=" * 60)
    
    # Initialize pipeline
    pipeline = ContactEnhancementPipeline()
    
    # Load data to enhance
    input_files = [
        'campaigns/sponsor_data/intelligent_campaign_20251022_154639.csv',
        'campaigns/sponsor_data/high_priority_sponsors.csv'
    ]
    
    for input_file in input_files:
        if os.path.exists(input_file):
            logger.info(f"Processing {input_file}")
            
            # Load data
            df = pd.read_csv(input_file)
            logger.info(f"Loaded {len(df)} records from {input_file}")
            
            # Enhance contact data (start with top 20 for testing)
            enhanced_df = pipeline.enhance_contact_data(df, max_records=20)
            
            # Save enhanced data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = input_file.replace('.csv', f'_enhanced_{timestamp}.csv')
            enhanced_df.to_csv(output_file, index=False)
            
            logger.info(f"Enhanced data saved to: {output_file}")
            
            # Summary statistics
            websites_found = enhanced_df['website'].notna().sum()
            emails_found = enhanced_df['email'].notna().sum()
            
            print(f"\n📊 ENHANCEMENT RESULTS for {input_file}:")
            print(f"   • Records processed: {len(enhanced_df)}")
            print(f"   • Websites found: {websites_found} ({websites_found/len(enhanced_df)*100:.1f}%)")
            print(f"   • Emails found/estimated: {emails_found} ({emails_found/len(enhanced_df)*100:.1f}%)")
            print(f"   • Enhanced file: {output_file}")
            
        else:
            logger.warning(f"File not found: {input_file}")

if __name__ == "__main__":
    main()