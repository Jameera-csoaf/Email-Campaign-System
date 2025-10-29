#!/usr/bin/env python3
"""
Fortune 100 Corporation Data Scraper
Focuses on NY/CA companies with sponsorship history analysis
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from datetime import datetime
import json
import re
from urllib.parse import urljoin, urlparse
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class Fortune100Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Fortune 100 companies with NY/CA presence (sample list)
        self.target_companies = [
            # NY-based or major NY presence
            {'name': 'JPMorgan Chase', 'ticker': 'JPM', 'hq_city': 'New York', 'state': 'NY'},
            {'name': 'Citigroup', 'ticker': 'C', 'hq_city': 'New York', 'state': 'NY'},
            {'name': 'Goldman Sachs', 'ticker': 'GS', 'hq_city': 'New York', 'state': 'NY'},
            {'name': 'Morgan Stanley', 'ticker': 'MS', 'hq_city': 'New York', 'state': 'NY'},
            {'name': 'American Express', 'ticker': 'AXP', 'hq_city': 'New York', 'state': 'NY'},
            {'name': 'MetLife', 'ticker': 'MET', 'hq_city': 'New York', 'state': 'NY'},
            {'name': 'Pfizer', 'ticker': 'PFE', 'hq_city': 'New York', 'state': 'NY'},
            {'name': 'IBM', 'ticker': 'IBM', 'hq_city': 'Armonk', 'state': 'NY'},
            {'name': 'Mastercard', 'ticker': 'MA', 'hq_city': 'Purchase', 'state': 'NY'},
            {'name': 'Colgate-Palmolive', 'ticker': 'CL', 'hq_city': 'New York', 'state': 'NY'},
            
            # CA-based companies
            {'name': 'Apple', 'ticker': 'AAPL', 'hq_city': 'Cupertino', 'state': 'CA'},
            {'name': 'Alphabet', 'ticker': 'GOOGL', 'hq_city': 'Mountain View', 'state': 'CA'},
            {'name': 'Meta', 'ticker': 'META', 'hq_city': 'Menlo Park', 'state': 'CA'},
            {'name': 'Tesla', 'ticker': 'TSLA', 'hq_city': 'Austin', 'state': 'TX', 'ca_presence': True},
            {'name': 'Netflix', 'ticker': 'NFLX', 'hq_city': 'Los Gatos', 'state': 'CA'},
            {'name': 'Intel', 'ticker': 'INTC', 'hq_city': 'Santa Clara', 'state': 'CA'},
            {'name': 'Cisco', 'ticker': 'CSCO', 'hq_city': 'San Jose', 'state': 'CA'},
            {'name': 'Oracle', 'ticker': 'ORCL', 'hq_city': 'Austin', 'state': 'TX', 'ca_presence': True},
            {'name': 'Salesforce', 'ticker': 'CRM', 'hq_city': 'San Francisco', 'state': 'CA'},
            {'name': 'Adobe', 'ticker': 'ADBE', 'hq_city': 'San Jose', 'state': 'CA'},
            {'name': 'Broadcom', 'ticker': 'AVGO', 'hq_city': 'San Jose', 'state': 'CA'},
            {'name': 'Qualcomm', 'ticker': 'QCOM', 'hq_city': 'San Diego', 'state': 'CA'},
            {'name': 'Advanced Micro Devices', 'ticker': 'AMD', 'hq_city': 'Santa Clara', 'state': 'CA'},
            {'name': 'Nvidia', 'ticker': 'NVDA', 'hq_city': 'Santa Clara', 'state': 'CA'},
            {'name': 'PayPal', 'ticker': 'PYPL', 'hq_city': 'San Jose', 'state': 'CA'},
        ]
        
        # Arts/education sponsorship keywords
        self.sponsorship_keywords = [
            'arts education', 'arts program', 'educational sponsorship', 'community arts',
            'arts foundation', 'cultural program', 'music education', 'dance program',
            'visual arts', 'creative education', 'arts initiative', 'youth arts',
            'arts funding', 'cultural sponsorship', 'education grant', 'community education',
            'disability arts', 'inclusive arts', 'accessibility program', 'diverse education'
        ]

    def search_company_website(self, company_name):
        """Find company website URL"""
        try:
            search_query = f"{company_name} official website"
            search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            
            response = self.session.get(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for first organic result
            results = soup.find_all('a', href=True)
            for result in results:
                href = result['href']
                if '/url?q=' in href:
                    url = href.split('/url?q=')[1].split('&')[0]
                    if any(domain in url.lower() for domain in [company_name.lower().replace(' ', ''), '.com', '.org']):
                        return url
            
            # Fallback: construct likely URL
            company_domain = company_name.lower().replace(' ', '').replace('-', '').replace('.', '')
            return f"https://www.{company_domain}.com"
            
        except Exception as e:
            logger.error(f"Error finding website for {company_name}: {e}")
            return None

    def scrape_sponsorship_history(self, company_name, website_url):
        """Scrape company website for sponsorship and CSR information"""
        sponsorship_data = {
            'arts_sponsorships': [],
            'education_programs': [],
            'community_investments': [],
            'estimated_amounts': []
        }
        
        try:
            if not website_url:
                return sponsorship_data
                
            # Try common CSR/sponsorship page patterns
            csr_paths = [
                '/sustainability', '/csr', '/corporate-responsibility', 
                '/community', '/giving', '/foundation', '/social-impact',
                '/citizenship', '/responsibility', '/community-investment',
                '/about/community', '/about/giving', '/newsroom'
            ]
            
            for path in csr_paths:
                try:
                    full_url = urljoin(website_url, path)
                    response = self.session.get(full_url, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        text_content = soup.get_text().lower()
                        
                        # Search for arts/education sponsorship mentions
                        for keyword in self.sponsorship_keywords:
                            if keyword in text_content:
                                # Extract surrounding context
                                sentences = self.extract_context(soup, keyword)
                                sponsorship_data['arts_sponsorships'].extend(sentences)
                        
                        # Look for dollar amounts mentioned
                        amounts = self.extract_dollar_amounts(text_content)
                        sponsorship_data['estimated_amounts'].extend(amounts)
                        
                        # Extract program names
                        programs = self.extract_program_names(soup)
                        sponsorship_data['education_programs'].extend(programs)
                        
                        time.sleep(random.uniform(1, 3))  # Be respectful
                        
                except Exception as e:
                    logger.debug(f"Error accessing {full_url}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping sponsorship for {company_name}: {e}")
            
        return sponsorship_data

    def extract_context(self, soup, keyword):
        """Extract sentences containing sponsorship keywords"""
        contexts = []
        text_elements = soup.find_all(['p', 'div', 'span', 'li'])
        
        for element in text_elements:
            text = element.get_text().strip()
            if keyword in text.lower() and len(text) > 20:
                contexts.append(text[:200])  # First 200 chars
                
        return contexts[:3]  # Limit to 3 contexts per keyword

    def extract_dollar_amounts(self, text):
        """Extract dollar amounts from text"""
        # Pattern for dollar amounts: $X million, $X,XXX, etc.
        amount_patterns = [
            r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?',  # $1,000 or $1,000.00
            r'\$\d+(?:\.\d+)?\s*(?:million|billion|thousand)',  # $5 million
            r'\d+(?:\.\d+)?\s*(?:million|billion|thousand)\s*dollars'  # 5 million dollars
        ]
        
        amounts = []
        for pattern in amount_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            amounts.extend(matches)
            
        return amounts[:5]  # Limit to 5 amounts

    def extract_program_names(self, soup):
        """Extract program/initiative names"""
        programs = []
        
        # Look for headings that might be program names
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        for heading in headings:
            text = heading.get_text().strip()
            if any(word in text.lower() for word in ['program', 'initiative', 'fund', 'foundation', 'scholarship']):
                if len(text) < 100:  # Reasonable program name length
                    programs.append(text)
                    
        return programs[:5]  # Limit to 5 programs

    def estimate_sponsorship_capacity(self, company_info, sponsorship_data):
        """Estimate potential sponsorship amounts based on company size and history"""
        
        # Base estimates by company type/size (Fortune 100)
        base_estimates = {
            'tech': {'min': 10000, 'max': 500000, 'typical': 50000},
            'finance': {'min': 15000, 'max': 300000, 'typical': 75000},
            'healthcare': {'min': 5000, 'max': 200000, 'typical': 30000},
            'retail': {'min': 5000, 'max': 150000, 'typical': 25000},
            'default': {'min': 10000, 'max': 100000, 'typical': 25000}
        }
        
        # Classify company by industry (simplified)
        company_name = company_info['name'].lower()
        if any(tech in company_name for tech in ['apple', 'google', 'meta', 'tesla', 'netflix', 'intel', 'cisco', 'oracle', 'salesforce', 'adobe', 'nvidia']):
            category = 'tech'
        elif any(fin in company_name for fin in ['jpmorgan', 'citigroup', 'goldman', 'morgan', 'express']):
            category = 'finance'
        elif any(health in company_name for health in ['pfizer', 'metlife']):
            category = 'healthcare'
        else:
            category = 'default'
            
        estimates = base_estimates[category]
        
        # Adjust based on sponsorship history
        if sponsorship_data['arts_sponsorships']:
            estimates['typical'] = int(estimates['typical'] * 1.5)  # More likely to sponsor
            
        if sponsorship_data['estimated_amounts']:
            estimates['typical'] = int(estimates['typical'] * 1.3)  # Has donation history
            
        return estimates

    def scrape_company_data(self, company_info):
        """Scrape comprehensive data for a single company"""
        logger.info(f"Scraping data for {company_info['name']}")
        
        # Find website
        website_url = self.search_company_website(company_info['name'])
        
        # Scrape sponsorship history
        sponsorship_data = self.scrape_sponsorship_history(company_info['name'], website_url)
        
        # Estimate sponsorship capacity
        capacity_estimates = self.estimate_sponsorship_capacity(company_info, sponsorship_data)
        
        # Compile complete record
        record = {
            'organization_name': company_info['name'],
            'organization_type': 'corporation',
            'ticker_symbol': company_info.get('ticker', ''),
            'city': company_info['hq_city'],
            'state': company_info['state'],
            'website': website_url,
            'industry_sector': self.classify_industry(company_info['name']),
            'arts_sponsorship_history': '; '.join(sponsorship_data['arts_sponsorships'][:3]),
            'education_programs': '; '.join(sponsorship_data['education_programs'][:3]),
            'estimated_min_sponsorship': capacity_estimates['min'],
            'estimated_max_sponsorship': capacity_estimates['max'],
            'estimated_typical_sponsorship': capacity_estimates['typical'],
            'sponsorship_evidence_count': len(sponsorship_data['arts_sponsorships']),
            'dollar_amounts_found': '; '.join(sponsorship_data['estimated_amounts'][:3]),
            'scraped_at': datetime.now().isoformat(),
            'data_quality_score': self.calculate_quality_score(sponsorship_data, website_url)
        }
        
        return record

    def classify_industry(self, company_name):
        """Classify company into industry sector"""
        name_lower = company_name.lower()
        
        if any(tech in name_lower for tech in ['apple', 'google', 'meta', 'tesla', 'netflix', 'intel', 'cisco', 'oracle', 'salesforce', 'adobe', 'nvidia', 'paypal']):
            return 'Technology'
        elif any(fin in name_lower for fin in ['jpmorgan', 'citigroup', 'goldman', 'morgan', 'express', 'mastercard']):
            return 'Financial Services'
        elif 'pfizer' in name_lower:
            return 'Healthcare'
        elif any(media in name_lower for media in ['netflix', 'meta']):
            return 'Media & Entertainment'
        else:
            return 'Other'

    def calculate_quality_score(self, sponsorship_data, website_url):
        """Calculate data quality score (0-100)"""
        score = 0
        
        if website_url:
            score += 20
        if sponsorship_data['arts_sponsorships']:
            score += 30
        if sponsorship_data['education_programs']:
            score += 20
        if sponsorship_data['estimated_amounts']:
            score += 20
        if len(sponsorship_data['arts_sponsorships']) >= 2:
            score += 10
            
        return min(score, 100)

    def run_full_scrape(self, max_companies=None):
        """Run complete scraping process for all target companies"""
        logger.info("Starting Fortune 100 corporation scraping for NY/CA companies")
        
        companies_to_process = self.target_companies
        if max_companies:
            companies_to_process = companies_to_process[:max_companies]
            
        results = []
        
        for i, company_info in enumerate(companies_to_process):
            try:
                logger.info(f"Processing {i+1}/{len(companies_to_process)}: {company_info['name']}")
                
                record = self.scrape_company_data(company_info)
                results.append(record)
                
                # Save intermediate results every 10 companies
                if (i + 1) % 10 == 0:
                    temp_df = pd.DataFrame(results)
                    temp_df.to_csv(f'corporations_temp_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', index=False)
                    logger.info(f"Saved intermediate results: {len(results)} companies processed")
                
                # Be respectful with delays
                time.sleep(random.uniform(3, 7))
                
            except Exception as e:
                logger.error(f"Error processing {company_info['name']}: {e}")
                continue
                
        # Save final results
        df = pd.DataFrame(results)
        output_file = f'corporations_fortune100_ny_ca_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(output_file, index=False)
        
        logger.info(f"Scraping complete! Processed {len(results)} companies")
        logger.info(f"Results saved to: {output_file}")
        
        return df

if __name__ == "__main__":
    scraper = Fortune100Scraper()
    
    # Run with first 10 companies for testing
    results_df = scraper.run_full_scrape(max_companies=10)
    print(f"Scraped {len(results_df)} companies")
    print(results_df[['organization_name', 'industry_sector', 'estimated_typical_sponsorship', 'data_quality_score']].head())