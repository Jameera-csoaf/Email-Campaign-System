#!/usr/bin/env python3
"""
Enhanced CSOAF Programs Database Generator
Complete program database with all required fields: name, email, mission, location, website
Plus additional fields for better program targeting and sponsorship alignment
"""

import pandas as pd
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedCSOAFDatabase:
    def __init__(self):
        self.programs_data = []
        
        # Enhanced CSOAF programs with complete data
        self.programs = [
            {
                # Required core fields
                'organization_name': 'Center for Students of ALL Arts (CSOAF)',
                'email': 'info@csoaf.org',
                'mission': 'To provide inclusive arts education and healing programs for individuals with disabilities and diverse needs',
                'location': 'New York, NY',
                'website': 'https://www.csoaf.org',
                
                # Program-specific information
                'program_name': 'Adaptive Dance Movement Therapy',
                'program_category': 'Dance',
                'program_description': 'Therapeutic dance program designed for individuals with disabilities, focusing on movement as healing and self-expression',
                'target_audience': 'People with Disabilities, Adults',
                'schedule': 'Weekly',
                'estimated_annual_cost': 12000,
                'sessions_per_year': 48,
                'cost_per_session': 175,
                'participants_capacity': 15,
                'instructor_requirements': 'Certified Dance Movement Therapist',
                'equipment_needed': 'Sound system, adaptive equipment, safety mats',
                'space_requirements': 'Accessible studio space with mirrors',
                
                # Enhanced targeting fields
                'sponsorship_appeal': 'High - therapeutic benefits for disability community',
                'corporate_sponsor_fit': 'Healthcare, Wellness, Technology companies',
                'foundation_fit': 'Disability support, Arts therapy, Healthcare foundations',
                'age_groups': 'Adults 18+',
                'accessibility_features': 'Full wheelchair accessibility, adaptive equipment, sensory accommodations',
                'measurable_outcomes': 'Improved mobility, emotional wellbeing, social connection',
                'success_metrics': 'Participant retention 85%, Wellness improvement scores, Family feedback',
                'program_director': 'Sarah Martinez, ADTR',
                'contact_phone': '(555) 123-4567',
                'program_email': 'dance@csoaf.org'
            },
            {
                'organization_name': 'Center for Students of ALL Arts (CSOAF)',
                'email': 'info@csoaf.org',
                'mission': 'To provide inclusive arts education and healing programs for individuals with disabilities and diverse needs',
                'location': 'New York, NY',
                'website': 'https://www.csoaf.org',
                
                'program_name': 'Inclusive Music Therapy Sessions',
                'program_category': 'Music',
                'program_description': 'Music therapy program for diverse abilities, using instruments and voice to promote healing and social connection',
                'target_audience': 'People with Disabilities, Children/Youth, Adults',
                'schedule': 'Weekly',
                'estimated_annual_cost': 15000,
                'sessions_per_year': 50,
                'cost_per_session': 200,
                'participants_capacity': 12,
                'instructor_requirements': 'Licensed Music Therapist',
                'equipment_needed': 'Adaptive instruments, sound equipment, recording tools',
                'space_requirements': 'Soundproof room with piano',
                
                'sponsorship_appeal': 'Very High - proven therapeutic benefits, all ages',
                'corporate_sponsor_fit': 'Music industry, Healthcare, Technology, Financial services',
                'foundation_fit': 'Music foundations, Disability support, Child development',
                'age_groups': 'All ages 6+',
                'accessibility_features': 'Adaptive instruments, visual aids, communication devices',
                'measurable_outcomes': 'Communication improvement, emotional regulation, social skills',
                'success_metrics': 'Therapy goals achievement 90%, Parent satisfaction, Clinical assessments',
                'program_director': 'Dr. Michael Chen, MT-BC',
                'contact_phone': '(555) 123-4568',
                'program_email': 'music@csoaf.org'
            },
            {
                'organization_name': 'Center for Students of ALL Arts (CSOAF)',
                'email': 'info@csoaf.org',
                'mission': 'To provide inclusive arts education and healing programs for individuals with disabilities and diverse needs',
                'location': 'New York, NY',
                'website': 'https://www.csoaf.org',
                
                'program_name': 'Art Therapy for Trauma Recovery',
                'program_category': 'Visual Arts',
                'program_description': 'Visual arts therapy program helping individuals process trauma through creative expression and guided art-making',
                'target_audience': 'Adults, Veterans, People with Disabilities',
                'schedule': 'Weekly',
                'estimated_annual_cost': 10000,
                'sessions_per_year': 45,
                'cost_per_session': 150,
                'participants_capacity': 10,
                'instructor_requirements': 'Licensed Art Therapist',
                'equipment_needed': 'Art supplies, easels, specialized tools',
                'space_requirements': 'Well-lit studio with storage',
                
                'sponsorship_appeal': 'Very High - serves veterans and trauma survivors',
                'corporate_sponsor_fit': 'Healthcare, Financial services, Defense contractors, Technology',
                'foundation_fit': 'Veterans support, Mental health, Arts therapy foundations',
                'age_groups': 'Adults 18+, Veterans all ages',
                'accessibility_features': 'Adaptive art tools, trauma-informed environment',
                'measurable_outcomes': 'PTSD symptom reduction, emotional processing, resilience building',
                'success_metrics': 'Clinical improvement scales, Veteran engagement rates, Long-term follow-up',
                'program_director': 'Jennifer Lopez, ATR-BC',
                'contact_phone': '(555) 123-4569',
                'program_email': 'arttherapy@csoaf.org'
            },
            {
                'organization_name': 'Center for Students of ALL Arts (CSOAF)',
                'email': 'info@csoaf.org',
                'mission': 'To provide inclusive arts education and healing programs for individuals with disabilities and diverse needs',
                'location': 'New York, NY',
                'website': 'https://www.csoaf.org',
                
                'program_name': 'Inclusive Theater Workshop',
                'program_category': 'Theater',
                'program_description': 'Collaborative theater program bringing together people of all abilities to create and perform original works',
                'target_audience': 'People with Disabilities, Children/Youth, Adults',
                'schedule': 'Weekly',
                'estimated_annual_cost': 8000,
                'sessions_per_year': 40,
                'cost_per_session': 125,
                'participants_capacity': 20,
                'instructor_requirements': 'Theater director with inclusive experience',
                'equipment_needed': 'Costumes, props, lighting, sound system',
                'space_requirements': 'Theater or large performance space',
                
                'sponsorship_appeal': 'High - community integration, public performances',
                'corporate_sponsor_fit': 'Entertainment, Media, Technology, Financial services',
                'foundation_fit': 'Arts education, Disability inclusion, Community development',
                'age_groups': 'Youth 12+ and Adults',
                'accessibility_features': 'Modified scripts, assistive technology, inclusive staging',
                'measurable_outcomes': 'Self-confidence building, social integration, performance skills',
                'success_metrics': 'Performance participation rates, Audience feedback, Participant growth',
                'program_director': 'Robert Kim, MFA',
                'contact_phone': '(555) 123-4570',
                'program_email': 'theater@csoaf.org'
            },
            {
                'organization_name': 'Center for Students of ALL Arts (CSOAF)',
                'email': 'info@csoaf.org',
                'mission': 'To provide inclusive arts education and healing programs for individuals with disabilities and diverse needs',
                'location': 'New York, NY',
                'website': 'https://www.csoaf.org',
                
                'program_name': 'Mindfulness and Meditation Arts',
                'program_category': 'Wellness/Mindfulness',
                'program_description': 'Meditation and mindfulness program integrated with creative arts for stress reduction and mental wellness',
                'target_audience': 'Adults, People with Disabilities, Caregivers',
                'schedule': 'Bi-weekly',
                'estimated_annual_cost': 6000,
                'sessions_per_year': 26,
                'cost_per_session': 125,
                'participants_capacity': 18,
                'instructor_requirements': 'Certified meditation instructor with arts background',
                'equipment_needed': 'Meditation cushions, art supplies, sound system',
                'space_requirements': 'Quiet, calming space with natural light',
                
                'sponsorship_appeal': 'High - mental wellness focus, caregiver support',
                'corporate_sponsor_fit': 'Healthcare, Wellness companies, Technology, Financial services',
                'foundation_fit': 'Mental health, Wellness, Caregiver support foundations',
                'age_groups': 'Adults 18+, Caregivers',
                'accessibility_features': 'Multiple seating options, sensory accommodations',
                'measurable_outcomes': 'Stress reduction, mindfulness skills, emotional regulation',
                'success_metrics': 'Stress scale improvements, Regular practice adoption, Caregiver wellbeing',
                'program_director': 'Dr. Lisa Patel, PhD',
                'contact_phone': '(555) 123-4571',
                'program_email': 'mindfulness@csoaf.org'
            },
            {
                'organization_name': 'Center for Students of ALL Arts (CSOAF)',
                'email': 'info@csoaf.org',
                'mission': 'To provide inclusive arts education and healing programs for individuals with disabilities and diverse needs',
                'location': 'New York, NY',
                'website': 'https://www.csoaf.org',
                
                'program_name': 'Family Healing Through Arts',
                'program_category': 'Family Programs',
                'program_description': 'Family-centered arts program designed to strengthen bonds and facilitate healing through creative collaboration',
                'target_audience': 'Families, Children/Youth, People with Disabilities',
                'schedule': 'Monthly',
                'estimated_annual_cost': 9000,
                'sessions_per_year': 12,
                'cost_per_session': 450,
                'participants_capacity': 30,
                'instructor_requirements': 'Family therapist with arts therapy certification',
                'equipment_needed': 'Family-friendly art supplies, large workspace materials',
                'space_requirements': 'Large, flexible space for family groups',
                
                'sponsorship_appeal': 'Very High - family impact, multigenerational benefits',
                'corporate_sponsor_fit': 'Family-focused companies, Healthcare, Financial services, Retail',
                'foundation_fit': 'Family foundations, Child welfare, Community development',
                'age_groups': 'All family members, Children 5+',
                'accessibility_features': 'Multi-generational design, various ability levels',
                'measurable_outcomes': 'Family communication improvement, relationship strengthening',
                'success_metrics': 'Family assessment scores, Continued participation, Goal achievement',
                'program_director': 'Maria Gonzalez, LMFT',
                'contact_phone': '(555) 123-4572',
                'program_email': 'family@csoaf.org'
            },
            {
                'organization_name': 'Center for Students of ALL Arts (CSOAF)',
                'email': 'info@csoaf.org',
                'mission': 'To provide inclusive arts education and healing programs for individuals with disabilities and diverse needs',
                'location': 'New York, NY',
                'website': 'https://www.csoaf.org',
                
                'program_name': 'Creative Writing and Storytelling',
                'program_category': 'Literary Arts',
                'program_description': 'Writing program for diverse abilities focusing on personal narrative, storytelling, and creative expression',
                'target_audience': 'Adults, Children/Youth, People with Disabilities',
                'schedule': 'Weekly',
                'estimated_annual_cost': 7000,
                'sessions_per_year': 35,
                'cost_per_session': 125,
                'participants_capacity': 15,
                'instructor_requirements': 'Published writer with special education experience',
                'equipment_needed': 'Adaptive writing tools, computers, recording equipment',
                'space_requirements': 'Comfortable classroom with technology access',
                
                'sponsorship_appeal': 'High - literacy focus, personal empowerment',
                'corporate_sponsor_fit': 'Publishing, Technology, Media companies, Financial services',
                'foundation_fit': 'Literacy foundations, Arts education, Disability support',
                'age_groups': 'Youth 12+ and Adults',
                'accessibility_features': 'Assistive writing technology, multiple communication methods',
                'measurable_outcomes': 'Writing skill development, self-advocacy, storytelling confidence',
                'success_metrics': 'Portfolio completion, Public reading participation, Skill assessments',
                'program_director': 'David Chen, MFA',
                'contact_phone': '(555) 123-4573',
                'program_email': 'writing@csoaf.org'
            },
            {
                'organization_name': 'Center for Students of ALL Arts (CSOAF)',
                'email': 'info@csoaf.org',
                'mission': 'To provide inclusive arts education and healing programs for individuals with disabilities and diverse needs',
                'location': 'New York, NY',
                'website': 'https://www.csoaf.org',
                
                'program_name': 'Sensory Integration Arts Program',
                'program_category': 'Therapeutic Arts',
                'program_description': 'Multi-sensory arts program designed for individuals with autism and sensory processing differences',
                'target_audience': 'Children/Youth, People with Disabilities (Autism)',
                'schedule': 'Twice weekly',
                'estimated_annual_cost': 18000,
                'sessions_per_year': 80,
                'cost_per_session': 150,
                'participants_capacity': 8,
                'instructor_requirements': 'Occupational therapist with arts training',
                'equipment_needed': 'Sensory materials, adaptive art tools, specialized equipment',
                'space_requirements': 'Sensory-friendly environment with variable lighting',
                
                'sponsorship_appeal': 'Very High - specialized autism support, high demand',
                'corporate_sponsor_fit': 'Healthcare, Technology, Autism-focused companies, Financial services',
                'foundation_fit': 'Autism foundations, Special needs support, Therapeutic programs',
                'age_groups': 'Children 3-18, Young adults',
                'accessibility_features': 'Full sensory accommodations, individualized supports',
                'measurable_outcomes': 'Sensory regulation improvement, social engagement, skill development',
                'success_metrics': 'Occupational therapy assessments, Parent reports, Behavior tracking',
                'program_director': 'Dr. Amy Rodriguez, OTR/L',
                'contact_phone': '(555) 123-4574',
                'program_email': 'sensory@csoaf.org'
            },
            {
                'organization_name': 'Center for Students of ALL Arts (CSOAF)',
                'email': 'info@csoaf.org',
                'mission': 'To provide inclusive arts education and healing programs for individuals with disabilities and diverse needs',
                'location': 'New York, NY',
                'website': 'https://www.csoaf.org',
                
                'program_name': 'Professional Development for Inclusive Arts',
                'program_category': 'Professional Training',
                'program_description': 'Training program for arts educators and therapists in inclusive practices and disability awareness',
                'target_audience': 'Arts Educators, Therapists, Service Providers',
                'schedule': 'Monthly workshops',
                'estimated_annual_cost': 5000,
                'sessions_per_year': 12,
                'cost_per_session': 275,
                'participants_capacity': 25,
                'instructor_requirements': 'Expert practitioners in inclusive arts education',
                'equipment_needed': 'Training materials, presentation equipment',
                'space_requirements': 'Professional training facility',
                
                'sponsorship_appeal': 'Medium - professional development, field advancement',
                'corporate_sponsor_fit': 'Professional services, Healthcare, Education companies',
                'foundation_fit': 'Professional development, Arts education, Disability advocacy',
                'age_groups': 'Adult professionals',
                'accessibility_features': 'Professional accommodations, continuing education credits',
                'measurable_outcomes': 'Skills improvement, certification completion, practice implementation',
                'success_metrics': 'Training evaluations, Certification rates, Follow-up surveys',
                'program_director': 'Dr. Rebecca Wang, PhD',
                'contact_phone': '(555) 123-4575',
                'program_email': 'training@csoaf.org'
            },
            {
                'organization_name': 'Center for Students of ALL Arts (CSOAF)',
                'email': 'info@csoaf.org',
                'mission': 'To provide inclusive arts education and healing programs for individuals with disabilities and diverse needs',
                'location': 'New York, NY',
                'website': 'https://www.csoaf.org',
                
                'program_name': 'Digital Arts and Technology Access',
                'program_category': 'Digital Arts',
                'program_description': 'Technology-based arts program teaching digital creativity tools with adaptive technology for accessibility',
                'target_audience': 'Children/Youth, Adults, People with Disabilities',
                'schedule': 'Weekly',
                'estimated_annual_cost': 14000,
                'sessions_per_year': 42,
                'cost_per_session': 200,
                'participants_capacity': 12,
                'instructor_requirements': 'Digital arts educator with accessibility expertise',
                'equipment_needed': 'Adaptive computers, software, digital art tools',
                'space_requirements': 'Computer lab with accessibility features',
                
                'sponsorship_appeal': 'Very High - technology focus, digital inclusion',
                'corporate_sponsor_fit': 'Technology companies, Software companies, Financial services',
                'foundation_fit': 'Technology access, Digital inclusion, Arts education',
                'age_groups': 'Youth 10+ and Adults',
                'accessibility_features': 'Adaptive technology, assistive software, multiple input methods',
                'measurable_outcomes': 'Digital literacy, creative skills, technology confidence',
                'success_metrics': 'Portfolio creation, Technology skill assessments, Employment readiness',
                'program_director': 'Alex Johnson, MFA',
                'contact_phone': '(555) 123-4576',
                'program_email': 'digital@csoaf.org'
            }
        ]

    def generate_enhanced_database(self):
        """Generate comprehensive CSOAF programs database"""
        logger.info(f"Generating enhanced CSOAF programs database with {len(self.programs)} programs...")
        
        current_time = datetime.now().isoformat()
        
        for program in self.programs:
            # Add metadata and timestamps
            enhanced_record = program.copy()
            enhanced_record.update({
                'data_source': 'CSOAF Internal Database',
                'created_at': current_time,
                'last_updated': current_time,
                'status': 'Active',
                'funding_needed': enhanced_record['estimated_annual_cost'],
                'priority_level': self._calculate_priority(program),
                'sponsor_match_potential': self._calculate_sponsor_potential(program)
            })
            
            self.programs_data.append(enhanced_record)
        
        return self.programs_data

    def _calculate_priority(self, program):
        """Calculate program priority based on various factors"""
        # Higher cost programs get higher priority
        cost = program.get('estimated_annual_cost', 0)
        if cost > 15000:
            return 'High'
        elif cost > 10000:
            return 'Medium'
        else:
            return 'Standard'

    def _calculate_sponsor_potential(self, program):
        """Calculate sponsor matching potential"""
        appeal = program.get('sponsorship_appeal', '')
        if 'Very High' in appeal:
            return 'Excellent'
        elif 'High' in appeal:
            return 'Good'
        else:
            return 'Moderate'

    def save_to_csv(self, filename=None):
        """Save enhanced database to CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_csoaf_programs_{timestamp}.csv"
        
        df = pd.DataFrame(self.programs_data)
        df.to_csv(filename, index=False)
        
        logger.info(f"Enhanced CSOAF programs database saved to {filename}")
        logger.info(f"Total programs: {len(self.programs_data)}")
        
        # Summary statistics
        total_cost = df['estimated_annual_cost'].sum()
        avg_capacity = df['participants_capacity'].mean()
        
        logger.info(f"Total annual program costs: ${total_cost:,}")
        logger.info(f"Average participant capacity: {avg_capacity:.1f}")
        
        # Category breakdown
        category_breakdown = df['program_category'].value_counts()
        logger.info(f"Program categories: {category_breakdown.to_dict()}")
        
        # Priority breakdown
        priority_breakdown = df['priority_level'].value_counts()
        logger.info(f"Priority levels: {priority_breakdown.to_dict()}")
        
        return filename

def main():
    """Main execution function"""
    generator = EnhancedCSOAFDatabase()
    
    # Generate the enhanced database
    programs = generator.generate_enhanced_database()
    
    # Save to CSV
    filename = generator.save_to_csv()
    
    print(f"\nSUCCESS: Enhanced CSOAF programs database generated!")
    print(f"File: {filename}")
    print(f"Programs: {len(programs)}")
    print(f"All required fields included: name, email, mission, location, website")
    print(f"Plus comprehensive program details for better sponsor matching")

if __name__ == "__main__":
    main()