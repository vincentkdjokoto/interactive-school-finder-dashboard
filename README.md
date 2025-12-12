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
