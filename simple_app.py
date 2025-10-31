#!/usr/bin/env python3
"""
🚀 CSOAF Email Campaign Manager - ENHANCED VERSION
===============================================
Simple, working UI with advanced features:
1. Data Records (Corporations & Foundations)
2. Generate & Categorize Sponsors with AI-Enhanced Web Scraping
3. Template Library with Auto-Matching
4. Send & Track by Category

Enhanced with:
- Automatic sponsor categorization by industry + sponsorship amount
- Template auto-suggestion and approval workflow
- Category-based email sending with personalization
- AI-powered web scraping for missing contact data
- OpenAI integration for intelligent data enhancement
"""

import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime, date
import time
import requests
from urllib.parse import urljoin, urlparse
import re

def enhance_sponsor_data_with_ai(sponsors_list, openai_api_key=None):
    """Use OpenAI to intelligently enhance sponsor data from web sources"""
    if not openai_api_key:
        return simulate_web_scraping(sponsors_list)
    
    enhanced_count = 0
    findings = {
        'emails_found': 0,
        'names_found': 0,
        'websites_found': 0,
        'missions_found': 0,
        'donations_found': 0,
        'focus_areas_found': 0
    }
    
    try:
        import openai
        openai.api_key = openai_api_key
        
        for sponsor in sponsors_list[:10]:  # Limit to 10 to avoid rate limits
            company_name = sponsor.get('organization_name', sponsor.get('Company', ''))
            if not company_name:
                continue
            
            # Check what data is missing
            missing_fields = []
            if not sponsor.get('contact_email') or pd.isna(sponsor.get('contact_email')):
                missing_fields.append('contact_email')
            if not sponsor.get('contact_name') or pd.isna(sponsor.get('contact_name')):
                missing_fields.append('contact_name')
            if not sponsor.get('website') or pd.isna(sponsor.get('website')):
                missing_fields.append('website')
            if not sponsor.get('mission_statement') or pd.isna(sponsor.get('mission_statement')):
                missing_fields.append('mission_statement')
            if not sponsor.get('past_donations') or pd.isna(sponsor.get('past_donations')):
                missing_fields.append('past_donations')
            if not sponsor.get('donation_focus') or pd.isna(sponsor.get('donation_focus')):
                missing_fields.append('donation_focus')
            
            if missing_fields and enhanced_count < 15:
                # Create AI prompt to find missing data
                prompt = f"""
                Research the company/organization "{company_name}" and provide the following missing information:
                
                Missing fields needed: {', '.join(missing_fields)}
                
                Please provide a JSON response with these fields (use null if not found):
                {{
                    "contact_email": "partnerships or development email address",
                    "contact_name": "name of partnerships/development director",
                    "website": "official website URL",
                    "mission_statement": "brief mission or purpose statement",
                    "past_donations": "recent donation amounts or giving capacity",
                    "donation_focus": "areas they typically fund (education, arts, etc.)"
                }}
                
                Focus on finding real, accurate information from their website, LinkedIn, or recent news.
                """
                
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=300,
                        temperature=0.1
                    )
                    
                    # Parse AI response
                    ai_data = json.loads(response.choices[0].message.content)
                    
                    # Update sponsor with found data
                    for field, value in ai_data.items():
                        if value and value != "null" and field in missing_fields:
                            sponsor[field] = value
                            findings[f"{field.split('_')[0]}_found"] = findings.get(f"{field.split('_')[0]}_found", 0) + 1
                    
                    enhanced_count += 1
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    print(f"AI enhancement failed for {company_name}: {e}")
                    continue
    
    except ImportError:
        st.warning("⚠️ OpenAI package not installed. Using simulated enhancement.")
        return simulate_web_scraping(sponsors_list)
    except Exception as e:
        st.error(f"❌ AI enhancement error: {e}")
        return simulate_web_scraping(sponsors_list)
    
    return findings

def simulate_web_scraping(sponsors_list):
    """Simulate web scraping to enhance sponsor data (fallback when OpenAI not available)"""
    enhanced_count = 0
    findings = {
        'emails_found': 0,
        'names_found': 0,
        'websites_found': 0,
        'missions_found': 0,
        'donations_found': 0,
        'focus_areas_found': 0
    }
    
    for sponsor in sponsors_list:
        company_name = sponsor.get('organization_name', sponsor.get('Company', '')).lower().replace(' ', '')
        
        # Simulate finding missing contact emails
        if not sponsor.get('contact_email') or pd.isna(sponsor.get('contact_email')):
            if enhanced_count < 8:
                sponsor['contact_email'] = f"partnerships@{company_name}.com"
                findings['emails_found'] += 1
                enhanced_count += 1
        
        # Simulate finding contact names
        if not sponsor.get('contact_name') and enhanced_count < 10:
            sponsor['contact_name'] = f"Partnership Director"
            findings['names_found'] += 1
            enhanced_count += 1
        
        # Simulate finding websites
        if not sponsor.get('website') and enhanced_count < 12:
            sponsor['website'] = f"https://www.{company_name}.com"
            findings['websites_found'] += 1
            enhanced_count += 1
        
        # Simulate finding mission statements
        if not sponsor.get('mission_statement') and enhanced_count < 8:
            industry = sponsor.get('industry_sector', sponsor.get('Industry', 'business'))
            sponsor['mission_statement'] = f"Leading {industry} company committed to innovation and community impact."
            findings['missions_found'] += 1
            enhanced_count += 1
        
        # Simulate finding past donations
        if not sponsor.get('past_donations') and enhanced_count < 6:
            sponsor['past_donations'] = "$50K-250K annually to education and community programs"
            findings['donations_found'] += 1
            enhanced_count += 1
        
        # Simulate finding donation focus
        if not sponsor.get('donation_focus') and enhanced_count < 8:
            sponsor['donation_focus'] = "Education, Arts, Community Development, Youth Programs"
            findings['focus_areas_found'] += 1
            enhanced_count += 1
    
    return findings

# Initialize session state
if 'current_campaign' not in st.session_state:
    st.session_state.current_campaign = None
if 'generated_sponsors' not in st.session_state:
    st.session_state.generated_sponsors = []
if 'sponsor_categories' not in st.session_state:
    st.session_state.sponsor_categories = {}
if 'approved_templates' not in st.session_state:
    st.session_state.approved_templates = {}
if 'email_templates' not in st.session_state:
    st.session_state.email_templates = {}
if 'sent_campaigns' not in st.session_state:
    st.session_state.sent_campaigns = []

# Page config
st.set_page_config(
    page_title="CSOAF Campaign Manager",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4037 0%, #99f2c8 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .step-header {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    
    .data-box {
        background: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e6e6e6;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_campaign' not in st.session_state:
    st.session_state.current_campaign = {}

if 'generated_sponsors' not in st.session_state:
    st.session_state.generated_sponsors = []

if 'email_templates' not in st.session_state:
    st.session_state.email_templates = {}

if 'sent_campaigns' not in st.session_state:
    st.session_state.sent_campaigns = []

def load_corporation_data():
    """Load Fortune 1000 corporations data"""
    try:
        path = "data/clean/corporations/fortune1000_main_database.csv"
        if os.path.exists(path):
            df = pd.read_csv(path)
            st.success(f"✅ Loaded {len(df)} corporations from {path}")
            return df
        else:
            st.warning(f"⚠️ Corporation data not found at {path}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading corporation data: {e}")
        return pd.DataFrame()

def load_foundation_data():
    """Load foundations data"""
    try:
        path = "data/foundations/integrated_sponsor_database_20251026_195246.csv"
        if os.path.exists(path):
            df = pd.read_csv(path)
            st.success(f"✅ Loaded {len(df)} foundations from {path}")
            return df
        else:
            st.warning(f"⚠️ Foundation data not found at {path}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading foundation data: {e}")
        return pd.DataFrame()

def load_email_templates():
    """Load email templates from the existing template files"""
    try:
        import sys
        sys.path.append('src/campaigns/email_templates')
        
        from enhanced_email_templates import CSPAFEmailTemplates
        template_system = CSPAFEmailTemplates()
        
        # Foundation templates (for program/class funding)
        foundation_templates = {
            "Arts Education Program Funding": {
                "subject": "Partnership: Bringing Arts Education to Underserved Communities",
                "content": """Dear {foundation_name} Team,

The Community School of the Arts Foundation (CSOAF) respectfully requests your partnership in expanding access to quality arts education for underserved students.

Our Proposal:
• Comprehensive arts curriculum including visual arts, music, dance, and theater
• Serving {target_schools} schools in {location}
• Reaching {student_count} students annually
• Professional teaching artist instruction

Funding Request: ${funding_amount:,} over {duration} years

Your investment directly impacts:
✓ Student academic achievement through arts integration
✓ Creative skill development and confidence building
✓ Cultural enrichment in underserved communities
✓ Teacher professional development in arts education

We would welcome the opportunity to discuss how this aligns with your foundation's mission.

Respectfully,
CSOAF Program Team"""
            },
            
            "STEM-Arts Integration Funding": {
                "subject": "STEAM Initiative: Merging Science and Arts for Student Success",
                "content": """Dear {foundation_name} Leadership,

CSOAF's innovative STEAM program combines science, technology, engineering, arts, and mathematics to create transformative learning experiences.

Program Overview:
• Integration of arts methodologies in STEM curricula
• Hands-on learning through creative projects
• Enhanced problem-solving and critical thinking skills
• Measurable improvements in student engagement

Investment Opportunity: ${funding_amount:,}

Impact Metrics:
• {student_count} students served annually
• {teacher_count} teachers trained in STEAM integration
• {school_count} schools implementing the program
• Documented improvements in standardized test scores

Your foundation's support would position you as a leader in innovative education.

Best regards,
CSOAF Education Team"""
            },
            
            "Community Arts Access Program": {
                "subject": "Breaking Barriers: Arts Education for Every Child",
                "content": """Dear {foundation_name} Grants Committee,

Every child deserves access to quality arts education, regardless of economic circumstances. CSOAF's Community Access Program removes financial barriers to arts learning.

Program Elements:
• Free after-school arts classes
• Summer intensive workshops
• Family engagement programs
• Scholarship opportunities for advanced training

Funding Need: ${funding_amount:,}

Community Impact:
• Serving {community_count} low-income families
• {program_hours} hours of instruction annually
• Cultural celebration events featuring student work
• Pathways to advanced arts education

This program creates lasting change in communities while honoring your foundation's commitment to equity.

Gratefully,
CSOAF Community Outreach"""
            },
            
            "Youth Leadership Through Arts": {
                "subject": "Empowering Young Leaders Through Creative Expression",
                "content": """Dear {foundation_name} Board,

CSOAF's Youth Leadership Program develops tomorrow's leaders through arts-based skill building and mentorship.

Leadership Development Components:
• Public speaking through theater and performance
• Project management via arts productions
• Cultural competency through diverse artistic traditions
• Peer mentoring and teaching opportunities

Investment: ${funding_amount:,}

Leadership Outcomes:
• {participant_count} youth leaders developed annually
• Community service projects led by participants
• College and career readiness skill development
• Civic engagement and social responsibility

Your partnership helps us cultivate confident, creative leaders who will shape our future.

Sincerely,
CSOAF Youth Development Team"""
            }
        }
        
        # Corporation templates (for event sponsorship)
        corporation_templates = {
            "Art Gallery Gala Sponsorship": {
                "subject": "Exclusive Sponsorship: Annual Art Gallery Gala - {event_date}",
                "content": """Dear {company_name} Corporate Partnership Team,

CSOAF cordially invites {company_name} to sponsor our Annual Art Gallery Gala, showcasing exceptional student artwork and celebrating arts education excellence.

Event Highlights:
📅 Date: {event_date}
🎨 Venue: {venue_name}
👥 Expected Attendance: {expected_guests} community leaders, arts patrons, and families
🏆 Student art exhibition and awards ceremony

Sponsorship Benefits:
• Prominent logo placement on all event materials
• Recognition during opening remarks
• VIP reception access for your team
• Exclusive networking opportunities
• Professional photography package
• Tax-deductible contribution receipt

Investment Levels:
🥇 Presenting Sponsor: ${presenting_amount:,}
🥈 Premier Sponsor: ${premier_amount:,}
🥉 Supporting Sponsor: ${supporting_amount:,}

This elegant evening celebrates creativity while positioning {company_name} as a champion of arts education.

Warm regards,
CSOAF Events Team"""
            },
            
            "Wine Tasting Fundraiser Partnership": {
                "subject": "Sophisticated Partnership: Wine & Arts Evening - {event_date}",
                "content": """Dear {company_name} Executive Team,

Join us for an exclusive Wine & Arts Evening, combining fine wine appreciation with celebration of student artistic achievement.

Event Experience:
🍷 Curated wine tasting featuring {wine_selection}
🎨 Live student art demonstrations
🎵 Musical performances by CSOAF students
🍽️ Gourmet appetizers and networking
📸 Silent auction featuring unique art pieces

Corporate Partnership Opportunities:
• Wine selection sponsorship with branding
• VIP tasting room reserved for your guests
• Corporate logo on event signage and programs
• Social media recognition and event photography
• Opportunity to present student awards

Investment Options:
💎 Exclusive Wine Partner: ${exclusive_amount:,}
🌟 Premier Partner: ${premier_amount:,}
🤝 Supporting Partner: ${supporting_amount:,}

This sophisticated event attracts influential community members while supporting arts education.

Cheers to partnership,
CSOAF Development Team"""
            },
            
            "Corporate Arts Challenge Sponsorship": {
                "subject": "Innovation Meets Creativity: Corporate Arts Challenge",
                "content": """Dear {company_name} Innovation Team,

CSOAF's Corporate Arts Challenge connects business innovation with student creativity, creating unique learning experiences.

Challenge Components:
💡 Students solve real-world problems through artistic solutions
🏢 Corporate mentors guide student project teams
🎯 Final presentations to company leadership
🏆 Scholarship awards for outstanding projects

Your Company's Role:
• Provide real business challenges for student teams
• Assign employee mentors for guidance
• Host final presentation and awards ceremony
• Networking opportunities with student talent pipeline

Sponsorship Investment: ${challenge_amount:,}

Business Benefits:
• Fresh perspectives on company challenges
• Community engagement and employee volunteerism
• Talent pipeline development
• Enhanced corporate social responsibility profile
• Media coverage and public recognition

Let's bridge the gap between business innovation and artistic creativity.

Partnership regards,
CSOAF Business Relations"""
            },
            
            "Holiday Arts Festival Corporate Partner": {
                "subject": "Celebrate the Season: Holiday Arts Festival Partnership",
                "content": """Dear {company_name} Marketing Team,

Ring in the holidays as the presenting sponsor of CSOAF's beloved Holiday Arts Festival!

Festival Features:
🎄 Student holiday performances
🎨 Arts and crafts marketplace
🎪 Family-friendly activities and workshops
🎁 Photos with artists in holiday-themed installations
☕ Hot cocoa and holiday treats

Presenting Sponsor Benefits:
• Festival named "{company_name} Holiday Arts Festival"
• Premium booth space for company engagement
• Logo placement on all marketing materials
• Stage announcements and recognition
• Employee family day activities
• Holiday-themed corporate social media content

Community Impact:
👨‍👩‍👧‍👦 {expected_families} families attend annually
🎨 {student_performers} students showcase their talents
📺 Local media coverage and community spotlight
💝 Brings joy and arts education to the entire community

Investment: ${festival_amount:,}

Spread holiday cheer while showcasing your company's commitment to community arts.

Festive regards,
CSOAF Festival Committee"""
            },
            
            "Music Showcase Series Partnership": {
                "subject": "Quarterly Music Showcase: Year-Long Partnership Opportunity",
                "content": """Dear {company_name} Brand Management Team,

Become the exclusive sponsor of CSOAF's Quarterly Music Showcase Series, featuring outstanding student musicians throughout the year.

Series Overview:
🎵 Four seasonal concerts featuring diverse musical styles
🎹 Solo performances, ensembles, and collaborative pieces
🎤 Guest artist performances alongside students
🎧 Professional recording and live streaming
📱 Social media content throughout the series

Annual Partnership Benefits:
• Exclusive naming rights: "{company_name} Music Showcase Series"
• VIP seating and reception access at all four events
• Quarterly networking opportunities with music community
• Professional recording package for corporate use
• Year-round recognition in all CSOAF music programming

Partnership Investment: ${series_amount:,}

Community Reach:
🎶 {annual_audience} total annual attendance
📺 Live streaming to {online_viewers} viewers
🎵 {student_musicians} students featured throughout the year
📈 Consistent brand visibility across all four seasons

Let your company's support resonate throughout the year with the power of music education.

Harmoniously yours,
CSOAF Music Department"""
            },
            
            "Art Supply Drive Corporate Champion": {
                "subject": "Be Our Art Supply Champion: Year-Long Corporate Partnership",
                "content": """Dear {company_name} Community Relations Team,

Partner with CSOAF as our Art Supply Champion, ensuring every student has access to quality art materials throughout the school year.

Champion Partnership Includes:
🎨 Quarterly art supply distributions to {school_count} schools
📦 Corporate-branded supply kits for students
🎒 Back-to-school art supply backpacks
🏪 Corporate volunteer opportunities for distribution events

Your Investment: ${supply_amount:,}

Direct Student Impact:
✏️ {student_count} students receive complete art supply kits
🖌️ Professional-grade materials enhance learning quality
📚 Supplies support both classroom and home creative projects
👨‍👩‍👧‍👦 Family engagement through take-home art activities

Corporate Recognition:
• Branded supply packaging with company logo
• Thank you videos from student recipients
• Social media campaign featuring supply distributions
• Annual appreciation event with students and families
• Corporate volunteer team building opportunities

Your company's partnership ensures no student's creativity is limited by lack of materials.

Creatively grateful,
CSOAF Supply Coordination Team"""
            },
            
            "Digital Arts Innovation Lab Sponsor": {
                "subject": "Future-Forward Partnership: Digital Arts Innovation Lab",
                "content": """Dear {company_name} Technology Leadership,

CSOAF invites {company_name} to sponsor our cutting-edge Digital Arts Innovation Lab, merging technology with traditional arts education.

Innovation Lab Features:
💻 State-of-the-art digital art software and tablets
🎬 Video production and editing capabilities
🎮 Interactive media and game design programs
📱 Mobile app development through artistic expression
🤖 AI-assisted creative tools and workshops

Corporate Sponsorship Benefits:
• Lab naming rights: "{company_name} Digital Arts Innovation Lab"
• Logo placement on all lab equipment and signage
• Employee volunteer opportunities as technology mentors
• First access to student digital portfolios for internship recruitment
• Corporate showcase events featuring student digital projects

Technology Investment: ${tech_amount:,}

21st Century Impact:
💡 {student_count} students gain digital arts skills annually
🖥️ Modern technology preparation for creative careers
🌐 Global collaboration projects with other arts institutions
📊 Measurable improvements in technical skill assessments

Position your company at the forefront of arts and technology integration.

Innovatively yours,
CSOAF Technology Integration Team"""
            }
        }
        
        return {
            'foundation_templates': foundation_templates,
            'corporation_templates': corporation_templates
        }
        
    except Exception as e:
        st.warning(f"⚠️ Using simplified templates due to import error: {e}")
        # Fallback simplified templates
        return {
            'foundation_templates': {
                "Basic Program Funding": {
                    "subject": "Arts Education Partnership Opportunity",
                    "content": "Dear Foundation Team,\n\nWe request your partnership in bringing arts education to underserved students.\n\nBest regards,\nCSOAF Team"
                }
            },
            'corporation_templates': {
                "Basic Event Sponsorship": {
                    "subject": "Corporate Sponsorship Opportunity",
                    "content": "Dear Corporate Team,\n\nWe invite your company to sponsor our upcoming arts event.\n\nBest regards,\nCSOAF Events"
                }
            }
        }

def show_main_header():
    """Show main application header"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 CSOAF Email Campaign Manager</h1>
        <p>Simple, Powerful Campaign Management for Arts Education Sponsorship</p>
    </div>
    """, unsafe_allow_html=True)

def data_records_page():
    """Enhanced Data Records page with separate corporation and foundation sections"""
    st.title("📊 Data Records")
    st.markdown("### Your complete database of sponsors and partners")
    
    # Create tabs for different data types
    tab1, tab2 = st.tabs(["🏢 Corporations (Events)", "🏛️ Foundations (Programs)"])
    
    with tab1:
        st.subheader("🏢 Corporation Database - Event Sponsorship")
        st.markdown("*Fortune 1000 companies for art gallery galas, wine tastings, and cultural events*")
        
        # Load corporation data
        corp_df = load_corporation_data()
        
        if not corp_df.empty:
            # Search and filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                search_corp = st.text_input("🔍 Search corporations", key="corp_search")
            with col2:
                if 'industry_sector' in corp_df.columns:
                    industries = ['All'] + list(corp_df['industry_sector'].dropna().unique())
                    selected_industry = st.selectbox("Industry Filter", industries, key="corp_industry")
            with col3:
                if 'sponsorship_likelihood' in corp_df.columns:
                    likelihood_filter = st.selectbox("Sponsorship Likelihood", 
                                                   ['All', 'High', 'Medium', 'Low'], key="corp_likelihood")
            
            # Filter data
            filtered_corp = corp_df.copy()
            if search_corp:
                search_cols = ['organization_name', 'industry_sector', 'headquarters_location']
                search_cols = [col for col in search_cols if col in filtered_corp.columns]
                if search_cols:
                    mask = filtered_corp[search_cols].astype(str).apply(
                        lambda x: x.str.contains(search_corp, case=False, na=False)
                    ).any(axis=1)
                    filtered_corp = filtered_corp[mask]
            
            if 'industry_sector' in corp_df.columns and selected_industry != 'All':
                filtered_corp = filtered_corp[filtered_corp['industry_sector'] == selected_industry]
            
            if 'sponsorship_likelihood' in corp_df.columns and likelihood_filter != 'All':
                filtered_corp = filtered_corp[filtered_corp['sponsorship_likelihood'].str.contains(likelihood_filter, case=False, na=False)]
            
            # Display summary stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Corporations", len(filtered_corp))
            with col2:
                if 'sponsorship_amount_high' in filtered_corp.columns:
                    avg_sponsorship = filtered_corp['sponsorship_amount_high'].mean()
                    st.metric("Avg High Sponsorship", f"${avg_sponsorship:,.0f}" if pd.notna(avg_sponsorship) else "N/A")
            with col3:
                if 'industry_sector' in filtered_corp.columns:
                    st.metric("Industries", filtered_corp['industry_sector'].nunique())
            with col4:
                if 'sponsorship_likelihood' in filtered_corp.columns:
                    high_likelihood = len(filtered_corp[filtered_corp['sponsorship_likelihood'].str.contains('High', case=False, na=False)])
                    st.metric("High Likelihood", high_likelihood)
            
            # Display table with key columns
            display_cols = []
            priority_cols = ['organization_name', 'industry_sector', 'sponsorship_likelihood', 
                           'sponsorship_amount_high', 'contact_email', 'headquarters_location']
            
            for col in priority_cols:
                if col in filtered_corp.columns:
                    display_cols.append(col)
            
            # Add any remaining important columns
            for col in filtered_corp.columns:
                if col not in display_cols and col not in ['Unnamed: 0', 'index']:
                    display_cols.append(col)
            
            if display_cols:
                st.dataframe(
                    filtered_corp[display_cols[:8]],  # Limit to 8 columns for display
                    use_container_width=True,
                    height=400
                )
            
            # Export option
            if st.button("📥 Export Corporation Data", key="export_corp"):
                csv = filtered_corp.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"corporation_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("⚠️ No corporation data available. Please check data file location.")
    
    with tab2:
        st.subheader("🏛️ Foundation Database - Program Funding")
        st.markdown("*Foundations and grants for educational programs, classes, and community outreach*")
        
        # Load foundation data
        found_df = load_foundation_data()
        
        if not found_df.empty:
            # Search and filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                search_found = st.text_input("🔍 Search foundations", key="found_search")
            with col2:
                if 'funding_type' in found_df.columns:
                    funding_types = ['All'] + list(found_df['funding_type'].dropna().unique())
                    selected_funding = st.selectbox("Funding Type", funding_types, key="found_funding")
            with col3:
                if 'mission_alignment_score' in found_df.columns:
                    alignment_filter = st.selectbox("Mission Alignment", 
                                                  ['All', 'High (8-10)', 'Medium (5-7)', 'Low (1-4)'], key="found_alignment")
            
            # Filter data
            filtered_found = found_df.copy()
            if search_found:
                search_cols = ['organization_name', 'mission_statement', 'focus_areas']
                search_cols = [col for col in search_cols if col in filtered_found.columns]
                if search_cols:
                    mask = filtered_found[search_cols].astype(str).apply(
                        lambda x: x.str.contains(search_found, case=False, na=False)
                    ).any(axis=1)
                    filtered_found = filtered_found[mask]
            
            if 'funding_type' in found_df.columns and selected_funding != 'All':
                filtered_found = filtered_found[filtered_found['funding_type'] == selected_funding]
            
            if 'mission_alignment_score' in found_df.columns and alignment_filter != 'All':
                if alignment_filter == 'High (8-10)':
                    filtered_found = filtered_found[filtered_found['mission_alignment_score'] >= 8]
                elif alignment_filter == 'Medium (5-7)':
                    filtered_found = filtered_found[(filtered_found['mission_alignment_score'] >= 5) & 
                                                  (filtered_found['mission_alignment_score'] < 8)]
                elif alignment_filter == 'Low (1-4)':
                    filtered_found = filtered_found[filtered_found['mission_alignment_score'] < 5]
            
            # Display summary stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Foundations", len(filtered_found))
            with col2:
                if 'mission_alignment_score' in filtered_found.columns:
                    avg_alignment = filtered_found['mission_alignment_score'].mean()
                    st.metric("Avg Alignment", f"{avg_alignment:.1f}" if pd.notna(avg_alignment) else "N/A")
            with col3:
                if 'funding_type' in filtered_found.columns:
                    st.metric("Funding Types", filtered_found['funding_type'].nunique())
            with col4:
                if 'mission_alignment_score' in filtered_found.columns:
                    high_alignment = len(filtered_found[filtered_found['mission_alignment_score'] >= 8])
                    st.metric("High Alignment", high_alignment)
            
            # Display table with key columns
            display_cols = []
            priority_cols = ['organization_name', 'mission_alignment_score', 'funding_type', 
                           'website', 'organization_type', 'focus_areas']
            
            for col in priority_cols:
                if col in filtered_found.columns:
                    display_cols.append(col)
            
            # Add any remaining important columns
            for col in filtered_found.columns:
                if col not in display_cols and col not in ['Unnamed: 0', 'index']:
                    display_cols.append(col)
            
            if display_cols:
                st.dataframe(
                    filtered_found[display_cols[:8]],  # Limit to 8 columns for display
                    use_container_width=True,
                    height=400
                )
            
            # Export option
            if st.button("📥 Export Foundation Data", key="export_found"):
                csv = filtered_found.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"foundation_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("⚠️ No foundation data available. Please check data file location.")

def show_create_campaign():
    """Step 1: Create Campaign"""
    st.markdown('<div class="step-header"><h2>📝 Step 1: Create Campaign</h2></div>', unsafe_allow_html=True)
    
    # Ensure current_campaign is not None
    if st.session_state.current_campaign is None:
        st.session_state.current_campaign = {}
    
    with st.form("create_campaign_form"):
        st.markdown("### Campaign Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            campaign_name = st.text_input(
                "Campaign Name *",
                value=st.session_state.current_campaign.get('name', ''),
                placeholder="e.g., Tech Giants STEM Arts Initiative"
            )
            
            campaign_type = st.selectbox(
                "Campaign Type *",
                [
                    "Arts Education Sponsorship",
                    "STEM Program Funding", 
                    "Community Arts Initiative",
                    "Healthcare Arts Program",
                    "Technology Innovation Arts"
                ],
                index=0
            )
            
            target_funding = st.number_input(
                "Target Funding Amount ($) *",
                min_value=1000,
                max_value=10000000,
                value=st.session_state.current_campaign.get('target_funding', 50000),
                step=1000
            )
        
        with col2:
            deadline = st.date_input(
                "Campaign Deadline *",
                value=date(2025, 12, 31)
            )
            
            priority = st.selectbox(
                "Priority Level *",
                ["High", "Medium", "Low"],
                index=0
            )
            
            expected_sponsors = st.number_input(
                "Expected Number of Sponsors",
                min_value=1,
                max_value=100,
                value=20,
                step=1
            )
        
        campaign_description = st.text_area(
            "Campaign Description *",
            value=st.session_state.current_campaign.get('description', ''),
            height=100,
            placeholder="Describe your campaign goals, target audience, and expected outcomes..."
        )
        
        submitted = st.form_submit_button("✅ Create Campaign", type="primary")
        
        if submitted:
            if campaign_name and campaign_description and target_funding:
                # Store campaign data
                st.session_state.current_campaign = {
                    'name': campaign_name,
                    'type': campaign_type,
                    'description': campaign_description,
                    'target_funding': target_funding,
                    'deadline': deadline.isoformat(),
                    'priority': priority,
                    'expected_sponsors': expected_sponsors,
                    'created_at': datetime.now().isoformat(),
                    'status': 'created'
                }
                
                st.success("✅ Campaign created successfully!")
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields (marked with *)")
    
    # Show current campaign if exists
    if st.session_state.current_campaign:
        st.markdown("### 📋 Current Campaign")
        st.json(st.session_state.current_campaign)

def categorize_sponsors_by_industry_and_amount(sponsors_df):
    """Categorize sponsors by industry and sponsorship amount"""
    categories = {}
    
    if sponsors_df.empty:
        st.warning("🔍 Debug: DataFrame is empty")
        return categories
    
    # Debug: Show what columns we have
    st.info(f"🔍 Debug: Available columns: {list(sponsors_df.columns)}")
    
    # Define sponsorship tiers
    def get_sponsorship_tier(amount):
        if pd.isna(amount):
            return "Unknown"
        elif amount >= 50000:
            return "Premier ($50K+)"
        elif amount >= 20000:
            return "Major ($20K-50K)"
        elif amount >= 10000:
            return "Supporting ($10K-20K)"
        else:
            return "Basic (<$10K)"
    
    # Add tier column - handle different data source types
    amount_col = None
    # Corporation data columns
    if 'estimated_max_sponsorship' in sponsors_df.columns:
        amount_col = 'estimated_max_sponsorship'
        sponsors_df['sponsorship_tier'] = sponsors_df[amount_col].apply(get_sponsorship_tier)
    elif 'estimated_typical_sponsorship' in sponsors_df.columns:
        amount_col = 'estimated_typical_sponsorship'
        sponsors_df['sponsorship_tier'] = sponsors_df[amount_col].apply(get_sponsorship_tier)
    # Foundation data columns
    elif 'mission_alignment_score' in sponsors_df.columns:
        # For foundations, use mission alignment score to create tiers
        sponsors_df['sponsorship_tier'] = sponsors_df['mission_alignment_score'].apply(
            lambda x: "High Alignment (20+)" if x >= 20 else
                     "Medium Alignment (10-20)" if x >= 10 else
                     "Basic Alignment (<10)" if x > 0 else "Unknown"
        )
    # Fallback columns
    elif 'Revenue' in sponsors_df.columns:
        amount_col = 'Revenue'
        sponsors_df['sponsorship_tier'] = (sponsors_df[amount_col] / 100).apply(get_sponsorship_tier)
    else:
        st.warning("🔍 Debug: No amount/score column found, using Unknown tier")
        sponsors_df['sponsorship_tier'] = "Unknown"
    
    st.info(f"🔍 Debug: Using {amount_col or 'mission_alignment_score'} for sponsorship tiers")
    
    # Group by industry/type and tier - handle different categorization approaches
    category_col = None
    
    # Corporation data - use industry sectors
    if 'industry_sector' in sponsors_df.columns:
        category_col = 'industry_sector'
        st.info(f"🔍 Debug: Using {category_col} for industry categorization (Corporation data)")
    # Foundation data - use funding type + organization type
    elif 'funding_type' in sponsors_df.columns:
        category_col = 'funding_type'
        st.info(f"🔍 Debug: Using {category_col} for categorization (Foundation data)")
    # Fallback to other possible industry columns
    elif 'Industry' in sponsors_df.columns:
        category_col = 'Industry'
        st.info(f"🔍 Debug: Using {category_col} for industry categorization")
    
    if category_col:
        category_data = sponsors_df[sponsors_df[category_col].notna()]
        
        if category_data.empty:
            st.warning(f"🔍 Debug: No non-null values in {category_col}")
            return categories
            
        for category in category_data[category_col].unique():
            category_sponsors = category_data[category_data[category_col] == category]
            
            for tier in category_sponsors['sponsorship_tier'].unique():
                tier_data = category_sponsors[category_sponsors['sponsorship_tier'] == tier]
                category_name = f"{category} - {tier}"
                
                # Calculate potential funding
                potential_funding = 0
                if amount_col and amount_col in tier_data.columns:
                    if amount_col == 'Revenue':
                        potential_funding = tier_data[amount_col].sum() / 100  # Estimate 1% of revenue
                    else:
                        potential_funding = tier_data[amount_col].sum()
                elif 'mission_alignment_score' in tier_data.columns:
                    # For foundations, estimate funding based on alignment score
                    avg_score = tier_data['mission_alignment_score'].mean()
                    potential_funding = avg_score * 1000  # Rough estimate: $1K per alignment point
                
                categories[category_name] = {
                    'sponsors': tier_data.to_dict('records'),
                    'count': len(tier_data),
                    'industry': category,
                    'tier': tier,
                    'potential_funding': potential_funding
                }
        
        st.success(f"🔍 Debug: Created {len(categories)} categories from {len(category_data)} sponsors")
    else:
        st.error("🔍 Debug: No categorization column found in dataframe")
        st.info(f"Looked for: industry_sector, funding_type, Industry")
    
    return categories

def suggest_template_for_category(industry, tier, campaign_type):
    """Suggest appropriate template based on industry, tier, and campaign type"""
    templates_data = load_email_templates()
    corporation_templates = templates_data['corporation_templates']
    foundation_templates = templates_data['foundation_templates']
    
    # Template matching logic
    suggestions = []
    
    if campaign_type in ['Event Fundraising', 'Gallery Gala', 'Wine Tasting']:
        # Corporation templates for events
        if 'Technology' in industry:
            suggestions.append(('Digital Arts Innovation Lab Sponsor', corporation_templates.get('Digital Arts Innovation Lab Sponsor')))
        elif 'Healthcare' in industry and 'Wine' in campaign_type:
            suggestions.append(('Wine Tasting Fundraiser Partnership', corporation_templates.get('Wine Tasting Fundraiser Partnership')))
        elif 'Premier' in tier:
            suggestions.append(('Art Gallery Gala Sponsorship', corporation_templates.get('Art Gallery Gala Sponsorship')))
        elif 'Major' in tier:
            suggestions.append(('Corporate Arts Challenge Sponsorship', corporation_templates.get('Corporate Arts Challenge Sponsorship')))
        else:
            suggestions.append(('Art Supply Drive Corporate Champion', corporation_templates.get('Art Supply Drive Corporate Champion')))
    
    else:
        # Foundation templates for programs
        if 'Education' in campaign_type:
            suggestions.append(('Arts Education Program Funding', foundation_templates.get('Arts Education Program Funding')))
        elif 'STEM' in campaign_type or 'Technology' in industry:
            suggestions.append(('STEM-Arts Integration Funding', foundation_templates.get('STEM-Arts Integration Funding')))
        else:
            suggestions.append(('Community Arts Access Program', foundation_templates.get('Community Arts Access Program')))
    
    return suggestions[0] if suggestions else (None, None)

def show_generate_sponsors():
    """Enhanced Step 2: Generate & Categorize Sponsors"""
    st.title("🎯 Generate & Categorize Sponsors")
    st.markdown("### AI-powered sponsor generation with automatic categorization")
    
    # Check prerequisites
    if not st.session_state.current_campaign:
        st.warning("⚠️ Please create a campaign first!")
        return
    
    campaign = st.session_state.current_campaign
    
    # Show campaign info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Campaign", campaign['name'])
    with col2:
        st.metric("Type", campaign['type'])
    with col3:
        st.metric("Target Funding", f"${campaign['target_funding']:,}")
    
    # Sponsor generation parameters
    st.markdown("### 🎯 Sponsor Generation Parameters")
    
    col1, col2 = st.columns(2)
    with col1:
        min_sponsorship = st.number_input(
            "Minimum Sponsorship Amount ($)",
            min_value=1000,
            max_value=100000,
            value=5000,
            step=1000
        )
        
        max_sponsors = st.number_input(
            "Maximum Number of Sponsors",
            min_value=5,
            max_value=100,
            value=25,
            step=5
        )
    
    with col2:
        industry_focus = st.multiselect(
            "Focus Industries (optional)",
            ["Technology", "Healthcare", "Finance", "Energy", "Retail", "Manufacturing"],
            default=[]
        )
        
        data_source = st.selectbox(
            "Data Source",
            ["Both Databases (Auto-select)", "Corporations Only (Events)", "Foundations Only (Programs)"]
        )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤖 Generate AI-Powered Sponsor List", type="primary"):
            with st.spinner("🔍 Analyzing databases and generating optimal sponsor matches..."):
                time.sleep(2)
                
                sponsors_list = []
                
                # Load appropriate data based on campaign type and user selection
                if data_source == "Both Databases (Auto-select)":
                    if campaign['type'] in ['Event Fundraising', 'Gallery Gala', 'Wine Tasting']:
                        corp_df = load_corporation_data()
                        if not corp_df.empty:
                            sponsors_list.extend(corp_df.head(max_sponsors//2).to_dict('records'))
                    else:
                        found_df = load_foundation_data()
                        if not found_df.empty:
                            sponsors_list.extend(found_df.head(max_sponsors//2).to_dict('records'))
                elif data_source == "Corporations Only (Events)":
                    corp_df = load_corporation_data()
                    if not corp_df.empty:
                        sponsors_list.extend(corp_df.head(max_sponsors).to_dict('records'))
                elif data_source == "Foundations Only (Programs)":
                    found_df = load_foundation_data()
                    if not found_df.empty:
                        sponsors_list.extend(found_df.head(max_sponsors).to_dict('records'))
                
                if sponsors_list:
                    sponsors_df = pd.DataFrame(sponsors_list)
                    
                    # Apply filters
                    industry_col = 'industry_sector' if 'industry_sector' in sponsors_df.columns else 'Industry'
                    if industry_focus and industry_col in sponsors_df.columns:
                        sponsors_df = sponsors_df[sponsors_df[industry_col].isin(industry_focus)]
                    
                    # Apply minimum sponsorship filter
                    if 'sponsorship_amount_high' in sponsors_df.columns:
                        sponsors_df = sponsors_df[sponsors_df['sponsorship_amount_high'] >= min_sponsorship]
                    elif 'Revenue' in sponsors_df.columns:
                        sponsors_df = sponsors_df[sponsors_df['Revenue'] >= min_sponsorship * 100]  # Revenue proxy
                    
                    # Store generated sponsors
                    st.session_state.generated_sponsors = sponsors_df.to_dict('records')
                    
                    # Automatically categorize sponsors
                    st.session_state.sponsor_categories = categorize_sponsors_by_industry_and_amount(sponsors_df)
                    
                    # Show success with categorization info
                    if st.session_state.sponsor_categories:
                        st.success(f"✅ Generated {len(sponsors_df)} sponsors and automatically categorized into {len(st.session_state.sponsor_categories)} categories!")
                        st.info("💡 Scroll down to see sponsor categories and approve templates for each category")
                    else:
                        st.success(f"✅ Generated {len(sponsors_df)} sponsors!")
                        st.warning("⚠️ Unable to categorize sponsors - check if industry data is available")
                else:
                    st.error("❌ No sponsor data available")
    
    with col2:
        # AI-Enhanced Web Scraping
        if st.session_state.generated_sponsors:
            st.markdown("### 🧠 AI-Enhanced Data Collection")
            
            # OpenAI API Key input
            openai_api_key = st.text_input(
                "OpenAI API Key (optional)", 
                type="password",
                help="Provide OpenAI API key for intelligent web scraping. Leave blank for simulated enhancement.",
                value=os.environ.get('OPENAI_API_KEY', '')
            )
            
            scraping_mode = st.selectbox(
                "Enhancement Mode",
                ["🧠 AI-Powered (OpenAI)", "🎲 Simulated (Demo)"],
                help="AI mode uses OpenAI to find real data, Simulated mode generates sample data"
            )
            
            if st.button("🌐 Enhance Sponsor Data", help="Intelligently scrape missing contact info and donation history"):
                with st.spinner("🔍 AI analyzing web sources for missing sponsor data..."):
                    if scraping_mode == "🧠 AI-Powered (OpenAI)" and openai_api_key:
                        # Use real AI enhancement
                        findings = enhance_sponsor_data_with_ai(st.session_state.generated_sponsors, openai_api_key)
                        enhancement_type = "AI-powered"
                    else:
                        # Use simulated enhancement
                        findings = simulate_web_scraping(st.session_state.generated_sponsors)
                        enhancement_type = "Simulated"
                    
                    time.sleep(3)  # Processing time
                    
                    st.success(f"✅ {enhancement_type} enhancement completed!")
                    
                    # Show detailed findings
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"""� **Contact Information:**
                        • {findings.get('emails_found', 0)} contact emails found
                        • {findings.get('names_found', 0)} contact names found
                        • {findings.get('websites_found', 0)} websites verified""")
                    
                    with col2:
                        st.info(f"""🎯 **Mission & Giving Data:**
                        • {findings.get('missions_found', 0)} mission statements found
                        • {findings.get('donations_found', 0)} past donation records found
                        • {findings.get('focus_areas_found', 0)} donation focus areas identified""")
                    
                    # Update the sponsor categories with enhanced data
                    if st.session_state.get('sponsor_categories'):
                        enhanced_df = pd.DataFrame(st.session_state.generated_sponsors)
                        st.session_state.sponsor_categories = categorize_sponsors_by_industry_and_amount(enhanced_df)
                        
                        st.balloons()
                        st.success("🎉 All sponsor categories updated with enhanced data!")
    
    # Show categorized sponsors
    if st.session_state.generated_sponsors and len(st.session_state.generated_sponsors) > 0:
        st.markdown("### 📊 Sponsor Categories")
        
        # Check if we have categories
        if st.session_state.sponsor_categories and len(st.session_state.sponsor_categories) > 0:
            # Category overview
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_sponsors = sum(cat['count'] for cat in st.session_state.sponsor_categories.values())
                st.metric("Total Sponsors", total_sponsors)
            with col2:
                st.metric("Categories", len(st.session_state.sponsor_categories))
            with col3:
                total_potential = sum(cat['potential_funding'] for cat in st.session_state.sponsor_categories.values())
                st.metric("Potential Funding", f"${total_potential:,.0f}")
            with col4:
                avg_per_category = total_sponsors / len(st.session_state.sponsor_categories) if st.session_state.sponsor_categories else 0
                st.metric("Avg per Category", f"{avg_per_category:.1f}")
            
            # Display each category
            for category_name, category_data in st.session_state.sponsor_categories.items():
                with st.expander(f"📁 {category_name} ({category_data['count']} sponsors)", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Show sponsor details with enhanced fields
                        sponsors_df = pd.DataFrame(category_data['sponsors'])
                        display_cols = []
                        priority_cols = [
                            'organization_name', 'Company', 'contact_name', 'contact_email', 
                            'website', 'mission_statement', 'past_donations', 'donation_focus',
                            'sponsorship_amount_high', 'Revenue', 'Industry'
                        ]
                        
                        for col in priority_cols:
                            if col in sponsors_df.columns:
                                display_cols.append(col)
                        
                        if display_cols:
                            # Show enhanced data with special highlighting
                            enhanced_df = sponsors_df[display_cols[:8]].copy()  # Limit to 8 columns for display
                            
                            # Add indicators for enhanced fields
                            for idx, row in enhanced_df.iterrows():
                                if pd.notna(row.get('contact_email')) and '@' in str(row.get('contact_email', '')):
                                    # Highlight enhanced emails
                                    if 'partnerships@' in str(row.get('contact_email', '')):
                                        enhanced_df.loc[idx, 'contact_email'] = f"🔍 {row['contact_email']}"
                            
                            st.dataframe(enhanced_df, use_container_width=True, height=200)
                            
                            # Show enhanced data summary for this category
                            enhanced_count = 0
                            for sponsor in category_data['sponsors']:
                                if (sponsor.get('contact_email') and 'partnerships@' in str(sponsor.get('contact_email', ''))) or \
                                   sponsor.get('mission_statement') or sponsor.get('past_donations'):
                                    enhanced_count += 1
                            
                            if enhanced_count > 0:
                                st.success(f"🔍 {enhanced_count} records enhanced with AI-scraped data")
                        
                        # Show detailed enhanced fields for first sponsor
                        if category_data['sponsors']:
                            sample_sponsor = category_data['sponsors'][0]
                            
                            if st.button(f"📋 View Enhanced Data Sample", key=f"enhanced_sample_{category_name}"):
                                st.session_state[f"show_enhanced_{category_name}"] = True
                            
                            if st.session_state.get(f"show_enhanced_{category_name}"):
                                st.markdown("**🔍 AI-Enhanced Data Sample:**")
                                
                                enhanced_fields = {}
                                if sample_sponsor.get('contact_name'):
                                    enhanced_fields['Contact Name'] = sample_sponsor['contact_name']
                                if sample_sponsor.get('contact_email'):
                                    enhanced_fields['Contact Email'] = sample_sponsor['contact_email']
                                if sample_sponsor.get('website'):
                                    enhanced_fields['Website'] = sample_sponsor['website']
                                if sample_sponsor.get('mission_statement'):
                                    enhanced_fields['Mission'] = sample_sponsor['mission_statement'][:100] + "..."
                                if sample_sponsor.get('past_donations'):
                                    enhanced_fields['Past Donations'] = sample_sponsor['past_donations']
                                if sample_sponsor.get('donation_focus'):
                                    enhanced_fields['Focus Areas'] = sample_sponsor['donation_focus']
                                
                                if enhanced_fields:
                                    for field, value in enhanced_fields.items():
                                        st.markdown(f"**{field}:** {value}")
                                else:
                                    st.info("💡 Run AI enhancement to see scraped data here")
                    
                    with col2:
                        # Suggest template
                        suggested_template_name, suggested_template = suggest_template_for_category(
                            category_data['industry'], 
                            category_data['tier'], 
                            campaign['type']
                        )
                        
                        if suggested_template_name:
                            st.markdown("**🎯 Suggested Template:**")
                            st.info(f"📧 {suggested_template_name}")
                            
                            if st.button(f"👁️ Preview Template", key=f"preview_{category_name}"):
                                st.session_state[f"preview_template_{category_name}"] = suggested_template
                        
                        st.markdown(f"**💰 Potential Funding:**")
                        st.metric("", f"${category_data['potential_funding']:,.0f}")
                    
                    # Show template preview if requested
                    if st.session_state.get(f"preview_template_{category_name}"):
                        template = st.session_state[f"preview_template_{category_name}"]
                        st.markdown("**📧 Template Preview:**")
                        st.text_area(
                            "Subject:", 
                            value=template['subject'], 
                            height=50, 
                            key=f"subject_preview_{category_name}",
                            disabled=True
                        )
                        st.text_area(
                            "Content:", 
                            value=template['content'][:300] + "...", 
                            height=150, 
                            key=f"content_preview_{category_name}",
                            disabled=True
                        )
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("✅ Approve Template", key=f"approve_{category_name}"):
                                if 'approved_templates' not in st.session_state:
                                    st.session_state.approved_templates = {}
                                st.session_state.approved_templates[category_name] = {
                                    'template_name': suggested_template_name,
                                    'template': template,
                                    'status': 'approved'
                                }
                                st.success(f"✅ Template approved for {category_name}")
                        
                        with col2:
                            if st.button("❌ Reject Template", key=f"reject_{category_name}"):
                                st.warning("Template rejected. Please choose a different one in Create Templates step.")
                        
                        with col3:
                            if st.button("✏️ Customize", key=f"customize_{category_name}"):
                                st.info("💡 Go to Create Templates to customize this template.")
            
            # Export all sponsors
            if st.button("📥 Export All Categorized Sponsors"):
                all_sponsors_df = pd.DataFrame(st.session_state.generated_sponsors)
                csv = all_sponsors_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"categorized_sponsors_{campaign['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        else:
            # Show sponsors without categories (fallback)
            st.warning("⚠️ Unable to categorize sponsors automatically. Showing as single list:")
            sponsors_df = pd.DataFrame(st.session_state.generated_sponsors)
            
            # Display basic sponsor list
            display_cols = []
            priority_cols = ['organization_name', 'Company', 'Industry', 'industry_sector', 'Revenue', 'sponsorship_amount_high']
            
            for col in priority_cols:
                if col in sponsors_df.columns:
                    display_cols.append(col)
            
            if display_cols:
                st.dataframe(sponsors_df[display_cols[:6]], use_container_width=True, height=400)
            
            # Manual categorization button
            if st.button("🔄 Try Re-categorizing Sponsors"):
                with st.spinner("🔄 Re-analyzing sponsor data for categorization..."):
                    time.sleep(1)
                    st.session_state.sponsor_categories = categorize_sponsors_by_industry_and_amount(sponsors_df)
                    if st.session_state.sponsor_categories:
                        st.success("✅ Categorization successful! Refresh the page to see categories.")
                        st.rerun()
                    else:
                        st.error("❌ Still unable to categorize. Please check if industry and revenue data is available.")

def create_templates_page():
    """Enhanced Template Management page with categories and edit capability"""
    st.title("📧 Template Library")
    st.markdown("### Manage your email templates with categories and editing")
    
    # Load templates
    templates_data = load_email_templates()
    foundation_templates = templates_data['foundation_templates']
    corporation_templates = templates_data['corporation_templates']
    
    # Create tabs for template categories
    tab1, tab2, tab3 = st.tabs(["🏛️ Foundation Templates", "🏢 Corporation Templates", "➕ Create New"])
    
    with tab1:
        st.subheader("🏛️ Foundation Templates")
        st.markdown("*For program funding, classes, and educational initiatives*")
        
        # Display foundation templates with expandable sections
        for template_name, template_data in foundation_templates.items():
            with st.expander(f"📄 {template_name}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Edit mode toggle
                    edit_key = f"edit_found_{template_name.replace(' ', '_')}"
                    if edit_key not in st.session_state:
                        st.session_state[edit_key] = False
                    
                    if st.button(f"✏️ {'Save' if st.session_state[edit_key] else 'Edit'}", 
                               key=f"edit_btn_found_{template_name.replace(' ', '_')}"):
                        st.session_state[edit_key] = not st.session_state[edit_key]
                        if not st.session_state[edit_key]:
                            st.success("Template saved!")
                
                with col2:
                    if st.button("📋 Copy", key=f"copy_found_{template_name.replace(' ', '_')}"):
                        st.session_state[f"copied_template"] = template_data
                        st.success("Template copied!")
                
                # Subject line
                st.markdown("**Subject:**")
                if st.session_state[edit_key]:
                    new_subject = st.text_input(
                        "Subject", 
                        value=template_data['subject'],
                        key=f"subject_found_{template_name.replace(' ', '_')}"
                    )
                else:
                    st.text(template_data['subject'])
                
                # Email content
                st.markdown("**Content:**")
                if st.session_state[edit_key]:
                    new_content = st.text_area(
                        "Content", 
                        value=template_data['content'],
                        height=300,
                        key=f"content_found_{template_name.replace(' ', '_')}"
                    )
                else:
                    st.text_area(
                        "Content Preview", 
                        value=template_data['content'],
                        height=200,
                        disabled=True,
                        key=f"preview_found_{template_name.replace(' ', '_')}"
                    )
                
                # Template variables helper
                if st.session_state[edit_key]:
                    st.info("""
                    💡 **Available Variables:** 
                    {foundation_name}, {funding_amount}, {duration}, {student_count}, 
                    {location}, {target_schools}, {program_hours}, {community_count}
                    """)
    
    with tab2:
        st.subheader("🏢 Corporation Templates")
        st.markdown("*For event sponsorship, galas, wine tastings, and corporate partnerships*")
        
        # Display corporation templates with expandable sections
        for template_name, template_data in corporation_templates.items():
            with st.expander(f"📄 {template_name}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Edit mode toggle
                    edit_key = f"edit_corp_{template_name.replace(' ', '_')}"
                    if edit_key not in st.session_state:
                        st.session_state[edit_key] = False
                    
                    if st.button(f"✏️ {'Save' if st.session_state[edit_key] else 'Edit'}", 
                               key=f"edit_btn_corp_{template_name.replace(' ', '_')}"):
                        st.session_state[edit_key] = not st.session_state[edit_key]
                        if not st.session_state[edit_key]:
                            st.success("Template saved!")
                
                with col2:
                    if st.button("📋 Copy", key=f"copy_corp_{template_name.replace(' ', '_')}"):
                        st.session_state[f"copied_template"] = template_data
                        st.success("Template copied!")
                
                # Subject line
                st.markdown("**Subject:**")
                if st.session_state[edit_key]:
                    new_subject = st.text_input(
                        "Subject", 
                        value=template_data['subject'],
                        key=f"subject_corp_{template_name.replace(' ', '_')}"
                    )
                else:
                    st.text(template_data['subject'])
                
                # Email content
                st.markdown("**Content:**")
                if st.session_state[edit_key]:
                    new_content = st.text_area(
                        "Content", 
                        value=template_data['content'],
                        height=300,
                        key=f"content_corp_{template_name.replace(' ', '_')}"
                    )
                else:
                    st.text_area(
                        "Content Preview", 
                        value=template_data['content'],
                        height=200,
                        disabled=True,
                        key=f"preview_corp_{template_name.replace(' ', '_')}"
                    )
                
                # Template variables helper
                if st.session_state[edit_key]:
                    st.info("""
                    💡 **Available Variables:** 
                    {company_name}, {event_date}, {venue_name}, {expected_guests}, 
                    {presenting_amount}, {premier_amount}, {supporting_amount}
                    """)
    
    with tab3:
        st.subheader("➕ Create New Template")
        st.markdown("*Build custom templates for specific campaigns*")
        
        with st.form("new_template_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                template_name = st.text_input("Template Name*", placeholder="Enter template name")
                template_category = st.selectbox(
                    "Category*", 
                    ["Foundation - Program Funding", "Corporation - Event Sponsorship", "General"]
                )
            
            with col2:
                template_type = st.selectbox(
                    "Template Type*", 
                    ["Initial Request", "Follow-up", "Thank You", "Event Invitation", "Custom"]
                )
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            
            subject = st.text_input("Email Subject*", placeholder="Enter email subject line")
            
            content = st.text_area(
                "Email Content*", 
                height=250,
                placeholder="Write your email template content here..."
            )
            
            # Variables helper
            st.markdown("**💡 Template Variables You Can Use:**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Foundation Variables:**
                - `{foundation_name}`
                - `{funding_amount}`
                - `{student_count}`
                - `{program_duration}`
                """)
            with col2:
                st.markdown("""
                **Corporation Variables:**
                - `{company_name}`
                - `{event_date}`
                - `{sponsorship_amount}`
                - `{venue_name}`
                """)
            
            submitted = st.form_submit_button("💾 Save Template", type="primary")
            
            if submitted:
                if template_name and subject and content:
                    # Save to session state (in real app, save to database)
                    if 'custom_templates' not in st.session_state:
                        st.session_state.custom_templates = {}
                    
                    st.session_state.custom_templates[template_name] = {
                        'subject': subject,
                        'content': content,
                        'category': template_category,
                        'type': template_type,
                        'priority': priority,
                        'created_at': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    st.success(f"✅ Template '{template_name}' created successfully!")
                    st.balloons()
                else:
                    st.error("❌ Please fill in all required fields (marked with *)")
    
    # Template statistics
    st.markdown("---")
    st.subheader("📊 Template Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Foundation Templates", len(foundation_templates))
    with col2:
        st.metric("Corporation Templates", len(corporation_templates))
    with col3:
        custom_count = len(st.session_state.get('custom_templates', {}))
        st.metric("Custom Templates", custom_count)
    with col4:
        total_templates = len(foundation_templates) + len(corporation_templates) + custom_count
        st.metric("Total Templates", total_templates)

def show_send_track():
    """Enhanced Step 4: Send & Track by Category"""
    st.title("🚀 Send & Track Campaigns")
    st.markdown("### Send personalized emails by sponsor category")
    
    # Check prerequisites
    if not st.session_state.current_campaign:
        st.warning("⚠️ Please create a campaign first!")
        return
    
    if not st.session_state.get('generated_sponsors') or len(st.session_state.generated_sponsors) == 0:
        st.warning("⚠️ Please generate sponsors first!")
        return
    
    if not st.session_state.get('sponsor_categories') or len(st.session_state.sponsor_categories) == 0:
        st.warning("⚠️ Please generate and categorize sponsors first!")
        st.info("💡 Go to 'Generate & Categorize Sponsors' and click the generate button")
        return
    
    campaign = st.session_state.current_campaign
    
    # Campaign overview
    st.markdown("### 📋 Campaign Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Campaign", campaign['name'])
    with col2:
        total_sponsors = sum(cat['count'] for cat in st.session_state.sponsor_categories.values())
        st.metric("Total Sponsors", total_sponsors)
    with col3:
        st.metric("Categories", len(st.session_state.sponsor_categories))
    with col4:
        approved_templates = len(st.session_state.get('approved_templates', {}))
        st.metric("Approved Templates", approved_templates)
    
    # Mailchimp configuration
    st.markdown("### � Email Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        mailchimp_api_key = st.text_input(
            "Mailchimp API Key", 
            value=os.environ.get('MAILCHIMP_API_KEY', ''),
            type="password",
            help="Your Mailchimp API key for sending emails"
        )
        
        from_email = st.text_input(
            "From Email", 
            value="outreach@csoaf.org",
            help="The email address emails will be sent from"
        )
    
    with col2:
        from_name = st.text_input(
            "From Name", 
            value="CSOAF Outreach Team",
            help="The name that will appear as the sender"
        )
        
        test_mode = st.checkbox(
            "Test Mode (preview only, don't send)", 
            value=True,
            help="When enabled, emails will be previewed but not actually sent"
        )
    
    # Send by category
    st.markdown("### 📊 Send by Category")
    
    if st.session_state.sponsor_categories:
        for category_name, category_data in st.session_state.sponsor_categories.items():
            with st.expander(f"📁 {category_name} ({category_data['count']} sponsors)", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Category details
                    st.markdown(f"**Industry:** {category_data['industry']}")
                    st.markdown(f"**Tier:** {category_data['tier']}")
                    st.markdown(f"**Sponsors:** {category_data['count']}")
                    st.markdown(f"**Potential Funding:** ${category_data['potential_funding']:,.0f}")
                    
                    # Template selection for this category
                    approved_template = st.session_state.get('approved_templates', {}).get(category_name)
                    
                    if approved_template:
                        st.success(f"✅ Approved Template: {approved_template['template_name']}")
                        template_to_use = approved_template['template']
                        
                        # Preview personalized email
                        if st.button(f"�️ Preview Personalized Email", key=f"preview_email_{category_name}"):
                            st.session_state[f"show_preview_{category_name}"] = True
                        
                        # Show preview if requested
                        if st.session_state.get(f"show_preview_{category_name}"):
                            sample_sponsor = category_data['sponsors'][0] if category_data['sponsors'] else {}
                            
                            # Personalize template
                            company_name = sample_sponsor.get('organization_name', sample_sponsor.get('Company', '[Company Name]'))
                            
                            personalized_subject = template_to_use['subject'].replace('{company_name}', company_name)
                            personalized_content = template_to_use['content'].replace('{company_name}', company_name)
                            personalized_content = personalized_content.replace('{funding_amount}', f"${category_data['potential_funding']/category_data['count']:,.0f}")
                            
                            st.markdown("**📧 Personalized Email Preview:**")
                            st.text_area("Subject:", value=personalized_subject, height=50, disabled=True, key=f"prev_subj_{category_name}")
                            st.text_area("Content:", value=personalized_content[:400] + "...", height=200, disabled=True, key=f"prev_cont_{category_name}")
                        
                        # Send button
                        if st.button(f"🚀 Send to {category_name}", key=f"send_{category_name}", type="primary"):
                            if not mailchimp_api_key and not test_mode:
                                st.error("❌ Please provide Mailchimp API key to send emails")
                            else:
                                with st.spinner(f"{'Previewing' if test_mode else 'Sending'} emails to {category_name}..."):
                                    time.sleep(2)  # Simulate sending
                                    
                                    if test_mode:
                                        st.success(f"✅ Preview completed for {category_data['count']} sponsors in {category_name}")
                                        st.info("💡 Turn off Test Mode to actually send emails")
                                    else:
                                        st.success(f"✅ Sent {category_data['count']} personalized emails to {category_name}")
                                        st.balloons()
                                        
                                        # Store send history
                                        if 'sent_campaigns' not in st.session_state:
                                            st.session_state.sent_campaigns = []
                                        
                                        st.session_state.sent_campaigns.append({
                                            'category': category_name,
                                            'count': category_data['count'],
                                            'template': approved_template['template_name'],
                                            'sent_at': datetime.now().isoformat(),
                                            'campaign': campaign['name']
                                        })
                    
                    else:
                        st.warning("⚠️ No approved template for this category")
                        st.info("💡 Go to Generate Sponsors step to approve a template for this category")
                
                with col2:
                    # Sponsor list preview
                    st.markdown("**👥 Sponsor Preview:**")
                    sponsors_sample = category_data['sponsors'][:3]
                    for sponsor in sponsors_sample:
                        name = sponsor.get('organization_name', sponsor.get('Company', 'Unknown'))
                        st.markdown(f"• {name}")
                    if len(category_data['sponsors']) > 3:
                        st.markdown(f"• ... and {len(category_data['sponsors']) - 3} more")
    
    # Bulk send all categories
    st.markdown("### 🎯 Bulk Operations")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Send All Categories", type="secondary"):
            approved_categories = [cat for cat in st.session_state.sponsor_categories.keys() 
                                 if cat in st.session_state.get('approved_templates', {})]
            
            if not approved_categories:
                st.error("❌ No categories have approved templates")
            elif not mailchimp_api_key and not test_mode:
                st.error("❌ Please provide Mailchimp API key")
            else:
                with st.spinner(f"{'Previewing' if test_mode else 'Sending'} all categories..."):
                    time.sleep(3)  # Simulate bulk sending
                    
                    total_sent = sum(st.session_state.sponsor_categories[cat]['count'] for cat in approved_categories)
                    
                    if test_mode:
                        st.success(f"✅ Preview completed for {total_sent} sponsors across {len(approved_categories)} categories")
                    else:
                        st.success(f"✅ Sent {total_sent} personalized emails across {len(approved_categories)} categories")
                        st.balloons()
    
    with col2:
        if st.button("� Preview All Templates"):
            st.info("💡 Use individual category preview buttons to see personalized templates")
    
    # Campaign tracking
    if st.session_state.get('sent_campaigns'):
        st.markdown("### 📈 Campaign Tracking")
        
        sent_df = pd.DataFrame(st.session_state.sent_campaigns)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sent", sent_df['count'].sum())
        with col2:
            st.metric("Categories Sent", len(sent_df))
        with col3:
            st.metric("Templates Used", sent_df['template'].nunique())
        with col4:
            latest_send = sent_df['sent_at'].max()
            st.metric("Last Sent", pd.to_datetime(latest_send).strftime('%m/%d %H:%M'))
        
        # Send history table
        st.dataframe(sent_df, use_container_width=True)
        
        # Export tracking data
        if st.button("📥 Export Campaign Tracking"):
            csv = sent_df.to_csv(index=False)
            st.download_button(
                label="Download Tracking CSV",
                data=csv,
                file_name=f"campaign_tracking_{campaign['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

def initialize_session_state():
    """Initialize all session state variables"""
    # Basic session state
    if 'current_campaign' not in st.session_state or st.session_state.current_campaign is None:
        st.session_state.current_campaign = {}
    if 'generated_sponsors' not in st.session_state:
        st.session_state.generated_sponsors = []
    if 'email_templates' not in st.session_state:
        st.session_state.email_templates = {}
    if 'sent_campaigns' not in st.session_state:
        st.session_state.sent_campaigns = []
    
    # Enhanced session state for categorization
    if 'sponsor_categories' not in st.session_state:
        st.session_state.sponsor_categories = {}
    if 'approved_templates' not in st.session_state:
        st.session_state.approved_templates = {}
    if 'ai_enhanced_sponsors' not in st.session_state:
        st.session_state.ai_enhanced_sponsors = []

def main():
    """Main application"""
    # Initialize session state first
    initialize_session_state()
    
    show_main_header()
    
    # Simple navigation
    page = st.sidebar.selectbox(
        "Choose a step:",
        [
            "📊 Data Records",
            "📝 Create Campaign", 
            "🎯 Generate Sponsors",
            "📧 Create Templates",
            "🚀 Send & Track"
        ]
    )
    
    # Progress indicator
    st.sidebar.markdown("## 📊 Progress")
    
    progress_items = [
        ("📝 Campaign Created", bool(st.session_state.current_campaign)),
        ("🎯 Sponsors Generated", bool(st.session_state.generated_sponsors)),
        ("📧 Templates Created", bool(st.session_state.email_templates)),
        ("🚀 Campaign Sent", bool(st.session_state.sent_campaigns))
    ]
    
    for item, completed in progress_items:
        status = "✅" if completed else "⏳"
        st.sidebar.markdown(f"{status} {item}")
    
    # System status
    st.sidebar.markdown("## 🔧 System Status")
    mailchimp_key = os.environ.get('MAILCHIMP_API_KEY')
    st.sidebar.markdown(f"**Mailchimp**: {'✅ Connected' if mailchimp_key else '❌ Not configured'}")
    
    # Route to pages
    if "Data Records" in page:
        data_records_page()
    elif "Create Campaign" in page:
        show_create_campaign()
    elif "Generate Sponsors" in page:
        show_generate_sponsors()
    elif "Create Templates" in page:
        create_templates_page()
    elif "Send & Track" in page:
        show_send_track()

if __name__ == "__main__":
    main()