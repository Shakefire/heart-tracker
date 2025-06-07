import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


def initialize_session_state():
    """Initialize session state variables"""
    if 'models' not in st.session_state:
        st.session_state.models = None

    if 'model_results' not in st.session_state:
        st.session_state.model_results = None

    if 'preprocessor' not in st.session_state:
        st.session_state.preprocessor = None

    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}

    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []

    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': 'Guest User',
            'age': 0,
            'points': 0,
            'badges': [],
            'streak': 0
        }


def load_custom_css():
    """Load custom CSS styling"""
    st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b6b;
    }
    
    .risk-high {
        background-color: #ffebee;
        border-left-color: #f44336;
    }
    
    .risk-medium {
        background-color: #fff3e0;
        border-left-color: #ff9800;
    }
    
    .risk-low {
        background-color: #e8f5e8;
        border-left-color: #4caf50;
    }
    
    .recommendation-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #007bff;
    }
    </style>
    """, unsafe_allow_html=True)


def create_risk_gauge(risk_probability, risk_level):
    """Create risk gauge visualization"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_probability * 100,
        title={"text": f"Risk Level: {risk_level}"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': get_risk_color(risk_level)},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))

    fig.update_layout(height=300)
    return fig


def get_risk_color(risk_level):
    """Get color based on risk level"""
    colors = {
        'Low': '#4caf50',
        'Medium': '#ff9800',
        'High': '#f44336'
    }
    return colors.get(risk_level, '#007bff')


def create_feature_importance_plot(importance_df):
    """Create feature importance visualization"""
    if importance_df is None or importance_df.empty:
        return None

    fig = px.bar(
        importance_df.head(10),
        x='Importance',
        y='Feature',
        orientation='h',
        title='Top 10 Feature Importances',
        color='Importance',
        color_continuous_scale='RdYlBu_r'
    )

    fig.update_layout(
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )

    return fig


def create_model_comparison_plot(comparison_df):
    """Create model comparison visualization"""
    if comparison_df is None or comparison_df.empty:
        return None

    fig = px.bar(
        comparison_df,
        x='Model',
        y='Risk Probability',
        color='Risk Level',
        title='Model Comparison - Risk Probabilities',
        color_discrete_map={'Low': '#4caf50',
                            'Medium': '#ff9800', 'High': '#f44336'}
    )

    fig.update_layout(height=400)
    return fig


def format_input_data(input_data):
    """Format input data for display"""
    feature_names = [
        'Age', 'Sex', 'Chest Pain Type', 'Resting BP', 'Cholesterol',
        'Fasting Blood Sugar', 'Resting ECG', 'Max Heart Rate',
        'Exercise Angina', 'ST Depression', 'Slope', 'Major Vessels', 'Thalassemia'
    ]

    formatted_data = {}
    for i, (name, value) in enumerate(zip(feature_names, input_data)):
        if name == 'Sex':
            formatted_data[name] = 'Male' if value == 1 else 'Female'
        elif name == 'Fasting Blood Sugar':
            formatted_data[name] = 'Yes' if value == 1 else 'No'
        elif name == 'Exercise Angina':
            formatted_data[name] = 'Yes' if value == 1 else 'No'
        else:
            formatted_data[name] = value

    return formatted_data


def validate_input_data(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    """Validate user input data"""
    errors = []

    if not (20 <= age <= 120):
        errors.append("Age must be between 20 and 120 years")

    if not (70 <= trestbps <= 250):
        errors.append("Resting blood pressure must be between 70 and 250 mmHg")

    if not (100 <= chol <= 600):
        errors.append("Cholesterol must be between 100 and 600 mg/dL")

    if not (60 <= thalach <= 220):
        errors.append("Maximum heart rate must be between 60 and 220 bpm")

    if not (0 <= oldpeak <= 10):
        errors.append("ST depression must be between 0 and 10")

    return errors


def generate_health_tips():
    """Generate daily health tips"""
    tips = [
        "💪 Take a 10-minute walk after each meal to help with digestion and blood sugar control.",
        "🥗 Include at least 5 servings of fruits and vegetables in your daily diet.",
        "💧 Drink at least 8 glasses of water throughout the day to stay hydrated.",
        "😴 Aim for 7-9 hours of quality sleep each night for optimal heart health.",
        "🧘 Practice deep breathing exercises for 5 minutes daily to reduce stress.",
        "🚭 If you smoke, consider quitting - it's the best gift you can give your heart.",
        "🏃 Engage in moderate exercise for at least 30 minutes, 5 days a week.",
        "🧂 Limit sodium intake to less than 2,300mg per day to maintain healthy blood pressure.",
        "❤️ Check your blood pressure regularly and keep a log for your doctor.",
        "😊 Stay socially connected - strong relationships contribute to heart health."
    ]

    # Return a random tip for today
    today = datetime.now().day
    return tips[today % len(tips)]


def calculate_health_score(input_data):
    """Calculate a simple health score based on input parameters"""
    age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal = input_data

    score = 100  # Start with perfect score

    # Age factor
    if age > 65:
        score -= 10
    elif age > 55:
        score -= 5

    # Blood pressure
    if trestbps > 140:
        score -= 15
    elif trestbps > 130:
        score -= 10

    # Cholesterol
    if chol > 240:
        score -= 15
    elif chol > 200:
        score -= 10

    # Heart rate
    if thalach < 100:
        score -= 10

    # Other risk factors
    if fbs == 1:  # High fasting blood sugar
        score -= 10

    if exang == 1:  # Exercise induced angina
        score -= 15

    if oldpeak > 2:  # Significant ST depression
        score -= 10

    return max(0, score)  # Ensure score doesn't go below 0


def create_trend_chart(history_data):
    """Create trend chart for prediction history"""
    if not history_data:
        return None

    df = pd.DataFrame(history_data)

    fig = px.line(
        df,
        x='timestamp',
        y='risk_probability',
        title='Risk Probability Trend Over Time',
        markers=True
    )

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Risk Probability',
        height=400
    )

    return fig


def add_prediction_to_history(prediction_result, input_data):
    """Add prediction to user's history"""
    history_entry = {
        'timestamp': datetime.now(),
        'risk_level': prediction_result['risk_level'],
        'risk_probability': prediction_result['risk_probability'],
        'model_used': prediction_result['model_used'],
        'input_data': input_data
    }

    st.session_state.prediction_history.append(history_entry)

    # Keep only last 50 predictions
    if len(st.session_state.prediction_history) > 50:
        st.session_state.prediction_history = st.session_state.prediction_history[-50:]


def get_emergency_contacts():
    """Get emergency contact information"""
    return {
        'Emergency Services': '112',
        'American Heart Association': '1-800-AHA-USA1',
        'Poison Control': '1-800-222-1222',
        'Crisis Text Line': 'Text HOME to 741741'
    }


def generate_workout_plan(risk_level):
    """Generate workout plan based on risk level"""
    if risk_level == "Low":
        return {
            'cardio': "30-45 minutes of moderate cardio 5 days/week",
            'strength': "2-3 strength training sessions per week",
            'flexibility': "Daily stretching or yoga",
            'intensity': "Moderate to vigorous intensity"
        }
    elif risk_level == "Medium":
        return {
            'cardio': "20-30 minutes of light to moderate cardio 4-5 days/week",
            'strength': "2 light strength training sessions per week",
            'flexibility': "Daily gentle stretching",
            'intensity': "Light to moderate intensity (consult doctor first)"
        }
    else:  # High risk
        return {
            'cardio': "10-15 minutes of light walking as tolerated",
            'strength': "Light resistance exercises 2 days/week",
            'flexibility': "Gentle stretching daily",
            'intensity': "Light intensity only (medical supervision required)"
        }
