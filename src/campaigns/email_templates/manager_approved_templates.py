"""
CSOAF Email Template Library
Manager-approved templates with customization capabilities
"""

# Manager's Approved Template (Base)
MANAGER_APPROVED_TEMPLATE = """Subject: Partner with Us to Bring Arts Education to {location} Schools

Dear {contact_name},

I hope this message finds you well.

The Community School of the Arts Foundation (CSOAF) is reaching out to invite your organization to become a sponsor in support of implementing our arts curriculum at {target_schools}.

Our mission is to make high-quality arts education accessible to every child, especially in underserved public schools. Your sponsorship will help us deliver a comprehensive arts curriculum that includes visual arts, dance, music, and theater, giving students the opportunity to explore creativity, build confidence, and express their unique voices.

{mission_alignment_section}

As a valued partner, your organization will:
• Help us implement and sustain the arts curriculum at {target_location} public schools
• Receive recognition on school materials, program flyers, and social media campaigns
• Be associated with a trusted 501(c)(3) nonprofit that has provided arts programs across New York public schools since 2003
• Gain positive community visibility through direct engagement with students, teachers, and families

{sponsorship_specific_benefits}

We would love to schedule a short call or meeting next week to discuss sponsorship levels and how your support can help make this initiative a success.

Thank you for considering this opportunity to invest in creativity, education, and the next generation of young artists.

Warm regards,

Anthony Villacis
Executive Director
Community School of the Arts Foundation
917 216-5176
info@csoaf.org
www.csoaf.org"""

# Mission Alignment Variations
MISSION_ALIGNMENT_VARIATIONS = {
    'disability_focus': """We noticed your organization's commitment to supporting individuals with disabilities, which aligns perfectly with our inclusive arts programs designed to serve students of all abilities.""",
    
    'education_focus': """Given your foundation's dedication to educational excellence, we believe you'll appreciate our evidence-based approach to arts integration in academic curricula.""",
    
    'arts_focus': """Your organization's support for the arts makes you an ideal partner for our comprehensive visual arts, music, dance, and theater programs.""",
    
    'community_focus': """We're impressed by your commitment to community development, which mirrors our work in strengthening neighborhoods through accessible arts education.""",
    
    'youth_focus': """Your foundation's focus on youth development aligns beautifully with our mission to empower young people through creative expression and artistic skill-building.""",
    
    'health_focus': """Understanding your interest in health and wellness, you'll appreciate how our arts programs support mental health, social-emotional learning, and overall student well-being.""",
    
    'general': """We believe your organization's values align with our commitment to providing transformative arts education to underserved communities."""
}

# Sponsorship Level Specific Benefits
SPONSORSHIP_BENEFITS = {
    'major_sponsor': """
Sponsorship opportunities include:
• Program Title Sponsorship ($15,000-$25,000): Your organization's name featured prominently
• Annual Showcase Presenting Sponsor ($10,000-$20,000): Recognition at our signature event
• Equipment Sponsor ($5,000-$15,000): Naming rights on instruments and art supplies
• Classroom Sponsor ($2,500-$7,500): Direct impact on individual classrooms""",
    
    'corporate_sponsor': """
Corporate partnership benefits include:
• Employee volunteer opportunities at our programs
• Corporate social responsibility storytelling opportunities
• Networking events with other education-focused corporate partners
• Customized recognition packages for your marketing needs""",
    
    'foundation_grant': """
Grant funding will directly support:
• Certified teaching artist salaries and training
• Art supplies and musical instruments
• Program evaluation and impact measurement
• Expansion to additional school sites in underserved areas""",
    
    'standard': """
Additional partnership benefits:
• Quarterly impact reports showing student progress
• Invitation to student showcase performances
• Recognition in our annual report and website
• Tax-deductible contribution with full documentation"""
}

# Location Variations
LOCATION_VARIATIONS = {
    'new_york': {
        'location': 'New York',
        'target_schools': 'New York Public Schools',
        'target_location': 'New York City'
    },
    'brooklyn': {
        'location': 'Brooklyn',
        'target_schools': 'Brooklyn Public Schools',
        'target_location': 'Brooklyn'
    },
    'manhattan': {
        'location': 'Manhattan',
        'target_schools': 'Manhattan Public Schools', 
        'target_location': 'Manhattan'
    },
    'general_nyc': {
        'location': 'New York City',
        'target_schools': 'NYC Public Schools',
        'target_location': 'New York City'
    }
}

def generate_personalized_email(sponsor_data, template_type='standard', location='new_york'):
    """
    Generate personalized email using manager's approved template
    
    Args:
        sponsor_data: Dictionary with sponsor information
        template_type: Type of sponsorship (major_sponsor, corporate_sponsor, foundation_grant, standard)
        location: Geographic focus (new_york, brooklyn, manhattan, general_nyc)
    
    Returns:
        Formatted email string
    """
    
    # Extract sponsor information
    org_name = sponsor_data.get('organization_name', 'Organization')
    contact_name = sponsor_data.get('contact_name', 'Valued Partner')
    program_areas = sponsor_data.get('program_areas', '').lower()
    mission_score = sponsor_data.get('mission_alignment_score', 0)
    
    # Determine mission alignment approach
    alignment_key = 'general'
    if 'disability' in program_areas or 'inclusive' in program_areas:
        alignment_key = 'disability_focus'
    elif 'education' in program_areas:
        alignment_key = 'education_focus'
    elif 'arts' in program_areas or 'cultural' in program_areas:
        alignment_key = 'arts_focus'
    elif 'community' in program_areas:
        alignment_key = 'community_focus'
    elif 'youth' in program_areas or 'children' in program_areas:
        alignment_key = 'youth_focus'
    elif 'health' in program_areas:
        alignment_key = 'health_focus'
    
    # Get location data
    location_data = LOCATION_VARIATIONS.get(location, LOCATION_VARIATIONS['new_york'])
    
    # Format the email
    email_content = MANAGER_APPROVED_TEMPLATE.format(
        contact_name=contact_name,
        location=location_data['location'],
        target_schools=location_data['target_schools'],
        target_location=location_data['target_location'],
        mission_alignment_section=MISSION_ALIGNMENT_VARIATIONS[alignment_key],
        sponsorship_specific_benefits=SPONSORSHIP_BENEFITS.get(template_type, SPONSORSHIP_BENEFITS['standard'])
    )
    
    return email_content

def get_available_templates():
    """Return list of available template types"""
    return list(SPONSORSHIP_BENEFITS.keys())

def get_available_locations():
    """Return list of available location options"""
    return list(LOCATION_VARIATIONS.keys())

# Subject Line Variations
SUBJECT_VARIATIONS = {
    'arts_partnership': "Partner with Us to Bring Arts Education to {location} Schools",
    'sponsorship_opportunity': "Exclusive Sponsorship Opportunity: {location} Arts Education Initiative", 
    'community_impact': "Transform {location} Communities Through Arts Education Partnership",
    'education_excellence': "Enhance {location} Education Through Innovative Arts Programming",
    'custom': "Partnership Opportunity: CSOAF Arts Education in {location}"
}

def generate_subject_line(subject_type='arts_partnership', location='New York'):
    """Generate subject line based on type and location"""
    return SUBJECT_VARIATIONS.get(subject_type, SUBJECT_VARIATIONS['arts_partnership']).format(location=location)

# Template for manager customization interface
TEMPLATE_CUSTOMIZATION_OPTIONS = {
    'contact_greeting': [
        "Dear {contact_name},",
        "Hello {contact_name},", 
        "Greetings {contact_name},",
        "Dear Friends at {organization_name},"
    ],
    'opening_line': [
        "I hope this message finds you well.",
        "I hope you're having a wonderful day.",
        "Thank you for your organization's commitment to community impact.",
        "I'm reaching out regarding an exciting partnership opportunity."
    ],
    'call_to_action': [
        "We would love to schedule a short call or meeting next week to discuss sponsorship levels and how your support can help make this initiative a success.",
        "I'd welcome the opportunity to discuss how we can partner together for maximum community impact.",
        "Would you be available for a brief conversation about this partnership opportunity?",
        "I'd be happy to provide additional information and discuss how we can work together."
    ]
}

def get_customization_options():
    """Return available customization options for managers"""
    return TEMPLATE_CUSTOMIZATION_OPTIONS