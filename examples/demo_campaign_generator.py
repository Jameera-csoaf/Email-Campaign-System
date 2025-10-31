#!/usr/bin/env python3
"""
🎯 DEMO Campaign Generator for Manager Presentation
Creates impressive sample campaigns to showcase CSOAF Email Campaign Manager capabilities
"""

import pandas as pd
import json
from datetime import datetime, timedelta
import os

class DemoCampaignGenerator:
    def __init__(self):
        self.demo_campaigns = []
        self.fortune1000_path = "data/clean/corporations/fortune1000_main_database.csv"
        
    def create_demo_campaigns(self):
        """Generate 5 impressive demo campaigns"""
        
        # Load Fortune 1000 data
        if os.path.exists(self.fortune1000_path):
            corps_df = pd.read_csv(self.fortune1000_path)
            print(f"✅ Loaded {len(corps_df)} Fortune 1000 companies")
        else:
            print("⚠️ Fortune 1000 data not found - creating sample data")
            corps_df = self._create_sample_data()
        
        # Demo Campaign 1: Tech Giants for STEM Arts Education
        tech_campaign = {
            "campaign_id": "DEMO_001",
            "name": "Tech Giants STEM Arts Initiative",
            "description": "Target major technology corporations for STEM-integrated arts education programs",
            "target_companies": self._get_tech_companies(corps_df),
            "email_template": "tech_stem_arts_partnership",
            "expected_response_rate": "15-20%",
            "projected_funding": "$2.5M - $4M",
            "campaign_timeline": "Q1 2026",
            "key_features": [
                "AI-personalized emails for each tech executive",
                "STEM-Arts curriculum alignment proposals",
                "Corporate innovation partnership opportunities",
                "Student tech showcase events"
            ]
        }
        
        # Demo Campaign 2: Healthcare for Healing Arts
        healthcare_campaign = {
            "campaign_id": "DEMO_002", 
            "name": "Healthcare Healing Through Arts Program",
            "description": "Partner with healthcare organizations for therapeutic arts programs",
            "target_companies": self._get_healthcare_companies(corps_df),
            "email_template": "healthcare_healing_arts",
            "expected_response_rate": "18-25%",
            "projected_funding": "$1.8M - $3.2M",
            "campaign_timeline": "Q2 2026",
            "key_features": [
                "Evidence-based therapeutic arts benefits",
                "Hospital and clinic partnership programs",
                "Community health arts initiatives",
                "Healthcare worker wellness through arts"
            ]
        }
        
        # Demo Campaign 3: Financial Services Community Impact
        finance_campaign = {
            "campaign_id": "DEMO_003",
            "name": "Financial Services Community Arts Investment",
            "description": "Engage financial institutions in community arts education funding",
            "target_companies": self._get_finance_companies(corps_df),
            "email_template": "financial_community_investment",
            "expected_response_rate": "12-18%",
            "projected_funding": "$3.2M - $5.5M",
            "campaign_timeline": "Q3 2026",
            "key_features": [
                "Community development through arts education",
                "Financial literacy + creative arts programs",
                "Underserved neighborhood focus",
                "Long-term community partnership models"
            ]
        }
        
        # Demo Campaign 4: NY/CA Major Corporations
        geographic_campaign = {
            "campaign_id": "DEMO_004",
            "name": "NY-CA Arts Education Corridor",
            "description": "Target Fortune 500 companies in New York and California",
            "target_companies": self._get_ny_ca_companies(corps_df),
            "email_template": "geographic_major_sponsor",
            "expected_response_rate": "20-28%",
            "projected_funding": "$4.5M - $7M",
            "campaign_timeline": "Q4 2025 - Q1 2026",
            "key_features": [
                "Bi-coastal arts education network",
                "Major metropolitan school districts",
                "Corporate headquarters proximity advantage",
                "High-visibility sponsorship opportunities"
            ]
        }
        
        # Demo Campaign 5: Emerging Tech for Innovation Arts
        innovation_campaign = {
            "campaign_id": "DEMO_005",
            "name": "Innovation Arts: AI & Creative Expression",
            "description": "Partner with emerging tech companies for AI-enhanced arts education",
            "target_companies": self._get_innovation_companies(corps_df),
            "email_template": "innovation_ai_arts",
            "expected_response_rate": "25-35%",
            "projected_funding": "$1.5M - $2.8M",
            "campaign_timeline": "Q2-Q3 2026",
            "key_features": [
                "AI-powered creative arts tools for students",
                "Technology-enhanced art creation",
                "Digital arts curriculum development",
                "Future-ready creative skills training"
            ]
        }
        
        self.demo_campaigns = [
            tech_campaign,
            healthcare_campaign, 
            finance_campaign,
            geographic_campaign,
            innovation_campaign
        ]
        
        return self.demo_campaigns
    
    def _get_tech_companies(self, df):
        """Get technology companies for STEM arts campaign"""
        tech_companies = []
        if 'industry_sector' in df.columns:
            tech_df = df[df['industry_sector'].str.contains('Technology|Software|Tech', case=False, na=False)]
            tech_companies = tech_df.head(15).to_dict('records')
        else:
            # Fallback sample data
            tech_companies = [
                {"company_name": "Microsoft Corporation", "city": "Redmond", "state": "WA", "estimated_min_sponsorship": "$500,000"},
                {"company_name": "Apple Inc.", "city": "Cupertino", "state": "CA", "estimated_min_sponsorship": "$750,000"},
                {"company_name": "Google (Alphabet)", "city": "Mountain View", "state": "CA", "estimated_min_sponsorship": "$600,000"},
                {"company_name": "Meta Platforms", "city": "Menlo Park", "state": "CA", "estimated_min_sponsorship": "$400,000"},
                {"company_name": "Amazon", "city": "Seattle", "state": "WA", "estimated_min_sponsorship": "$650,000"}
            ]
        return tech_companies
    
    def _get_healthcare_companies(self, df):
        """Get healthcare companies for healing arts campaign"""
        if 'industry_sector' in df.columns:
            health_df = df[df['industry_sector'].str.contains('Healthcare|Medical|Pharma', case=False, na=False)]
            return health_df.head(12).to_dict('records')
        else:
            return [
                {"company_name": "Johnson & Johnson", "city": "New Brunswick", "state": "NJ", "estimated_min_sponsorship": "$400,000"},
                {"company_name": "Pfizer Inc.", "city": "New York", "state": "NY", "estimated_min_sponsorship": "$350,000"},
                {"company_name": "UnitedHealth Group", "city": "Minneapolis", "state": "MN", "estimated_min_sponsorship": "$450,000"}
            ]
    
    def _get_finance_companies(self, df):
        """Get financial services companies"""
        if 'industry_sector' in df.columns:
            finance_df = df[df['industry_sector'].str.contains('Financial|Banking|Insurance', case=False, na=False)]
            return finance_df.head(10).to_dict('records')
        else:
            return [
                {"company_name": "JPMorgan Chase", "city": "New York", "state": "NY", "estimated_min_sponsorship": "$600,000"},
                {"company_name": "Bank of America", "city": "Charlotte", "state": "NC", "estimated_min_sponsorship": "$500,000"},
                {"company_name": "Goldman Sachs", "city": "New York", "state": "NY", "estimated_min_sponsorship": "$550,000"}
            ]
    
    def _get_ny_ca_companies(self, df):
        """Get companies in NY and CA"""
        if 'state' in df.columns:
            ny_ca_df = df[df['state'].isin(['NY', 'CA'])]
            return ny_ca_df.head(20).to_dict('records')
        else:
            return [
                {"company_name": "IBM", "city": "Armonk", "state": "NY", "estimated_min_sponsorship": "$400,000"},
                {"company_name": "Salesforce", "city": "San Francisco", "state": "CA", "estimated_min_sponsorship": "$350,000"}
            ]
    
    def _get_innovation_companies(self, df):
        """Get emerging tech and innovation companies"""
        if 'industry_sector' in df.columns:
            innovation_df = df[df['industry_sector'].str.contains('Technology|Software|AI|Innovation', case=False, na=False)]
            return innovation_df.head(8).to_dict('records')
        else:
            return [
                {"company_name": "OpenAI", "city": "San Francisco", "state": "CA", "estimated_min_sponsorship": "$200,000"},
                {"company_name": "NVIDIA", "city": "Santa Clara", "state": "CA", "estimated_min_sponsorship": "$300,000"}
            ]
    
    def _create_sample_data(self):
        """Create sample Fortune 1000 data if file doesn't exist"""
        sample_data = []
        companies = [
            ("Apple Inc.", "Cupertino", "CA", "Technology", "$750,000"),
            ("Microsoft Corporation", "Redmond", "WA", "Technology", "$500,000"),
            ("Google (Alphabet)", "Mountain View", "CA", "Technology", "$600,000"),
            ("Amazon", "Seattle", "WA", "Technology", "$650,000"),
            ("Johnson & Johnson", "New Brunswick", "NJ", "Healthcare", "$400,000"),
            ("JPMorgan Chase", "New York", "NY", "Financial Services", "$600,000"),
            ("Goldman Sachs", "New York", "NY", "Financial Services", "$550,000"),
            ("Pfizer Inc.", "New York", "NY", "Healthcare", "$350,000"),
            ("IBM", "Armonk", "NY", "Technology", "$400,000"),
            ("Salesforce", "San Francisco", "CA", "Technology", "$350,000")
        ]
        
        for company, city, state, industry, sponsorship in companies:
            sample_data.append({
                "company_name": company,
                "city": city,
                "state": state,
                "industry_sector": industry,
                "estimated_min_sponsorship": sponsorship,
                "arts_education_potential": "High"
            })
        
        return pd.DataFrame(sample_data)
    
    def save_demo_campaigns(self):
        """Save demo campaigns to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/campaigns/demo_campaigns_{timestamp}.json"
        
        os.makedirs("data/campaigns", exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(self.demo_campaigns, f, indent=2, default=str)
        
        print(f"✅ Demo campaigns saved to: {filename}")
        return filename
    
    def generate_campaign_summary(self):
        """Generate executive summary of demo campaigns"""
        total_companies = sum(len(campaign['target_companies']) for campaign in self.demo_campaigns)
        total_projected_min = sum(float(campaign['projected_funding'].split('$')[1].split('M')[0]) for campaign in self.demo_campaigns)
        total_projected_max = sum(float(campaign['projected_funding'].split(' - $')[1].split('M')[0]) for campaign in self.demo_campaigns)
        
        summary = {
            "total_campaigns": len(self.demo_campaigns),
            "total_target_companies": total_companies,
            "projected_funding_range": f"${total_projected_min:.1f}M - ${total_projected_max:.1f}M",
            "campaign_timeline": "Q4 2025 - Q3 2026",
            "key_industries": ["Technology", "Healthcare", "Financial Services", "Innovation"],
            "expected_avg_response_rate": "18-25%",
            "campaigns": [
                {
                    "name": campaign['name'],
                    "targets": len(campaign['target_companies']),
                    "funding": campaign['projected_funding'],
                    "timeline": campaign['campaign_timeline']
                }
                for campaign in self.demo_campaigns
            ]
        }
        
        return summary

if __name__ == "__main__":
    print("🎯 Generating Demo Campaigns for Manager Presentation...")
    
    generator = DemoCampaignGenerator()
    campaigns = generator.create_demo_campaigns()
    
    print(f"\n✅ Created {len(campaigns)} impressive demo campaigns:")
    for campaign in campaigns:
        print(f"  📧 {campaign['name']} ({len(campaign['target_companies'])} targets)")
    
    # Save campaigns
    filename = generator.save_demo_campaigns()
    
    # Generate summary
    summary = generator.generate_campaign_summary()
    print(f"\n📊 Campaign Summary:")
    print(f"  Total Campaigns: {summary['total_campaigns']}")
    print(f"  Total Companies: {summary['total_target_companies']}")
    print(f"  Projected Funding: {summary['projected_funding_range']}")
    print(f"  Timeline: {summary['campaign_timeline']}")
    
    print("\n🚀 Demo campaigns ready for presentation!")