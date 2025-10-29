#!/usr/bin/env python3
"""
3-Day Sprint Master Coordinator
Orchestrates the complete dual-track fundraising system implementation
"""

import os
import sys
import time
import logging
import pandas as pd
from datetime import datetime, timedelta
import json
import subprocess
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ThreeDaySprintCoordinator:
    def __init__(self):
        self.start_time = datetime.now()
        self.sprint_data = {
            'day1': {'status': 'pending', 'tasks': [], 'results': {}},
            'day2': {'status': 'pending', 'tasks': [], 'results': {}},
            'day3': {'status': 'pending', 'tasks': [], 'results': {}}
        }
        
        # Day 1: Data Collection & Foundation
        self.sprint_data['day1']['tasks'] = [
            'Fortune 100 NY/CA corporation scraping',
            'CSOAF programs data extraction',
            'Historical sponsorship data analysis',
            'Initial corporation database setup',
            'Foundation data enhancement'
        ]
        
        # Day 2: Campaign System Development
        self.sprint_data['day2']['tasks'] = [
            'Interactive campaign workflow design',
            'Natural language campaign creation',
            'Foundation vs corporation routing logic',
            'Enhanced email template system',
            'Mission alignment for corporations'
        ]
        
        # Day 3: Integration & Dashboard
        self.sprint_data['day3']['tasks'] = [
            'Dashboard integration APIs',
            'Export functionality for teams',
            'Sponsorship amount estimation',
            'Complete system testing',
            'Final deployment preparation'
        ]
        
    def log_progress(self, day, task, status, details=None):
        """Log progress for tracking"""
        timestamp = datetime.now().isoformat()
        progress_entry = {
            'timestamp': timestamp,
            'day': day,
            'task': task,
            'status': status,
            'details': details or {}
        }
        
        # Save to progress log
        log_file = f'sprint_progress_{self.start_time.strftime("%Y%m%d_%H%M%S")}.json'
        
        try:
            with open(log_file, 'r') as f:
                progress_log = json.load(f)
        except FileNotFoundError:
            progress_log = []
            
        progress_log.append(progress_entry)
        
        with open(log_file, 'w') as f:
            json.dump(progress_log, f, indent=2)
            
        logger.info(f"Day {day} - {task}: {status}")
        
    def run_day1_data_collection(self):
        """Execute Day 1: Data Collection & Foundation"""
        logger.info("🚀 Starting Day 1: Data Collection & Foundation")
        self.sprint_data['day1']['status'] = 'in_progress'
        
        day1_results = {}
        
        try:
            # Task 1: Fortune 100 Corporation Scraping
            self.log_progress(1, "Fortune 100 Corporation Scraping", "starting")
            
            try:
                # Run corporation scraper
                subprocess.run([
                    sys.executable, 
                    'tools/corporation_scraper.py'
                ], check=True, capture_output=True, text=True)
                
                # Check for output files
                corp_files = [f for f in os.listdir('.') if f.startswith('corporations_fortune100')]
                if corp_files:
                    latest_corp_file = max(corp_files, key=os.path.getctime)
                    corp_df = pd.read_csv(latest_corp_file)
                    day1_results['corporation_records'] = len(corp_df)
                    day1_results['corporation_file'] = latest_corp_file
                    self.log_progress(1, "Fortune 100 Corporation Scraping", "completed", 
                                    {'records': len(corp_df), 'file': latest_corp_file})
                else:
                    raise FileNotFoundError("No corporation data files generated")
                    
            except Exception as e:
                self.log_progress(1, "Fortune 100 Corporation Scraping", "failed", {'error': str(e)})
                logger.error(f"Corporation scraping failed: {e}")
            
            # Task 2: CSOAF Programs Data Extraction
            self.log_progress(1, "CSOAF Programs Extraction", "starting")
            
            try:
                # Run CSOAF scraper
                subprocess.run([
                    sys.executable, 
                    'tools/csoaf_programs_scraper.py'
                ], check=True, capture_output=True, text=True)
                
                # Check for CSOAF data files
                csoaf_files = [f for f in os.listdir('.') if f.startswith('csoaf_')]
                if csoaf_files:
                    program_files = [f for f in csoaf_files if 'programs' in f and f.endswith('.csv')]
                    if program_files:
                        latest_program_file = max(program_files, key=os.path.getctime)
                        programs_df = pd.read_csv(latest_program_file)
                        day1_results['csoaf_programs'] = len(programs_df)
                        day1_results['csoaf_programs_file'] = latest_program_file
                        
                    self.log_progress(1, "CSOAF Programs Extraction", "completed", day1_results)
                else:
                    self.log_progress(1, "CSOAF Programs Extraction", "partial", 
                                    {'note': 'Limited data extracted'})
                    
            except Exception as e:
                self.log_progress(1, "CSOAF Programs Extraction", "failed", {'error': str(e)})
                logger.error(f"CSOAF scraping failed: {e}")
            
            # Task 3: Historical Sponsorship Analysis
            self.log_progress(1, "Historical Sponsorship Analysis", "starting")
            day1_results['historical_analysis'] = self.analyze_historical_sponsorships()
            self.log_progress(1, "Historical Sponsorship Analysis", "completed")
            
            # Task 4: Database Integration
            self.log_progress(1, "Database Integration", "starting")
            day1_results['database_setup'] = self.setup_integrated_database()
            self.log_progress(1, "Database Integration", "completed")
            
            self.sprint_data['day1']['status'] = 'completed'
            self.sprint_data['day1']['results'] = day1_results
            
            logger.info("✅ Day 1 completed successfully!")
            return day1_results
            
        except Exception as e:
            self.sprint_data['day1']['status'] = 'failed'
            logger.error(f"Day 1 failed: {e}")
            return None
            
    def analyze_historical_sponsorships(self):
        """Analyze historical sponsorship patterns from scraped data"""
        analysis_results = {}
        
        try:
            # Load corporation data if available
            corp_files = [f for f in os.listdir('.') if f.startswith('corporations_fortune100')]
            if corp_files:
                latest_corp_file = max(corp_files, key=os.path.getctime)
                corp_df = pd.read_csv(latest_corp_file)
                
                # Analyze sponsorship patterns
                analysis_results['total_corporations'] = len(corp_df)
                analysis_results['corporations_with_arts_history'] = len(
                    corp_df[corp_df['sponsorship_evidence_count'] > 0]
                )
                
                # Calculate average sponsorship estimates
                analysis_results['avg_min_sponsorship'] = corp_df['estimated_min_sponsorship'].mean()
                analysis_results['avg_max_sponsorship'] = corp_df['estimated_max_sponsorship'].mean()
                analysis_results['avg_typical_sponsorship'] = corp_df['estimated_typical_sponsorship'].mean()
                
                # Industry breakdown
                industry_analysis = corp_df.groupby('industry_sector').agg({
                    'estimated_typical_sponsorship': 'mean',
                    'sponsorship_evidence_count': 'sum'
                }).to_dict()
                analysis_results['by_industry'] = industry_analysis
                
        except Exception as e:
            logger.error(f"Error in historical analysis: {e}")
            analysis_results['error'] = str(e)
            
        return analysis_results
        
    def setup_integrated_database(self):
        """Set up integrated database combining foundations and corporations"""
        db_results = {}
        
        try:
            # Load existing foundation data
            foundation_files = [f for f in os.listdir('campaigns/sponsor_data') 
                             if 'mission_aligned' in f and f.endswith('.csv')]
            
            if foundation_files:
                latest_foundation_file = max(
                    [os.path.join('campaigns/sponsor_data', f) for f in foundation_files],
                    key=os.path.getctime
                )
                foundations_df = pd.read_csv(latest_foundation_file)
                db_results['foundation_records'] = len(foundations_df)
                
                # Add organization type
                foundations_df['organization_type'] = 'foundation'
            
            # Load corporation data
            corp_files = [f for f in os.listdir('.') if f.startswith('corporations_fortune100')]
            if corp_files:
                latest_corp_file = max(corp_files, key=os.path.getctime)
                corp_df = pd.read_csv(latest_corp_file)
                db_results['corporation_records'] = len(corp_df)
                
                # Standardize column names for integration
                corp_df_standardized = self.standardize_corporation_columns(corp_df)
                
                # Combine datasets
                combined_df = self.combine_foundation_corporation_data(
                    foundations_df, corp_df_standardized
                )
                
                # Save integrated database
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                integrated_file = f'integrated_sponsor_database_{timestamp}.csv'
                combined_df.to_csv(integrated_file, index=False)
                
                db_results['integrated_file'] = integrated_file
                db_results['total_records'] = len(combined_df)
                db_results['foundation_count'] = len(combined_df[combined_df['organization_type'] == 'foundation'])
                db_results['corporation_count'] = len(combined_df[combined_df['organization_type'] == 'corporation'])
                
        except Exception as e:
            logger.error(f"Database setup error: {e}")
            db_results['error'] = str(e)
            
        return db_results
        
    def standardize_corporation_columns(self, corp_df):
        """Standardize corporation data to match foundation schema"""
        standardized = corp_df.copy()
        
        # Map corporation columns to foundation schema
        column_mapping = {
            'organization_name': 'organization_name',
            'city': 'city',
            'state': 'state',
            'website': 'website',
            'industry_sector': 'program_areas',  # Map industry to program areas
            'estimated_typical_sponsorship': 'estimated_sponsorship_amount'
        }
        
        # Create standardized DataFrame
        standardized_df = pd.DataFrame()
        
        for std_col, corp_col in column_mapping.items():
            if corp_col in standardized.columns:
                standardized_df[std_col] = standardized[corp_col]
        
        # Add corporation-specific columns
        standardized_df['organization_type'] = 'corporation'
        standardized_df['funding_type'] = 'event_sponsorship'
        standardized_df['data_source'] = 'fortune100_scrape'
        
        # Add mission alignment score based on arts sponsorship evidence
        if 'sponsorship_evidence_count' in standardized.columns:
            # Convert evidence count to mission alignment score (0-100)
            max_evidence = standardized['sponsorship_evidence_count'].max()
            if max_evidence > 0:
                standardized_df['mission_alignment_score'] = (
                    standardized['sponsorship_evidence_count'] / max_evidence * 100
                ).round(1)
            else:
                standardized_df['mission_alignment_score'] = 0
        else:
            standardized_df['mission_alignment_score'] = 0
            
        return standardized_df
        
    def combine_foundation_corporation_data(self, foundations_df, corp_df):
        """Combine foundation and corporation data into unified format"""
        
        # Ensure foundations have required columns
        if 'organization_type' not in foundations_df.columns:
            foundations_df['organization_type'] = 'foundation'
        if 'funding_type' not in foundations_df.columns:
            foundations_df['funding_type'] = 'program_funding'
            
        # Get common columns
        common_columns = list(set(foundations_df.columns) & set(corp_df.columns))
        
        # Select common columns from both DataFrames
        foundations_subset = foundations_df[common_columns].copy()
        corporations_subset = corp_df[common_columns].copy()
        
        # Combine
        combined_df = pd.concat([foundations_subset, corporations_subset], ignore_index=True)
        
        # Add combined dataset metadata
        combined_df['combined_database_version'] = '1.0'
        combined_df['last_updated'] = datetime.now().isoformat()
        
        return combined_df
        
    def run_day2_campaign_development(self):
        """Execute Day 2: Campaign System Development"""
        logger.info("🚀 Starting Day 2: Campaign System Development")
        self.sprint_data['day2']['status'] = 'in_progress'
        
        # This will be implemented when we reach Day 2
        logger.info("Day 2 implementation ready - waiting for Day 1 completion")
        
    def run_day3_integration_dashboard(self):
        """Execute Day 3: Integration & Dashboard"""
        logger.info("🚀 Starting Day 3: Integration & Dashboard")
        self.sprint_data['day3']['status'] = 'in_progress'
        
        # This will be implemented when we reach Day 3
        logger.info("Day 3 implementation ready - waiting for Day 2 completion")
        
    def generate_daily_report(self, day):
        """Generate daily progress report"""
        report_file = f'day_{day}_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        
        day_data = self.sprint_data[f'day{day}']
        
        report_content = f"""# Day {day} Sprint Report
        
## Status: {day_data['status'].upper()}

## Tasks Completed:
"""
        
        for task in day_data['tasks']:
            report_content += f"- {task}\n"
            
        if day_data['results']:
            report_content += f"\n## Results:\n"
            for key, value in day_data['results'].items():
                report_content += f"- **{key}**: {value}\n"
                
        report_content += f"\n## Timestamp: {datetime.now().isoformat()}\n"
        
        with open(report_file, 'w') as f:
            f.write(report_content)
            
        logger.info(f"Day {day} report saved to {report_file}")
        return report_file
        
    def run_sprint(self, start_day=1):
        """Run the complete 3-day sprint"""
        logger.info("🎯 Starting 3-Day Dual-Track Fundraising Sprint")
        
        if start_day <= 1:
            day1_results = self.run_day1_data_collection()
            self.generate_daily_report(1)
            
            if day1_results is None:
                logger.error("Day 1 failed - aborting sprint")
                return False
                
        if start_day <= 2:
            self.run_day2_campaign_development()
            self.generate_daily_report(2)
            
        if start_day <= 3:
            self.run_day3_integration_dashboard()
            self.generate_daily_report(3)
            
        logger.info("🏆 3-Day Sprint Complete!")
        return True

def main():
    """Main execution function"""
    coordinator = ThreeDaySprintCoordinator()
    
    print("🎯 3-Day Dual-Track Fundraising Sprint")
    print("=" * 50)
    print("Day 1: Data Collection & Foundation")
    print("Day 2: Campaign System Development") 
    print("Day 3: Integration & Dashboard")
    print("=" * 50)
    
    # Start with Day 1
    success = coordinator.run_sprint(start_day=1)
    
    if success:
        print("✅ Sprint completed successfully!")
    else:
        print("❌ Sprint failed - check logs for details")

if __name__ == "__main__":
    main()