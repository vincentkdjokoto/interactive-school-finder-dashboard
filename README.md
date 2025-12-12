# interactive-school-finder-dashboard
# 🏫 School Finder Dashboard

## 📊 Making School Choice Accessible Through Data

**Live Demo:** [https://school-finder.streamlit.app](https://school-finder.streamlit.app)

## 🎯 The Problem
Choosing a school is one of the most important decisions families make, yet the information needed is often:
- **Scattered** across multiple websites
- **Overwhelming** in volume
- **Difficult to compare** side-by-side
- **Missing parent perspectives**

## 💡 Our Solution
School Finder consolidates test scores, demographics, programs, and reviews into an **intuitive, data-driven dashboard** that empowers families to make informed decisions.

### Key Question Answered:
**"How can we present complex school choice information in an accessible, data-driven way for families?"**

## ✨ Features

### 🏠 **Interactive Home Page**
- District overview and quick stats
- School type distribution
- Parent testimonials
- Quick search with filters

### 🗺️ **Interactive School Map**
- Visual school locations with Folium
- Color-coded by type or rating
- Cluster markers for dense areas
- Clickable details for each school

### 📊 **Smart School Comparison**
- Side-by-side comparison of up to 4 schools
- Academic performance radar charts
- Demographic composition comparison
- Program offerings heatmap
- Export comparison data

### 📈 **Academic Performance Analysis**
- Performance trends by school type
- Interactive scatter plots
- School performance rankings
- Achievement gap analysis

### 👥 **Demographic Insights**
- District-wide demographic composition
- Socioeconomic analysis
- Neighborhood patterns
- Equity and access analysis

## 🚀 Quick Start

### Option 1: Local Installation
```bash
# Clone repository
git clone https://github.com/yourusername/school-finder.git
cd school-finder

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app/Home.py

🔧 Key NLP Techniques Implemented
1. Sentiment Analysis:
VADER: Rule-based for social media/text with sentiment lexicon

TextBlob: Pattern-based with subjectivity detection

Custom Categorization: Positive/Neutral/Negative based on thresholds

2. Topic Modeling:
LDA (Latent Dirichlet Allocation): Discover latent topics

Coherence Scoring: Determine optimal number of topics

Topic Interpretation: Map topics to educational themes

3. Text Processing:
Lemmatization: Reduce words to base forms

Stopword Removal: Custom education-specific stopwords

N-gram Analysis: Identify common phrases

4. Visualization:
Interactive Dashboards: Plotly for faculty insights

Word Clouds: Visual representation of themes

Sentiment Maps: Geographic/temporal sentiment patterns

💡 Actionable Faculty Development Insights
🏆 Top 3 Priority Areas:
Assessment & Grading Fairness

Issue: Perceived inconsistency and lack of transparency

Action: Develop detailed rubrics, offer grading examples

Workload Balance

Issue: Excessive workload relative to credit hours

Action: Conduct time audits, balance assignment types

Course Organization

Issue: Disorganized materials and unclear structure

Action: Standardize course templates, improve LMS use

🌟 Strengths to Reinforce:
Teaching Clarity - Faculty excel at clear explanations

Instructor Support - High accessibility and responsiveness

Subject Passion - Enthusiasm for material is evident

📋 Implementation Roadmap:
Immediate (1-2 months): Address critical assessment issues

Short-term (3-6 months): Faculty development workshops

Medium-term (6-12 months): Advanced pedagogical training

Long-term (1-2 years): Culture of continuous improvement

🚀 Deployment for Faculty Use
1. Interactive Dashboard:
python

Copy

Download
# Streamlit dashboard for faculty
streamlit run faculty_dashboard.py
2. Regular Reporting:
Monthly sentiment trend reports

Department-level benchmarking

Individual faculty development plans

3. Integration with LMS:
Real-time feedback analysis

Automated alerting for critical issues

Personalized development recommendations

📊 Expected Educational Impact
For Faculty:
Targeted Development: Focus on areas with most impact

Evidence-Based Improvement: Data-driven teaching enhancements

Recognition of Strengths: Celebrate effective practices

For Students:
Improved Learning Experience: Better teaching and assessment

Voice Heard: Feedback leads to tangible changes

Fairer Assessments: More transparent grading practices

For Institutions:
Retention Improvement: Better teaching leads to higher retention

Resource Optimization: Targeted faculty development

Quality Assurance: Ongoing monitoring of teaching quality

🎓 Educational Research Contribution
This project demonstrates how NLP and data science can transform educational feedback from:

Qualitative → Quantitative

Subjective → Objective

Reactive → Proactive

Individual → Systemic

By answering the key question about predominant themes and sentiment distribution, we provide a evidence-based foundation for faculty development that is:

Specific to actual student concerns

Measurable through sentiment scores

Actionable with clear recommendations

Impactful on teaching effectiveness
