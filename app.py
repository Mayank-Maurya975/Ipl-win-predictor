import streamlit as st
import pandas as pd
import pickle
import base64
import os
import numpy as np
# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="IPL Win Predictor", 
    page_icon="🏏", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================
# ASSET LOADER
# ======================================
def get_base64_bin(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_base64 = get_base64_bin("background.jpg")

# ======================================
# MODERN iOS/ANDROID 16 THEME CSS
# ======================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman:wght@400;700;800&display=swap');
    
    * {{
        font-family: 'Times New Roman', serif !important;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 50%, #0a0e17 100%);
        background-attachment: fixed;
    }}
    
    /* Modern glass morphism */
    .glass-card {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }}
    
    .glass-card-dark {{
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 20px;
    }}
    
    /* Modern input styling */
    .stSelectbox > div > div {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        color: white;
        font-size: 16px;
        height: 56px;
        padding: 0 16px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .stSelectbox > div > div:hover {{
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }}
    
    .stNumberInput input {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: white !important;
        font-size: 16px !important;
        height: 56px !important;
        padding: 0 16px !important;
    }}
    
    .stNumberInput input:focus {{
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }}
    
    /* Modern button */
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 20px 0;
        font-weight: 700;
        border-radius: 16px;
        width: 100%;
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    div.stButton > button:first-child::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }}
    
    div.stButton > button:hover:first-child {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
    }}
    
    div.stButton > button:hover:first-child::before {{
        left: 100%;
    }}
    
    /* Modern progress bars */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        border-radius: 12px;
        height: 12px;
    }}
    
    .stProgress > div > div {{
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
    }}
    
    /* Stat cards */
    .stat-card-modern {{
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: transform 0.3s ease;
    }}
    
    .stat-card-modern:hover {{
        transform: translateY(-5px);
    }}
    
    .stat-val-modern {{
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(135deg, #3b82f6, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Times New Roman', serif;
    }}
    
    /* Probability circles */
    .prob-circle {{
        width: 180px;
        height: 180px;
        border-radius: 50%;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        background: conic-gradient(#10b981 var(--progress), rgba(255, 255, 255, 0.1) 0%);
        position: relative;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.2);
    }}
    
    
    
    .prob-circle::before {{
        content: '';
        position: absolute;
        width: 160px;
        height: 160px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 50%;
    }}
    
    .prob-circle-content {{
        position: relative;
        z-index: 2;
        text-align: center;
    }}
    
    /* Tags */
    .status-tag {{
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        margin: 4px;
    }}
    
    .tag-success {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    
    .tag-warning {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1));
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    
    .tag-danger {{
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.1));
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .animate-in {{
        animation: fadeIn 0.5s ease forwards;
    }}
    
    /* Hide Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Headers */
    h1, h2, h3, h4 {{
        background: linear-gradient(135deg, #ffffff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.5px;
        font-family: 'Times New Roman', serif;
    }}
    
    h1 {{
        font-size: 3.5rem !important;
        margin-bottom: 1rem !important;
    }}
    
    /* Smooth scrolling */
    html {{
        scroll-behavior: smooth;
    }}
    
    /* Custom metric styling */
    .stMetric {{
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: rgba(255, 255, 255, 0.08) !important;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }}
    
    
    </style>
""", unsafe_allow_html=True)

# ======================================
# CRICKET LOGIC FUNCTIONS (Same as before)
# ======================================
def calculate_required_run_rate(runs_needed, balls_left):
    if balls_left > 0:
        return (runs_needed * 6) / balls_left
    return 999

def is_impossible_situation(runs_needed, balls_left, wickets_left):
    """Check if winning is impossible based on cricket logic"""
    
    # 1. If no balls left and runs still needed
    if balls_left <= 0 and runs_needed > 0:
        return True, "Match is over! Batting team lost."
    
    # 2. If no wickets left
    if wickets_left <= 0:
        return True, "All wickets fallen! Batting team lost."
    
    # 3. If runs needed is impossible for remaining balls
    # Maximum realistic runs in T20 cricket scenarios:
    # - Last over (6 balls): Maximum realistic is 36 runs (6 sixes)
    # - Last 2 overs (12 balls): Maximum realistic is 48 runs (4 sixes per over)
    # - Last 3+ overs: Consider run rate
    
    # Calculate maximum possible runs based on balls left
    if balls_left <= 6:
        # Last over: Maximum 36 runs
        max_possible = 36
        if runs_needed > max_possible:
            return True, f"Cannot score {runs_needed} in last {balls_left} balls (max: {max_possible})"
    
    elif balls_left <= 12:
        # Last 2 overs: Maximum 48 runs (24 per over)
        max_possible = 48
        if runs_needed > max_possible:
            return True, f"Cannot score {runs_needed} in last {balls_left} balls (max: {max_possible})"
    
    elif balls_left <= 30:
        # Last 5 overs: Maximum 90 runs (18 per over)
        max_possible = 90
        if runs_needed > max_possible:
            return True, f"Cannot score {runs_needed} in last {balls_left} balls (max: {max_possible})"
    
    else:
        # More than 5 overs left: Use run rate logic
        # Maximum sustainable RR in T20 is about 15
        required_rr = calculate_required_run_rate(runs_needed, balls_left)
        if required_rr > 15:
            return True, f"Required RR {required_rr:.1f} is practically impossible to sustain"
    
    # 4. Special case: If many balls left but required RR is astronomical
    if balls_left > 6:
        required_rr = calculate_required_run_rate(runs_needed, balls_left)
        if required_rr > 20:
            return True, f"Required RR {required_rr:.1f} is too high to achieve"
    
    # 5. Last ball scenarios
    if balls_left == 1 and runs_needed > 6:
        return True, f"Cannot score {runs_needed} runs off the last ball"
    
    if balls_left == 2 and runs_needed > 12:
        return True, f"Cannot score {runs_needed} runs in last 2 balls"
    
    if balls_left == 3 and runs_needed > 18:
        return True, f"Cannot score {runs_needed} runs in last 3 balls"
    
    if balls_left == 4 and runs_needed > 24:
        return True, f"Cannot score {runs_needed} runs in last 4 balls"
    
    if balls_left == 5 and runs_needed > 30:
        return True, f"Cannot score {runs_needed} runs in last 5 balls"
    
    return False, ""

def adjust_probability_by_cricket_logic(base_prob, runs_needed, balls_left, wickets_left, crr, rrr):
    adjusted_prob = base_prob
    
    if wickets_left >= 8:
        adjusted_prob *= 1.15
    elif wickets_left >= 5:
        adjusted_prob *= 1.0
    elif wickets_left >= 3:
        adjusted_prob *= 0.85
    else:
        adjusted_prob *= 0.5
    
    if rrr > 0:
        if crr > rrr * 1.2:
            adjusted_prob *= 1.2
        elif crr < rrr * 0.8:
            adjusted_prob *= 0.8
    
    if balls_left <= 24:
        pressure_factor = 1 - (balls_left / 24) * 0.3
        adjusted_prob *= pressure_factor
    
    runs_per_ball_needed = runs_needed / balls_left if balls_left > 0 else 100
    if runs_per_ball_needed > 2:
        adjusted_prob *= 0.7
    elif runs_per_ball_needed < 0.5:
        adjusted_prob *= 1.3
    
    if runs_needed <= 10:
        adjusted_prob = max(adjusted_prob, 0.9)
    
    if wickets_left <= 3 and runs_needed > 20:
        adjusted_prob *= 0.6
    
    return np.clip(adjusted_prob, 0.01, 0.99)

def get_home_advantage(bat_team, city, matches_df):
    try:
        team_city_mapping = {
            'Chennai Super Kings': 'Chennai',
            'Mumbai Indians': 'Mumbai',
            'Royal Challengers Bangalore': 'Bengaluru',
            'Kolkata Knight Riders': 'Kolkata',
            'Delhi Capitals': 'Delhi',
            'Rajasthan Royals': 'Jaipur',
            'Sunrisers Hyderabad': 'Hyderabad',
            'Punjab Kings': 'Mohali',
            'Lucknow Super Giants': 'Lucknow',
            'Gujarat Titans': 'Ahmedabad'
        }
        
        if bat_team in team_city_mapping and team_city_mapping[bat_team] == city:
            return 1.1
    except:
        pass
    return 1.0

# ======================================
# DATA & LOGIC
# ======================================
@st.cache_resource
def load_assets():
    model = pickle.load(open("model.pkl", "rb"))
    model_cols = pickle.load(open("columns.pkl", "rb"))
    matches = pd.read_csv("data/matches.csv")
    return model, model_cols, matches

model, model_cols, matches = load_assets()

team_mapping = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Kings XI Punjab': 'Punjab Kings',
    'Rising Pune Supergiant': 'Rising Pune Supergiants',
    'Gujarat Lions': 'Gujarat Titans'
}

for old_name, new_name in team_mapping.items():
    matches.replace(old_name, new_name, inplace=True)

# ======================================
# MODERN UI COMPONENTS
# ======================================
def create_stat_card(title, value, icon="📊"):
    return f"""
    <div class="stat-card-modern animate-in">
        <div style="font-size: 14px; opacity: 0.8; margin-bottom: 8px;">{icon} {title}</div>
        <div class="stat-val-modern">{value}</div>
    </div>
    """

def create_probability_circle(team, probability, color="#10b981"):
    return f"""
    <div class="prob-circle" style="--progress: {probability*360}deg;">
        <div class="prob-circle-content">
            <div style="font-size: 40px; font-weight: 800; color: {color};">{probability*100:.1f}%</div>
            <div style="font-size: 14px; opacity: 0.8;">{team}</div>
        </div>
    </div>
    """

# ======================================
# SIDEBAR
# ======================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 20px; text-align: center;">
        <div style="font-size: 24px; font-weight: 800; margin-bottom: 20px;">🏏 IPL AI PREDICTOR</div>
        <div style="font-size: 14px; opacity: 0.7; margin-bottom: 30px;">Advanced Cricket Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Model Intelligence")
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 16px; margin: 10px 0;">
    <div style="display: flex; align-items: center; margin: 8px 0;">
        <div style="width: 8px; height: 8px; background: #10b981; border-radius: 50%; margin-right: 10px;"></div>
        <div>Home Advantage (+10%)</div>
    </div>
    <div style="display: flex; align-items: center; margin: 8px 0;">
        <div style="width: 8px; height: 8px; background: #3b82f6; border-radius: 50%; margin-right: 10px;"></div>
        <div>Wicket Impact Analysis</div>
    </div>
    <div style="display: flex; align-items: center; margin: 8px 0;">
        <div style="width: 8px; height: 8px; background: #f59e0b; border-radius: 50%; margin-right: 10px;"></div>
        <div>Death Overs Pressure</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

# ======================================
# MAIN INTERFACE
# ======================================
# Header with gradient
col_header1, col_header2, col_header3 = st.columns([1, 2, 1])
with col_header2:
    st.markdown("<h1 style='text-align: center;'>IPL MATCH WIN PREDICTOR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.8; font-size: 18px;'>Powered by Machine Learning & Cricket Intelligence</p>", unsafe_allow_html=True)

# Main input cards
st.markdown("<div class='animate-in'>", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        
        st.markdown("### 🏏 Batting Team")
        teams = sorted(pd.unique(matches[["team1", "team2"]].values.ravel()))
        
        # Add "Select Team" as first option
        teams_with_placeholder = ["Select Team"] + teams
        
        # Default to "Select Team" (index 0)
        bat_team = st.selectbox("", teams_with_placeholder, index=0, key='bat_team')
        
        st.markdown("### 🎯 Target")
        target = st.number_input("", min_value=1, value=180, key='target', label_visibility="collapsed")
        
        st.markdown("### 📈 Current Score")
        score = st.number_input("", min_value=0, value=100, key='score', label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        
        st.markdown("### 🎳 Bowling Team")
        
        # For bowling team, filter based on batting selection
        if bat_team != "Select Team":
            bowl_options = ["Select Team"] + [t for t in teams if t != bat_team]
        else:
            bowl_options = ["Select Team"] + teams
        
        bowl_team = st.selectbox("", bowl_options, index=0, key='bowl_team')
        
        st.markdown("### 🏟️ Venue")
        venue_city = matches[['venue', 'city']].dropna().drop_duplicates(subset=['venue'])
        venue_list = sorted(venue_city['venue'].tolist())
        venue_to_city = dict(zip(venue_city['venue'], venue_city['city']))
        
        # Add "Select Venue" as first option
        venue_with_placeholder = ["Select Venue"] + venue_list
        selected_venue = st.selectbox("", venue_with_placeholder, index=0, key='venue')
        
        # Get city only if venue is selected
        if selected_venue != "Select Venue":
            city = venue_to_city.get(selected_venue, "Mumbai")
        else:
            city = ""
        
        col_overs, col_wickets = st.columns(2)
        with col_overs:
            st.markdown("### ⏱️ Overs")
            overs = st.number_input("", min_value=0.0, max_value=20.0, 
                                   value=10.0, step=0.1, key='overs', label_visibility="collapsed")
        
        with col_wickets:
            st.markdown("### 🪓 Wickets")
            wickets = st.number_input("", min_value=0, max_value=10, 
                                     value=3, key='wickets', label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Validation
validation_errors = []

# Check if teams/venue are selected
if bat_team == "Select Team":
    validation_errors.append("⚠️ Please select a Batting Team!")
    
if bowl_team == "Select Team":
    validation_errors.append("⚠️ Please select a Bowling Team!")
    
if selected_venue == "Select Venue":
    validation_errors.append("⚠️ Please select a Venue!")

# Check if same team selected (only if both are selected)
if bat_team != "Select Team" and bowl_team != "Select Team":
    if bat_team == bowl_team:
        validation_errors.append("⚠️ Batting and Bowling teams cannot be the same!")

# Check if score exceeds target
if score >= target:
    validation_errors.append("⚠️ Batting team has already won! Score ≥ Target")

# Check if overs exceed 20
if overs > 20:
    validation_errors.append("⚠️ Overs cannot exceed 20")

# Check if wickets exceed 10
if wickets > 10:
    validation_errors.append("⚠️ Wickets cannot exceed 10")

# Check if overs complete but score < target
if overs >= 20 and score < target:
    validation_errors.append("⚠️ Match over! Batting team lost (20 overs completed)")

# Calculate parameters
runs_left = target - score
balls_left = max(0, 120 - int(overs * 6))
wkts_left = 10 - wickets

# Prediction Button
col_btn = st.columns([1, 2, 1])[1]
with col_btn:
    predict_btn = st.button("🚀 PREDICT WINNING PROBABILITY", use_container_width=True)

if predict_btn:
    st.markdown("<div class='animate-in'>", unsafe_allow_html=True)
    
    # Check impossible situations
    impossible, reason = is_impossible_situation(runs_left, balls_left, wkts_left)
    
    if impossible:
        st.markdown(f"""
        <div style="text-align: center; padding: 40px;">
            <div style="font-size: 48px; margin-bottom: 20px;">⛔</div>
            <h2 style="color: #ef4444;">IMPOSSIBLE TO WIN</h2>
            <p style="opacity: 0.8; font-size: 18px;">{reason}</p>
        </div>
        """, unsafe_allow_html=True)
        bat_prob = 0.01
        bowl_prob = 0.99
    else:
        # Calculate metrics
        overs_completed = overs if overs > 0 else 0.1
        crr = score / overs_completed
        rrr = calculate_required_run_rate(runs_left, balls_left)
        
        # Live Stats
        st.markdown("### 📊 Live Match Statistics")
        col_stats = st.columns(5)
        
        with col_stats[0]:
            st.markdown(create_stat_card("Runs Needed", runs_left, "🎯"), unsafe_allow_html=True)
        with col_stats[1]:
            st.markdown(create_stat_card("Balls Left", balls_left, "⏱️"), unsafe_allow_html=True)
        with col_stats[2]:
            st.markdown(create_stat_card("Req. RR", f"{rrr:.2f}", "📈"), unsafe_allow_html=True)
        with col_stats[3]:
            st.markdown(create_stat_card("Current RR", f"{crr:.2f}", "⚡"), unsafe_allow_html=True)
        with col_stats[4]:
            st.markdown(create_stat_card("Wickets Left", wkts_left, "🪓"), unsafe_allow_html=True)
        
                     # Insights
        with st.expander("🔍 **Match Analysis & Insights**", expanded=True):
            # Create 3 columns for better organization
            insight_col1, insight_col2, insight_col3 = st.columns(3)
            
            with insight_col1:
                st.markdown("### 🎯 **Match Situation**")
                
                # Wicket Analysis
                if wkts_left >= 8:
                    st.markdown('<div class="status-tag tag-success" style="margin: 10px 0;">✅ Strong Batting Position</div>', unsafe_allow_html=True)
                    st.caption(f"Only {wickets} wicket(s) down")
                elif wkts_left >= 5:
                    st.markdown('<div class="status-tag tag-warning" style="margin: 10px 0;">⚖️ Balanced Situation</div>', unsafe_allow_html=True)
                    st.caption(f"{wickets} wickets down")
                else:
                    st.markdown('<div class="status-tag tag-danger" style="margin: 10px 0;">⚠️ Batting Collapse Risk</div>', unsafe_allow_html=True)
                    st.caption(f"{wickets} wickets down")
                
                # Home Advantage
                home_advantage = get_home_advantage(bat_team, city, matches)
                if home_advantage > 1.0:
                    st.markdown('<div style="margin-top: 15px;"><span class="status-tag tag-success">🏠 Home Advantage Active</span></div>', unsafe_allow_html=True)
                    st.caption(f"{bat_team} playing at home")
            
            with insight_col2:
                st.markdown("### 📊 **Run Rate Analysis**")
                
                # Run rate analysis
                if rrr > 0:
                    if crr > rrr:
                        st.markdown('<div class="status-tag tag-success" style="margin: 10px 0;">📈 Ahead of Required Rate</div>', unsafe_allow_html=True)
                        st.caption(f"Current RR ({crr:.1f}) > Required RR ({rrr:.1f})")
                    else:
                        st.markdown('<div class="status-tag tag-warning" style="margin: 10px 0;">📉 Behind Required Rate</div>', unsafe_allow_html=True)
                        st.caption(f"Need to accelerate")
                
                # Pressure Analysis
                if balls_left <= 24:
                    st.markdown('<div style="margin-top: 15px;"><span class="status-tag tag-warning">🎯 Death Overs Phase</span></div>', unsafe_allow_html=True)
                    st.caption(f"{balls_left//6}.{balls_left%6} overs remaining")
                
                # Pressure Index
                if crr > 0:
                    pressure_index = int((rrr/crr)*100)
                    if pressure_index > 120:
                        st.markdown(f'<div style="margin-top: 15px; padding: 8px; background: rgba(239, 68, 68, 0.1); border-radius: 8px; color: #ef4444; font-weight: bold;">High Pressure: {pressure_index}%</div>', unsafe_allow_html=True)
                    elif pressure_index > 80:
                        st.markdown(f'<div style="margin-top: 15px; padding: 8px; background: rgba(245, 158, 11, 0.1); border-radius: 8px; color: #f59e0b; font-weight: bold;">Medium Pressure: {pressure_index}%</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="margin-top: 15px; padding: 8px; background: rgba(16, 185, 129, 0.1); border-radius: 8px; color: #10b981; font-weight: bold;">Low Pressure: {pressure_index}%</div>', unsafe_allow_html=True)
            
            with insight_col3:
                st.markdown("### ⚡ **Boundary Requirements**")
                
                # Calculate boundaries needed
                sixes_needed = (runs_left + 5) // 6  # Ceiling division
                fours_needed = (runs_left + 3) // 4
                
                # Display boundary info in cards
                st.markdown(f"""
                <div style="background: rgba(59, 130, 246, 0.1); border-radius: 12px; padding: 15px; margin: 10px 0;">
                    <div style="font-size: 14px; opacity: 0.8;">Sixes Required</div>
                    <div style="font-size: 28px; font-weight: bold; color: #3b82f6;">{sixes_needed}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.1); border-radius: 12px; padding: 15px; margin: 10px 0;">
                    <div style="font-size: 14px; opacity: 0.8;">Fours Required</div>
                    <div style="font-size: 28px; font-weight: bold; color: #10b981;">{fours_needed}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Projected Score
                projected_score = int(score + (crr * (20 - overs)))
                st.markdown(f"""
                <div style="background: rgba(168, 85, 247, 0.1); border-radius: 12px; padding: 15px; margin: 10px 0;">
                    <div style="font-size: 14px; opacity: 0.8;">Projected Score</div>
                    <div style="font-size: 28px; font-weight: bold; color: #a855f7;">{projected_score}</div>
                </div>
                """, unsafe_allow_html=True)   
                # Model Prediction
        try:
            # Check if all required fields are selected
            if bat_team == "Select Team" or bowl_team == "Select Team" or selected_venue == "Select Venue":
                st.error("Please select teams and venue before prediction")
                st.stop()
                
            input_df = pd.DataFrame({
                'batting_team': [bat_team], 'bowling_team': [bowl_team], 'city': [city],
                'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets_left': [wkts_left],
                'runs_target': [target], 'crr': [crr], 'rrr': [rrr]
            })
            input_df = pd.get_dummies(input_df).reindex(columns=model_cols, fill_value=0)
            base_prob = model.predict_proba(input_df)[0][1]
            
            adjusted_prob = adjust_probability_by_cricket_logic(
                base_prob, runs_left, balls_left, wkts_left, crr, rrr
            )
            
            # Only apply home advantage if we have a valid city
            if city:
                adjusted_prob *= get_home_advantage(bat_team, city, matches)
            
            bat_prob = np.clip(adjusted_prob, 0.01, 0.99)
            bowl_prob = 1 - bat_prob
            
        except Exception as e:
            st.error(f"Model error: {str(e)}")
            # Fallback to logical calculation
            bat_prob = min(0.9, max(0.1, (target - runs_left) / target * (wkts_left / 10)))
            bowl_prob = 1 - bat_prob
    
    # Probability Display
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏆 WIN PROBABILITY")
    
    prob_col1, prob_col2 = st.columns(2)
    
    with prob_col1:
        st.markdown(f"<div style='text-align: center; margin-bottom: 20px; font-size: 24px; font-weight: 700;'>{bat_team}</div>", unsafe_allow_html=True)
        st.markdown(create_probability_circle(bat_team[:15], bat_prob, "#10b981"), unsafe_allow_html=True)
        st.progress(bat_prob)
        
        if bat_prob > 0.7:
            st.markdown('<span class="status-tag tag-success" style="display: block; text-align: center; margin-top: 15px;">🎯 STRONG FAVORITES</span>', unsafe_allow_html=True)
        elif bat_prob < 0.3:
            st.markdown('<span class="status-tag tag-danger" style="display: block; text-align: center; margin-top: 15px;">⚡ UNDERDOGS</span>', unsafe_allow_html=True)
    
    with prob_col2:
        st.markdown(f"<div style='text-align: center; margin-bottom: 20px; font-size: 24px; font-weight: 700;'>{bowl_team}</div>", unsafe_allow_html=True)
        st.markdown(create_probability_circle(bowl_team[:15], bowl_prob, "#ef4444"), unsafe_allow_html=True)
        st.progress(bowl_prob)
        
        if bowl_prob > 0.7:
            st.markdown('<span class="status-tag tag-success" style="display: block; text-align: center; margin-top: 15px;">🛡️ STRONG DEFENSE</span>', unsafe_allow_html=True)
        elif bowl_prob < 0.3:
            st.markdown('<span class="status-tag tag-danger" style="display: block; text-align: center; margin-top: 15px;">🎯 NEED BREAKTHROUGHS</span>', unsafe_allow_html=True)
    
        # Match Summary
    st.markdown("---")
    st.markdown("### 📋 Match Summary")
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        # Only show RRR if it was calculated (not impossible case)
        if 'rrr' in locals() and not impossible:
            st.metric("Required Run Rate", f"{rrr:.2f}", delta=None)
        else:
            st.metric("Required Run Rate", "N/A")
    
    with summary_col2:
        # Check if balls_left exists
        if balls_left > 0 and not impossible:
            st.metric("Runs per Ball", f"{runs_left/balls_left:.2f}")
        else:
            st.metric("Runs per Ball", "N/A")
    
    with summary_col3:
        # Check if both crr and rrr exist and crr > 0
        if 'crr' in locals() and 'rrr' in locals() and crr > 0 and not impossible:
            pressure_index = int((rrr/crr)*100) if rrr > 0 else 0
            st.metric("Pressure Index", f"{pressure_index}%")
        else:
            st.metric("Pressure Index", "N/A")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer - Sticky at bottom
st.markdown("""
<div style="
    margin-top: auto;
    padding: 20px 0;
    text-align: center;
    background: linear-gradient(135deg, rgba(10, 14, 23, 0.9) 0%, rgba(26, 31, 46, 0.9) 100%);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0 0 24px 24px;
">
    <div style="font-size: 16px; font-weight: bold; color: #a5b4fc; margin-bottom: 8px;">
        🏏 IPL WIN PREDICTOR
    </div>
    <div style="font-size: 14px; opacity: 0.9; margin-bottom: 5px;">
        📊 <strong>Made By Mayank Maurya</strong>
    </div>
    <div style="font-size: 12px; opacity: 0.7;">
        Probabilities adjusted using cricket logic including home advantage, wicket impact, death overs pressure, and run rate analysis
    </div>
</div>
""", unsafe_allow_html=True)