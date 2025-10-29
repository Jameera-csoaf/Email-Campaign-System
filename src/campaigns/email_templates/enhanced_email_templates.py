#!/usr/bin/env python3
"""
Enhanced Email Templates for CSOAF Campaigns
Professional email templates with industry-specific personalization
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

class CSPAFEmailTemplates:
    """
    Enhanced email template system for CSOAF campaigns
    Features: Industry personalization, event-specific templates, sponsorship tiers
    """
    
    def __init__(self):
        self.organization = "Community School of the Arts Foundation"
        self.sender_name = "CSOAF Team"
        self.sender_email = "promo@csoaf.org"
        self.website = "www.csoaf.org"
        self.phone = "(555) 123-ARTS"
        
        # Template categories
        self.templates = {
            'sponsorship_request': self._get_sponsorship_templates(),
            'event_invitation': self._get_event_templates(),
            'partnership_proposal': self._get_partnership_templates(),
            'thank_you': self._get_thank_you_templates(),
            'follow_up': self._get_follow_up_templates()
        }
        
        # Industry-specific messaging
        self.industry_messaging = self._get_industry_messaging()
        
        # Sponsorship tier messaging
        self.tier_messaging = self._get_tier_messaging()
    
    def _get_sponsorship_templates(self) -> Dict:
        """Sponsorship request email templates"""
        
        return {
            'standard': {
                'subject': 'Partnership Opportunity: Supporting Arts Education in {city}',
                'html': '''
                <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                        .header { background-color: #2c3e50; color: white; padding: 20px; text-align: center; }
                        .content { padding: 30px; max-width: 600px; margin: 0 auto; }
                        .highlight { background-color: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0; }
                        .cta-button { background-color: #e74c3c; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
                        .footer { background-color: #ecf0f1; padding: 20px; text-align: center; font-size: 12px; color: #7f8c8d; }
                        .logo { max-width: 150px; height: auto; }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>Community School of the Arts Foundation</h1>
                        <p>Empowering Communities Through Arts Education</p>
                    </div>
                    
                    <div class="content">
                        <h2>Dear {contact_name},</h2>
                        
                        <p>I hope this message finds you well. I'm reaching out from the Community School of the Arts Foundation (CSOAF) regarding an exciting partnership opportunity that aligns perfectly with {organization_name}'s commitment to community development.</p>
                        
                        <div class="highlight">
                            <h3>🎨 Why Arts Education Matters</h3>
                            <p>Research shows that students involved in arts programs score 100+ points higher on SATs and have 4x lower dropout rates. {industry_mention} we believe your organization would be an ideal partner in expanding these opportunities.</p>
                        </div>
                        
                        <h3>Partnership Opportunities:</h3>
                        <ul>
                            <li><strong>Program Sponsorship:</strong> Direct support for after-school arts programs</li>
                            <li><strong>Event Partnership:</strong> Collaborate on community arts events</li>
                            <li><strong>Scholarship Fund:</strong> Help talented students access arts education</li>
                            <li><strong>Corporate Engagement:</strong> Team-building through arts workshops</li>
                        </ul>
                        
                        <div class="highlight">
                            <h3>🌟 Impact in {city}, {state}</h3>
                            <p>With your support, we can reach an additional 200+ students in the {city} area, providing them with transformative arts education that builds confidence, creativity, and community connections.</p>
                        </div>
                        
                        <p><strong>Next Steps:</strong> I'd love to schedule a brief 15-minute call to discuss how {organization_name} can make a meaningful impact in our community while achieving your corporate social responsibility goals.</p>
                        
                        <a href="mailto:{reply_email}?subject=Partnership Discussion - {organization_name}" class="cta-button">Let's Connect</a>
                        
                        <p>Thank you for your time and consideration. Together, we can transform lives through the power of arts education.</p>
                        
                        <p>Warm regards,<br>
                        <strong>{sender_name}</strong><br>
                        Community Outreach Director<br>
                        Community School of the Arts Foundation</p>
                    </div>
                    
                    <div class="footer">
                        <p><strong>Community School of the Arts Foundation</strong><br>
                        📧 {sender_email} | 📞 {phone} | 🌐 {website}<br>
                        Empowering communities through accessible, high-quality arts education</p>
                        
                        <p><em>This email was sent to {organization_name} because we believe in the power of community partnerships to transform lives through arts education. If you'd prefer not to receive these messages, please reply with "UNSUBSCRIBE".</em></p>
                    </div>
                </body>
                </html>
                '''
            },
            
            'premium': {
                'subject': 'Exclusive Partnership: {organization_name} x CSOAF Arts Initiative',
                'html': '''
                <html>
                <head>
                    <style>
                        body { font-family: Georgia, serif; line-height: 1.8; color: #2c3e50; background-color: #fafafa; }
                        .container { max-width: 700px; margin: 0 auto; background-color: white; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
                        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }
                        .content { padding: 40px; }
                        .premium-highlight { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 10px; margin: 30px 0; text-align: center; }
                        .benefits-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }
                        .benefit-card { background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; }
                        .cta-section { background-color: #2c3e50; color: white; padding: 30px; text-align: center; margin: 30px 0; border-radius: 10px; }
                        .cta-button { background-color: #e74c3c; color: white; padding: 15px 40px; text-decoration: none; border-radius: 25px; display: inline-block; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
                        .footer { background-color: #34495e; color: white; padding: 30px; text-align: center; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>🎭 Exclusive Partnership Invitation</h1>
                            <h2>Community School of the Arts Foundation</h2>
                            <p>Where Art Meets Impact</p>
                        </div>
                        
                        <div class="content">
                            <h2>Dear {contact_name},</h2>
                            
                            <p>As a distinguished leader at {organization_name}, you understand the profound impact that strategic community investments can have on both social good and business outcomes.</p>
                            
                            <div class="premium-highlight">
                                <h3>🌟 Exclusive Partnership Opportunity</h3>
                                <p>We're inviting {organization_name} to join an exclusive circle of visionary partners who are transforming communities through arts education.</p>
                            </div>
                            
                            <p>{industry_mention} your organization is uniquely positioned to make a transformative impact in {city}, {state}.</p>
                            
                            <h3>📊 Proven Impact</h3>
                            <div class="benefits-grid">
                                <div class="benefit-card">
                                    <h4>🎓 Educational Excellence</h4>
                                    <p>Students in our programs show 40% improvement in academic performance and 95% graduation rates.</p>
                                </div>
                                <div class="benefit-card">
                                    <h4>🤝 Community Building</h4>
                                    <p>Our programs bring together diverse communities, fostering understanding and collaboration.</p>
                                </div>
                                <div class="benefit-card">
                                    <h4>💼 Workforce Development</h4>
                                    <p>Arts education develops critical thinking, creativity, and communication skills essential for 21st-century careers.</p>
                                </div>
                                <div class="benefit-card">
                                    <h4>🏆 Brand Recognition</h4>
                                    <p>Partner organizations receive extensive community recognition and positive brand association.</p>
                                </div>
                            </div>
                            
                            <h3>🎯 Strategic Partnership Tiers</h3>
                            <ul style="list-style-type: none; padding-left: 0;">
                                <li>🥇 <strong>Platinum Partner ($50,000+):</strong> Program naming rights, executive board seat, premium event access</li>
                                <li>🥈 <strong>Gold Partner ($25,000+):</strong> Scholarship fund establishment, quarterly impact reports, VIP events</li>
                                <li>🥉 <strong>Silver Partner ($10,000+):</strong> Workshop sponsorship, bi-annual meetings, community recognition</li>
                                <li>🎨 <strong>Creative Partner ($5,000+):</strong> Event collaboration, monthly updates, volunteer opportunities</li>
                            </ul>
                            
                            <div class="cta-section">
                                <h3>Ready to Make a Transformative Impact?</h3>
                                <p>Let's schedule a personalized presentation to explore how {organization_name} can become a cornerstone partner in our mission.</p>
                                <a href="mailto:{reply_email}?subject=Partnership Discussion - {organization_name}" class="cta-button">Schedule Partnership Meeting</a>
                            </div>
                            
                            <p>Thank you for your commitment to community excellence. I look forward to discussing how we can create lasting impact together.</p>
                            
                            <p>Best regards,<br>
                            <strong>{sender_name}</strong><br>
                            Partnership Development Director<br>
                            Community School of the Arts Foundation</p>
                        </div>
                        
                        <div class="footer">
                            <p><strong>Community School of the Arts Foundation</strong><br>
                            📧 {sender_email} | 📞 {phone} | 🌐 {website}</p>
                            
                            <p><em>This exclusive invitation was sent to {organization_name} due to your reputation for community leadership and social impact.</em></p>
                        </div>
                    </div>
                </body>
                </html>
                '''
            }
        }
    
    def _get_event_templates(self) -> Dict:
        """Event invitation email templates"""
        
        return {
            'gala': {
                'subject': 'You\'re Invited: CSOAF Annual Arts Gala - {event_date}',
                'html': '''
                <html>
                <head>
                    <style>
                        body { font-family: 'Playfair Display', serif; line-height: 1.6; color: #2c3e50; }
                        .invitation { max-width: 600px; margin: 0 auto; border: 2px solid #d4af37; background-color: #fefefe; }
                        .header { background: linear-gradient(45deg, #d4af37, #ffd700); padding: 40px; text-align: center; color: #2c3e50; }
                        .content { padding: 40px; }
                        .event-details { background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center; }
                        .highlight { color: #d4af37; font-weight: bold; }
                        .rsvp-section { background-color: #2c3e50; color: white; padding: 30px; text-align: center; margin: 20px 0; }
                        .rsvp-button { background-color: #d4af37; color: #2c3e50; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block; }
                    </style>
                </head>
                <body>
                    <div class="invitation">
                        <div class="header">
                            <h1>🎭 Annual Arts Gala</h1>
                            <h2>A Night of Inspiration & Impact</h2>
                            <p>Community School of the Arts Foundation</p>
                        </div>
                        
                        <div class="content">
                            <h2>Dear {contact_name},</h2>
                            
                            <p>You are cordially invited to join us for an extraordinary evening celebrating the transformative power of arts education in our community.</p>
                            
                            <div class="event-details">
                                <h3>📅 Event Details</h3>
                                <p><strong>Date:</strong> <span class="highlight">{event_date}</span><br>
                                <strong>Time:</strong> <span class="highlight">6:00 PM - 10:00 PM</span><br>
                                <strong>Venue:</strong> <span class="highlight">{venue_name}</span><br>
                                <strong>Address:</strong> {venue_address}<br>
                                <strong>Dress Code:</strong> <span class="highlight">Cocktail Attire</span></p>
                            </div>
                            
                            <p>This year's gala will feature:</p>
                            <ul>
                                <li>🎵 Performances by our talented students</li>
                                <li>🍷 Cocktail reception and gourmet dinner</li>
                                <li>🎨 Silent auction featuring local artist works</li>
                                <li>🏆 Recognition of community champions</li>
                                <li>💝 Inspiring stories of student transformation</li>
                            </ul>
                            
                            <p>As a valued member of our {city} business community, {organization_name} embodies the spirit of giving that makes events like this possible.</p>
                            
                            <div class="rsvp-section">
                                <h3>Reserve Your Table Today</h3>
                                <p>Individual tickets: $150 | Corporate table (10 guests): $1,200</p>
                                <a href="mailto:{reply_email}?subject=Gala RSVP - {organization_name}" class="rsvp-button">RSVP Now</a>
                            </div>
                            
                            <p>We hope to see you there as we celebrate another year of changing lives through arts education.</p>
                            
                            <p>With warm regards,<br>
                            <strong>{sender_name}</strong><br>
                            Event Coordination Team<br>
                            Community School of the Arts Foundation</p>
                        </div>
                    </div>
                </body>
                </html>
                '''
            }
        }
    
    def _get_partnership_templates(self) -> Dict:
        """Partnership proposal templates"""
        
        return {
            'collaboration': {
                'subject': 'Strategic Partnership Proposal: {organization_name} & CSOAF',
                'html': '''
                <html>
                <head>
                    <style>
                        body { font-family: 'Open Sans', sans-serif; line-height: 1.7; color: #444; }
                        .proposal { max-width: 700px; margin: 0 auto; background-color: white; }
                        .header { background-color: #3498db; color: white; padding: 30px; text-align: center; }
                        .content { padding: 40px; }
                        .collaboration-highlight { background: linear-gradient(135deg, #74b9ff, #0984e3); color: white; padding: 25px; border-radius: 10px; margin: 25px 0; }
                        .benefits-section { background-color: #f1f2f6; padding: 30px; border-radius: 10px; margin: 25px 0; }
                        .next-steps { background-color: #2d3436; color: white; padding: 25px; border-radius: 10px; }
                        .cta-button { background-color: #00b894; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block; }
                    </style>
                </head>
                <body>
                    <div class="proposal">
                        <div class="header">
                            <h1>🤝 Strategic Partnership Proposal</h1>
                            <h2>{organization_name} & CSOAF</h2>
                            <p>Building Stronger Communities Together</p>
                        </div>
                        
                        <div class="content">
                            <h2>Dear {contact_name},</h2>
                            
                            <p>I'm excited to present a strategic partnership opportunity that aligns {organization_name}'s community values with CSOAF's mission to transform lives through arts education.</p>
                            
                            <div class="collaboration-highlight">
                                <h3>🎯 Partnership Vision</h3>
                                <p>Together, we can create a comprehensive arts education ecosystem that serves {city} and surrounding communities, while advancing both organizations' goals for social impact and community engagement.</p>
                            </div>
                            
                            <h3>🔄 Mutual Benefits</h3>
                            <div class="benefits-section">
                                <h4>For {organization_name}:</h4>
                                <ul>
                                    <li>Enhanced community presence and positive brand association</li>
                                    <li>Employee engagement through volunteer opportunities</li>
                                    <li>Corporate social responsibility goal achievement</li>
                                    <li>Networking opportunities with other community leaders</li>
                                    <li>Team building through collaborative arts workshops</li>
                                </ul>
                                
                                <h4>For CSOAF:</h4>
                                <ul>
                                    <li>Expanded program reach and sustainability</li>
                                    <li>Access to professional expertise and mentorship</li>
                                    <li>Increased community visibility and support</li>
                                    <li>Enhanced program quality through corporate partnerships</li>
                                </ul>
                            </div>
                            
                            <h3>🚀 Proposed Collaboration Areas</h3>
                            <ul>
                                <li><strong>Scholarship Program:</strong> {organization_name}-sponsored scholarships for underserved students</li>
                                <li><strong>Mentorship Initiative:</strong> Employee volunteers as mentors for aspiring young artists</li>
                                <li><strong>Facility Partnership:</strong> Use of corporate spaces for exhibitions and performances</li>
                                <li><strong>Technology Integration:</strong> Digital arts programs leveraging {organization_name}'s expertise</li>
                                <li><strong>Community Events:</strong> Co-hosted events that celebrate arts and {industry} innovation</li>
                            </ul>
                            
                            <div class="next-steps">
                                <h3>🎯 Next Steps</h3>
                                <p>I'd love to schedule a meeting to discuss how we can customize this partnership to maximize benefit for both organizations and our community.</p>
                                <a href="mailto:{reply_email}?subject=Partnership Meeting - {organization_name}" class="cta-button">Schedule Meeting</a>
                            </div>
                            
                            <p>Thank you for considering this partnership opportunity. Together, we can create lasting positive impact in {city}.</p>
                            
                            <p>Best regards,<br>
                            <strong>{sender_name}</strong><br>
                            Strategic Partnerships Director<br>
                            Community School of the Arts Foundation</p>
                        </div>
                    </div>
                </body>
                </html>
                '''
            }
        }
    
    def _get_thank_you_templates(self) -> Dict:
        """Thank you email templates"""
        
        return {
            'donation': {
                'subject': 'Thank You for Your Generous Support - {organization_name}',
                'html': '''
                <html>
                <head>
                    <style>
                        body { font-family: Georgia, serif; line-height: 1.8; color: #2c3e50; }
                        .thank-you { max-width: 600px; margin: 0 auto; }
                        .header { background-color: #27ae60; color: white; padding: 30px; text-align: center; }
                        .content { padding: 40px; }
                        .impact-highlight { background-color: #d5f4e6; padding: 20px; border-left: 5px solid #27ae60; margin: 20px 0; }
                        .gratitude-section { background-color: #f8f9fa; padding: 25px; border-radius: 10px; text-align: center; margin: 25px 0; }
                    </style>
                </head>
                <body>
                    <div class="thank-you">
                        <div class="header">
                            <h1>💝 Thank You!</h1>
                            <h2>Your Generosity Changes Lives</h2>
                        </div>
                        
                        <div class="content">
                            <h2>Dear {contact_name},</h2>
                            
                            <div class="gratitude-section">
                                <h3>🙏 Heartfelt Gratitude</h3>
                                <p>On behalf of everyone at CSOAF and the students whose lives you're transforming, thank you for {organization_name}'s generous contribution of <strong>${donation_amount}</strong>.</p>
                            </div>
                            
                            <div class="impact-highlight">
                                <h3>🌟 Your Impact</h3>
                                <p>Your support will directly enable:</p>
                                <ul>
                                    <li>Arts education for {student_count} students this year</li>
                                    <li>After-school programs in {program_locations}</li>
                                    <li>Professional artist instruction and mentorship</li>
                                    <li>Performance opportunities and community showcases</li>
                                </ul>
                            </div>
                            
                            <p>We're committed to transparency and will send you quarterly impact reports showing exactly how your investment is transforming young lives in {city}.</p>
                            
                            <p><strong>Recognition:</strong> {organization_name} will be prominently featured as a {sponsorship_tier} sponsor in all our materials, and we'd love to arrange a visit so you can see your impact firsthand.</p>
                            
                            <p>Thank you again for believing in the power of arts education and for being a true champion of our community.</p>
                            
                            <p>With deepest appreciation,<br>
                            <strong>{sender_name}</strong><br>
                            Executive Director<br>
                            Community School of the Arts Foundation</p>
                        </div>
                    </div>
                </body>
                </html>
                '''
            }
        }
    
    def _get_follow_up_templates(self) -> Dict:
        """Follow-up email templates"""
        
        return {
            'meeting_follow_up': {
                'subject': 'Following Up: CSOAF Partnership Discussion',
                'html': '''
                <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                        .follow-up { max-width: 600px; margin: 0 auto; }
                        .header { background-color: #6c5ce7; color: white; padding: 25px; text-align: center; }
                        .content { padding: 35px; }
                        .recap-section { background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }
                        .next-steps { background-color: #fd79a8; color: white; padding: 20px; border-radius: 8px; margin: 20px 0; }
                        .cta-button { background-color: #e17055; color: white; padding: 10px 25px; text-decoration: none; border-radius: 5px; display: inline-block; }
                    </style>
                </head>
                <body>
                    <div class="follow-up">
                        <div class="header">
                            <h1>📞 Thank You for Your Time</h1>
                            <h2>CSOAF Partnership Follow-Up</h2>
                        </div>
                        
                        <div class="content">
                            <h2>Dear {contact_name},</h2>
                            
                            <p>Thank you for taking the time to discuss partnership opportunities between {organization_name} and CSOAF. It was wonderful to learn more about your organization's commitment to community development.</p>
                            
                            <div class="recap-section">
                                <h3>📝 Meeting Recap</h3>
                                <p>As discussed, we explored how {organization_name} could support our mission through:</p>
                                <ul>
                                    <li>{discussed_opportunity_1}</li>
                                    <li>{discussed_opportunity_2}</li>
                                    <li>{discussed_opportunity_3}</li>
                                </ul>
                            </div>
                            
                            <p>I've attached the partnership proposal we discussed, including the specific sponsorship packages and their benefits.</p>
                            
                            <div class="next-steps">
                                <h3>🎯 Next Steps</h3>
                                <p>As mentioned, I'll follow up in {follow_up_timeframe} to answer any questions and discuss next steps. In the meantime, please feel free to reach out if you need any additional information.</p>
                            </div>
                            
                            <p>We're excited about the possibility of partnering with {organization_name} to make a meaningful impact in {city}.</p>
                            
                            <a href="mailto:{reply_email}?subject=Partnership Questions - {organization_name}" class="cta-button">Contact Us</a>
                            
                            <p>Best regards,<br>
                            <strong>{sender_name}</strong><br>
                            Community Partnership Coordinator<br>
                            Community School of the Arts Foundation</p>
                        </div>
                    </div>
                </body>
                </html>
                '''
            }
        }
    
    def _get_industry_messaging(self) -> Dict:
        """Industry-specific messaging variations"""
        
        return {
            'Technology': {
                'intro': "As a leader in technology innovation, {organization_name} understands the importance of creativity and out-of-the-box thinking.",
                'connection': "Arts education develops the same creative problem-solving skills that drive technological breakthroughs.",
                'benefit': "Supporting arts education helps cultivate the next generation of innovative thinkers."
            },
            'Financial Services': {
                'intro': "As a respected financial institution, {organization_name} recognizes the value of strategic community investments.",
                'connection': "Arts education provides measurable returns through improved academic performance and community engagement.",
                'benefit': "This partnership demonstrates your commitment to long-term community growth and stability."
            },
            'Healthcare': {
                'intro': "Healthcare organizations like {organization_name} understand the connection between wellness and creative expression.",
                'connection': "Arts therapy and creative programs contribute significantly to mental health and community well-being.",
                'benefit': "Supporting arts education aligns with your mission of promoting overall community health."
            },
            'Manufacturing': {
                'intro': "Manufacturing leaders like {organization_name} appreciate the precision and craftsmanship that goes into creating something meaningful.",
                'connection': "Arts education teaches attention to detail, quality craftsmanship, and pride in creation.",
                'benefit': "These partnerships help develop the skilled, creative workforce that drives manufacturing innovation."
            },
            'Retail': {
                'intro': "Retail organizations like {organization_name} understand the importance of customer experience and community connection.",
                'connection': "Arts programs create vibrant communities that attract customers and enhance local economies.",
                'benefit': "Supporting local arts education strengthens the communities where your customers live and work."
            },
            'Education': {
                'intro': "Educational institutions like {organization_name} recognize the vital role that arts play in comprehensive learning.",
                'connection': "Arts education enhances critical thinking, creativity, and academic performance across all subjects.",
                'benefit': "This partnership amplifies your commitment to holistic educational excellence."
            }
        }
    
    def _get_tier_messaging(self) -> Dict:
        """Sponsorship tier specific messaging"""
        
        return {
            'high': {
                'approach': 'exclusive',
                'benefits_focus': 'strategic partnership, naming rights, board representation',
                'tone': 'prestigious, exclusive, transformative impact'
            },
            'medium': {
                'approach': 'collaborative',
                'benefits_focus': 'community recognition, employee engagement, measurable impact',
                'tone': 'professional, partnership-focused, community-minded'
            },
            'standard': {
                'approach': 'accessible',
                'benefits_focus': 'local impact, volunteer opportunities, community connection',
                'tone': 'friendly, approachable, community-focused'
            }
        }
    
    def get_template(self, template_type: str, template_name: str, 
                    recipient_data: Dict, campaign_data: Dict = None) -> Dict:
        """
        Get personalized email template
        
        Args:
            template_type: Type of template ('sponsorship_request', 'event_invitation', etc.)
            template_name: Specific template name ('standard', 'premium', etc.)
            recipient_data: Recipient information for personalization
            campaign_data: Additional campaign-specific data
            
        Returns:
            Dict with subject and html content
        """
        
        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")
        
        if template_name not in self.templates[template_type]:
            raise ValueError(f"Unknown template name: {template_name} for type {template_type}")
        
        template = self.templates[template_type][template_name]
        
        # Prepare personalization data
        personalization_data = {
            'organization_name': recipient_data.get('organization_name', 'Your Organization'),
            'contact_name': recipient_data.get('contact_name', recipient_data.get('name', 'Dear Colleague')),
            'city': recipient_data.get('city', ''),
            'state': recipient_data.get('state', ''),
            'industry': recipient_data.get('industry_sector', ''),
            'website': recipient_data.get('website', ''),
            'sender_name': self.sender_name,
            'sender_email': self.sender_email,
            'reply_email': self.sender_email,
            'phone': self.phone,
            'website': self.website
        }
        
        # Add industry-specific messaging
        industry = recipient_data.get('industry_sector', 'Technology')
        if industry in self.industry_messaging:
            industry_msg = self.industry_messaging[industry]
            personalization_data['industry_mention'] = industry_msg['intro'].format(**personalization_data)
        else:
            personalization_data['industry_mention'] = "Given your organization's community leadership,"
        
        # Add campaign-specific data
        if campaign_data:
            personalization_data.update(campaign_data)
        
        # Personalize template
        subject = template['subject'].format(**personalization_data)
        html_content = template['html'].format(**personalization_data)
        
        return {
            'subject': subject,
            'html': html_content,
            'personalization_data': personalization_data
        }
    
    def list_available_templates(self) -> Dict:
        """List all available templates"""
        
        template_list = {}
        for template_type, templates in self.templates.items():
            template_list[template_type] = list(templates.keys())
        
        return template_list
    
    def create_custom_template(self, template_type: str, template_name: str, 
                             subject: str, html_content: str):
        """Add a custom template to the system"""
        
        if template_type not in self.templates:
            self.templates[template_type] = {}
        
        self.templates[template_type][template_name] = {
            'subject': subject,
            'html': html_content
        }
        
        return f"Custom template '{template_name}' added to '{template_type}'"

def main():
    """Test the enhanced email templates"""
    print("🧪 Testing Enhanced Email Templates")
    print("="*50)
    
    # Initialize template system
    templates = CSPAFEmailTemplates()
    
    # List available templates
    available = templates.list_available_templates()
    print("📋 Available Templates:")
    for template_type, template_names in available.items():
        print(f"  {template_type}: {template_names}")
    
    # Test template generation
    test_recipient = {
        'organization_name': 'TechCorp Industries',
        'contact_name': 'Sarah Johnson',
        'city': 'New York',
        'state': 'NY',
        'industry_sector': 'Technology',
        'website': 'www.techcorp.com'
    }
    
    # Generate sponsorship email
    email = templates.get_template('sponsorship_request', 'standard', test_recipient)
    
    print(f"\n📧 Generated Email:")
    print(f"Subject: {email['subject']}")
    print(f"Content length: {len(email['html'])} characters")
    print("✅ Template generation successful")

if __name__ == "__main__":
    main()