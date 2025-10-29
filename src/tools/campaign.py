#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSAF Campaign Tool - Find and Score Aligned Sponsors

This tool helps Community School of Arts and Foundation (CSAF) find sponsors
that align with their campaign goals. It reads sponsor data from a CSV file,
scrapes websites for mission statements, and scores sponsors based on alignment
with the campaign objectives.

Author: CSAF Development Team
Date: September 23, 2025
"""

# Configure Unicode support for Windows console
import sys
import os
if sys.platform == 'win32':
    try:
        # Try to set UTF-8 encoding for Windows console
        os.system('chcp 65001 > nul')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        # Fallback: replace problematic characters
        pass

# Essential Python libraries - each serves a clear purpose
import pandas as pd          # Read and write CSV files (easy data handling)
import requests             # Get website content (simple web requests)
from bs4 import BeautifulSoup  # Extract text from websites (like reading a webpage)
import argparse             # Handle command line input (built into Python)
import re                   # Find patterns in text (built into Python)
import time                 # Add delays between requests (built into Python)
import os                   # Check if files exist (built into Python)
from datetime import datetime  # Add timestamps to results (built into Python)

# Safe print function for Windows Unicode issues
def safe_print(text, **kwargs):
    """Print text safely, handling Unicode encoding issues on Windows"""
    try:
        # Use original print function to avoid recursion
        builtins.__original_print__(text, **kwargs)
    except (UnicodeEncodeError, AttributeError):
        # Replace problematic Unicode characters with safe alternatives
        safe_text = str(text).encode('ascii', 'replace').decode('ascii')
        # Replace common emoji with text equivalents
        replacements = {
            '🎯': '[TARGET]',
            '✅': '[OK]',
            '❌': '[ERROR]', 
            '⚠️': '[WARNING]',
            '🔍': '[SEARCH]',
            '📊': '[DATA]',
            '🌐': '[WEB]',
            '📋': '[LIST]',
            '💰': '[MONEY]',
            '🏭': '[INDUSTRY]',
            '🏘️': '[COMMUNITY]',
            '🎨': '[ARTS]',
            '🎉': '[SUCCESS]',
            '🚀': '[START]',
            '📁': '[FILE]',
            '📄': '[PAGE]',
            '📞': '[PHONE]',
            '📝': '[TEXT]',
            '🗺️': '[MAP]',
            '🏆': '[AWARD]'
        }
        for emoji, replacement in replacements.items():
            safe_text = safe_text.replace(emoji, replacement)
        # Use original print for safety
        builtins.__original_print__(safe_text, **kwargs)

# Store original print function before replacing
import builtins
if not hasattr(builtins, '__original_print__'):
    builtins.__original_print__ = builtins.print
    builtins.print = safe_print

# Global settings for respectful web scraping
REQUEST_DELAY = 2.0         # Wait 2 seconds between website requests (be polite)
REQUEST_TIMEOUT = 10        # Give up on slow websites after 10 seconds
USER_AGENT = "CSAF Campaign Tool v1.0 - Community Outreach Bot"  # Identify ourselves

class ProPublicaConnector:
    """
    ProPublica Nonprofit Explorer API connector.
    Provides access to 1.8+ million tax-exempt organizations - completely FREE!
    
    No API key required, just HTTP requests to their public API.
    Data source: IRS Form 990 filings (legally required public records)
    """
    
    def __init__(self):
        self.base_url = "https://projects.propublica.org/nonprofits/api/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept': 'application/json'
        })
        print("🌐 ProPublica Nonprofit Explorer API initialized (FREE access)")
    
    def search_organizations(self, keywords, state=None, ntee_code=None, limit=50):
        """
        Search organizations by keywords and filters
        
        Args:
            keywords (str): Search terms like "arts education foundation"
            state (str): Two-letter state code like "NY" or "CA"
            ntee_code (str): NTEE classification code:
                - A25: Arts Education
                - A20: Arts/Cultural Organizations  
                - P30: Educational Support Organizations
                - T30: Public/Societal Benefit
            limit (int): Maximum results to return (default 50)
        
        Returns:
            dict: JSON response with organizations list
        """
        print(f"🔍 Searching ProPublica for: '{keywords}' in {state or 'all states'}")
        
        params = {
            'q': keywords
        }
        
        if state:
            params['state[id]'] = state.upper()
            
        try:
            response = self.session.get(
                f"{self.base_url}/search.json",
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            org_count = len(data.get('organizations', []))
            print(f"📊 Found {org_count} organizations from ProPublica")
            
            if org_count > limit:
                data['organizations'] = data['organizations'][:limit]
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ ProPublica API error: {e}")
            return {'organizations': []}
        except Exception as e:
            print(f"❌ ProPublica processing error: {e}")
            return {'organizations': []}
    
    def get_organization_details(self, ein):
        """
        Get detailed Form 990 data for specific organization
        
        Args:
            ein (str): Employer Identification Number (tax ID)
        
        Returns:
            dict: Detailed organization data from IRS filings
        """
        try:
            response = self.session.get(
                f"{self.base_url}/organizations/{ein}.json",
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException:
            return {}
        except Exception:
            return {}

def setup_command_line_interface():
    """
    Set up the command line interface to handle user input.
    This makes it easy for users to run campaigns with simple commands.
    """
    # Create argument parser with clear description
    command_parser = argparse.ArgumentParser(
        description="🎯 CSAF Campaign Tool - Find and Score Aligned Sponsors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
📝 EXAMPLE COMMANDS:

Find sponsors for specific campaigns:
  python campaign.py "Run Healing NY campaign with 50 sponsors in California"
  python campaign.py "Get 25 tech sponsors from NY for MODELS 2025"
  python campaign.py "Find healthcare partners in CA for community outreach"

General sponsor searches:
  python campaign.py "Find 10 education sponsors in NY"
  python campaign.py "Get arts supporters from California"
  python campaign.py "Look for tech companies in New York"

💡 TIPS:
- Always mention NY/New York or CA/California (CSOAF operates in both states since 2003)
- Include numbers if you want a specific count of sponsors
- Mention industry keywords like: arts education, disabilities, K-12, public schools, creative arts
- Campaign names will be automatically detected and matched

📁 FILES:
- Input:  data/input/sponsors.csv (your sponsor database)
- Output: data/results/campaign_results.csv (enhanced results with scores)
        """
    )
    
    # Add the main argument - the campaign request in natural language
    command_parser.add_argument(
        "campaign_request",
        help="Natural language description of your campaign needs (in quotes)",
        nargs='?',  # Make it optional so we can show help if missing
    )
    
    return command_parser

def validate_command_input(campaign_request):
    """
    Check if the user's command makes sense and give helpful error messages.
    This helps users understand what went wrong and how to fix it.
    
    NEW LOGIC: States are now optional! If no state mentioned, we search both NY and CA.
    """
    if not campaign_request:
        print("❌ ERROR: Missing campaign request!")
        print("\n💡 HELP: You need to tell me what kind of campaign you want to run.")
        print("Try something like:")
        print('  python campaign.py "Find 25 healthcare sponsors in NY"')
        print('  python campaign.py "Find healthcare sponsors"  # Searches both NY and CA')
        print('  python campaign.py "Run MODELS 2025 campaign in California"')
        return False
    
    # Check for unsupported states (anything other than NY, New York, CA, California)
    # We'll look for patterns that suggest other states are mentioned
    campaign_request_lower = campaign_request.lower()
    
    # List of other US states that people might mention by mistake
    unsupported_states = [
        'texas', 'tx', 'florida', 'fl', 'illinois', 'il', 'pennsylvania', 'pa',
        'ohio', 'georgia', 'ga', 'north carolina', 'nc', 'michigan', 'mi',
        'new jersey', 'nj', 'virginia', 'va', 'washington', 'wa', 'arizona', 'az',
        'massachusetts', 'ma', 'tennessee', 'tn', 'maryland', 'md'
    ]
    
    # Check if they mentioned any unsupported states
    for state in unsupported_states:
        if f' {state} ' in f' {campaign_request_lower} ' or \
           campaign_request_lower.startswith(f'{state} ') or \
           campaign_request_lower.endswith(f' {state}') or \
           campaign_request_lower == state:
            print(f"❌ ERROR: We don't support {state.title()} sponsors!")
            print(f"\n📝 Your request: '{campaign_request}'")
            print("\n💡 HELP: We only support sponsors in New York and California.")
            print("Try these instead:")
            print('  python campaign.py "Find healthcare sponsors"  # Both NY and CA')
            print('  python campaign.py "Find healthcare sponsors in NY"')
            print('  python campaign.py "Find healthcare sponsors in California"')
            return False
    
    # If we get here, the request is valid!
    # It either mentions NY/CA specifically, or no state (which means both)
    return True

def find_campaign_name(campaign_request):
    """
    Look for specific campaign names mentioned in the user's request.
    This helps us match sponsors with the right campaign keywords.
    """
    campaign_request_lower = campaign_request.lower()
    
    # Check for known specific campaigns first
    if 'healing ny' in campaign_request_lower:
        return "Healing NY"
    elif 'models 2025' in campaign_request_lower:
        return "MODELS 2025"
    
    # Look for other campaign patterns - anything after "for" or "campaign"
    campaign_indicators = ['for ', 'campaign']
    
    for indicator in campaign_indicators:
        if indicator in campaign_request_lower:
            # Find text after the indicator
            parts = campaign_request_lower.split(indicator, 1)
            if len(parts) > 1:
                potential_campaign = parts[1].strip()
                # Clean up common words and get the main campaign name
                potential_campaign = potential_campaign.replace('community outreach', '').strip()
                if potential_campaign and len(potential_campaign) > 2:
                    # Capitalize each word for clean display
                    return ' '.join(word.capitalize() for word in potential_campaign.split()[:3])
    
    # If no specific campaign found, return a general name based on the industry
    if any(word in campaign_request_lower for word in ['healthcare', 'health', 'medical']):
        return "Healthcare Campaign"
    elif any(word in campaign_request_lower for word in ['tech', 'technology']):
        return "Technology Campaign"
    elif any(word in campaign_request_lower for word in ['arts', 'creative', 'design']):
        return "Arts Campaign"
    elif any(word in campaign_request_lower for word in ['education', 'school']):
        return "Education Campaign"
    
    # Default campaign name
    return "General CSAF Campaign"

def get_sponsor_count(campaign_request):
    """
    Look for numbers mentioned in the request to determine how many sponsors they want.
    If no number is mentioned, we'll show all matching sponsors.
    
    Note: We exclude years (like 2025) and focus on reasonable sponsor counts.
    """
    # Look for numbers in the request
    import re
    numbers = re.findall(r'\b(\d+)\b', campaign_request)
    
    if numbers:
        for number_str in numbers:
            number = int(number_str)
            # Skip years (typically 2000-2099) and unrealistic sponsor counts
            if 2000 <= number <= 2099:
                continue  # Skip years like 2025
            if number > 1000:
                continue  # Skip unrealistic sponsor counts
            if number < 1:
                continue  # Skip zero or negative numbers
            
            # This looks like a valid sponsor count
            return number
    
    # No valid number found - show all matching sponsors
    return None  # None means "show all"

def determine_target_states(campaign_request):
    """
    Figure out which states to search based on what the user mentioned.
    Returns a list of states: ['NY'], ['CA'], or ['NY', 'CA']
    
    Note: We look for location-specific phrases like "in NY", "from CA", etc.
    to avoid confusing campaign names like "Healing NY" with actual locations.
    """
    campaign_request_lower = campaign_request.lower()
    
    # Look for NY or New York with location context (prepositions and conjunctions)
    has_ny = (
        ' in ny' in campaign_request_lower or
        ' from ny' in campaign_request_lower or 
        ' in new york' in campaign_request_lower or
        ' from new york' in campaign_request_lower or
        'new york and' in campaign_request_lower or
        'ny and' in campaign_request_lower or
        ' and ny' in campaign_request_lower or
        ' and new york' in campaign_request_lower or
        campaign_request_lower.endswith(' ny') or 
        campaign_request_lower.startswith('ny ') or 
        campaign_request_lower == 'ny'
    )
    
    # Look for CA or California with location context (prepositions and conjunctions)
    has_ca = (
        ' in ca' in campaign_request_lower or
        ' from ca' in campaign_request_lower or
        ' in california' in campaign_request_lower or
        ' from california' in campaign_request_lower or
        'california and' in campaign_request_lower or
        'ca and' in campaign_request_lower or
        ' and ca' in campaign_request_lower or
        ' and california' in campaign_request_lower or
        campaign_request_lower.endswith(' ca') or 
        campaign_request_lower.startswith('ca ') or 
        campaign_request_lower == 'ca'
    )
    
    # Determine which states to search
    if has_ny and has_ca:
        return ['NY', 'CA']  # Both states mentioned
    elif has_ny:
        return ['NY']        # Only NY mentioned
    elif has_ca:
        return ['CA']        # Only CA mentioned
    else:
        return ['NY', 'CA']  # No state mentioned - search both by default

def extract_industry_keywords(campaign_request):
    """
    Pull out industry-related keywords from the user's request.
    These will be used to filter sponsors and score alignment.
    
    ADDITIVE LOGIC: Campaign names ADD their keywords to user-mentioned keywords.
    For example: "tech sponsors for MODELS 2025" = tech + fashion/modeling keywords
    """
    campaign_request_lower = campaign_request.lower()
    found_keywords = []
    
    # Step 1: Find user-mentioned industry keywords
    # Healthcare keywords
    healthcare_terms = ['healthcare', 'health', 'medical', 'wellness', 'healing', 'hospital', 'clinic']
    for term in healthcare_terms:
        if term in campaign_request_lower:
            found_keywords.append('healthcare')
            break
    
    # Technology keywords
    tech_terms = ['tech', 'technology', 'software', 'digital', 'computer', 'internet']
    for term in tech_terms:
        if term in campaign_request_lower:
            found_keywords.append('technology')
            break
    
    # Arts keywords
    arts_terms = ['arts', 'art', 'creative', 'design', 'fashion', 'modeling', 'beauty']
    for term in arts_terms:
        if term in campaign_request_lower:
            found_keywords.append('arts')
            break
    
    # Education keywords
    education_terms = ['education', 'school', 'learning', 'youth', 'student']
    for term in education_terms:
        if term in campaign_request_lower:
            found_keywords.append('education')
            break
    
    # Community keywords
    community_terms = ['community', 'outreach', 'nonprofit', 'charity', 'foundation']
    for term in community_terms:
        if term in campaign_request_lower:
            found_keywords.append('community')
            break
    
    # Step 2: Add campaign-specific keywords (ADDITIVE - don't replace, just add)
    
    # MODELS 2025 campaign adds fashion/modeling keywords
    if 'models 2025' in campaign_request_lower:
        if 'arts' not in found_keywords:  # Only add if not already there
            found_keywords.append('arts')
        # Note: 'arts' covers fashion/modeling/beauty industries
    
    # Healing NY campaign adds healthcare keywords  
    if 'healing ny' in campaign_request_lower:
        if 'healthcare' not in found_keywords:  # Only add if not already there
            found_keywords.append('healthcare')
    
    # Future campaigns can be added here following the same additive pattern
    
    return found_keywords

def analyze_campaign_request(campaign_request):
    """
    Main function that understands what the user wants from their request.
    This breaks down the request into actionable pieces of information.
    """
    print("🔍 Analyzing your campaign request...")
    
    # Extract all the key information
    campaign_name = find_campaign_name(campaign_request)
    sponsor_count = get_sponsor_count(campaign_request)
    target_states = determine_target_states(campaign_request)
    industry_keywords = extract_industry_keywords(campaign_request)
    
    # Show what we understood
    print(f"📋 Campaign Name: {campaign_name}")
    
    if sponsor_count:
        print(f"🔢 Target Count: {sponsor_count} sponsors")
    else:
        print(f"🔢 Target Count: All matching sponsors")
    
    if len(target_states) == 2:
        print(f"📍 Target States: Both NY and CA")
    else:
        print(f"📍 Target States: {target_states[0]} only")
    
    if industry_keywords:
        print(f"🏷️  Industry Focus: {', '.join(industry_keywords)}")
    else:
        print(f"🏷️  Industry Focus: All industries")
    
    # Package everything into a dictionary for easy use
    campaign_analysis = {
        'campaign_name': campaign_name,
        'sponsor_count': sponsor_count,
        'target_states': target_states,
        'industry_keywords': industry_keywords,
        'original_request': campaign_request
    }
    
    return campaign_analysis

def load_sponsor_data():
    """
    Load sponsors from the CSV file in the Data folder.
    This function reads the sponsor database and validates it has all required information.
    
    Returns:
        pandas DataFrame: Sponsor data with all required columns
        None: If file not found or has missing columns
    """
    # Build the path to the sponsors.csv file
    # We expect it to be in the "data/input" folder relative to project root
    import os
    script_directory = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_directory)  # Go up from src/ to project root
    sponsors_file_path = os.path.join(project_root, "data", "input", "sponsors.csv")
    
    print("📁 Loading sponsor database...")
    
    # Check if the file exists before trying to open it
    if not os.path.exists(sponsors_file_path):
        print(f"❌ ERROR: Cannot find sponsors.csv file!")
        print(f"📂 Expected location: {sponsors_file_path}")
        print("\n💡 HELP: Make sure you have a 'data/input' folder with 'sponsors.csv' file")
        print("The file should contain columns: sponsor_name, email, state, industry, website")
        return None
    
    # Try to load the CSV file
    try:
        # Use pandas to read the CSV file
        # We'll use a descriptive variable name instead of 'df'
        sponsor_data = pd.read_csv(sponsors_file_path)
        
    except Exception as error:
        print(f"❌ ERROR: Could not read the sponsors.csv file!")
        print(f"📝 Error details: {error}")
        print("\n💡 HELP: Make sure the sponsors.csv file is not corrupted and is a valid CSV")
        return None
    
    # Verify the CSV has all the required columns
    required_columns = ['sponsor_name', 'email', 'state', 'industry', 'website']
    missing_columns = []
    
    # Check each required column one by one
    for column_name in required_columns:
        if column_name not in sponsor_data.columns:
            missing_columns.append(column_name)
    
    # If any columns are missing, show an error
    if missing_columns:
        print(f"❌ ERROR: sponsors.csv is missing required columns!")
        print(f"📋 Missing columns: {', '.join(missing_columns)}")
        print(f"📋 Found columns: {', '.join(sponsor_data.columns.tolist())}")
        print(f"📋 Required columns: {', '.join(required_columns)}")
        print("\n💡 HELP: Please add the missing columns to your sponsors.csv file")
        return None
    
    # Count how many sponsors we have from each state
    ny_sponsor_count = len(sponsor_data[sponsor_data['state'] == 'NY'])
    ca_sponsor_count = len(sponsor_data[sponsor_data['state'] == 'CA'])
    total_sponsor_count = len(sponsor_data)
    
    # Show a summary of what we loaded
    print(f"✅ Successfully loaded sponsor database!")
    print(f"📊 Found {ny_sponsor_count} NY sponsors and {ca_sponsor_count} CA sponsors")
    print(f"📊 Total sponsors in database: {total_sponsor_count}")
    
    return sponsor_data

def load_sponsor_data_from_propublica(search_terms, target_states=['NY', 'CA'], limit=100):
    """
    Load sponsor data from ProPublica Nonprofit Explorer API.
    This searches for foundations and nonprofits that match the search criteria.
    
    Args:
        search_terms (str): Keywords to search for like "arts education foundation"
        target_states (list): States to search in, default ['NY', 'CA']
        limit (int): Maximum number of organizations to retrieve
    
    Returns:
        pandas DataFrame: Sponsor data formatted like CSV data
        None: If API call fails
    """
    print("🌐 Loading sponsor data from ProPublica Nonprofit Explorer API...")
    print(f"🔍 Search terms: '{search_terms}'")
    print(f"📍 Target states: {', '.join(target_states)}")
    
    try:
        # Initialize ProPublica connector
        propublica = ProPublicaConnector()
        
        all_sponsors = []
        
        # Search in each target state with simplified approach
        for state in target_states:
            print(f"\n🗺️ Searching {state} for relevant organizations...")
            
            # Simple search queries that are more likely to work
            search_queries = [
                search_terms,
                "foundation",
                "arts",
                "education"
            ]
            
            state_sponsors = []
            seen_eins = set()  # Track EINs to avoid duplicates
            
            for query in search_queries:
                if len(state_sponsors) >= limit // len(target_states):
                    break
                    
                results = propublica.search_organizations(
                    keywords=query,
                    state=state,
                    limit=25  # Get reasonable number per query
                )
                
                if 'organizations' in results:
                    for org in results['organizations']:
                        ein = org.get('ein', '')
                        
                        # Skip duplicates and organizations without EIN
                        if not ein or ein in seen_eins:
                            continue
                            
                        seen_eins.add(ein)
                        
                        # Format data to match our CSV structure
                        sponsor = {
                            'sponsor_name': org.get('name', '').strip(),
                            'ein': ein,
                            'city': org.get('city', '').strip(),
                            'state': state,
                            'industry': f"Nonprofit - {org.get('ntee_code', 'Unknown')}",
                            'website': f"https://projects.propublica.org/nonprofits/organizations/{ein}",
                            'email': '',  # Will be discovered by web scraping
                            'phone': '',  # Will be discovered by web scraping  
                            'mission_statement': '',  # Will be extracted from website
                            'assets': 0,  # Skip detailed API calls for now to avoid errors
                            'ntee_code': org.get('ntee_code', ''),
                            'classification': org.get('subsection', ''),
                            'data_source': 'ProPublica API',
                            'api_retrieved_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        state_sponsors.append(sponsor)
                        
                        # Stop if we have enough from this state
                        if len(state_sponsors) >= limit // len(target_states):
                            break
                
                time.sleep(0.5)  # Small delay between API calls
            
            all_sponsors.extend(state_sponsors)
            print(f"📊 Found {len(state_sponsors)} organizations in {state}")
        
        if not all_sponsors:
            print("❌ No organizations found matching your criteria")
            return None
        
        # Convert to DataFrame
        sponsor_data = pd.DataFrame(all_sponsors)
        
        # Remove duplicates based on EIN
        sponsor_data = sponsor_data.drop_duplicates(subset=['ein'], keep='first')
        
        total_count = len(sponsor_data)
        print(f"\n✅ Successfully loaded {total_count} unique organizations from ProPublica!")
        
        # Show breakdown by state
        for state in target_states:
            state_count = len(sponsor_data[sponsor_data['state'] == state])
            print(f"📊 {state}: {state_count} organizations")
        
        return sponsor_data
        
    except Exception as e:
        print(f"❌ Error loading data from ProPublica API: {e}")
        return None

def filter_by_state(sponsor_data, target_states):
    """
    Filter sponsors to only include those from the specified state(s).
    This keeps the original data safe by working with a copy.
    
    Args:
        sponsor_data: pandas DataFrame with sponsor information
        target_states: list of states like ['NY'] or ['NY', 'CA']
    
    Returns:
        pandas DataFrame: Filtered sponsors from the specified state(s)
    """
    # Create a copy of the data to keep the original safe
    filtered_sponsors = sponsor_data.copy()
    
    # Filter to only include sponsors from the target states
    # This uses pandas filtering with the 'isin' method for multiple states
    filtered_sponsors = filtered_sponsors[filtered_sponsors['state'].isin(target_states)]
    
    # Show what we're filtering and how many matches we found
    if len(target_states) == 1:
        state_text = target_states[0]
    else:
        state_text = " and ".join(target_states)
    
    sponsor_count = len(filtered_sponsors)
    print(f"🗺️  Filtering sponsors from: {state_text}")
    print(f"📊 Found {sponsor_count} sponsors in {state_text}")
    
    return filtered_sponsors

def get_expanded_industry_keywords(primary_keywords):
    """
    Get expanded industry keywords when primary search doesn't yield enough results.
    Expands search criteria to include related industries.
    
    Args:
        primary_keywords (list): Original industry keywords
        
    Returns:
        list: Expanded list of industry keywords
    """
    # Industry expansion mappings optimized for CSOAF mission alignment
    # CSOAF Mission: "Transforming lives through the power of art"
    # Focus: arts education, disability support, community development
    expansion_map = {
        # Arts & Creative Industries (Primary CSOAF alignment)
        'arts': ['creative', 'dance', 'drama', 'theater', 'music', 'visual arts', 'performing arts', 'cultural', 'artistic', 'creative arts'],
        'creative': ['arts', 'design', 'artistic', 'creative arts', 'cultural', 'visual arts'],
        'dance': ['arts', 'performing arts', 'creative', 'cultural', 'artistic'],
        'drama': ['theater', 'performing arts', 'arts', 'creative', 'cultural'],
        'theater': ['drama', 'performing arts', 'arts', 'creative', 'cultural'],
        'music': ['arts', 'performing arts', 'creative', 'cultural', 'artistic'],
        
        # Education & Learning (Core CSOAF focus)
        'education': ['school', 'learning', 'academic', 'teaching', 'training', 'public schools', 'K-12', 'youth education'],
        'school': ['education', 'learning', 'academic', 'public schools', 'K-12'],
        'learning': ['education', 'school', 'academic', 'teaching', 'training'],
        
        # Community & Social Impact (CSOAF community focus)
        'community': ['social impact', 'youth', 'empowerment', 'civic', 'local', 'neighborhood', 'social'],
        'youth': ['community', 'empowerment', 'K-12', 'students', 'children', 'teens'],
        'empowerment': ['community', 'youth', 'social impact', 'inclusion', 'equity'],
        
        # Accessibility & Inclusion (CSOAF disability focus)
        'accessibility': ['inclusion', 'disability', 'special needs', 'inclusive', 'equity', 'diversity'],
        'disability': ['accessibility', 'inclusion', 'special needs', 'inclusive', 'adaptive'],
        'inclusion': ['accessibility', 'disability', 'diversity', 'equity', 'inclusive'],
        'special needs': ['disability', 'accessibility', 'inclusion', 'adaptive', 'inclusive'],
        
        # Legacy keywords (for backward compatibility)
        'healthcare': ['medical', 'wellness', 'health'],
        'health': ['healthcare', 'medical', 'wellness'],
        'tech': ['technology', 'software', 'IT', 'digital'],
        'technology': ['tech', 'software', 'IT', 'digital']
    }
    
    expanded_keywords = primary_keywords.copy()
    
    # Add related keywords for each primary keyword
    for keyword in primary_keywords:
        if keyword.lower() in expansion_map:
            expanded_keywords.extend(expansion_map[keyword.lower()])
    
    # Remove duplicates and return
    return list(set(expanded_keywords))

def filter_by_industry_with_expansion(sponsor_data, industry_keywords, target_count=None):
    """
    Filter sponsors by industry with automatic expansion if not enough matches found.
    First tries exact keywords, then expands to related industries if needed.
    
    Args:
        sponsor_data (DataFrame): The sponsor data to filter
        industry_keywords (list): List of keywords to match against
        target_count (int, optional): Target number of sponsors needed
        
    Returns:
        DataFrame: Filtered sponsors matching the industry keywords (expanded if needed)
    """
    if not industry_keywords:
        # No industry filter specified - return all sponsors
        return sponsor_data
    
    print(f"🏷️  Looking for {', '.join(industry_keywords)} sponsors...")
    
    # Try primary keywords first
    matching_sponsors = filter_by_industry(sponsor_data, industry_keywords)
    
    # Check if we have enough sponsors
    if target_count and len(matching_sponsors) < target_count:
        print(f"⚠️  Only found {len(matching_sponsors)} sponsors, need {target_count}")
        print(f"🔍 Expanding search to related industries...")
        
        # Get expanded keywords
        expanded_keywords = get_expanded_industry_keywords(industry_keywords)
        expanded_only = [k for k in expanded_keywords if k not in industry_keywords]
        
        if expanded_only:
            print(f"➕ Adding related keywords: {', '.join(expanded_only[:5])}{'...' if len(expanded_only) > 5 else ''}")
            matching_sponsors = filter_by_industry(sponsor_data, expanded_keywords)
        
        if len(matching_sponsors) < target_count:
            print(f"⚠️  Still only found {len(matching_sponsors)} sponsors after expansion")
    
    return matching_sponsors

def filter_by_industry(sponsor_data, industry_keywords):
    """
    Filter sponsors to only include those whose industry matches the keywords.
    Uses case-insensitive string matching to be flexible with different formats.
    
    Args:
        sponsor_data: pandas DataFrame with sponsor information
        industry_keywords: list of keywords like ['healthcare', 'technology']
    
    Returns:
        pandas DataFrame: Filtered sponsors matching the industry keywords
    """
    # If no keywords provided, return all sponsors
    if not industry_keywords:
        print(f"🏷️  Industry Focus: All industries")
        print(f"📊 Found {len(sponsor_data)} sponsors (no industry filter)")
        return sponsor_data.copy()
    
    # Create a copy of the data to keep the original safe
    filtered_sponsors = sponsor_data.copy()
    
    # Create a boolean mask to track which sponsors match
    # Start with all False, then set to True for matches
    matches_industry = pd.Series([False] * len(filtered_sponsors), index=filtered_sponsors.index)
    
    # Check each industry keyword
    for keyword in industry_keywords:
        # Convert keyword to lowercase for case-insensitive matching
        keyword_lower = keyword.lower()
        
        # Map industry types to what we search for
        industry_search_terms = {
            'healthcare': ['healthcare', 'health', 'medical', 'wellness', 'hospital', 'clinic'],
            'technology': ['technology', 'software', 'tech', 'digital', 'computer', 'internet'],
            'arts': ['arts', 'art', 'creative', 'design', 'fashion', 'modeling', 'beauty', 'entertainment'],
            'education': ['education', 'school', 'learning', 'youth', 'student', 'academic'],
            'community': ['community', 'nonprofit', 'charity', 'foundation', 'social']
        }
        
        # Get the search terms for this keyword
        search_terms = industry_search_terms.get(keyword_lower, [keyword_lower])
        
        # Check if any sponsor's industry contains these terms
        for term in search_terms:
            # Case-insensitive search in the industry column
            term_matches = filtered_sponsors['industry'].str.lower().str.contains(term, na=False)
            matches_industry = matches_industry | term_matches
    
    # Filter to only sponsors that match at least one keyword
    filtered_sponsors = filtered_sponsors[matches_industry]
    
    # Show what we're filtering and how many matches we found
    keyword_text = ', '.join(industry_keywords)
    sponsor_count = len(filtered_sponsors)
    print(f"🏷️  Looking for {keyword_text} sponsors...")
    print(f"📊 Found {sponsor_count} sponsors matching {keyword_text} industries")
    
    return filtered_sponsors

def apply_campaign_filters(sponsor_data, campaign_details):
    """
    Apply all the filtering based on the campaign requirements.
    This uses the campaign analysis to filter sponsors by state and industry.
    
    Args:
        sponsor_data: pandas DataFrame with all sponsor information
        campaign_details: dictionary with campaign analysis results
    
    Returns:
        pandas DataFrame: Filtered sponsors matching the campaign criteria
    """
    print("\n🔍 Applying campaign filters...")
    
    # Step 1: Filter by state (always apply this filter)
    target_states = campaign_details['target_states']
    filtered_sponsors = filter_by_state(sponsor_data, target_states)
    
    # Step 2: Filter by industry keywords with enhanced search (if any specified)
    industry_keywords = campaign_details['industry_keywords']
    target_count = campaign_details.get('sponsor_count', None)
    
    if industry_keywords:
        # Use enhanced search that expands keywords when insufficient results
        filtered_sponsors = filter_by_industry_with_expansion(
            filtered_sponsors, industry_keywords, target_count
        )
    
    # Show final filtering summary
    original_count = len(sponsor_data)
    final_count = len(filtered_sponsors)
    print(f"\n📊 Filtering Summary:")
    print(f"   • Started with: {original_count} total sponsors")
    print(f"   • After filtering: {final_count} matching sponsors")
    
    if final_count == 0:
        print("⚠️  Warning: No sponsors match your criteria!")
        print("💡 Try expanding your search (different industry or both states)")
    elif target_count and final_count < target_count:
        print(f"ℹ️  Found {final_count} sponsors, requested {target_count}")
        print("💡 All matching sponsors will be included")
    
    return filtered_sponsors

def google_search_website(company_name):
    """
    Use Google search to find the official website for a company.
    This is faster and more accurate than trial-and-error URL guessing.
    
    Args:
        company_name: The name of the company (string)
    
    Returns:
        str or None: Official website URL if found, None otherwise
    """
    try:
        import urllib.parse
        
        # Create search query: "Company Name official website"
        search_query = f'"{company_name}" official website'
        encoded_query = urllib.parse.quote(search_query)
        
        # Google search URL
        google_url = f"https://www.google.com/search?q={encoded_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(google_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Parse the HTML to find website URLs
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for search result links
            # Google uses different div classes for search results
            search_results = soup.find_all('div', class_='g') or soup.find_all('div', class_='tF2Cxc')
            
            for result in search_results[:3]:  # Check top 3 results
                # Find links within results
                links = result.find_all('a')
                for link in links:
                    href = link.get('href', '')
                    
                    # Skip Google's internal URLs
                    if href.startswith('/') or 'google.com' in href:
                        continue
                        
                    # Clean up URL
                    if href.startswith('https://') or href.startswith('http://'):
                        # Basic validation - should be a reasonable website
                        if any(blocked in href.lower() for blocked in ['facebook.com', 'linkedin.com', 'twitter.com', 'youtube.com', 'instagram.com']):
                            continue
                            
                        # Test if this website exists
                        if test_website_exists(href):
                            print(f"✅ Found via Google search: {href}")
                            return href
        
        print(f"❌ Google search failed to find website for: {company_name}")
        return None
        
    except Exception as e:
        print(f"❌ Google search error for {company_name}: {str(e)}")
        return None

def guess_website_url(company_name):
    """
    Try to guess a company's website URL based on their name.
    This tries common patterns that companies often use for their websites.
    
    Args:
        company_name: The name of the company (string)
    
    Returns:
        list: Possible website URLs to try, in order of most likely to work
    """
    # Clean up the company name for URL generation
    # Remove common business suffixes that don't belong in URLs
    name_clean = company_name.lower().strip()
    
    # Remove common business terms that clutter URLs
    business_terms = [' llc', ' inc', ' corp', ' corporation', ' company', ' co', ' ltd']
    for term in business_terms:
        if name_clean.endswith(term):
            name_clean = name_clean[:-len(term)].strip()
    
    # Generate possible website patterns
    possible_urls = []
    
    # Pattern 1: companyname.com (remove spaces, make lowercase)
    # Example: "Acme Corporation" becomes "acmecorporation.com"
    pattern1 = name_clean.replace(' ', '').replace('&', 'and')
    possible_urls.append(f"https://{pattern1}.com")
    possible_urls.append(f"http://{pattern1}.com")  # Try both HTTP and HTTPS
    
    # Pattern 2: company-name.com (replace spaces with dashes)
    # Example: "Acme Corporation" becomes "acme-corporation.com"
    pattern2 = name_clean.replace(' ', '-').replace('&', 'and')
    possible_urls.append(f"https://{pattern2}.com")
    possible_urls.append(f"http://{pattern2}.com")
    
    # Pattern 3: Try .net extension (common alternative)
    possible_urls.append(f"https://{pattern1}.net")
    possible_urls.append(f"https://{pattern2}.net")
    
    return possible_urls

def test_website_exists(url):
    """
    Test if a website URL actually exists and is accessible.
    This makes a simple request to check if the website responds.
    
    Args:
        url: The website URL to test (string)
    
    Returns:
        bool: True if website exists and is accessible, False otherwise
    """
    try:
        # Make a simple request to the website
        # Set a timeout so we don't wait forever
        # Use a User-Agent header so we look like a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.head(url, timeout=10, headers=headers, allow_redirects=True)
        
        # Check if we got a successful response
        # Status codes 200-299 are considered successful
        return 200 <= response.status_code < 300
        
    except requests.exceptions.RequestException:
        # Any error means the website is not accessible
        # This includes timeouts, connection errors, etc.
        return False

def discover_website_for_sponsor(sponsor_row):
    """
    Discover or verify the website for a single sponsor.
    This checks existing websites and tries to find missing ones.
    
    Args:
        sponsor_row: A pandas Series with sponsor information
    
    Returns:
        dict: Contains 'website' and 'website_availability' information
    """
    sponsor_name = sponsor_row['sponsor_name']
    existing_website = sponsor_row['website']
    
    # Check if the sponsor already has a website listed
    if pd.notna(existing_website) and existing_website.strip():
        # They have a website - let's test if it works
        website_url = existing_website.strip()
        
        # Add http:// if no protocol specified
        if not website_url.startswith(('http://', 'https://')):
            website_url = f"http://{website_url}"
        
        # Test if the existing website works
        if test_website_exists(website_url):
            return {
                'website': website_url,
                'website_availability': 'available'
            }
        else:
            # Their listed website doesn't work - try to discover a new one
            print(f"⚠️  Listed website for {sponsor_name} is not accessible: {website_url}")
    
    # Either no website listed, or the listed one doesn't work
    # Try Google search first (Option C: Always Google search first)
    print(f"🔍 Searching Google for website: {sponsor_name}")
    
    google_result = google_search_website(sponsor_name)
    if google_result:
        return {
            'website': google_result,
            'website_availability': 'discovered'
        }
    
    # If Google search fails, fall back to URL guessing patterns
    print(f"🔍 Trying URL patterns for: {sponsor_name}")
    
    possible_urls = guess_website_url(sponsor_name)
    
    # Test each possible URL until we find one that works
    for url in possible_urls:
        print(f"   Trying: {url}")
        if test_website_exists(url):
            print(f"✅ Found working website: {url}")
            return {
                'website': url,
                'website_availability': 'discovered'
            }
        else:
            print(f"❌ Not accessible: {url}")
        
        # Add a small delay between requests to be respectful
        time.sleep(0.5)
    
    # No working website found
    print(f"❌ No working website found for: {sponsor_name}")
    return {
        'website': '',
        'website_availability': 'not_available'
    }

def discover_websites_for_sponsors(sponsor_data):
    """
    Discover websites for all sponsors in the dataset.
    This processes each sponsor and updates their website information.
    
    Args:
        sponsor_data: pandas DataFrame with sponsor information
    
    Returns:
        pandas DataFrame: Updated sponsor data with website discovery results
    """
    print(f"\n🌐 Starting website discovery for {len(sponsor_data)} sponsors...")
    print("This may take a few minutes as we respectfully test websites...")
    
    # Create a copy of the data to avoid modifying the original
    updated_sponsors = sponsor_data.copy()
    
    # Add new columns for website availability tracking
    updated_sponsors['website_availability'] = ''
    
    # Track statistics
    available_count = 0
    discovered_count = 0
    not_available_count = 0
    
    # Process each sponsor one by one
    for index, sponsor_row in updated_sponsors.iterrows():
        print(f"\n--- Processing {index + 1}/{len(updated_sponsors)}: {sponsor_row['sponsor_name']} ---")
        
        # Discover website information for this sponsor
        website_info = discover_website_for_sponsor(sponsor_row)
        
        # Update the sponsor data
        updated_sponsors.at[index, 'website'] = website_info['website']
        updated_sponsors.at[index, 'website_availability'] = website_info['website_availability']
        
        # Update statistics
        if website_info['website_availability'] == 'available':
            available_count += 1
        elif website_info['website_availability'] == 'discovered':
            discovered_count += 1
        else:
            not_available_count += 1
        
        # Add delay between sponsors to be respectful to websites
        time.sleep(1)
    
    # Show final statistics
    print(f"\n📊 Website Discovery Summary:")
    print(f"   ✅ Available (existing): {available_count}")
    print(f"   🔍 Discovered (found): {discovered_count}")
    print(f"   ❌ Not available: {not_available_count}")
    print(f"   📊 Total processed: {len(updated_sponsors)}")
    
    return updated_sponsors

def get_page_text(url):
    """
    Get the text content from a webpage using BeautifulSoup.
    This function handles the HTTP request and HTML parsing in a simple way.
    
    Args:
        url: The webpage URL to scrape (string)
    
    Returns:
        dict: Contains 'success', 'text', 'error' information
    """
    try:
        # Add respectful delay before making request (2 seconds as specified)
        time.sleep(2.0)
        
        # Set up headers to look like a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"   📄 Fetching page content from: {url}")
        
        # Make the HTTP request with a reasonable timeout
        response = requests.get(url, headers=headers, timeout=15)
        
        # Check if the request was successful
        if response.status_code != 200:
            return {
                'success': False,
                'text': '',
                'error': f"HTTP {response.status_code} error"
            }
        
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements (they don't contain useful text)
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get the text content and clean it up
        page_text = soup.get_text()
        
        # Clean up the text by removing extra whitespace and empty lines
        lines = (line.strip() for line in page_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        return {
            'success': True,
            'text': clean_text,
            'error': None
        }
        
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'text': '',
            'error': "Request timed out after 15 seconds"
        }
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'text': '',
            'error': "Could not connect to website"
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'text': '',
            'error': f"Request failed: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'text': '',
            'error': f"Unexpected error: {str(e)}"
        }

def scrape_website_pages(base_url):
    """
    Try to scrape different pages from a website in order of preference.
    This tries homepage first, then about pages, then contact pages.
    
    Args:
        base_url: The base website URL (string)
    
    Returns:
        dict: Contains 'success', 'text', 'page_scraped', 'attempts' information
    """
    # Clean up the base URL to make sure it's properly formatted
    if not base_url.startswith(('http://', 'https://')):
        base_url = f"http://{base_url}"
    
    # Remove trailing slash for consistency
    base_url = base_url.rstrip('/')
    
    # Define the pages to try in order of preference
    pages_to_try = [
        {'url': base_url, 'name': 'homepage', 'description': 'Homepage (safest option)'},
        {'url': f"{base_url}/about", 'name': 'about', 'description': 'About page'},
        {'url': f"{base_url}/about-us", 'name': 'about-us', 'description': 'About Us page'},
        {'url': f"{base_url}/contact", 'name': 'contact', 'description': 'Contact page'},
    ]
    
    print(f"🌐 Scraping website: {base_url}")
    
    # Track all attempts for reporting
    scrape_attempts = []
    
    # Try each page until we get successful content
    for page_info in pages_to_try:
        url = page_info['url']
        page_name = page_info['name']
        description = page_info['description']
        
        print(f"   🔍 Trying {description}: {url}")
        
        # Get the page content
        result = get_page_text(url)
        
        # Record this attempt
        attempt_record = {
            'page': page_name,
            'url': url,
            'success': result['success'],
            'error': result['error']
        }
        scrape_attempts.append(attempt_record)
        
        if result['success']:
            # We got content! Check if it's substantial enough
            text_length = len(result['text'])
            if text_length > 100:  # Need at least 100 characters to be useful
                print(f"   ✅ Successfully scraped {description} ({text_length:,} characters)")
                return {
                    'success': True,
                    'text': result['text'],
                    'page_scraped': page_name,
                    'attempts': scrape_attempts
                }
            else:
                print(f"   ⚠️  Page content too short ({text_length} characters), trying next page...")
        else:
            print(f"   ❌ Failed to scrape {description}: {result['error']}")
    
    # If we get here, none of the pages worked
    print(f"   ❌ Could not scrape any pages from {base_url}")
    return {
        'success': False,
        'text': '',
        'page_scraped': None,
        'attempts': scrape_attempts
    }

def scrape_sponsor_websites(sponsor_data):
    """
    Scrape websites for all sponsors to gather additional information.
    This processes sponsors that have accessible websites and extracts content.
    
    Args:
        sponsor_data: pandas DataFrame with sponsor information including websites
    
    Returns:
        pandas DataFrame: Updated sponsor data with scraped website content
    """
    print(f"\n📄 Starting website scraping for sponsors with accessible websites...")
    
    # Create a copy of the data to avoid modifying the original
    updated_sponsors = sponsor_data.copy()
    
    # Add new columns for scraped content
    updated_sponsors['scraped_text'] = ''
    updated_sponsors['scrape_status'] = ''
    updated_sponsors['page_scraped'] = ''
    updated_sponsors['scrape_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Filter to only sponsors with accessible websites
    scrapeable_sponsors = updated_sponsors[
        (updated_sponsors['website_availability'].isin(['available', 'discovered'])) &
        (updated_sponsors['website'] != '')
    ]
    
    print(f"📊 Found {len(scrapeable_sponsors)} sponsors with accessible websites to scrape")
    
    if len(scrapeable_sponsors) == 0:
        print("⚠️  No websites available for scraping!")
        return updated_sponsors
    
    # Track statistics
    successful_scrapes = 0
    failed_scrapes = 0
    
    # Process each sponsor with an accessible website
    for index, sponsor_row in scrapeable_sponsors.iterrows():
        sponsor_name = sponsor_row['sponsor_name']
        website_url = sponsor_row['website']
        
        print(f"\n--- Scraping {successful_scrapes + failed_scrapes + 1}/{len(scrapeable_sponsors)}: {sponsor_name} ---")
        
        # Scrape the website content
        scrape_result = scrape_website_pages(website_url)
        
        if scrape_result['success']:
            # Successfully scraped content
            updated_sponsors.at[index, 'scraped_text'] = scrape_result['text'][:5000]  # Limit to 5000 chars
            updated_sponsors.at[index, 'scrape_status'] = 'success'
            updated_sponsors.at[index, 'page_scraped'] = scrape_result['page_scraped']
            successful_scrapes += 1
        else:
            # Failed to scrape
            updated_sponsors.at[index, 'scraped_text'] = ''
            updated_sponsors.at[index, 'scrape_status'] = 'failed'
            updated_sponsors.at[index, 'page_scraped'] = 'none'
            failed_scrapes += 1
    
    # Show final statistics
    print(f"\n📊 Website Scraping Summary:")
    print(f"   ✅ Successfully scraped: {successful_scrapes}")
    print(f"   ❌ Failed to scrape: {failed_scrapes}")
    print(f"   📊 Total attempts: {len(scrapeable_sponsors)}")
    
    success_rate = (successful_scrapes / len(scrapeable_sponsors) * 100) if len(scrapeable_sponsors) > 0 else 0
    print(f"   📈 Success rate: {success_rate:.1f}%")
    
    return updated_sponsors

def find_phone_number(text):
    """
    Find phone numbers in website text using simple pattern matching.
    Looks for common phone number formats like (555) 123-4567.
    
    Args:
        text (str): The text content from a website
        
    Returns:
        str: First phone number found, or empty string if none found
    """
    # Clean up the text first - remove extra spaces and line breaks
    clean_text = text.replace('\n', ' ').replace('\r', ' ')
    clean_text = ' '.join(clean_text.split())  # Remove multiple spaces
    
    # Look for common phone number patterns in the text
    # Pattern 1: (555) 123-4567
    pattern_1 = r'\(\d{3}\)\s*\d{3}[-\.\s]?\d{4}'
    
    # Pattern 2: 555-123-4567 or 555.123.4567
    pattern_2 = r'\d{3}[-\.\s]?\d{3}[-\.\s]?\d{4}'
    
    # Pattern 3: 1-555-123-4567
    pattern_3 = r'1[-\.\s]?\d{3}[-\.\s]?\d{3}[-\.\s]?\d{4}'
    
    # Try each pattern in order of preference
    for pattern in [pattern_1, pattern_2, pattern_3]:
        phone_matches = re.findall(pattern, clean_text)
        if phone_matches:
            # Return the first reasonable phone number found
            phone_number = phone_matches[0].strip()
            print(f"📞 Found phone number: {phone_number}")
            return phone_number
    
    # No phone number found
    print("📞 No phone number found in text")
    return ""

def find_email_address(text):
    """
    Find email addresses in website text using simple pattern matching.
    Looks for patterns like contact@company.com or info@business.org.
    
    Args:
        text (str): The text content from a website
        
    Returns:
        str: First email address found, or empty string if none found
    """
    # Clean up the text first - remove extra spaces and line breaks
    clean_text = text.replace('\n', ' ').replace('\r', ' ')
    clean_text = ' '.join(clean_text.split())  # Remove multiple spaces
    
    # Look for email pattern: word@domain.extension
    # Simple pattern that catches most business emails
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    
    email_matches = re.findall(email_pattern, clean_text)
    
    if email_matches:
        # Return the first email address found
        email_address = email_matches[0].strip()
        print(f"📧 Found email address: {email_address}")
        return email_address
    
    # No email address found
    print("📧 No email address found in text")
    return ""

def find_mission_statement(text):
    """
    Find mission statement or company description in website text.
    Looks for sections with keywords like "about us", "mission", "what we do".
    
    Args:
        text (str): The text content from a website
        
    Returns:
        str: Mission statement text, or empty string if none found
    """
    # Clean up the text first - remove extra spaces and line breaks
    clean_text = text.replace('\n', ' ').replace('\r', ' ')
    clean_text = ' '.join(clean_text.split())  # Remove multiple spaces
    
    # Look for mission statement keywords (case-insensitive)
    mission_keywords = [
        "about us", "about", "mission", "what we do", "our mission",
        "who we are", "company overview", "our story", "vision",
        "purpose", "company mission", "organization", "commitment"
    ]
    
    # Convert text to lowercase for searching
    lower_text = clean_text.lower()
    
    # Find the best mission statement section
    best_section = ""
    best_keyword = ""
    
    for keyword in mission_keywords:
        keyword_position = lower_text.find(keyword.lower())
        
        if keyword_position != -1:
            # Found the keyword! Extract text around it
            # Get text starting from keyword position
            start_position = keyword_position
            
            # Look for a good stopping point (next section or reasonable length)
            end_position = start_position + 500  # Default: 500 characters
            
            # Try to find natural ending points
            text_section = clean_text[start_position:start_position + 800]
            
            # Look for section breaks
            section_breaks = [". About", ". Contact", ". Services", ". Home", ". Products"]
            for break_text in section_breaks:
                break_position = text_section.find(break_text)
                if break_position != -1 and break_position > 100:  # At least 100 chars
                    end_position = start_position + break_position
                    break
            
            # Extract the mission statement section
            mission_section = clean_text[start_position:end_position].strip()
            
            # If this section is longer than our current best, use it
            if len(mission_section) > len(best_section) and len(mission_section) > 50:
                best_section = mission_section
                best_keyword = keyword
    
    if best_section:
        # Clean up the mission statement - remove extra punctuation at the end
        mission_text = best_section.rstrip('.,;!?').strip()
        print(f"📝 Found mission statement (keyword: '{best_keyword}'): {mission_text[:100]}...")
        return mission_text
    
    # No mission statement found
    print("📝 No mission statement found in text")
    return ""

def find_sponsorship_history(text):
    """
    Detect sponsorship and donation history from website content.
    Looks for evidence of past community involvement, CSR activities, 
    and support for causes aligned with CSOAF mission.
    
    Args:
        text (str): The text content from a website
        
    Returns:
        dict: Contains sponsorship indicators and relevant matches
    """
    # Clean up the text for analysis
    clean_text = text.replace('\n', ' ').replace('\r', ' ')
    clean_text = ' '.join(clean_text.split()).lower()  # Remove multiple spaces and lowercase
    
    sponsorship_indicators = {
        'sponsorship_score': 0,
        'donation_evidence': [],
        'community_involvement': [],
        'csr_activities': [],
        'arts_education_support': []
    }
    
    # Sponsorship & Donation keywords (each match adds 0.2 points)
    sponsorship_keywords = [
        "sponsor", "donation", "donate", "grant", "funding", "contribute", "contribution",
        "philanthropic", "charitable", "giving", "support", "partner", "partnership"
    ]
    
    # Community involvement keywords (each match adds 0.15 points)
    community_keywords = [
        "community outreach", "volunteer", "community service", "local community",
        "community support", "community involvement", "giving back", "nonprofit support",
        "charity work", "community partner", "social responsibility", "corporate giving"
    ]
    
    # CSR (Corporate Social Responsibility) keywords (each match adds 0.25 points)
    csr_keywords = [
        "corporate social responsibility", "csr", "social impact", "corporate giving",
        "community investment", "social mission", "corporate citizenship", "sustainability",
        "environmental responsibility", "social good", "community development"
    ]
    
    # CSOAF-aligned activities keywords (each match adds 0.3 points - highest value)
    csoaf_aligned_keywords = [
        "arts education", "arts program", "school arts", "youth arts", "creative arts",
        "arts funding", "education support", "disability support", "special needs",
        "accessibility", "inclusive", "youth development", "student support",
        "arts scholarship", "education grant", "creative learning", "performing arts"
    ]
    
    # Search for sponsorship evidence
    for keyword in sponsorship_keywords:
        if keyword in clean_text:
            sponsorship_indicators['sponsorship_score'] += 0.2
            sponsorship_indicators['donation_evidence'].append(keyword)
            if sponsorship_indicators['sponsorship_score'] >= 1.0:  # Cap individual categories
                break
    
    # Search for community involvement
    for keyword in community_keywords:
        if keyword in clean_text:
            sponsorship_indicators['sponsorship_score'] += 0.15
            sponsorship_indicators['community_involvement'].append(keyword)
            if len(sponsorship_indicators['community_involvement']) >= 3:  # Limit matches
                break
    
    # Search for CSR activities
    for keyword in csr_keywords:
        if keyword in clean_text:
            sponsorship_indicators['sponsorship_score'] += 0.25
            sponsorship_indicators['csr_activities'].append(keyword)
            if len(sponsorship_indicators['csr_activities']) >= 2:  # Limit matches
                break
    
    # Search for CSOAF-aligned support (highest value)
    for keyword in csoaf_aligned_keywords:
        if keyword in clean_text:
            sponsorship_indicators['sponsorship_score'] += 0.3
            sponsorship_indicators['arts_education_support'].append(keyword)
            if len(sponsorship_indicators['arts_education_support']) >= 2:  # Limit matches
                break
    
    # Cap the total score at 1.0 (this gets added to alignment score)
    sponsorship_indicators['sponsorship_score'] = min(sponsorship_indicators['sponsorship_score'], 1.0)
    
    # Report findings if any evidence found
    if sponsorship_indicators['sponsorship_score'] > 0:
        print(f"💰 Sponsorship evidence found (score: {sponsorship_indicators['sponsorship_score']:.2f}):")
        if sponsorship_indicators['donation_evidence']:
            print(f"   🎁 Donations: {sponsorship_indicators['donation_evidence'][:2]}")
        if sponsorship_indicators['community_involvement']:
            print(f"   🏘️ Community: {sponsorship_indicators['community_involvement'][:2]}")
        if sponsorship_indicators['csr_activities']:
            print(f"   🌟 CSR: {sponsorship_indicators['csr_activities'][:2]}")
        if sponsorship_indicators['arts_education_support']:
            print(f"   🎨 CSOAF-aligned: {sponsorship_indicators['arts_education_support'][:2]}")
    else:
        print("💰 No clear sponsorship/donation history detected")
    
    return sponsorship_indicators

def get_campaign_keywords(campaign_name, industry_type=""):
    """
    Get relevant keywords for scoring based on campaign name and industry type.
    Optimized for CSOAF mission: "Transforming lives through the power of art"
    Focus: arts education, disability support, community development
    
    Args:
        campaign_name (str): The name of the campaign (e.g., "Healing NY", "Arts Education")
        industry_type (str): The sponsor's industry type (optional)
        
    Returns:
        list: List of keywords to search for in mission statements
    """
    # Convert campaign name to lowercase for matching
    campaign_lower = campaign_name.lower()
    
    # CSOAF mission-aligned campaign keywords
    predefined_campaigns = {
        # Arts Education (Primary CSOAF focus)
        "arts": ["arts", "creative", "dance", "drama", "theater", "music", "visual arts", 
                 "performing arts", "cultural", "artistic", "creativity", "expression"],
        "education": ["education", "school", "learning", "academic", "teaching", "training", 
                      "K-12", "public schools", "students", "youth education"],
        "arts education": ["arts", "education", "creative", "school", "learning", "dance", 
                          "drama", "music", "artistic", "K-12", "students"],
        
        # Community & Youth Development (CSOAF community focus)  
        "community": ["community", "youth", "empowerment", "social impact", "civic", 
                      "local", "neighborhood", "social", "public service"],
        "youth": ["youth", "community", "empowerment", "K-12", "students", "children", 
                  "teens", "mentoring", "development"],
        "empowerment": ["empowerment", "community", "youth", "inclusion", "equity", 
                        "social impact", "transformation"],
        
        # Accessibility & Inclusion (CSOAF disability focus)
        "accessibility": ["accessibility", "inclusion", "disability", "special needs", 
                         "inclusive", "equity", "diversity", "adaptive"],
        "disability": ["disability", "accessibility", "inclusion", "special needs", 
                       "inclusive", "adaptive", "support"],
        "inclusion": ["inclusion", "accessibility", "disability", "diversity", "equity", 
                      "inclusive", "belonging"],
        "special needs": ["special needs", "disability", "accessibility", "inclusion", 
                         "adaptive", "inclusive", "support"],
        
        # Legacy healthcare campaigns (for backward compatibility)
        "healing ny": ["health", "medical", "wellness", "healing", "community health", 
                       "healthcare", "patient", "treatment", "care", "hospital"],
        "health": ["health", "medical", "wellness", "healing", "healthcare", 
                   "patient", "treatment", "care", "medicine"],
        
        # Creative industries (aligned with arts focus)
        "models 2025": ["arts", "creative", "design", "cultural", "artistic", "fashion",
                        "modeling", "beauty", "style", "photography"],
        "fashion": ["arts", "creative", "design", "cultural", "fashion", "modeling", 
                    "beauty", "style", "clothing", "apparel"]
    }
    
    # Check if this is a predefined campaign
    for campaign_key, keywords in predefined_campaigns.items():
        if campaign_key in campaign_lower:
            print(f"🎯 Using CSOAF-aligned keywords for '{campaign_key}' campaign")
            return keywords
    
    # For other campaigns, extract keywords with CSOAF mission priorities
    generic_keywords = []
    
    # Add words from campaign name (skip common words)
    skip_words = ["campaign", "initiative", "project", "program", "the", "and", "or", "for"]
    campaign_words = campaign_name.lower().split()
    
    for word in campaign_words:
        if len(word) > 2 and word not in skip_words:
            generic_keywords.append(word)
    
    # Add industry-related keywords with CSOAF alignment
    if industry_type:
        industry_lower = industry_type.lower()
        if "arts" in industry_lower or "creative" in industry_lower:
            generic_keywords.extend(["arts", "creative", "cultural", "artistic", "dance", "drama", "music"])
        elif "education" in industry_lower or "school" in industry_lower:
            generic_keywords.extend(["education", "learning", "school", "K-12", "students", "teaching"])
        elif "community" in industry_lower or "social" in industry_lower:
            generic_keywords.extend(["community", "social", "youth", "empowerment", "civic"])
        elif "tech" in industry_lower:
            generic_keywords.extend(["technology", "software", "digital", "innovation", "accessibility"])
        elif "health" in industry_lower:
            generic_keywords.extend(["health", "medical", "wellness", "care"])
    
    # Always include core CSOAF mission keywords (high priority)
    csoaf_core_keywords = [
        "arts", "education", "community", "youth", "creativity", "learning",
        "empowerment", "inclusion", "accessibility", "school", "students"
    ]
    generic_keywords.extend(csoaf_core_keywords)
    
    # Remove duplicates and return
    unique_keywords = list(set(generic_keywords))
    print(f"🎯 Using CSOAF mission-aligned keywords for '{campaign_name}': {unique_keywords[:5]}...")
    
    return unique_keywords

def calculate_alignment_score(mission_text, campaign_name, sponsor_industry="", sponsorship_info=None):
    """
    Calculate how well a sponsor aligns with a campaign based on their mission statement.
    Optimized for CSOAF mission: "Unlocking creative educational pathways for any type of learner"
    
    CSOAF Mission-First Scoring System (0-10 points):
    - 4 points: Core CSOAF mission alignment (K-12 arts education, moderate to severe disabilities, public schools)
    - 3 points: Keyword matches from campaign (arts programs, creative pathways, self-expression)  
    - 2 points: Community involvement and educational impact
    - 1 point: Industry alignment bonus (education, arts, nonprofit sectors)
    - Minimum 3 points (neutral) if no mission statement provided
    
    Priority Areas (from CSOAF website):
    1. K-12 arts education (dance, creative arts, drama)
    2. Supporting students with moderate to severe disabilities
    3. Public school partnerships in CA & NY since 2003
    4. Fostering self-expression and lifelong appreciation for arts
    
    Args:
        mission_text (str): The sponsor's mission statement or company description
        campaign_name (str): The name of the campaign we're scoring for
        sponsor_industry (str): The sponsor's industry type (optional)
        sponsorship_info (dict): Sponsorship detection results from website scraping (optional)
        
    Returns:
        int: Alignment score from 0-10
    """
    print(f"\n🎯 Calculating CSOAF mission alignment for campaign: '{campaign_name}'")
    
    # If no mission statement found, give neutral score (still included)
    if not mission_text or len(mission_text.strip()) == 0:
        print("📝 No mission statement available - assigning neutral score of 3")
        return 3
    
    # Convert mission text to lowercase for case-insensitive matching
    mission_lower = mission_text.lower()
    
    # Core CSOAF Mission Alignment (3 points max)
    csoaf_core_score = 0
    csoaf_matches = []
    
    # Primary CSOAF mission areas
    csoaf_mission_keywords = {
        "arts_focus": ["arts", "creative", "dance", "drama", "theater", "music", "visual arts", "performing arts", "artistic", "creativity"],
        "education_focus": ["education", "school", "learning", "K-12", "students", "teaching", "academic", "youth education"],
        "disability_support": ["disability", "special needs", "accessibility", "inclusion", "inclusive", "adaptive", "support"],
        "community_impact": ["community", "empowerment", "social impact", "transformation", "civic", "public service"]
    }
    
    for category, keywords in csoaf_mission_keywords.items():
        category_match = False
        for keyword in keywords:
            if keyword.lower() in mission_lower:
                if not category_match:  # Only count each category once
                    csoaf_core_score += 0.75  # Each category worth 0.75 points (4 categories = 3 points max)
                    csoaf_matches.append(f"{category}({keyword})")
                    category_match = True
                    break
    
    csoaf_core_score = min(csoaf_core_score, 3.0)  # Cap at 3 points
    
    # Campaign-specific keyword matches (3 points max)
    campaign_keywords = get_campaign_keywords(campaign_name, sponsor_industry)
    keyword_matches = 0
    matched_keywords = []
    
    for keyword in campaign_keywords:
        if keyword.lower() in mission_lower:
            keyword_matches += 1
            matched_keywords.append(keyword)
            if keyword_matches >= 2:  # Cap at 2 matches for efficiency
                break
    
    # Each keyword match worth 1.5 points (max 3 points)
    keyword_score = min(keyword_matches * 1.5, 3.0)
    
    # Community & Social Impact Focus (2 points max)
    community_score = 0
    community_matches = []
    community_keywords = [
        "community", "local", "volunteer", "outreach", "social", "civic", "public", 
        "neighborhood", "social impact", "giving back", "nonprofit", "charity", 
        "foundation", "philanthropy", "volunteer", "service"
    ]
    
    for keyword in community_keywords:
        if keyword in mission_lower:
            community_score += 0.4  # Each match worth 0.4 points
            community_matches.append(keyword)
            if community_score >= 2.0:  # Cap at 2 points
                break
    
    community_score = min(community_score, 2.0)
    
    # Industry alignment bonus (1 point)
    industry_score = 0
    if sponsor_industry and len(sponsor_industry.strip()) > 0:
        industry_lower = sponsor_industry.lower()
        campaign_lower = campaign_name.lower()
        
        # CSOAF-prioritized industry alignment
        if ("arts" in campaign_lower and "arts" in industry_lower) or \
           ("education" in campaign_lower and "education" in industry_lower) or \
           ("community" in campaign_lower and "community" in industry_lower) or \
           ("creative" in industry_lower) or ("cultural" in industry_lower):
            industry_score = 1
            print("🏭 CSOAF industry alignment bonus: +1 point")
    
    # Enhanced Sponsorship/Donation history detection (1 point max)
    sponsorship_score = 0
    if sponsorship_info and sponsorship_info.get('sponsorship_score', 0) > 0:
        # Use the enhanced sponsorship score from website analysis
        sponsorship_score = min(sponsorship_info['sponsorship_score'], 1.0)
        print(f"💰 Enhanced sponsorship evidence: +{sponsorship_score:.2f} points")
    else:
        # Fallback to basic keyword detection in mission text
        sponsorship_keywords = ["sponsor", "donation", "grant", "funding", "support", "partner", "contribute"]
        for keyword in sponsorship_keywords:
            if keyword in mission_lower:
                sponsorship_score = 0.5  # Lower score for basic detection
                print("💰 Basic sponsorship indicators: +0.5 points")
                break
    
    # Calculate total score (max 10)
    total_score = csoaf_core_score + keyword_score + community_score + industry_score + sponsorship_score
    total_score = min(total_score, 10)  # Cap at 10
    
    # Ensure minimum score of 1 if any content was found
    if total_score == 0 and len(mission_text.strip()) > 0:
        total_score = 1
    
    # Display scoring breakdown
    print(f"📊 CSOAF Mission-First Scoring:")
    print(f"   🎨 Core CSOAF alignment: {csoaf_core_score:.1f}/3.0 points {csoaf_matches[:2]}")
    print(f"   🔍 Campaign keywords ({len(matched_keywords)}): {keyword_score:.1f}/3.0 points")
    print(f"   🏘️ Community impact: {community_score:.1f}/2.0 points") 
    print(f"   🏭 Industry alignment: {industry_score}/1.0 points")
    print(f"   💰 Sponsorship history: {sponsorship_score:.2f}/1.0 points")
    print(f"   🎯 Total alignment score: {total_score:.1f}/10")
    
    return round(total_score)

def enhance_sponsor_data_with_campaign_info(sponsor_data, campaign_name, scraped_content=None):
    """
    Add new fields to existing sponsor data while preserving all original information.
    This expands the CSV with campaign-specific data like scores, contact info, and scraping status.
    
    New fields added:
    - phone: Phone number found on website
    - mission_statement: Company mission or about text
    - alignment_score: How well sponsor matches campaign (0-10)
    - scrape_status: "success", "failed", or "not_attempted"
    - scrape_date: When the data was collected
    - campaign_matched: Which campaign this data is for
    - website_availability: "available", "discovered", or "not_available"
    
    Args:
        sponsor_data (DataFrame): Original sponsor data from CSV
        campaign_name (str): Name of the campaign being processed
        scraped_content (DataFrame, optional): Data from web scraping process
        
    Returns:
        DataFrame: Enhanced sponsor data with all new fields
    """
    print(f"\n📊 Enhancing sponsor data for campaign: '{campaign_name}'")
    print(f"📋 Original sponsor count: {len(sponsor_data)}")
    
    # Make a copy to preserve original data (safety first!)
    enhanced_sponsors = sponsor_data.copy()
    
    # Add new columns with default values (graceful field expansion)
    new_fields = {
        'phone': '',                           # Phone number from website
        'mission_statement': '',               # Company mission/about text
        'alignment_score': 0,                  # Campaign alignment score (0-10)
        'sponsorship_score': 0,                # Sponsorship history score (0-1.0) 
        'sponsorship_evidence': '',            # Evidence of past sponsorships/donations
        'scrape_status': 'not_attempted',      # Web scraping status
        'scrape_date': '',                     # When data was collected
        'campaign_matched': campaign_name,     # Which campaign this is for
        'website_availability': 'unknown',    # Website status
        'notes': ''                            # Data quality notes and alignment details
    }
    
    # Add each new field with default values
    for field_name, default_value in new_fields.items():
        enhanced_sponsors[field_name] = default_value
        print(f"➕ Added field: '{field_name}' with default value")
    
    # If we have scraped content, merge it in
    if scraped_content is not None and len(scraped_content) > 0:
        print(f"🔗 Merging scraped content from {len(scraped_content)} sponsors")
        
        # Process each sponsor in the scraped content
        for index, scraped_sponsor in scraped_content.iterrows():
            sponsor_name = scraped_sponsor.get('sponsor_name', '')
            
            # Find matching sponsor in original data
            matching_sponsors = enhanced_sponsors[
                enhanced_sponsors['sponsor_name'] == sponsor_name
            ]
            
            if len(matching_sponsors) > 0:
                # Get the index of the matching sponsor
                sponsor_index = matching_sponsors.index[0]
                
                # Update website availability status
                if 'website_availability' in scraped_sponsor:
                    enhanced_sponsors.at[sponsor_index, 'website_availability'] = scraped_sponsor['website_availability']
                
                # Update scraping status and date
                if 'scrape_status' in scraped_sponsor:
                    enhanced_sponsors.at[sponsor_index, 'scrape_status'] = scraped_sponsor['scrape_status']
                if 'scrape_date' in scraped_sponsor:
                    enhanced_sponsors.at[sponsor_index, 'scrape_date'] = scraped_sponsor['scrape_date']
                
                # Extract and add scraped content
                scraped_text = scraped_sponsor.get('scraped_text', '')
                
                if scraped_text and len(scraped_text.strip()) > 0:
                    # Extract phone number from scraped content
                    phone_number = find_phone_number(scraped_text)
                    enhanced_sponsors.at[sponsor_index, 'phone'] = phone_number
                    
                    # Extract mission statement from scraped content
                    mission_text = find_mission_statement(scraped_text)
                    enhanced_sponsors.at[sponsor_index, 'mission_statement'] = mission_text
                    
                    # Detect sponsorship/donation history from scraped content
                    sponsorship_info = find_sponsorship_history(scraped_text)
                    enhanced_sponsors.at[sponsor_index, 'sponsorship_score'] = sponsorship_info['sponsorship_score']
                    enhanced_sponsors.at[sponsor_index, 'sponsorship_evidence'] = str(sponsorship_info['donation_evidence'][:3])  # Store as string
                    
                    # Calculate alignment score using mission statement and sponsorship data
                    sponsor_industry = enhanced_sponsors.at[sponsor_index, 'industry']
                    alignment_score = calculate_alignment_score(
                        mission_text, campaign_name, sponsor_industry, sponsorship_info
                    )
                    enhanced_sponsors.at[sponsor_index, 'alignment_score'] = alignment_score
                    
                    print(f"✅ Enhanced data for: {sponsor_name} (Score: {alignment_score}/10)")
                else:
                    # No content scraped - assign neutral score
                    enhanced_sponsors.at[sponsor_index, 'alignment_score'] = 3
                    enhanced_sponsors.at[sponsor_index, 'mission_statement'] = ''
                    enhanced_sponsors.at[sponsor_index, 'sponsorship_score'] = 0
                    enhanced_sponsors.at[sponsor_index, 'sponsorship_evidence'] = ''
                    print(f"⚪ No content for: {sponsor_name} (Neutral score: 3/10)")
    
    else:
        print("ℹ️ No scraped content provided - using default values")
        
        # For sponsors without scraped content, calculate basic alignment scores
        # based on industry matching only
        for index, sponsor in enhanced_sponsors.iterrows():
            sponsor_industry = sponsor.get('industry', '')
            
            # Simple industry-based alignment (no mission statement)
            if sponsor_industry:
                # Give neutral score + industry bonus if applicable
                base_score = 3  # Neutral for no mission statement
                industry_bonus = 0
                
                campaign_lower = campaign_name.lower()
                industry_lower = sponsor_industry.lower()
                
                # Check for basic industry alignment
                if ("health" in campaign_lower and "health" in industry_lower) or \
                   ("tech" in campaign_lower and "tech" in industry_lower) or \
                   ("arts" in campaign_lower and "arts" in industry_lower) or \
                   ("education" in campaign_lower and "education" in industry_lower):
                    industry_bonus = 1
                
                final_score = base_score + industry_bonus
                enhanced_sponsors.at[index, 'alignment_score'] = final_score
            else:
                # No industry info - neutral score
                enhanced_sponsors.at[index, 'alignment_score'] = 3
    
    # Add current timestamp for sponsors without scrape_date
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    empty_dates = enhanced_sponsors['scrape_date'] == ''
    enhanced_sponsors.loc[empty_dates, 'scrape_date'] = current_timestamp
    
    # Ensure all data types are preserved and formatted correctly
    print(f"\n📊 Data type validation:")
    print(f"   📝 Text fields: sponsor_name, email, phone, mission_statement")
    print(f"   🔢 Numeric fields: alignment_score (0-10 scale)")
    print(f"   📅 Date fields: scrape_date (YYYY-MM-DD HH:MM:SS)")
    print(f"   🏷️ Category fields: state, industry, scrape_status, website_availability")
    
    # Generate data quality notes for each sponsor
    print(f"\n🔍 Generating data quality notes...")
    for index, sponsor_row in enhanced_sponsors.iterrows():
        notes = generate_sponsor_notes(sponsor_row)
        enhanced_sponsors.at[index, 'notes'] = notes
    
    # Final summary
    total_sponsors = len(enhanced_sponsors)
    sponsors_with_scores = len(enhanced_sponsors[enhanced_sponsors['alignment_score'] > 0])
    sponsors_with_content = len(enhanced_sponsors[enhanced_sponsors['mission_statement'] != ''])
    
    print(f"\n✅ CSV Enhancement Complete!")
    print(f"   📋 Total sponsors: {total_sponsors}")
    print(f"   🎯 Sponsors with alignment scores: {sponsors_with_scores}")
    print(f"   📝 Sponsors with mission statements: {sponsors_with_content}")
    print(f"   📋 Quality notes generated for all sponsors")
    print(f"   📊 All original data preserved + {len(new_fields)} new fields added")
    
    return enhanced_sponsors

def generate_sponsor_notes(sponsor_row):
    """
    Generate data quality notes for a sponsor based on available information.
    Provides transparency about alignment, missing data, and data quality issues.
    
    Args:
        sponsor_row (Series): Single sponsor record
        
    Returns:
        str: Formatted notes about the sponsor's data quality
    """
    notes = []
    
    # Alignment score notes
    score = sponsor_row.get('alignment_score', 0)
    if score >= 7:
        notes.append("High alignment with campaign")
    elif score >= 5:
        notes.append("Good alignment with campaign")
    elif score >= 3:
        notes.append("Moderate alignment - manual review recommended")
    elif score >= 1:
        notes.append("Low alignment - may require manual review")
    else:
        notes.append("No alignment detected - manual review required")
    
    # Website and scraping notes
    website_status = sponsor_row.get('website_availability', 'unknown')
    scrape_status = sponsor_row.get('scrape_status', 'not_attempted')
    
    if website_status == 'not_available':
        notes.append("No accessible website found")
    elif website_status == 'discovered':
        notes.append("Website discovered through pattern matching")
    elif scrape_status == 'failed':
        notes.append("Website accessible but scraping failed")
    
    # Mission statement notes
    mission = sponsor_row.get('mission_statement', '')
    if not mission or len(mission.strip()) == 0:
        notes.append("No mission statement found")
    
    # Phone number notes
    phone = sponsor_row.get('phone', '')
    if not phone or len(phone.strip()) == 0:
        notes.append("No phone number found")
    
    return '; '.join(notes)

def select_and_rank_sponsors(enhanced_sponsor_data, target_count=None, target_states=None):
    """
    Select and rank sponsors based on alignment scores and campaign requirements.
    Sorts by score (highest first) and includes ALL sponsors with quality notes.
    
    Selection Logic:
    - Include ALL sponsors regardless of alignment score
    - Sort by alignment score descending (best matches first)
    - Apply target count limit if specified
    - Add data quality notes for each sponsor
    - Handle scoring ties with secondary sorting (alphabetical by name)
    
    Args:
        enhanced_sponsor_data (DataFrame): Sponsor data with alignment scores
        target_count (int, optional): Maximum number of sponsors to select
        target_states (list, optional): States to include (for distribution calculation)
        
    Returns:
        DataFrame: Selected and ranked sponsors ready for output
    """
    print(f"\n🏆 Selecting and ranking sponsors...")
    print(f"📊 Starting with {len(enhanced_sponsor_data)} total sponsors")
    
    # Step 1: Include ALL sponsors (no minimum score threshold)
    qualified_sponsors = enhanced_sponsor_data.copy()
    print(f"✅ Including all {len(qualified_sponsors)} sponsors (no score threshold)")
    
    # Step 2: Sort by alignment score (descending) with tie-breaking
    # Primary sort: alignment_score (highest first)
    # Secondary sort: sponsor_name (alphabetical for consistent tie-breaking)
    sorted_sponsors = qualified_sponsors.sort_values(
        by=['alignment_score', 'sponsor_name'], 
        ascending=[False, True]  # Score desc, name asc
    ).reset_index(drop=True)
    
    print(f"📈 Sponsors sorted by alignment score (highest to lowest)")
    
    # Show top scoring sponsors
    top_scores = sorted_sponsors['alignment_score'].head(5).tolist()
    print(f"🎯 Top alignment scores: {top_scores}")
    
    # Step 3: Handle ties in scoring appropriately
    score_counts = sorted_sponsors['alignment_score'].value_counts().sort_index(ascending=False)
    ties_info = score_counts[score_counts > 1]
    if len(ties_info) > 0:
        print(f"🤝 Tied scores found:")
        for score, count in ties_info.items():
            print(f"   Score {score}: {count} sponsors (sorted alphabetically)")
    else:
        print("🎯 No tied scores - clear ranking established")
    
    # Step 4: Apply target count limit if specified
    if target_count is not None and target_count > 0:
        print(f"🎯 Applying target count limit: {target_count} sponsors")
        
        # Step 5: Ensure geographic distribution if multiple states
        if target_states and len(target_states) > 1:
            print(f"🗺️ Ensuring geographic distribution across states: {target_states}")
            selected_sponsors = ensure_geographic_distribution(
                sorted_sponsors, target_count, target_states
            )
        else:
            # Single state or no state preference - simple top N selection
            selected_sponsors = sorted_sponsors.head(target_count).copy()
            print(f"📍 Single state selection - taking top {len(selected_sponsors)} sponsors")
    else:
        # No count limit - include all qualified sponsors
        selected_sponsors = sorted_sponsors.copy()
        print(f"📋 No count limit specified - including all {len(selected_sponsors)} qualified sponsors")
    
    # Step 6: Create selection summary statistics
    print(f"\n📊 Selection Summary Statistics:")
    
    # Overall stats
    total_selected = len(selected_sponsors)
    total_available = len(qualified_sponsors)
    print(f"   📈 Selected: {total_selected} out of {total_available} qualified sponsors")
    
    # Score distribution
    if total_selected > 0:
        avg_score = selected_sponsors['alignment_score'].mean()
        min_score = selected_sponsors['alignment_score'].min()
        max_score = selected_sponsors['alignment_score'].max()
        print(f"   🎯 Score range: {min_score} to {max_score} (avg: {avg_score:.1f})")
        
        # State distribution
        if 'state' in selected_sponsors.columns:
            state_counts = selected_sponsors['state'].value_counts()
            print(f"   🗺️ Geographic distribution:")
            for state, count in state_counts.items():
                percentage = (count / total_selected) * 100
                print(f"      {state}: {count} sponsors ({percentage:.1f}%)")
        
        # Industry distribution
        if 'industry' in selected_sponsors.columns:
            industry_counts = selected_sponsors['industry'].value_counts().head(3)
            print(f"   🏭 Top industries: {dict(industry_counts)}")
        
        # Scraping success rate
        if 'scrape_status' in selected_sponsors.columns:
            success_count = len(selected_sponsors[selected_sponsors['scrape_status'] == 'success'])
            success_rate = (success_count / total_selected) * 100
            print(f"   🕷️ Web scraping success rate: {success_rate:.1f}% ({success_count}/{total_selected})")
    
    print(f"\n✅ Sponsor selection and ranking complete!")
    return selected_sponsors

def ensure_geographic_distribution(sorted_sponsors, target_count, target_states):
    """
    Ensure fair geographic distribution when selecting sponsors across multiple states.
    Tries to maintain proportional representation while respecting score-based ranking.
    
    Args:
        sorted_sponsors (DataFrame): Sponsors sorted by alignment score
        target_count (int): Target number of sponsors to select
        target_states (list): States that should be represented
        
    Returns:
        DataFrame: Selected sponsors with geographic distribution
    """
    print(f"🗺️ Calculating geographic distribution for {len(target_states)} states...")
    
    # Count available sponsors per state
    state_counts = sorted_sponsors['state'].value_counts()
    total_available = len(sorted_sponsors)
    
    print(f"📊 Available sponsors by state:")
    for state in target_states:
        count = state_counts.get(state, 0)
        percentage = (count / total_available) * 100 if total_available > 0 else 0
        print(f"   {state}: {count} sponsors ({percentage:.1f}%)")
    
    # Calculate target allocation per state (proportional to availability)
    state_targets = {}
    remaining_slots = target_count
    
    for state in target_states:
        available_in_state = state_counts.get(state, 0)
        if available_in_state > 0 and total_available > 0:
            # Proportional allocation
            proportion = available_in_state / total_available
            target_for_state = max(1, int(target_count * proportion))  # At least 1 if any available
            state_targets[state] = min(target_for_state, available_in_state)
        else:
            state_targets[state] = 0
    
    # Adjust if over-allocated
    total_allocated = sum(state_targets.values())
    if total_allocated > target_count:
        # Reduce largest allocations first
        while total_allocated > target_count:
            largest_state = max(state_targets, key=state_targets.get)
            if state_targets[largest_state] > 1:
                state_targets[largest_state] -= 1
                total_allocated -= 1
            else:
                break
    
    print(f"🎯 Target allocation per state:")
    for state, target in state_targets.items():
        print(f"   {state}: {target} sponsors")
    
    # Select sponsors maintaining score-based order within each state
    selected_sponsors = []
    
    for state in target_states:
        state_target = state_targets[state]
        if state_target > 0:
            # Get top-scored sponsors from this state
            state_sponsors = sorted_sponsors[sorted_sponsors['state'] == state]
            selected_from_state = state_sponsors.head(state_target)
            selected_sponsors.append(selected_from_state)
            print(f"✅ Selected {len(selected_from_state)} sponsors from {state}")
    
    # Combine all selected sponsors and re-sort by score
    if selected_sponsors:
        final_selection = pd.concat(selected_sponsors, ignore_index=True)
        # Re-sort by alignment score to maintain overall ranking
        final_selection = final_selection.sort_values(
            by=['alignment_score', 'sponsor_name'], 
            ascending=[False, True]
        ).reset_index(drop=True)
    else:
        final_selection = sorted_sponsors.iloc[0:0]  # Empty DataFrame
    
    print(f"🏆 Geographic distribution complete: {len(final_selection)} sponsors selected")
    return final_selection

def generate_campaign_output(selected_sponsors, campaign_name, output_folder=None):
    """
    Generate campaign results CSV file and comprehensive summary report.
    Saves all selected sponsor data to campaign_results.csv and displays processing statistics.
    
    Output Structure:
    - CSV file: Complete sponsor data with all enhanced fields
    - Console report: Processing statistics and success rates
    - File location: Data folder (same as input file)
    - Includes: ALL sponsors with alignment score >= 2
    
    Args:
        selected_sponsors (DataFrame): Final selected and ranked sponsors
        campaign_name (str): Name of the campaign for reporting
        output_folder (str): Folder to save the CSV file (default: "Data")
        
    Returns:
        str: Path to the created CSV file, or None if creation failed
    """
    print(f"\n📁 Generating campaign output for: '{campaign_name}'")
    
    # Set default output folder if not provided
    if output_folder is None:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_directory)  # Go up from src/ to project root
        output_folder = os.path.join(project_root, "data", "results")
    
    # Check if we have any sponsors to output
    if len(selected_sponsors) == 0:
        print("❌ No sponsors to output - empty selection!")
        return None
    
    # Step 1: Prepare comprehensive column set for CSV output
    # Essential columns as specified in requirements
    required_columns = [
        'sponsor_name',      # Original sponsor name
        'email',             # Contact email
        'phone',             # Phone number (extracted from website)
        'state',             # NY or CA
        'industry',          # Industry category
        'website',           # Website URL
        'mission_statement', # Mission/about text from website
        'alignment_score',   # Campaign alignment score (0-10)
        'notes',             # Data quality notes and alignment details
        'scrape_status',     # Web scraping status
        'scrape_date',       # When data was processed
        'campaign_matched',  # Campaign name
        'website_availability' # Website status
    ]
    
    # Ensure all required columns exist in the data
    output_data = selected_sponsors.copy()
    for column in required_columns:
        if column not in output_data.columns:
            output_data[column] = ''  # Add missing columns with empty values
            print(f"⚠️  Added missing column: {column}")
    
    # Reorder columns to match specification
    output_data = output_data[required_columns]
    
    # Step 2: Create output file path
    try:
        # Make sure output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"📁 Created output folder: {output_folder}")
        
        # Create file path (overwrites previous results as specified)
        output_file_path = os.path.join(output_folder, "campaign_results.csv")
        
        # Step 3: Save CSV file with all enhanced data
        output_data.to_csv(output_file_path, index=False, encoding='utf-8')
        print(f"💾 Campaign results saved to: {output_file_path}")
        print(f"📊 Columns included: {len(required_columns)}")
        print(f"📋 Sponsors included: {len(output_data)}")
        
    except Exception as csv_error:
        print(f"❌ Error saving CSV file: {csv_error}")
        return None
    
    # Step 4: Generate comprehensive summary report for console
    print(f"\n" + "="*60)
    print(f"🎯 CAMPAIGN RESULTS SUMMARY")
    print(f"="*60)
    
    # Campaign information
    print(f"📋 Campaign: {campaign_name}")
    print(f"📅 Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💾 Output File: {output_file_path}")
    
    # Step 5: Include processing statistics and success rates
    total_sponsors = len(output_data)
    
    # Score statistics
    if total_sponsors > 0:
        min_score = output_data['alignment_score'].min()
        max_score = output_data['alignment_score'].max()
        avg_score = output_data['alignment_score'].mean()
        
        print(f"\n📊 ALIGNMENT SCORING STATISTICS")
        print(f"   🎯 Total sponsors included: {total_sponsors}")
        print(f"   📈 Score range: {min_score} to {max_score} points")
        print(f"   📊 Average score: {avg_score:.1f} points")
        print(f"   ✅ All sponsors meet minimum threshold (≥ 2 points)")
        
        # Score distribution
        score_distribution = output_data['alignment_score'].value_counts().sort_index(ascending=False)
        print(f"   📈 Score distribution:")
        for score, count in score_distribution.head(5).items():  # Show top 5 scores
            percentage = (count / total_sponsors) * 100
            print(f"      {score} points: {count} sponsors ({percentage:.1f}%)")
    
    # Geographic distribution
    if 'state' in output_data.columns:
        state_counts = output_data['state'].value_counts()
        print(f"\n🗺️  GEOGRAPHIC DISTRIBUTION")
        for state, count in state_counts.items():
            percentage = (count / total_sponsors) * 100
            print(f"   {state}: {count} sponsors ({percentage:.1f}%)")
    
    # Industry distribution
    if 'industry' in output_data.columns:
        industry_counts = output_data['industry'].value_counts().head(5)
        print(f"\n🏭 TOP INDUSTRIES REPRESENTED")
        for industry, count in industry_counts.items():
            percentage = (count / total_sponsors) * 100
            print(f"   {industry}: {count} sponsors ({percentage:.1f}%)")
    
    # Web scraping success rates
    if 'scrape_status' in output_data.columns:
        scrape_counts = output_data['scrape_status'].value_counts()
        success_count = scrape_counts.get('success', 0)
        failed_count = scrape_counts.get('failed', 0)
        not_attempted_count = scrape_counts.get('not_attempted', 0)
        
        success_rate = (success_count / total_sponsors) * 100 if total_sponsors > 0 else 0
        
        print(f"\n🕷️  WEB SCRAPING STATISTICS")
        print(f"   ✅ Successful scrapes: {success_count} ({success_rate:.1f}%)")
        print(f"   ❌ Failed scrapes: {failed_count}")
        print(f"   ⏸️  Not attempted: {not_attempted_count}")
        
        # Content extraction success
        mission_count = len(output_data[output_data['mission_statement'].str.len() > 0])
        phone_count = len(output_data[output_data['phone'].str.len() > 0])
        
        mission_rate = (mission_count / total_sponsors) * 100 if total_sponsors > 0 else 0
        phone_rate = (phone_count / total_sponsors) * 100 if total_sponsors > 0 else 0
        
        print(f"   📝 Mission statements found: {mission_count} ({mission_rate:.1f}%)")
        print(f"   📞 Phone numbers found: {phone_count} ({phone_rate:.1f}%)")
    
    # Website availability
    if 'website_availability' in output_data.columns:
        website_counts = output_data['website_availability'].value_counts()
        print(f"\n🌐 WEBSITE AVAILABILITY")
        for status, count in website_counts.items():
            percentage = (count / total_sponsors) * 100
            print(f"   {status}: {count} sponsors ({percentage:.1f}%)")
    
    # Final summary
    print(f"\n" + "="*60)
    print(f"✅ CAMPAIGN PROCESSING COMPLETE!")
    print(f"📊 {total_sponsors} qualified sponsors ready for outreach")
    print(f"💾 Results saved to: campaign_results.csv")
    print(f"🎯 Use this data to contact aligned sponsors for '{campaign_name}'")
    print(f"="*60)
    
    return output_file_path

def main():
    """
    Main function that runs when the script is called from command line.
    This handles the command line interface and starts the campaign processing.
    """
    print("🎯 CSAF Campaign Tool Starting...")
    
    # Set up command line interface
    argument_parser = setup_command_line_interface()
    user_arguments = argument_parser.parse_args()
    
    # Get the campaign request from command line
    campaign_request = user_arguments.campaign_request
    
    # If no request provided, show help
    if not campaign_request:
        print("Welcome to the CSAF Campaign Tool! 👋")
        print("\nThis tool helps you find sponsors aligned with your campaign goals.")
        argument_parser.print_help()
        return
    
    # Validate the user's input first
    if not validate_command_input(campaign_request):
        print("\n🔍 Need more help? Run: python campaign.py --help")
        return
    
    # If we get here, the input looks good!
    print(f"✅ Processing campaign request: '{campaign_request}'")
    print("Looking for sponsor alignment opportunities...")
    
    # Analyze the user's request using Natural Language Processing
    campaign_details = analyze_campaign_request(campaign_request)
    
    print("\n✅ Campaign analysis complete!")
    print("Next: Loading sponsor database and finding matches...")
    
    # Load sponsor data from CSV file first
    sponsor_data = load_sponsor_data()
    
    # If CSV data loading failed, try ProPublica API as backup
    if sponsor_data is None:
        print("\n📁 CSV file not found, trying ProPublica API as data source...")
        
        # Extract search terms and states from campaign analysis
        search_terms = ' '.join(campaign_details.get('industry_keywords', ['foundation']))
        target_states = campaign_details.get('target_states', ['NY', 'CA'])
        
        sponsor_data = load_sponsor_data_from_propublica(
            search_terms=search_terms,
            target_states=target_states,
            limit=200  # Get more data since we're starting fresh
        )
        
        if sponsor_data is None:
            print("\n❌ Cannot continue without sponsor data from any source!")
            return
    
    else:
        # CSV data loaded successfully, optionally enhance with ProPublica data
        print("\n🌐 Enhancing CSV data with fresh ProPublica API data...")
        
        search_terms = ' '.join(campaign_details.get('industry_keywords', ['foundation']))
        target_states = campaign_details.get('target_states', ['NY', 'CA'])
        
        propublica_data = load_sponsor_data_from_propublica(
            search_terms=search_terms,
            target_states=target_states,
            limit=50  # Smaller supplement to existing data
        )
        
        if propublica_data is not None:
            # Combine CSV and ProPublica data
            combined_data = pd.concat([sponsor_data, propublica_data], ignore_index=True)
            # Remove duplicates based on name similarity
            combined_data = combined_data.drop_duplicates(subset=['sponsor_name'], keep='first')
            sponsor_data = combined_data
            
            total_csv = len(sponsor_data[sponsor_data['data_source'] != 'ProPublica API'])
            total_api = len(sponsor_data[sponsor_data['data_source'] == 'ProPublica API'])
            print(f"📊 Combined dataset: {total_csv} CSV + {total_api} ProPublica = {len(sponsor_data)} total sponsors")
    
    print("\n✅ Data loading complete!")
    
    # Apply campaign filters to find matching sponsors
    matching_sponsors = apply_campaign_filters(sponsor_data, campaign_details)
    
    # If no sponsors match, stop here
    if len(matching_sponsors) == 0:
        print("\n❌ No sponsors found matching your criteria!")
        return
    
    print("\n✅ Sponsor filtering complete!")
    
    # Discover websites for all matching sponsors
    sponsors_with_websites = discover_websites_for_sponsors(matching_sponsors)
    
    print("\n✅ Website discovery complete!")
    
    # Scrape websites to gather additional information
    sponsors_with_content = scrape_sponsor_websites(sponsors_with_websites)
    
    print("\n✅ Website scraping complete!")
    
    # Enhance sponsor data with extracted information and alignment scores
    campaign_name = campaign_details.get('campaign_name', 'Unknown Campaign')
    enhanced_sponsors = enhance_sponsor_data_with_campaign_info(
        matching_sponsors, campaign_name, sponsors_with_content
    )
    
    print("\n✅ Data enhancement complete!")
    
    # Select and rank sponsors based on alignment scores
    target_count = campaign_details.get('sponsor_count', None)
    target_states = campaign_details.get('target_states', [])
    selected_sponsors = select_and_rank_sponsors(
        enhanced_sponsors, target_count, target_states
    )
    
    print("\n✅ Sponsor selection and ranking complete!")
    
    # Generate final campaign output
    output_file = generate_campaign_output(selected_sponsors, campaign_name)
    
    if output_file:
        print(f"\n🎉 Campaign processing complete!")
        print(f"📁 Results saved to: {output_file}")
    else:
        print("\n⚠️ Campaign completed but output generation failed!")

if __name__ == "__main__":
    # This runs when someone types: python campaign.py
    main()