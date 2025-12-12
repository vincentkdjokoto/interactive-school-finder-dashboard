"""
School Finder Dashboard - Main Application
Interactive dashboard for comparing schools with multiple data sources
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="School Finder - Make Informed Education Choices",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        color: #3498DB;
        font-weight: 600;
        border-left: 5px solid #F18F01;
        padding-left: 10px;
        margin-top: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .school-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background: white;
        transition: all 0.3s ease;
    }
    .school-card:hover {
        border-color: #3498DB;
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
    }
    .stButton>button {
        background: linear-gradient(90deg, #2E86AB, #3498DB);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
    }
    .feature-icon {
        font-size: 2rem;
        margin-right: 10px;
        vertical-align: middle;
    }
    .parent-review {
        background: #F8F9FA;
        border-left: 4px solid #F18F01;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

class SchoolFinder:
    """Main application class for School Finder dashboard"""
    
    def __init__(self):
        self.schools_df = None
        self.demographics_df = None
        self.reviews_df = None
        self.programs_df = None
        self.load_data()
        
    def load_data(self):
        """Load all school data"""
        # In production, this would load from CSV/database
        # For demo, we'll generate realistic sample data
        self.generate_sample_data()
        
    def generate_sample_data(self):
        """Generate realistic sample school data"""
        np.random.seed(42)
        n_schools = 50
        
        # Generate schools
        schools = []
        school_types = ['Public Elementary', 'Public Middle', 'Public High', 
                       'Charter School', 'Magnet School', 'Private School']
        neighborhoods = ['Northside', 'Southside', 'Eastside', 'Westside', 
                        'Central District', 'Riverside', 'Hilltop', 'Valley View']
        
        for i in range(n_schools):
            school_type = np.random.choice(school_types, p=[0.25, 0.2, 0.2, 0.15, 0.1, 0.1])
            
            # Generate coordinates in a realistic area
            lat = 37.76 + np.random.uniform(-0.15, 0.15)
            lon = -122.44 + np.random.uniform(-0.2, 0.2)
            
            school = {
                'school_id': i + 1,
                'name': f"{np.random.choice(['Lincoln', 'Washington', 'Roosevelt', 'Kennedy', 'King'])} "
                       f"{np.random.choice(['Elementary', 'Middle', 'High', 'Academy', 'School'])}",
                'type': school_type,
                'address': f"{np.random.randint(100, 9999)} {np.random.choice(['Main', 'Oak', 'Maple', 'Pine'])} St",
                'neighborhood': np.random.choice(neighborhoods),
                'latitude': lat,
                'longitude': lon,
                'phone': f"({np.random.randint(200,999)}) {np.random.randint(200,999)}-{np.random.randint(1000,9999)}",
                'website': f"https://www.{'public' if 'Public' in school_type else 'private'}school{i+1}.edu",
                'overall_rating': np.random.uniform(3.0, 5.0),
                'academic_rating': np.random.uniform(3.0, 5.0),
                'teacher_rating': np.random.uniform(3.0, 5.0),
                'diversity_rating': np.random.uniform(3.0, 5.0),
                'safety_rating': np.random.uniform(3.0, 5.0),
                'total_students': np.random.randint(300, 2500),
                'student_teacher_ratio': np.random.uniform(15, 25),
                'graduation_rate': np.random.uniform(70, 99) if 'High' in school_type else None,
                'college_acceptance': np.random.uniform(60, 98) if 'High' in school_type else None,
                'avg_sat_score': np.random.randint(1000, 1500) if 'High' in school_type else None,
                'avg_act_score': np.random.uniform(18, 32) if 'High' in school_type else None,
                'math_proficiency': np.random.uniform(40, 95),
                'reading_proficiency': np.random.uniform(40, 95),
                'science_proficiency': np.random.uniform(40, 95) if 'Middle' in school_type or 'High' in school_type else None,
                'attendance_rate': np.random.uniform(85, 98),
                'chronic_absenteeism': np.random.uniform(5, 25),
                'title_i': np.random.choice([True, False], p=[0.4, 0.6]),
                'free_lunch_percent': np.random.uniform(10, 85),
                'reduced_lunch_percent': np.random.uniform(5, 20),
                'transportation_provided': np.random.choice([True, False], p=[0.8, 0.2]),
                'before_school_care': np.random.choice([True, False], p=[0.6, 0.4]),
                'after_school_care': np.random.choice([True, False], p=[0.7, 0.3]),
                'year_established': np.random.randint(1950, 2015),
                'last_renovation': np.random.randint(2000, 2023)
            }
            schools.append(school)
        
        self.schools_df = pd.DataFrame(schools)
        
        # Generate demographic data
        demographics = []
        ethnicities = ['White', 'Hispanic', 'Black', 'Asian', 'Multiracial', 'Native American', 'Pacific Islander']
        
        for school in schools:
            for ethnicity in ethnicities:
                demographics.append({
                    'school_id': school['school_id'],
                    'ethnicity': ethnicity,
                    'percentage': np.random.uniform(5, 40)
                })
        
        # Normalize percentages
        demo_df = pd.DataFrame(demographics)
        for school_id in demo_df['school_id'].unique():
            total = demo_df[demo_df['school_id'] == school_id]['percentage'].sum()
            demo_df.loc[demo_df['school_id'] == school_id, 'percentage'] *= (100 / total)
        
        self.demographics_df = demo_df
        
        # Generate programs data
        programs = []
        program_types = ['Sports', 'Arts', 'STEM', 'Music', 'Language', 'Leadership', 'Community Service']
        sports = ['Basketball', 'Soccer', 'Football', 'Volleyball', 'Track & Field', 'Swimming', 'Baseball']
        arts = ['Theater', 'Dance', 'Visual Arts', 'Photography', 'Film', 'Creative Writing']
        stem = ['Robotics', 'Coding Club', 'Science Olympiad', 'Math Club', 'Engineering']
        
        for school in schools:
            n_programs = np.random.randint(5, 15)
            selected_programs = np.random.choice(program_types, n_programs, replace=True)
            
            for program_type in selected_programs:
                if program_type == 'Sports':
                    program_name = np.random.choice(sports)
                elif program_type == 'Arts':
                    program_name = np.random.choice(arts)
                elif program_type == 'STEM':
                    program_name = np.random.choice(stem)
                else:
                    program_name = f"{program_type} Club"
                
                programs.append({
                    'school_id': school['school_id'],
                    'program_name': program_name,
                    'program_type': program_type,
                    'grade_levels': np.random.choice(['K-5', '6-8', '9-12', 'All'], p=[0.3, 0.3, 0.3, 0.1]),
                    'cost': np.random.choice(['Free', '$50-100', '$100-200', '$200+'], p=[0.6, 0.2, 0.15, 0.05]),
                    'meeting_time': np.random.choice(['Before School', 'After School', 'Weekends', 'Lunch']),
                    'availability': np.random.choice(['Open Enrollment', 'Tryouts Required', 'Application'])
                })
        
        self.programs_df = pd.DataFrame(programs)
        
        # Generate reviews
        reviews = []
        review_templates = [
            "Great school with dedicated teachers. My child loves going here!",
            "Strong academic program. Could improve on extracurricular offerings.",
            "Very diverse and inclusive environment. Parent involvement is encouraged.",
            "Facilities need updating, but the teaching staff is excellent.",
            "Communication from school administration could be better.",
            "Wonderful arts program. My child has flourished creatively.",
            "Strong STEM focus with great lab facilities.",
            "Safety is a top priority here. I feel my child is well-protected.",
            "Too much homework in my opinion, but academic results are good.",
            "Excellent sports programs and team spirit.",
            "Special education support needs improvement.",
            "Great community feeling. Lots of family events.",
            "Transportation is reliable and safe.",
            "Nutrition program could offer healthier options.",
            "College counseling in high school is exceptional."
        ]
        
        for school in schools:
            n_reviews = np.random.randint(5, 20)
            for _ in range(n_reviews):
                review_date = datetime(2023, np.random.randint(1, 13), np.random.randint(1, 28))
                reviews.append({
                    'school_id': school['school_id'],
                    'review_date': review_date,
                    'rating': np.random.randint(1, 6),
                    'review_text': np.random.choice(review_templates),
                    'parent_type': np.random.choice(['Current Parent', 'Former Parent', 'Community Member']),
                    'student_grade': np.random.choice(['K-2', '3-5', '6-8', '9-12']),
                    'helpful_votes': np.random.randint(0, 20)
                })
        
        self.reviews_df = pd.DataFrame(reviews)
        
    def create_home_page(self):
        """Create the home page"""
        st.markdown('<h1 class="main-header">🏫 School Finder</h1>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: #666;">Making Informed School Choices Through Data</h3>', 
                   unsafe_allow_html=True)
        
        # Hero section
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://cdn-icons-png.flaticon.com/512/2237/2237744.png", width=150)
        
        st.markdown("---")
        
        # Key features
        st.markdown('<h3 class="sub-header">🎯 Why Use School Finder?</h3>', unsafe_allow_html=True)
        
        features = [
            ("📊", "Comprehensive Data", "Test scores, demographics, programs, and reviews in one place"),
            ("🗺️", "Interactive Maps", "See school locations and compare neighborhoods"),
            ("📈", "Smart Comparisons", "Side-by-side comparison of up to 4 schools"),
            ("👨‍👩‍👧‍👦", "Parent-Centric", "Real reviews and ratings from families like yours"),
            ("🎨", "Program Matching", "Find schools with the extracurriculars your child wants"),
            ("📱", "Mobile-Friendly", "Access all features on any device")
        ]
        
        cols = st.columns(3)
        for idx, (icon, title, description) in enumerate(features):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
                    st.markdown(f'<span class="feature-icon">{icon}</span><strong>{title}</strong>', 
                               unsafe_allow_html=True)
                    st.markdown(f'<p style="margin-top: 10px; color: #555;">{description}</p>', 
                               unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick stats
        st.markdown('<h3 class="sub-header">📊 District Overview</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Schools", len(self.schools_df))
        with col2:
            avg_rating = self.schools_df['overall_rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.1f}/5")
        with col3:
            avg_students = self.schools_df['total_students'].mean()
            st.metric("Avg. Students", f"{int(avg_students):,}")
        with col4:
            high_grad_rate = self.schools_df['graduation_rate'].mean()
            st.metric("Avg. Grad Rate", f"{high_grad_rate:.1f}%" if pd.notna(high_grad_rate) else "N/A")
        
        # School type distribution
        st.markdown('<h3 class="sub-header">🏫 School Types in Our District</h3>', unsafe_allow_html=True)
        
        type_dist = self.schools_df['type'].value_counts()
        fig = px.pie(
            values=type_dist.values,
            names=type_dist.index,
            title="Distribution of School Types",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Quick search
        st.markdown('<h3 class="sub-header">🔍 Quick School Search</h3>', unsafe_allow_html=True)
        
        search_col1, search_col2, search_col3 = st.columns(3)
        
        with search_col1:
            school_types = ['All'] + self.schools_df['type'].unique().tolist()
            selected_type = st.selectbox("School Type", school_types)
        
        with search_col2:
            neighborhoods = ['All'] + self.schools_df['neighborhood'].unique().tolist()
            selected_neighborhood = st.selectbox("Neighborhood", neighborhoods)
        
        with search_col3:
            min_rating = st.slider("Minimum Rating", 1.0, 5.0, 3.0, 0.5)
        
        # Filter schools
        filtered_df = self.schools_df.copy()
        if selected_type != 'All':
            filtered_df = filtered_df[filtered_df['type'] == selected_type]
        if selected_neighborhood != 'All':
            filtered_df = filtered_df[filtered_df['neighborhood'] == selected_neighborhood]
        filtered_df = filtered_df[filtered_df['overall_rating'] >= min_rating]
        
        # Display results
        if len(filtered_df) > 0:
            st.markdown(f"**Found {len(filtered_df)} schools matching your criteria:**")
            
            for _, school in filtered_df.head(5).iterrows():
                with st.expander(f"{school['name']} ({school['type']}) - ⭐ {school['overall_rating']:.1f}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Location:** {school['neighborhood']}")
                        st.markdown(f"**Students:** {school['total_students']:,}")
                        st.markdown(f"**Student-Teacher Ratio:** {school['student_teacher_ratio']:.1f}:1")
                        
                        # Display ratings
                        ratings_cols = st.columns(5)
                        rating_labels = ['Academic', 'Teachers', 'Diversity', 'Safety']
                        rating_values = ['academic_rating', 'teacher_rating', 'diversity_rating', 'safety_rating']
                        
                        for i, (label, value_col) in enumerate(zip(rating_labels, rating_values)):
                            with ratings_cols[i]:
                                st.metric(label, f"{school[value_col]:.1f}")
                    
                    with col2:
                        # Quick actions
                        if st.button("View Details", key=f"view_{school['school_id']}"):
                            st.session_state['selected_school'] = school['school_id']
                            st.rerun()
                        
                        if st.button("Add to Compare", key=f"compare_{school['school_id']}"):
                            if 'compare_schools' not in st.session_state:
                                st.session_state['compare_schools'] = []
                            if school['school_id'] not in st.session_state['compare_schools']:
                                st.session_state['compare_schools'].append(school['school_id'])
                                st.success(f"Added {school['name']} to comparison list!")
        
        else:
            st.info("No schools match your current filters. Try adjusting your criteria.")
        
        # Testimonial section
        st.markdown('<h3 class="sub-header">💬 What Parents Are Saying</h3>', unsafe_allow_html=True)
        
        if len(self.reviews_df) > 0:
            sample_reviews = self.reviews_df.sample(min(3, len(self.reviews_df)))
            
            for _, review in sample_reviews.iterrows():
                school_name = self.schools_df[self.schools_df['school_id'] == review['school_id']]['name'].iloc[0]
                
                st.markdown(f"""
                <div class="parent-review">
                    <strong>{school_name}</strong><br>
                    ⭐ {'★' * int(review['rating'])}{'☆' * (5 - int(review['rating']))} ({review['rating']}/5)<br>
                    "{review['review_text']}"<br>
                    <em>- {review['parent_type']}, Grade {review['student_grade']}</em>
                </div>
                """, unsafe_allow_html=True)
        
        # Call to action
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #2E86AB20, #A23B7220); border-radius: 10px;">
            <h3>Ready to Find Your Perfect School?</h3>
            <p>Use our interactive tools to explore, compare, and choose with confidence.</p>
            <p><em>Data updated monthly from official district sources</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    def create_school_map(self):
        """Create interactive school map"""
        st.markdown('<h1 class="main-header">🗺️ School Locations Map</h1>', unsafe_allow_html=True)
        
        # Map controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            map_type = st.radio(
                "Map View",
                ["All Schools", "By School Type", "By Rating"],
                horizontal=True
            )
        
        with col2:
            show_programs = st.checkbox("Show Programs", value=True)
        
        with col3:
            cluster_markers = st.checkbox("Cluster Markers", value=True)
        
        # Create base map
        center_lat = self.schools_df['latitude'].mean()
        center_lon = self.schools_df['longitude'].mean()
        
        school_map = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12,
            tiles="CartoDB positron"
        )
        
        # Color coding based on selection
        if map_type == "By School Type":
            type_colors = {
                'Public Elementary': 'blue',
                'Public Middle': 'green',
                'Public High': 'red',
                'Charter School': 'purple',
                'Magnet School': 'orange',
                'Private School': 'gray'
            }
        elif map_type == "By Rating":
            def rating_color(rating):
                if rating >= 4.5: return 'darkgreen'
                elif rating >= 4.0: return 'green'
                elif rating >= 3.5: return 'lightgreen'
                elif rating >= 3.0: return 'orange'
                else: return 'red'
        
        # Add markers for each school
        for _, school in self.schools_df.iterrows():
            # Determine marker color
            if map_type == "By School Type":
                color = type_colors.get(school['type'], 'blue')
            elif map_type == "By Rating":
                color = rating_color(school['overall_rating'])
            else:
                color = 'blue'
            
            # Get programs for this school
            school_programs = self.programs_df[self.programs_df['school_id'] == school['school_id']]
            programs_list = school_programs['program_name'].unique()[:5]  # Limit to 5
            
            # Create popup content
            popup_content = f"""
            <div style="width: 250px;">
                <h4>{school['name']}</h4>
                <p><strong>Type:</strong> {school['type']}</p>
                <p><strong>Rating:</strong> ⭐ {school['overall_rating']:.1f}/5</p>
                <p><strong>Students:</strong> {school['total_students']:,}</p>
                <p><strong>Neighborhood:</strong> {school['neighborhood']}</p>
                """
            
            if show_programs and len(programs_list) > 0:
                popup_content += f"<p><strong>Programs:</strong> {', '.join(programs_list[:3])}"
                if len(programs_list) > 3:
                    popup_content += f"... (+{len(programs_list)-3} more)"
                popup_content += "</p>"
            
            popup_content += f"""
                <a href="#school_{school['school_id']}" target="_blank" 
                   style="color: white; background: #3498DB; padding: 5px 10px; 
                          border-radius: 3px; text-decoration: none;">
                   View Details
                </a>
            </div>
            """
            
            # Create marker
            folium.Marker(
                location=[school['latitude'], school['longitude']],
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=f"{school['name']} ⭐ {school['overall_rating']:.1f}",
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(school_map)
        
        # Add cluster if enabled
        if cluster_markers:
            from folium.plugins import MarkerCluster
            marker_cluster = MarkerCluster().add_to(school_map)
        
        # Display map
        folium_static(school_map, width=1200, height=600)
        
        # School list below map
        st.markdown('<h3 class="sub-header">🏫 Schools on Map</h3>', unsafe_allow_html=True)
        
        # Filter controls for the list
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            list_type_filter = st.multiselect(
                "Filter by Type",
                self.schools_df['type'].unique(),
                default=[]
            )
        
        with col2:
            list_neighborhood_filter = st.multiselect(
                "Filter by Neighborhood",
                self.schools_df['neighborhood'].unique(),
                default=[]
            )
        
        with col3:
            min_rating_filter = st.slider("Min Rating", 1.0, 5.0, 3.0, 0.5, key="map_filter")
        
        with col4:
            sort_by = st.selectbox(
                "Sort By",
                ["Rating (High to Low)", "Name", "Number of Students", "Student-Teacher Ratio"]
            )
        
        # Filter and sort schools
        filtered_list = self.schools_df.copy()
        
        if list_type_filter:
            filtered_list = filtered_list[filtered_list['type'].isin(list_type_filter)]
        
        if list_neighborhood_filter:
            filtered_list = filtered_list[filtered_list['neighborhood'].isin(list_neighborhood_filter)]
        
        filtered_list = filtered_list[filtered_list['overall_rating'] >= min_rating_filter]
        
        # Sort
        if sort_by == "Rating (High to Low)":
            filtered_list = filtered_list.sort_values('overall_rating', ascending=False)
        elif sort_by == "Name":
            filtered_list = filtered_list.sort_values('name')
        elif sort_by == "Number of Students":
            filtered_list = filtered_list.sort_values('total_students', ascending=False)
        elif sort_by == "Student-Teacher Ratio":
            filtered_list = filtered_list.sort_values('student_teacher_ratio')
        
        # Display school cards
        st.markdown(f"**Showing {len(filtered_list)} schools**")
        
        cols_per_row = 3
        school_cols = st.columns(cols_per_row)
        
        for idx, (_, school) in enumerate(filtered_list.iterrows()):
            with school_cols[idx % cols_per_row]:
                with st.container():
                    st.markdown(f"""
                    <div class="school-card">
                        <h4>{school['name']}</h4>
                        <p><strong>Type:</strong> {school['type']}</p>
                        <p><strong>Rating:</strong> ⭐ {school['overall_rating']:.1f}</p>
                        <p><strong>Students:</strong> {school['total_students']:,}</p>
                        <p><strong>Location:</strong> {school['neighborhood']}</p>
                        <p><strong>Math Proficiency:</strong> {school['math_proficiency']:.1f}%</p>
                        <p><strong>Reading Proficiency:</strong> {school['reading_proficiency']:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Action buttons
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("Details", key=f"map_details_{school['school_id']}"):
                            st.session_state['selected_school'] = school['school_id']
                            st.rerun()
                    with btn_col2:
                        if st.button("Compare", key=f"map_compare_{school['school_id']}"):
                            if 'compare_schools' not in st.session_state:
                                st.session_state['compare_schools'] = []
                            if school['school_id'] not in st.session_state['compare_schools']:
                                st.session_state['compare_schools'].append(school['school_id'])
                                st.success(f"Added to comparison!")
    
    def create_comparison_page(self):
        """Create school comparison page"""
        st.markdown('<h1 class="main-header">📊 Compare Schools</h1>', unsafe_allow_html=True)
        
        # Initialize comparison list in session state
        if 'compare_schools' not in st.session_state:
            st.session_state['compare_schools'] = []
        
        # Comparison controls
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### Select Schools to Compare")
            available_schools = self.schools_df[~self.schools_df['school_id'].isin(st.session_state['compare_schools'])]
            
            selected_schools = st.multiselect(
                "Add schools to comparison",
                options=[f"{row['name']} ({row['type']})" for _, row in available_schools.iterrows()],
                format_func=lambda x: x,
                key="comparison_selector"
            )
            
            # Add selected schools to comparison
            if st.button("Add Selected Schools") and selected_schools:
                for school_str in selected_schools:
                    school_name = school_str.split(" (")[0]
                    school_id = self.schools_df[self.schools_df['name'] == school_name]['school_id'].iloc[0]
                    if school_id not in st.session_state['compare_schools']:
                        st.session_state['compare_schools'].append(school_id)
                st.rerun()
        
        with col2:
            st.markdown("### Current Comparison")
            if st.session_state['compare_schools']:
                for school_id in st.session_state['compare_schools']:
                    school = self.schools_df[self.schools_df['school_id'] == school_id].iloc[0]
                    st.markdown(f"• {school['name']}")
                    if st.button("Remove", key=f"remove_{school_id}"):
                        st.session_state['compare_schools'].remove(school_id)
                        st.rerun()
                
                if st.button("Clear All"):
                    st.session_state['compare_schools'] = []
                    st.rerun()
            else:
                st.info("No schools selected for comparison")
        
        # Display comparison if schools are selected
        if st.session_state['compare_schools']:
            comparison_schools = self.schools_df[
                self.schools_df['school_id'].isin(st.session_state['compare_schools'])
            ]
            
            st.markdown("---")
            st.markdown(f"### Comparing {len(comparison_schools)} Schools")
            
            # Overview metrics comparison
            st.markdown("#### 📈 Key Metrics Comparison")
            
            metrics_to_compare = [
                ('Overall Rating', 'overall_rating', 'star', 'higher'),
                ('Academic Rating', 'academic_rating', 'star', 'higher'),
                ('Teacher Rating', 'teacher_rating', 'star', 'higher'),
                ('Total Students', 'total_students', 'users', 'context'),
                ('Student-Teacher Ratio', 'student_teacher_ratio', 'ratio', 'lower'),
                ('Attendance Rate', 'attendance_rate', 'percent', 'higher'),
                ('Math Proficiency', 'math_proficiency', 'percent', 'higher'),
                ('Reading Proficiency', 'reading_proficiency', 'percent', 'higher')
            ]
            
            # Create comparison table
            comparison_data = []
            for metric_name, col_name, metric_type, direction in metrics_to_compare:
                row = {'Metric': metric_name}
                for _, school in comparison_schools.iterrows():
                    value = school[col_name]
                    if pd.isna(value):
                        row[school['name']] = 'N/A'
                    elif metric_type == 'star':
                        row[school['name']] = f"{value:.1f}/5"
                    elif metric_type == 'percent':
                        row[school['name']] = f"{value:.1f}%"
                    elif metric_type == 'users':
                        row[school['name']] = f"{int(value):,}"
                    else:
                        row[school['name']] = f"{value:.1f}"
                comparison_data.append(row)
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(
                comparison_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Visual comparison charts
            st.markdown("#### 📊 Visual Comparison")
            
            tab1, tab2, tab3 = st.tabs(["Academic Performance", "Student Demographics", "Program Offerings"])
            
            with tab1:
                # Academic performance radar chart
                academic_metrics = ['math_proficiency', 'reading_proficiency', 'academic_rating', 
                                  'teacher_rating', 'attendance_rate']
                academic_labels = ['Math Proficiency', 'Reading Proficiency', 'Academic Rating', 
                                 'Teacher Rating', 'Attendance Rate']
                
                fig = go.Figure()
                
                for _, school in comparison_schools.iterrows():
                    values = [school[metric] for metric in academic_metrics]
                    # Normalize values to 0-100 scale
                    normalized_values = [(v / 100) * 100 if 'proficiency' in metric or 'attendance' in metric else v * 20 
                                       for v, metric in zip(values, academic_metrics)]
                    
                    fig.add_trace(go.Scatterpolar(
                        r=normalized_values,
                        theta=academic_labels,
                        fill='toself',
                        name=school['name']
                    ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    showlegend=True,
                    title='Academic Performance Comparison',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Demographic comparison
                st.markdown("##### Student Demographic Composition")
                
                # Get demographic data for comparison schools
                demo_comparison = self.demographics_df[
                    self.demographics_df['school_id'].isin(st.session_state['compare_schools'])
                ]
                
                # Merge with school names
                demo_comparison = demo_comparison.merge(
                    comparison_schools[['school_id', 'name']],
                    on='school_id'
                )
                
                # Create grouped bar chart
                fig = px.bar(
                    demo_comparison,
                    x='ethnicity',
                    y='percentage',
                    color='name',
                    barmode='group',
                    title='Ethnicity Distribution Comparison',
                    labels={'percentage': 'Percentage (%)', 'ethnicity': 'Ethnicity'},
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                # Program offerings comparison
                st.markdown("##### Extracurricular Program Availability")
                
                # Get program data for comparison schools
                program_comparison = self.programs_df[
                    self.programs_df['school_id'].isin(st.session_state['compare_schools'])
                ]
                
                # Count programs by type and school
                program_counts = program_comparison.groupby(
                    ['school_id', 'program_type']
                ).size().reset_index(name='count')
                
                # Merge with school names
                program_counts = program_counts.merge(
                    comparison_schools[['school_id', 'name']],
                    on='school_id'
                )
                
                # Create heatmap-style visualization
                pivot_df = program_counts.pivot_table(
                    index='program_type',
                    columns='name',
                    values='count',
                    fill_value=0
                )
                
                fig = px.imshow(
                    pivot_df,
                    labels=dict(x="School", y="Program Type", color="Number of Programs"),
                    title="Program Offerings Heatmap",
                    color_continuous_scale='Viridis',
                    aspect='auto'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show specific programs
                st.markdown("##### Available Programs by School")
                
                for _, school in comparison_schools.iterrows():
                    with st.expander(f"Programs at {school['name']}"):
                        school_programs = self.programs_df[
                            self.programs_df['school_id'] == school['school_id']
                        ]
                        
                        if len(school_programs) > 0:
                            program_cols = st.columns(3)
                            program_types = school_programs['program_type'].unique()
                            
                            for idx, program_type in enumerate(program_types):
                                with program_cols[idx % 3]:
                                    st.markdown(f"**{program_type}**")
                                    type_programs = school_programs[
                                        school_programs['program_type'] == program_type
                                    ]['program_name'].unique()
                                    for program in type_programs[:3]:  # Show first 3
                                        st.markdown(f"• {program}")
                                    if len(type_programs) > 3:
                                        st.markdown(f"*... and {len(type_programs)-3} more*")
                        else:
                            st.info("No program data available")
            
            # Side-by-side detailed view
            st.markdown("#### 🏫 School Details Side-by-Side")
            
            # Create columns for each school
            detail_cols = st.columns(len(comparison_schools))
            
            for idx, (_, school) in enumerate(comparison_schools.iterrows()):
                with detail_cols[idx]:
                    st.markdown(f"##### {school['name']}")
                    
                    # School image/icon
                    st.image(
                        "https://cdn-icons-png.flaticon.com/512/2237/2237744.png",
                        width=100
                    )
                    
                    # Key information
                    st.markdown(f"**Type:** {school['type']}")
                    st.markdown(f"**Neighborhood:** {school['neighborhood']}")
                    st.markdown(f"**Established:** {school['year_established']}")
                    
                    # Ratings breakdown
                    st.markdown("**Ratings:**")
                    rating_cols = st.columns(2)
                    with rating_cols[0]:
                        st.metric("Academic", f"{school['academic_rating']:.1f}")
                        st.metric("Teachers", f"{school['teacher_rating']:.1f}")
                    with rating_cols[1]:
                        st.metric("Diversity", f"{school['diversity_rating']:.1f}")
                        st.metric("Safety", f"{school['safety_rating']:.1f}")
                    
                    # Contact info
                    st.markdown("**Contact:**")
                    st.markdown(f"📞 {school['phone']}")
                    st.markdown(f"🌐 [{school['website']}]({school['website']})")
                    
                    # Action buttons
                    if st.button("View Full Profile", key=f"profile_{school['school_id']}"):
                        st.session_state['selected_school'] = school['school_id']
                        st.rerun()
            
            # Download comparison data
            st.markdown("---")
            st.markdown("##### 📥 Download Comparison Data")
            
            export_col1, export_col2, export_col3 = st.columns(3)
            
            with export_col1:
                if st.button("Export as CSV"):
                    # Create comprehensive comparison data
                    export_data = []
                    for _, school in comparison_schools.iterrows():
                        school_data = {
                            'School Name': school['name'],
                            'Type': school['type'],
                            'Overall Rating': school['overall_rating'],
                            'Academic Rating': school['academic_rating'],
                            'Total Students': school['total_students'],
                            'Student-Teacher Ratio': school['student_teacher_ratio'],
                            'Math Proficiency': school['math_proficiency'],
                            'Reading Proficiency': school['reading_proficiency'],
                            'Attendance Rate': school['attendance_rate'],
                            'Website': school['website']
                        }
                        export_data.append(school_data)
                    
                    export_df = pd.DataFrame(export_data)
                    csv = export_df.to_csv(index=False)
                    
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="school_comparison.csv",
                        mime="text/csv"
                    )
            
            with export_col2:
                if st.button("Export as PDF Report"):
                    # This would generate a PDF report in a real application
                    st.info("PDF export feature requires additional libraries. Coming soon!")
            
            with export_col3:
                if st.button("Print Comparison"):
                    st.info("Print functionality works best in browser print dialog")
        
        else:
            # If no schools selected for comparison
            st.info("👈 Select schools from the dropdown to start comparing!")
            
            # Show some school recommendations
            st.markdown("### 💡 School Recommendations")
            
            rec_col1, rec_col2, rec_col3 = st.columns(3)
            
            # Top rated schools
            top_rated = self.schools_df.nlargest(3, 'overall_rating')
            with rec_col1:
                st.markdown("##### Top Rated Schools")
                for _, school in top_rated.iterrows():
                    st.markdown(f"**{school['name']}**")
                    st.markdown(f"⭐ {school['overall_rating']:.1f} | {school['type']}")
                    if st.button("Add", key=f"add_top_{school['school_id']}"):
                        if 'compare_schools' not in st.session_state:
                            st.session_state['compare_schools'] = []
                        st.session_state['compare_schools'].append(school['school_id'])
                        st.rerun()
            
            # Best academic performance
            best_academic = self.schools_df.nlargest(3, 'academic_rating')
            with rec_col2:
                st.markdown("##### Best Academics")
                for _, school in best_academic.iterrows():
                    st.markdown(f"**{school['name']}**")
                    st.markdown(f"📚 {school['academic_rating']:.1f} | Math: {school['math_proficiency']:.0f}%")
                    if st.button("Add", key=f"add_academic_{school['school_id']}"):
                        if 'compare_schools' not in st.session_state:
                            st.session_state['compare_schools'] = []
                        st.session_state['compare_schools'].append(school['school_id'])
                        st.rerun()
            
            # Most programs
            program_counts = self.programs_df.groupby('school_id').size()
            program_counts_df = pd.DataFrame(program_counts, columns=['program_count']).reset_index()
            most_programs = program_counts_df.nlargest(3, 'program_count')
            most_programs = most_programs.merge(self.schools_df, on='school_id')
            
            with rec_col3:
                st.markdown("##### Most Programs")
                for _, school in most_programs.iterrows():
                    st.markdown(f"**{school['name']}**")
                    st.markdown(f"🎨 {school['program_count']} programs")
                    if st.button("Add", key=f"add_programs_{school['school_id']}"):
                        if 'compare_schools' not in st.session_state:
                            st.session_state['compare_schools'] = []
                        st.session_state['compare_schools'].append(school['school_id'])
                        st.rerun()
    
    def create_academic_page(self):
        """Create academic performance analysis page"""
        st.markdown('<h1 class="main-header">📈 Academic Performance Analysis</h1>', unsafe_allow_html=True)
        
        # Performance overview
        st.markdown("### District Academic Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            avg_math = self.schools_df['math_proficiency'].mean()
            st.metric("Avg. Math Proficiency", f"{avg_math:.1f}%")
        with col2:
            avg_reading = self.schools_df['reading_proficiency'].mean()
            st.metric("Avg. Reading Proficiency", f"{avg_reading:.1f}%")
        with col3:
            if 'science_proficiency' in self.schools_df.columns:
                avg_science = self.schools_df['science_proficiency'].mean()
                st.metric("Avg. Science Proficiency", f"{avg_science:.1f}%" if pd.notna(avg_science) else "N/A")
        with col4:
            avg_attendance = self.schools_df['attendance_rate'].mean()
            st.metric("Avg. Attendance Rate", f"{avg_attendance:.1f}%")
        
        # Performance trends by school type
        st.markdown("### Performance by School Type")
        
        performance_by_type = self.schools_df.groupby('type').agg({
            'math_proficiency': 'mean',
            'reading_proficiency': 'mean',
            'overall_rating': 'mean',
            'total_students': 'count'
        }).round(1)
        
        performance_by_type.columns = ['Avg Math %', 'Avg Reading %', 'Avg Rating', 'Number of Schools']
        
        st.dataframe(
            performance_by_type,
            use_container_width=True
        )
        
        # Interactive performance scatter plot
        st.markdown("### Academic Performance vs. School Characteristics")
        
        scatter_col1, scatter_col2, scatter_col3 = st.columns(3)
        
        with scatter_col1:
            x_axis = st.selectbox(
                "X-Axis Metric",
                ['total_students', 'student_teacher_ratio', 'free_lunch_percent', 'year_established'],
                format_func=lambda x: x.replace('_', ' ').title()
            )
        
        with scatter_col2:
            y_axis = st.selectbox(
                "Y-Axis Metric",
                ['math_proficiency', 'reading_proficiency', 'overall_rating', 'attendance_rate'],
                format_func=lambda x: x.replace('_', ' ').title()
            )
        
        with scatter_col3:
            color_by = st.selectbox(
                "Color By",
                ['type', 'neighborhood', 'overall_rating'],
                format_func=lambda x: x.replace('_', ' ').title()
            )
        
        # Create scatter plot
        fig = px.scatter(
            self.schools_df,
            x=x_axis,
            y=y_axis,
            color=color_by,
            size='total_students',
            hover_name='name',
            hover_data=['type', 'neighborhood', 'student_teacher_ratio'],
            title=f"{y_axis.replace('_', ' ').title()} vs {x_axis.replace('_', ' ').title()}",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # School ranking table
        st.markdown("### School Performance Rankings")
        
        rank_tab1, rank_tab2, rank_tab3 = st.tabs(["Math", "Reading", "Overall"])
        
        with rank_tab1:
            math_ranking = self.schools_df[['name', 'type', 'neighborhood', 'math_proficiency', 'overall_rating']]
            math_ranking = math_ranking.sort_values('math_proficiency', ascending=False)
            math_ranking['Rank'] = range(1, len(math_ranking) + 1)
            
            st.dataframe(
                math_ranking.head(20),
                column_order=['Rank', 'name', 'type', 'neighborhood', 'math_proficiency', 'overall_rating'],
                column_config={
                    'name': 'School Name',
                    'type': 'Type',
                    'neighborhood': 'Neighborhood',
                    'math_proficiency': st.column_config.NumberColumn(
                        'Math %',
                        format='%.1f%%'
                    ),
                    'overall_rating': st.column_config.NumberColumn(
                        'Overall Rating',
                        format='%.1f'
                    )
                },
                use_container_width=True
            )
        
        with rank_tab2:
            reading_ranking = self.schools_df[['name', 'type', 'neighborhood', 'reading_proficiency', 'overall_rating']]
            reading_ranking = reading_ranking.sort_values('reading_proficiency', ascending=False)
            reading_ranking['Rank'] = range(1, len(reading_ranking) + 1)
            
            st.dataframe(
                reading_ranking.head(20),
                column_order=['Rank', 'name', 'type', 'neighborhood', 'reading_proficiency', 'overall_rating'],
                use_container_width=True
            )
        
        with rank_tab3:
            overall_ranking = self.schools_df[['name', 'type', 'neighborhood', 'overall_rating', 'math_proficiency', 'reading_proficiency']]
            overall_ranking = overall_ranking.sort_values('overall_rating', ascending=False)
            overall_ranking['Rank'] = range(1, len(overall_ranking) + 1)
            
            st.dataframe(
                overall_ranking.head(20),
                use_container_width=True
            )
        
        # Performance trends over time (simulated)
        st.markdown("### Performance Trends (Last 5 Years)")
        
        # Generate simulated trend data
        years = list(range(2019, 2024))
        trend_data = []
        
        for _, school in self.schools_df.head(10).iterrows():
            base_math = school['math_proficiency']
            base_reading = school['reading_proficiency']
            
            for year in years:
                # Simulate some variation
                math_trend = base_math + np.random.uniform(-5, 5) + (year - 2022) * np.random.uniform(-1, 2)
                reading_trend = base_reading + np.random.uniform(-5, 5) + (year - 2022) * np.random.uniform(-1, 2)
                
                trend_data.append({
                    'School': school['name'],
                    'Year': year,
                    'Math Proficiency': max(0, min(100, math_trend)),
                    'Reading Proficiency': max(0, min(100, reading_trend))
                })
        
        trend_df = pd.DataFrame(trend_data)
        
        # Plot trends
        selected_schools = st.multiselect(
            "Select schools to view trends",
            trend_df['School'].unique(),
            default=trend_df['School'].unique()[:3]
        )
        
        if selected_schools:
            filtered_trend = trend_df[trend_df['School'].isin(selected_schools)]
            
            fig = px.line(
                filtered_trend,
                x='Year',
                y=['Math Proficiency', 'Reading Proficiency'],
                color='School',
                title='Academic Performance Trends 2019-2023',
                markers=True,
                height=500
            )
            
            fig.update_layout(
                yaxis_title="Proficiency (%)",
                yaxis_range=[0, 100]
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Achievement gap analysis
        st.markdown("### Achievement Gap Analysis")
        
        # Calculate correlation between poverty and achievement
        if 'free_lunch_percent' in self.schools_df.columns:
            corr_math = self.schools_df['free_lunch_percent'].corr(self.schools_df['math_proficiency'])
            corr_reading = self.schools_df['free_lunch_percent'].corr(self.schools_df['reading_proficiency'])
            
            gap_col1, gap_col2 = st.columns(2)
            
            with gap_col1:
                st.metric(
                    "Poverty-Math Correlation",
                    f"{corr_math:.3f}",
                    delta="Lower is better",
                    delta_color="inverse"
                )
            
            with gap_col2:
                st.metric(
                    "Poverty-Reading Correlation",
                    f"{corr_reading:.3f}",
                    delta="Lower is better",
                    delta_color="inverse"
                )
            
            # Scatter plot showing relationship
            fig = px.scatter(
                self.schools_df,
                x='free_lunch_percent',
                y='math_proficiency',
                trendline='ols',
                hover_name='name',
                title='Math Proficiency vs Free Lunch Percentage',
                labels={
                    'free_lunch_percent': 'Free Lunch Eligible (%)',
                    'math_proficiency': 'Math Proficiency (%)'
                },
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def create_demographics_page(self):
        """Create demographic insights page"""
        st.markdown('<h1 class="main-header">👥 Demographic Insights</h1>', unsafe_allow_html=True)
        
        # District demographic overview
        st.markdown("### District-Wide Demographic Composition")
        
        # Aggregate demographic data
        district_demo = self.demographics_df.groupby('ethnicity')['percentage'].mean().reset_index()
        district_demo = district_demo.sort_values('percentage', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Demographic pie chart
            fig = px.pie(
                district_demo,
                values='percentage',
                names='ethnicity',
                title='Average Ethnicity Distribution Across District',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Diversity metrics
            st.markdown("#### Diversity Metrics")
            
            # Calculate diversity index (simplified)
            diversity_index = 1 - sum((district_demo['percentage']/100) ** 2)
            
            st.metric(
                "Diversity Index",
                f"{diversity_index:.3f}",
                help="0 = no diversity, 1 = maximum diversity"
            )
            
            # Most diverse schools
            # Calculate diversity for each school
            school_diversity = []
            for school_id in self.demographics_df['school_id'].unique():
                school_demo = self.demographics_df[self.demographics_df['school_id'] == school_id]
                if len(school_demo) > 1:
                    div_index = 1 - sum((school_demo['percentage']/100) ** 2)
                    school_name = self.schools_df[self.schools_df['school_id'] == school_id]['name'].iloc[0]
                    school_diversity.append({
                        'school': school_name,
                        'diversity_index': div_index
                    })
            
            if school_diversity:
                most_diverse = max(school_diversity, key=lambda x: x['diversity_index'])
                st.metric("Most Diverse School", most_diverse['school'])
        
        # Socioeconomic analysis
        st.markdown("### Socioeconomic Factors")
        
        if 'free_lunch_percent' in self.schools_df.columns:
            # Free lunch distribution
            fig = px.histogram(
                self.schools_df,
                x='free_lunch_percent',
                nbins=20,
                title='Distribution of Free Lunch Eligibility',
                labels={'free_lunch_percent': 'Free Lunch Eligible (%)'},
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Correlation matrix
            st.markdown("#### Correlation Between Demographics and Performance")
            
            # Select numeric columns for correlation
            numeric_cols = ['math_proficiency', 'reading_proficiency', 'overall_rating', 
                          'free_lunch_percent', 'student_teacher_ratio', 'attendance_rate']
            numeric_cols = [col for col in numeric_cols if col in self.schools_df.columns]
            
            corr_matrix = self.schools_df[numeric_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto='.2f',
                color_continuous_scale='RdBu',
                title='Correlation Matrix',
                aspect='auto'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Neighborhood analysis
        st.markdown("### Neighborhood Demographic Patterns")
        
        # Aggregate by neighborhood
        neighborhood_data = []
        for neighborhood in self.schools_df['neighborhood'].unique():
            neighborhood_schools = self.schools_df[self.schools_df['neighborhood'] == neighborhood]
            
            # Get demographic data for schools in this neighborhood
            neighborhood_school_ids = neighborhood_schools['school_id'].unique()
            neighborhood_demo = self.demographics_df[
                self.demographics_df['school_id'].isin(neighborhood_school_ids)
            ]
            
            if len(neighborhood_demo) > 0:
                # Calculate average demographics
                avg_demo = neighborhood_demo.groupby('ethnicity')['percentage'].mean().to_dict()
                
                neighborhood_data.append({
                    'Neighborhood': neighborhood,
                    'Number of Schools': len(neighborhood_schools),
                    'Avg Math Proficiency': neighborhood_schools['math_proficiency'].mean(),
                    'Avg Reading Proficiency': neighborhood_schools['reading_proficiency'].mean(),
                    **avg_demo  # Unpack demographic percentages
                })
        
        if neighborhood_data:
            neighborhood_df = pd.DataFrame(neighborhood_data)
            
            # Neighborhood comparison
            selected_neighborhoods = st.multiselect(
                "Select neighborhoods to compare",
                neighborhood_df['Neighborhood'].unique(),
                default=neighborhood_df['Neighborhood'].unique()[:3]
            )
            
            if selected_neighborhoods:
                filtered_neighborhood = neighborhood_df[
                    neighborhood_df['Neighborhood'].isin(selected_neighborhoods)
                ]
                
                # Melt for plotting
                ethnicity_cols = [col for col in filtered_neighborhood.columns 
                                 if col not in ['Neighborhood', 'Number of Schools', 
                                              'Avg Math Proficiency', 'Avg Reading Proficiency']]
                
                melted_df = filtered_neighborhood.melt(
                    id_vars=['Neighborhood'],
                    value_vars=ethnicity_cols,
                    var_name='Ethnicity',
                    value_name='Percentage'
                )
                
                # Create grouped bar chart
                fig = px.bar(
                    melted_df,
                    x='Neighborhood',
                    y='Percentage',
                    color='Ethnicity',
                    barmode='group',
                    title='Ethnicity Distribution by Neighborhood',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Equity analysis
        st.markdown("### Equity and Access Analysis")
        
        equity_tab1, equity_tab2, equity_tab3 = st.tabs(["Program Access", "Resource Distribution", "Achievement Gaps"])
        
        with equity_tab1:
            st.markdown("##### Program Availability by School Demographics")
            
            # Merge program data with school demographics
            program_counts = self.programs_df.groupby('school_id').size().reset_index(name='program_count')
            equity_data = self.schools_df.merge(program_counts, on='school_id', how='left')
            equity_data['program_count'] = equity_data['program_count'].fillna(0)
            
            # Scatter plot: programs vs free lunch percentage
            if 'free_lunch_percent' in equity_data.columns:
                fig = px.scatter(
                    equity_data,
                    x='free_lunch_percent',
                    y='program_count',
                    hover_name='name',
                    trendline='ols',
                    title='Program Availability vs Economic Need',
                    labels={
                        'free_lunch_percent': 'Free Lunch Eligible (%)',
                        'program_count': 'Number of Programs'
                    },
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with equity_tab2:
            st.markdown("##### Resource Distribution Analysis")
            
            # Calculate resource scores (simplified)
            resource_data = self.schools_df.copy()
            
            # Create a composite resource score
            resource_metrics = []
            if 'student_teacher_ratio' in resource_data.columns:
                # Lower ratio is better
                resource_data['teacher_ratio_score'] = 100 - (resource_data['student_teacher_ratio'] - 15)
                resource_metrics.append('teacher_ratio_score')
            
            if 'last_renovation' in resource_data.columns:
                # More recent renovation is better
                resource_data['facility_score'] = (resource_data['last_renovation'] - 2000) * 5
                resource_metrics.append('facility_score')
            
            if resource_metrics:
                resource_data['resource_score'] = resource_data[resource_metrics].mean(axis=1)
                
                # Plot resource score distribution
                fig = px.histogram(
                    resource_data,
                    x='resource_score',
                    nbins=20,
                    title='Distribution of Resource Scores',
                    labels={'resource_score': 'Resource Score'},
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with equity_tab3:
            st.markdown("##### Achievement Gap Analysis")
            
            # Calculate achievement gaps within schools
            # This would require more detailed data in a real application
            
            st.info("""
            **Achievement Gap Analysis** requires detailed student-level data 
            to compare performance across different demographic groups within the same school.
            
            In a production system, this would include:
            - Performance by ethnicity within each school
            - Performance by socioeconomic status
            - Performance by English language learner status
            - Gender performance gaps
            
            This data helps identify which schools are most effective at supporting all students.
            """)

def main():
    """Main application entry point"""
    # Initialize app
    app = SchoolFinder()
    
    # Sidebar navigation
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2237/2237744.png", width=80)
    st.sidebar.title("School Finder")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Home", "🗺️ School Map", "📊 Compare Schools", "📈 Academic Performance", "👥 Demographic Insights"],
        label_visibility="collapsed"
    )
    
    # Display selected page
    if page == "🏠 Home":
        app.create_home_page()
    elif page == "🗺️ School Map":
        app.create_school_map()
    elif page == "📊 Compare Schools":
        app.create_comparison_page()
    elif page == "📈 Academic Performance":
        app.create_academic_page()
    elif page == "👥 Demographic Insights":
        app.create_demographics_page()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### About This Dashboard
    
    **School Finder** helps families make informed school choices by providing:
    
    - ✅ Comprehensive school data
    - ✅ Interactive comparisons
    - ✅ Real parent reviews
    - ✅ Equity analysis
    
    *Data updated monthly from official sources*
    
    ---
    
    **Need Help?**
    📞 (555) 123-4567
    📧 help@schoolfinder.edu
    
    © 2024 School Finder. All rights reserved.
    """)

if __name__ == "__main__":
    main()
