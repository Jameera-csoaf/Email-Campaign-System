# 🚀 CSOAF Email Campaign Manager - Complete Setup Guide

## 📋 Prerequisites
- Python 3.8+ installed
- Git installed
- VS Code (recommended)

## 🛠️ Setup Instructions (Run in VS Code Terminal)

### Step 1: Clone and Navigate
```bash
git clone https://github.com/Jameera-csoaf/Email-Campaign-System.git
cd Email-Campaign-System
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install streamlit pandas plotly mailchimp-marketing-python openai python-dotenv
```

### Step 4: Set Up API Keys (Optional for Demo)
```bash
# Create environment file
echo "MAILCHIMP_API_KEY=your-mailchimp-api-key-here" > .env
echo "OPENAI_API_KEY=your-openai-api-key-here" >> .env
```

### Step 5: Launch Application
```bash
streamlit run app/main.py
```

## 🎯 What You'll See
- **Browser opens automatically** at `http://localhost:8501`
- **Professional dashboard** with real Fortune 1000 data
- **Interactive UI** with all features functional
- **1,000 corporations** and **700 prospects** loaded

## 🔥 Key Features to Explore
1. **Executive Dashboard** - Real-time analytics
2. **Record Manager** - Browse 1,000 Fortune 1000 companies
3. **Campaign Creator** - AI-powered email campaigns
4. **Email Templates** - Professional, personalized templates
5. **Analytics** - Charts, maps, industry insights

## 📊 Performance Metrics
- **Data Loading**: ~2-3 seconds for 1,000 records
- **Search/Filter**: Instant response
- **Chart Rendering**: Real-time updates
- **Campaign Generation**: ~5 seconds with AI

---
*Built by Jameera for CSOAF - Professional AI-Powered Fundraising Platform*