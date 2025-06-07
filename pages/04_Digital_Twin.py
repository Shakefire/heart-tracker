import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Digital Twin", page_icon="🫀", layout="wide")

st.title("🫀 Digital Twin Heart Simulation")
st.markdown("Simulate how lifestyle changes and interventions might affect your heart health over time.")

st.markdown("---")

# Initialize session state for digital twin
if 'twin_baseline' not in st.session_state:
    st.session_state.twin_baseline = {
        'age': 45,
        'resting_hr': 72,
        'bp_systolic': 120,
        'bp_diastolic': 80,
        'cholesterol': 180,
        'bmi': 25,
        'fitness_level': 50,
        'stress_level': 40
    }

if 'simulation_history' not in st.session_state:
    st.session_state.simulation_history = []

# Simulation controls
st.subheader("⚙️ Digital Twin Setup")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 Baseline Profile")
    
    age = st.slider("Age", 20, 80, st.session_state.twin_baseline['age'])
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", 140, 220, 170)
    weight = st.number_input("Weight (kg)", 40, 150, 70)
    
    # Calculate BMI
    bmi = weight / ((height/100) ** 2)
    st.metric("BMI", f"{bmi:.1f}")
    
    # Health metrics
    st.markdown("### 📊 Current Health Metrics")
    resting_hr = st.slider("Resting Heart Rate (bpm)", 50, 100, st.session_state.twin_baseline['resting_hr'])
    bp_systolic = st.slider("Systolic BP (mmHg)", 90, 180, st.session_state.twin_baseline['bp_systolic'])
    bp_diastolic = st.slider("Diastolic BP (mmHg)", 60, 120, st.session_state.twin_baseline['bp_diastolic'])
    cholesterol = st.slider("Total Cholesterol (mg/dL)", 120, 300, st.session_state.twin_baseline['cholesterol'])

with col2:
    st.markdown("### 🎯 Lifestyle Factors")
    
    exercise_frequency = st.slider("Exercise Frequency (days/week)", 0, 7, 3)
    exercise_intensity = st.selectbox("Exercise Intensity", ["Light", "Moderate", "Vigorous"])
    
    diet_quality = st.slider("Diet Quality Score (0-100)", 0, 100, 60)
    smoking_status = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
    alcohol_consumption = st.selectbox("Alcohol Consumption", ["None", "Light", "Moderate", "Heavy"])
    
    stress_level = st.slider("Stress Level (0-100)", 0, 100, st.session_state.twin_baseline['stress_level'])
    sleep_quality = st.slider("Sleep Quality (0-100)", 0, 100, 70)
    
    # Medications
    st.markdown("### 💊 Medications")
    taking_bp_meds = st.checkbox("Blood Pressure Medication")
    taking_statins = st.checkbox("Cholesterol Medication")
    taking_aspirin = st.checkbox("Daily Aspirin")

# Simulation parameters
st.markdown("---")
st.subheader("🔬 Simulation Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    simulation_period = st.selectbox("Simulation Period", ["6 months", "1 year", "2 years", "5 years"])
    intervention_start = st.selectbox("Intervention Start", ["Immediately", "After 3 months", "After 6 months"])

with col2:
    # Lifestyle interventions
    st.markdown("**Lifestyle Interventions:**")
    diet_improvement = st.slider("Diet Improvement (%)", 0, 50, 0)
    exercise_increase = st.slider("Exercise Increase (%)", 0, 100, 0)
    stress_reduction = st.slider("Stress Reduction (%)", 0, 50, 0)
    
with col3:
    # Medical interventions
    st.markdown("**Medical Interventions:**")
    add_bp_medication = st.checkbox("Add BP Medication")
    add_statin = st.checkbox("Add Statin")
    add_lifestyle_program = st.checkbox("Join Lifestyle Program")

# Run simulation
if st.button("🚀 Run Simulation", type="primary"):
    
    # Convert simulation period to months
    period_months = {
        "6 months": 6,
        "1 year": 12,
        "2 years": 24,
        "5 years": 60
    }[simulation_period]
    
    # Calculate intervention start month
    intervention_month = {
        "Immediately": 0,
        "After 3 months": 3,
        "After 6 months": 6
    }[intervention_start]
    
    # Generate simulation data
    months = list(range(period_months + 1))
    dates = [datetime.now() + timedelta(days=30*i) for i in months]
    
    # Initialize baseline values
    sim_data = {
        'month': months,
        'date': dates,
        'resting_hr': [],
        'bp_systolic': [],
        'bp_diastolic': [],
        'cholesterol': [],
        'bmi': [],
        'fitness_level': [],
        'stress_level': [],
        'cardiovascular_age': [],
        'risk_score': []
    }
    
    # Simulate progression
    for month in months:
        # Natural aging effects
        age_factor = month / 12  # Age in years
        
        # Baseline deterioration due to aging
        hr_change = age_factor * 0.5
        bp_sys_change = age_factor * 1.0
        bp_dia_change = age_factor * 0.5
        chol_change = age_factor * 2.0
        
        # Intervention effects (start after intervention_month)
        if month >= intervention_month:
            # Diet improvement effects
            diet_factor = diet_improvement / 100
            chol_change -= diet_factor * 20  # Cholesterol reduction
            bp_sys_change -= diet_factor * 10  # BP reduction
            
            # Exercise increase effects
            exercise_factor = exercise_increase / 100
            hr_change -= exercise_factor * 5  # Lower resting HR
            bp_sys_change -= exercise_factor * 8
            bp_dia_change -= exercise_factor * 5
            
            # Stress reduction effects
            stress_factor = stress_reduction / 100
            hr_change -= stress_factor * 3
            bp_sys_change -= stress_factor * 6
            
            # Medication effects
            if add_bp_medication:
                bp_sys_change -= 15
                bp_dia_change -= 10
            
            if add_statin:
                chol_change -= 30
        
        # Apply changes with some randomness
        current_hr = max(50, resting_hr + hr_change + random.uniform(-2, 2))
        current_bp_sys = max(90, bp_systolic + bp_sys_change + random.uniform(-3, 3))
        current_bp_dia = max(60, bp_diastolic + bp_dia_change + random.uniform(-2, 2))
        current_chol = max(120, cholesterol + chol_change + random.uniform(-5, 5))
        current_bmi = max(15, bmi + (age_factor * 0.2) + random.uniform(-0.2, 0.2))
        
        # Calculate derived metrics
        fitness_level = max(0, min(100, 100 - (current_hr - 60) - (current_bmi - 25) * 2))
        current_stress = max(0, min(100, stress_level - stress_reduction))
        
        # Cardiovascular age calculation (simplified)
        cv_age = age + (current_bp_sys - 120) * 0.2 + (current_chol - 200) * 0.05 + (current_bmi - 25) * 0.5
        
        # Risk score calculation (0-100)
        risk_score = (
            (current_bp_sys - 120) * 0.3 +
            (current_chol - 200) * 0.1 +
            (current_bmi - 25) * 2 +
            (current_hr - 60) * 0.2 +
            current_stress * 0.3
        )
        risk_score = max(0, min(100, risk_score))
        
        # Store values
        sim_data['resting_hr'].append(current_hr)
        sim_data['bp_systolic'].append(current_bp_sys)
        sim_data['bp_diastolic'].append(current_bp_dia)
        sim_data['cholesterol'].append(current_chol)
        sim_data['bmi'].append(current_bmi)
        sim_data['fitness_level'].append(fitness_level)
        sim_data['stress_level'].append(current_stress)
        sim_data['cardiovascular_age'].append(cv_age)
        sim_data['risk_score'].append(risk_score)
    
    # Create DataFrame
    sim_df = pd.DataFrame(sim_data)
    
    # Display results
    st.markdown("---")
    st.subheader("📊 Simulation Results")
    
    # Key metrics comparison
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        initial_risk = sim_df['risk_score'].iloc[0]
        final_risk = sim_df['risk_score'].iloc[-1]
        risk_change = final_risk - initial_risk
        st.metric("Risk Score", f"{final_risk:.1f}", f"{risk_change:+.1f}")
    
    with col2:
        initial_bp = sim_df['bp_systolic'].iloc[0]
        final_bp = sim_df['bp_systolic'].iloc[-1]
        bp_change = final_bp - initial_bp
        st.metric("Systolic BP", f"{final_bp:.0f}", f"{bp_change:+.0f}")
    
    with col3:
        initial_chol = sim_df['cholesterol'].iloc[0]
        final_chol = sim_df['cholesterol'].iloc[-1]
        chol_change = final_chol - initial_chol
        st.metric("Cholesterol", f"{final_chol:.0f}", f"{chol_change:+.0f}")
    
    with col4:
        initial_cv_age = sim_df['cardiovascular_age'].iloc[0]
        final_cv_age = sim_df['cardiovascular_age'].iloc[-1]
        cv_age_change = final_cv_age - initial_cv_age
        st.metric("CV Age", f"{final_cv_age:.1f}", f"{cv_age_change:+.1f}")
    
    # Visualization tabs
    tab1, tab2, tab3 = st.tabs(["📈 Risk Trends", "🫀 Vital Signs", "💪 Fitness Metrics"])
    
    with tab1:
        # Risk score over time
        fig_risk = px.line(sim_df, x='date', y='risk_score', title='Cardiovascular Risk Score Over Time')
        # Fix: convert dates[intervention_month] to timestamp for add_vline
        vline_x = dates[intervention_month]
        if isinstance(vline_x, datetime):
            vline_x = vline_x.timestamp() * 1000  # convert to ms timestamp for plotly
        fig_risk.add_vline(x=vline_x, line_dash="dash", 
                          annotation_text="Intervention Start", annotation_position="top")
        fig_risk.update_layout(height=400)
        st.plotly_chart(fig_risk, use_container_width=True)
        
        # Cardiovascular age
        fig_cv_age = px.line(sim_df, x='date', y='cardiovascular_age', title='Cardiovascular Age Over Time')
        fig_cv_age.add_hline(y=age, line_dash="dash", annotation_text="Chronological Age")
        fig_cv_age.update_layout(height=400)
        st.plotly_chart(fig_cv_age, use_container_width=True)
    
    with tab2:
        # Blood pressure
        fig_bp = go.Figure()
        fig_bp.add_trace(go.Scatter(x=sim_df['date'], y=sim_df['bp_systolic'], name='Systolic BP'))
        fig_bp.add_trace(go.Scatter(x=sim_df['date'], y=sim_df['bp_diastolic'], name='Diastolic BP'))
        fig_bp.add_hline(y=140, line_dash="dash", line_color="red", annotation_text="High BP Threshold")
        fig_bp.update_layout(title='Blood Pressure Over Time', height=400)
        st.plotly_chart(fig_bp, use_container_width=True)
        
        # Heart rate and cholesterol
        col1, col2 = st.columns(2)
        
        with col1:
            fig_hr = px.line(sim_df, x='date', y='resting_hr', title='Resting Heart Rate')
            fig_hr.update_layout(height=300)
            st.plotly_chart(fig_hr, use_container_width=True)
        
        with col2:
            fig_chol = px.line(sim_df, x='date', y='cholesterol', title='Total Cholesterol')
            fig_chol.add_hline(y=240, line_dash="dash", line_color="red", annotation_text="High Cholesterol")
            fig_chol.update_layout(height=300)
            st.plotly_chart(fig_chol, use_container_width=True)
    
    with tab3:
        # Fitness and stress levels
        col1, col2 = st.columns(2)
        
        with col1:
            fig_fitness = px.line(sim_df, x='date', y='fitness_level', title='Fitness Level')
            fig_fitness.update_layout(height=300)
            st.plotly_chart(fig_fitness, use_container_width=True)
        
        with col2:
            fig_stress = px.line(sim_df, x='date', y='stress_level', title='Stress Level')
            fig_stress.update_layout(height=300)
            st.plotly_chart(fig_stress, use_container_width=True)
        
        # BMI trend
        fig_bmi = px.line(sim_df, x='date', y='bmi', title='BMI Over Time')
        fig_bmi.add_hline(y=25, line_dash="dash", annotation_text="Overweight Threshold")
        fig_bmi.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Obese Threshold")
        fig_bmi.update_layout(height=400)
        st.plotly_chart(fig_bmi, use_container_width=True)
    
    # Save simulation
    if st.button("💾 Save Simulation"):
        simulation_record = {
            'timestamp': datetime.now(),
            'period': simulation_period,
            'interventions': {
                'diet_improvement': diet_improvement,
                'exercise_increase': exercise_increase,
                'stress_reduction': stress_reduction,
                'medications': [add_bp_medication, add_statin]
            },
            'results': {
                'initial_risk': initial_risk,
                'final_risk': final_risk,
                'risk_change': risk_change
            }
        }
        
        st.session_state.simulation_history.append(simulation_record)
        st.success("✅ Simulation saved to your history!")

# Scenario presets
st.markdown("---")
st.subheader("🎭 Scenario Presets")

scenarios = {
    "Heart-Healthy Lifestyle": {
        "description": "Comprehensive lifestyle improvements",
        "diet_improvement": 30,
        "exercise_increase": 50,
        "stress_reduction": 25,
        "add_bp_medication": False,
        "add_statin": False
    },
    "Medical Management": {
        "description": "Medication-focused approach",
        "diet_improvement": 10,
        "exercise_increase": 20,
        "stress_reduction": 10,
        "add_bp_medication": True,
        "add_statin": True
    },
    "Gradual Improvement": {
        "description": "Modest, sustainable changes",
        "diet_improvement": 15,
        "exercise_increase": 25,
        "stress_reduction": 15,
        "add_bp_medication": False,
        "add_statin": False
    },
    "Aggressive Intervention": {
        "description": "Maximum lifestyle and medical intervention",
        "diet_improvement": 40,
        "exercise_increase": 75,
        "stress_reduction": 35,
        "add_bp_medication": True,
        "add_statin": True
    }
}

selected_scenario = st.selectbox("Try a preset scenario:", ["Custom"] + list(scenarios.keys()))

if selected_scenario != "Custom":
    scenario = scenarios[selected_scenario]
    st.info(f"**{selected_scenario}:** {scenario['description']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Lifestyle Changes:**")
        st.write(f"• Diet improvement: {scenario['diet_improvement']}%")
        st.write(f"• Exercise increase: {scenario['exercise_increase']}%")
        st.write(f"• Stress reduction: {scenario['stress_reduction']}%")
    
    with col2:
        st.markdown("**Medical Interventions:**")
        st.write(f"• BP medication: {'Yes' if scenario['add_bp_medication'] else 'No'}")
        st.write(f"• Statin: {'Yes' if scenario['add_statin'] else 'No'}")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About Digital Twin")
    st.markdown("""
    This digital twin simulation models how your heart health might change over time based on:
    
    **📊 Tracked Metrics:**
    - Blood pressure
    - Heart rate
    - Cholesterol levels
    - BMI and fitness
    - Stress levels
    - Cardiovascular age
    
    **🎯 Interventions:**
    - Lifestyle modifications
    - Medication effects
    - Timing of changes
    
    **⚠️ Important Notes:**
    - This is a simplified model
    - Results are estimations
    - Consult healthcare providers
    - Individual results may vary
    """)
    
    st.markdown("---")
    st.header("📈 Simulation History")
    
    if hasattr(st.session_state, 'simulation_history') and st.session_state.simulation_history:
        for i, sim in enumerate(st.session_state.simulation_history[-3:]):
            st.markdown(f"**{i+1}.** {sim['period']}")
            st.write(f"Risk change: {sim['results']['risk_change']:+.1f}")
    else:
        st.info("No simulations run yet.")
