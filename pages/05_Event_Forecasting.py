import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import random

st.set_page_config(page_title="Event Forecasting", page_icon="🔮", layout="wide")

st.title("🔮 Predictive Event Forecasting")
st.markdown("Use time-aware deep learning models to forecast your heart health risk trends over the next 3-6 months.")

st.markdown("---")

# Check if models are loaded
if not hasattr(st.session_state, 'models') or st.session_state.models is None:
    st.error("⚠️ Models not loaded! Please go to the main page and train the models first.")
    if st.button("Go to Main Page"):
        st.switch_page("app.py")
    st.stop()

# Initialize forecasting data in session state
if 'health_timeline' not in st.session_state:
    st.session_state.health_timeline = []

if 'forecast_results' not in st.session_state:
    st.session_state.forecast_results = {}

class HealthForecaster:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.sequence_length = 30  # Use 30 days of data for prediction
        
    def create_lstm_forecasting_model(self, input_shape):
        """Create LSTM model specifically for time series forecasting"""
        model = keras.Sequential([
            keras.layers.LSTM(64, return_sequences=True, input_shape=input_shape),
            keras.layers.Dropout(0.2),
            keras.layers.LSTM(32, return_sequences=True),
            keras.layers.Dropout(0.2),
            keras.layers.LSTM(16),
            keras.layers.Dropout(0.1),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')  # Risk probability output
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def generate_historical_data(self, base_metrics, days=90):
        """Generate realistic historical health data"""
        dates = [datetime.now() - timedelta(days=i) for i in range(days, 0, -1)]
        
        # Base values from user input
        age = base_metrics.get('age', 45)
        bp_systolic = base_metrics.get('bp_systolic', 120)
        cholesterol = base_metrics.get('cholesterol', 200)
        resting_hr = base_metrics.get('resting_hr', 70)
        bmi = base_metrics.get('bmi', 25)
        stress_level = base_metrics.get('stress_level', 40)
        exercise_frequency = base_metrics.get('exercise_frequency', 3)
        
        historical_data = []
        
        for i, date in enumerate(dates):
            # Add realistic variations and trends
            day_of_week = date.weekday()
            is_weekend = day_of_week >= 5
            
            # Weekly patterns
            stress_variation = 10 if not is_weekend else -5
            exercise_variation = -1 if not is_weekend else 1
            
            # Seasonal trends (simplified)
            seasonal_factor = np.sin(2 * np.pi * i / 365) * 5
            
            # Random daily variations
            daily_variation = random.uniform(-5, 5)
            
            # Calculate daily metrics with variations
            daily_bp = bp_systolic + stress_variation + seasonal_factor + daily_variation
            daily_cholesterol = cholesterol + random.uniform(-10, 10)
            daily_hr = resting_hr + stress_variation * 0.5 + random.uniform(-3, 3)
            daily_stress = max(0, min(100, stress_level + stress_variation + random.uniform(-10, 10)))
            daily_exercise = max(0, exercise_frequency + exercise_variation + random.uniform(-1, 1))
            
            # Calculate risk score
            risk_score = self._calculate_risk_score(daily_bp, daily_cholesterol, daily_hr, daily_stress, bmi, age)
            
            historical_data.append({
                'date': date,
                'bp_systolic': max(90, min(200, daily_bp)),
                'cholesterol': max(120, min(350, daily_cholesterol)),
                'resting_hr': max(50, min(120, daily_hr)),
                'stress_level': daily_stress,
                'exercise_frequency': daily_exercise,
                'bmi': bmi + random.uniform(-0.5, 0.5),
                'risk_score': max(0, min(1, risk_score))
            })
        
        return pd.DataFrame(historical_data)
    
    def _calculate_risk_score(self, bp_systolic, cholesterol, resting_hr, stress_level, bmi, age):
        """Calculate risk score based on health metrics"""
        score = 0
        
        # Blood pressure factor
        if bp_systolic > 140:
            score += 0.3
        elif bp_systolic > 130:
            score += 0.2
        
        # Cholesterol factor
        if cholesterol > 240:
            score += 0.2
        elif cholesterol > 200:
            score += 0.1
        
        # Heart rate factor
        if resting_hr > 80:
            score += 0.1
        
        # Stress factor
        score += (stress_level / 100) * 0.2
        
        # BMI factor
        if bmi > 30:
            score += 0.15
        elif bmi > 25:
            score += 0.1
        
        # Age factor
        if age > 65:
            score += 0.1
        elif age > 55:
            score += 0.05
        
        return score
    
    def prepare_sequences(self, data, sequence_length):
        """Prepare sequences for LSTM training"""
        features = ['bp_systolic', 'cholesterol', 'resting_hr', 'stress_level', 'exercise_frequency', 'bmi']
        X, y = [], []
        
        for i in range(sequence_length, len(data)):
            X.append(data[features].iloc[i-sequence_length:i].values)
            y.append(data['risk_score'].iloc[i])
        
        return np.array(X), np.array(y)
    
    def forecast_risk_trends(self, historical_data, forecast_days=90):
        """Forecast risk trends for the specified number of days"""
        
        # Normalize the data
        features = ['bp_systolic', 'cholesterol', 'resting_hr', 'stress_level', 'exercise_frequency', 'bmi']
        scaled_data = historical_data.copy()
        scaled_data[features] = self.scaler.fit_transform(historical_data[features])
        
        # Prepare sequences
        X, y = self.prepare_sequences(scaled_data, self.sequence_length)
        
        if len(X) == 0:
            return None, None
        
        # Create and train forecasting model
        model = self.create_lstm_forecasting_model((self.sequence_length, len(features)))
        
        # Train with early stopping
        early_stopping = keras.callbacks.EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
        
        model.fit(X, y, epochs=50, batch_size=8, verbose=0, callbacks=[early_stopping])
        
        # Generate forecasts
        forecast_dates = [historical_data['date'].iloc[-1] + timedelta(days=i) for i in range(1, forecast_days + 1)]
        forecasted_risks = []
        forecasted_metrics = []
        
        # Use the last sequence to start forecasting
        current_sequence = scaled_data[features].iloc[-self.sequence_length:].values
        
        for i in range(forecast_days):
            # Predict next risk score
            sequence_input = current_sequence.reshape(1, self.sequence_length, len(features))
            predicted_risk = model.predict(sequence_input, verbose=0)[0][0]
            forecasted_risks.append(predicted_risk)
            
            # Simulate next day's metrics (simplified approach)
            # In practice, you'd want separate models for each metric
            next_metrics = current_sequence[-1].copy()
            
            # Add some realistic variations
            for j, feature in enumerate(features):
                if feature == 'stress_level':
                    next_metrics[j] += random.uniform(-0.05, 0.05)
                elif feature == 'exercise_frequency':
                    next_metrics[j] += random.uniform(-0.02, 0.02)
                else:
                    next_metrics[j] += random.uniform(-0.01, 0.01)
            
            # Ensure values stay within reasonable bounds
            next_metrics = np.clip(next_metrics, 0, 1)
            
            # Update sequence for next prediction
            current_sequence = np.roll(current_sequence, -1, axis=0)
            current_sequence[-1] = next_metrics
            
            # Store denormalized metrics for display
            denormalized_metrics = self.scaler.inverse_transform([next_metrics])[0]
            forecasted_metrics.append({
                'date': forecast_dates[i],
                'bp_systolic': denormalized_metrics[0],
                'cholesterol': denormalized_metrics[1],
                'resting_hr': denormalized_metrics[2],
                'stress_level': denormalized_metrics[3],
                'exercise_frequency': denormalized_metrics[4],
                'bmi': denormalized_metrics[5],
                'risk_score': predicted_risk
            })
        
        forecast_df = pd.DataFrame(forecasted_metrics)
        return forecast_df, model

# Input section
st.subheader("📊 Current Health Profile")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 👤 Basic Information")
    age = st.number_input("Age", 20, 100, 45)
    height = st.number_input("Height (cm)", 140, 220, 170)
    weight = st.number_input("Weight (kg)", 40, 150, 70)
    bmi = weight / ((height/100) ** 2)
    st.metric("BMI", f"{bmi:.1f}")

with col2:
    st.markdown("### 🩺 Health Metrics")
    bp_systolic = st.number_input("Systolic BP (mmHg)", 90, 200, 120)
    cholesterol = st.number_input("Cholesterol (mg/dL)", 120, 400, 200)
    resting_hr = st.number_input("Resting HR (bpm)", 50, 120, 70)

with col3:
    st.markdown("### 🎯 Lifestyle Factors")
    stress_level = st.slider("Stress Level (0-100)", 0, 100, 40)
    exercise_frequency = st.slider("Exercise Days/Week", 0, 7, 3)
    sleep_hours = st.slider("Sleep Hours/Night", 4, 12, 7)

# Forecasting controls
st.markdown("---")
st.subheader("🔮 Forecasting Parameters")

col1, col2 = st.columns(2)

with col1:
    forecast_period = st.selectbox("Forecast Period", ["3 months", "6 months", "1 year"])
    include_interventions = st.checkbox("Include Planned Interventions", value=False)

with col2:
    confidence_intervals = st.checkbox("Show Confidence Intervals", value=True)
    detailed_breakdown = st.checkbox("Show Detailed Metric Forecasts", value=True)

# Intervention planning (if enabled)
if include_interventions:
    st.markdown("### 🎯 Planned Interventions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        diet_changes = st.selectbox("Dietary Changes", ["None", "Moderate Improvement", "Significant Improvement"])
        exercise_changes = st.selectbox("Exercise Changes", ["None", "Increase Frequency", "Increase Intensity", "Both"])
        stress_management = st.selectbox("Stress Management", ["None", "Meditation/Yoga", "Counseling", "Comprehensive Program"])
    
    with col2:
        medication_changes = st.multiselect("Medication Changes", 
                                          ["Start BP Medication", "Start Statin", "Adjust Current Meds"])
        lifestyle_program = st.selectbox("Lifestyle Program", ["None", "Cardiac Rehab", "Weight Management", "Diabetes Program"])

# Generate forecast
if st.button("🚀 Generate Forecast", type="primary"):
    
    # Convert forecast period to days
    period_days = {
        "3 months": 90,
        "6 months": 180,
        "1 year": 365
    }[forecast_period]
    
    with st.spinner("Generating health forecast... This may take a moment."):
        
        # Prepare base metrics
        base_metrics = {
            'age': age,
            'bp_systolic': bp_systolic,
            'cholesterol': cholesterol,
            'resting_hr': resting_hr,
            'bmi': bmi,
            'stress_level': stress_level,
            'exercise_frequency': exercise_frequency
        }
        
        # Initialize forecaster
        forecaster = HealthForecaster()
        
        # Generate historical data
        historical_data = forecaster.generate_historical_data(base_metrics, days=90)
        
        # Generate forecast
        forecast_df, model = forecaster.forecast_risk_trends(historical_data, forecast_days=period_days)
        
        if forecast_df is not None:
            # Store results in session state
            st.session_state.forecast_results = {
                'historical_data': historical_data,
                'forecast_data': forecast_df,
                'base_metrics': base_metrics,
                'period': forecast_period
            }
            
            # Display results
            st.markdown("---")
            st.subheader("📈 Forecast Results")
            
            # Key forecast metrics
            current_risk = historical_data['risk_score'].iloc[-1]
            avg_forecast_risk = forecast_df['risk_score'].mean()
            max_forecast_risk = forecast_df['risk_score'].max()
            risk_trend = "Increasing" if avg_forecast_risk > current_risk else "Decreasing"
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Risk", f"{current_risk:.1%}")
            
            with col2:
                risk_change = avg_forecast_risk - current_risk
                st.metric("Average Forecast Risk", f"{avg_forecast_risk:.1%}", f"{risk_change:+.1%}")
            
            with col3:
                st.metric("Peak Risk", f"{max_forecast_risk:.1%}")
            
            with col4:
                st.metric("Risk Trend", risk_trend)
            
            # Risk level interpretation
            if avg_forecast_risk < 0.3:
                st.success("✅ Your forecasted risk remains in the LOW range. Continue your current healthy habits!")
            elif avg_forecast_risk < 0.6:
                st.warning("⚠️ Your forecasted risk is in the MODERATE range. Consider preventive measures.")
            else:
                st.error("🚨 Your forecasted risk is HIGH. Please consult with a healthcare professional about prevention strategies.")
            
            # Visualization tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Risk Trend", "🔍 Detailed Metrics", "📅 Timeline View", "⚠️ Risk Events"])
            
            with tab1:
                # Combined historical and forecast risk chart
                fig_risk = go.Figure()
                
                # Historical data
                fig_risk.add_trace(go.Scatter(
                    x=historical_data['date'],
                    y=historical_data['risk_score'],
                    mode='lines',
                    name='Historical Risk',
                    line=dict(color='blue')
                ))
                
                # Forecast data
                fig_risk.add_trace(go.Scatter(
                    x=forecast_df['date'],
                    y=forecast_df['risk_score'],
                    mode='lines',
                    name='Forecasted Risk',
                    line=dict(color='red', dash='dash')
                ))
                
                # Add confidence intervals if requested
                if confidence_intervals:
                    # Simple confidence intervals (±10%)
                    upper_bound = forecast_df['risk_score'] * 1.1
                    lower_bound = forecast_df['risk_score'] * 0.9
                    
                    fig_risk.add_trace(go.Scatter(
                        x=forecast_df['date'],
                        y=upper_bound,
                        fill=None,
                        mode='lines',
                        line_color='rgba(0,0,0,0)',
                        showlegend=False
                    ))
                    
                    fig_risk.add_trace(go.Scatter(
                        x=forecast_df['date'],
                        y=lower_bound,
                        fill='tonexty',
                        mode='lines',
                        line_color='rgba(0,0,0,0)',
                        name='Confidence Interval',
                        fillcolor='rgba(255,0,0,0.2)'
                    ))
                
                # Add risk level thresholds
                fig_risk.add_hline(y=0.3, line_dash="dot", line_color="green", 
                                  annotation_text="Low Risk Threshold")
                fig_risk.add_hline(y=0.6, line_dash="dot", line_color="orange", 
                                  annotation_text="High Risk Threshold")
                
                # Add vertical line for current date
                # Fix: convert datetime.now() to timestamp for add_vline
                vline_x = datetime.now()
                if isinstance(vline_x, datetime):
                    vline_x = vline_x.timestamp() * 1000  # convert to ms timestamp for plotly
                fig_risk.add_vline(x=vline_x, line_dash="dash", line_color="black",
                                  annotation_text="Today")
                
                fig_risk.update_layout(
                    title='Heart Disease Risk Forecast',
                    xaxis_title='Date',
                    yaxis_title='Risk Score',
                    height=500,
                    yaxis=dict(tickformat='.0%')
                )
                
                st.plotly_chart(fig_risk, use_container_width=True)
            
            with tab2:
                if detailed_breakdown:
                    # Individual metric forecasts
                    metrics_to_plot = ['bp_systolic', 'cholesterol', 'resting_hr', 'stress_level']
                    metric_titles = ['Blood Pressure (Systolic)', 'Cholesterol', 'Resting Heart Rate', 'Stress Level']
                    
                    for i, (metric, title) in enumerate(zip(metrics_to_plot, metric_titles)):
                        if i % 2 == 0:
                            col1, col2 = st.columns(2)
                        
                        with col1 if i % 2 == 0 else col2:
                            fig_metric = go.Figure()
                            
                            # Historical
                            fig_metric.add_trace(go.Scatter(
                                x=historical_data['date'],
                                y=historical_data[metric],
                                mode='lines',
                                name='Historical',
                                line=dict(color='blue')
                            ))
                            
                            # Forecast
                            fig_metric.add_trace(go.Scatter(
                                x=forecast_df['date'],
                                y=forecast_df[metric],
                                mode='lines',
                                name='Forecast',
                                line=dict(color='red', dash='dash')
                            ))
                            
                            fig_metric.add_vline(x=datetime.now(), line_dash="dash", line_color="gray")
                            fig_metric.update_layout(title=title, height=300)
                            st.plotly_chart(fig_metric, use_container_width=True)
            
            with tab3:
                # Timeline view with key events
                st.subheader("📅 Forecast Timeline")
                
                # Identify significant events in forecast
                events = []
                
                # Risk threshold crossings
                for i in range(1, len(forecast_df)):
                    prev_risk = forecast_df['risk_score'].iloc[i-1]
                    curr_risk = forecast_df['risk_score'].iloc[i]
                    date = forecast_df['date'].iloc[i]
                    
                    if prev_risk < 0.3 and curr_risk >= 0.3:
                        events.append({'date': date, 'event': 'Risk increases to MODERATE', 'type': 'warning'})
                    elif prev_risk < 0.6 and curr_risk >= 0.6:
                        events.append({'date': date, 'event': 'Risk increases to HIGH', 'type': 'danger'})
                    elif prev_risk >= 0.6 and curr_risk < 0.6:
                        events.append({'date': date, 'event': 'Risk decreases to MODERATE', 'type': 'improvement'})
                    elif prev_risk >= 0.3 and curr_risk < 0.3:
                        events.append({'date': date, 'event': 'Risk decreases to LOW', 'type': 'improvement'})
                
                # Display events
                if events:
                    for event in events:
                        date_str = event['date'].strftime('%Y-%m-%d')
                        if event['type'] == 'danger':
                            st.error(f"🚨 {date_str}: {event['event']}")
                        elif event['type'] == 'warning':
                            st.warning(f"⚠️ {date_str}: {event['event']}")
                        else:
                            st.success(f"✅ {date_str}: {event['event']}")
                else:
                    st.info("No significant risk level changes predicted in this period.")
                
                # Monthly summary
                st.subheader("📊 Monthly Risk Summary")
                
                # Group forecast by month
                forecast_df['month'] = forecast_df['date'].dt.to_period('M')
                monthly_summary = forecast_df.groupby('month').agg({
                    'risk_score': ['mean', 'max', 'min'],
                    'bp_systolic': 'mean',
                    'cholesterol': 'mean'
                }).round(3)
                
                st.dataframe(monthly_summary, use_container_width=True)
            
            with tab4:
                # Risk events and recommendations
                st.subheader("⚠️ Predicted Risk Events")
                
                high_risk_days = forecast_df[forecast_df['risk_score'] > 0.6]
                moderate_risk_days = forecast_df[(forecast_df['risk_score'] >= 0.3) & (forecast_df['risk_score'] <= 0.6)]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**High Risk Periods:**")
                    if len(high_risk_days) > 0:
                        st.error(f"🚨 {len(high_risk_days)} days with high risk predicted")
                        st.write(f"Peak risk: {high_risk_days['risk_score'].max():.1%}")
                        st.write(f"First occurrence: {high_risk_days['date'].min().strftime('%Y-%m-%d')}")
                    else:
                        st.success("✅ No high-risk periods predicted")
                
                with col2:
                    st.markdown("**Moderate Risk Periods:**")
                    if len(moderate_risk_days) > 0:
                        st.warning(f"⚠️ {len(moderate_risk_days)} days with moderate risk predicted")
                        st.write(f"Average risk: {moderate_risk_days['risk_score'].mean():.1%}")
                    else:
                        st.success("✅ No moderate-risk periods predicted")
                
                # Preventive recommendations
                st.markdown("---")
                st.subheader("💡 Preventive Recommendations")
                
                if avg_forecast_risk > current_risk:
                    st.warning("Your risk is predicted to increase. Consider these preventive measures:")
                    recommendations = [
                        "Increase physical activity to 150+ minutes per week",
                        "Adopt a heart-healthy diet (Mediterranean or DASH)",
                        "Implement stress management techniques",
                        "Monitor blood pressure and cholesterol more frequently",
                        "Schedule a preventive cardiology consultation",
                        "Consider cardiac risk assessment tests"
                    ]
                else:
                    st.success("Your risk is predicted to remain stable or improve. Maintain these habits:")
                    recommendations = [
                        "Continue your current exercise routine",
                        "Maintain your healthy diet",
                        "Keep up with stress management practices",
                        "Continue regular health monitoring",
                        "Stay consistent with preventive care",
                        "Consider gradual improvements where possible"
                    ]
                
                for rec in recommendations:
                    st.write(f"• {rec}")
            
            # Save forecast button
            if st.button("💾 Save Forecast"):
                if 'saved_forecasts' not in st.session_state:
                    st.session_state.saved_forecasts = []
                
                forecast_summary = {
                    'timestamp': datetime.now(),
                    'period': forecast_period,
                    'current_risk': current_risk,
                    'avg_forecast_risk': avg_forecast_risk,
                    'max_forecast_risk': max_forecast_risk,
                    'base_metrics': base_metrics
                }
                
                st.session_state.saved_forecasts.append(forecast_summary)
                st.success("✅ Forecast saved to your history!")
        
        else:
            st.error("❌ Unable to generate forecast. Please check your input data.")

# Sidebar information
with st.sidebar:
    st.header("ℹ️ About Forecasting")
    st.markdown("""
    **How It Works:**
    - Uses LSTM neural networks for time series prediction
    - Analyzes historical health patterns
    - Projects future risk trends
    - Considers lifestyle factors
    
    **Forecast Accuracy:**
    - 3 months: High accuracy
    - 6 months: Moderate accuracy  
    - 1 year: General trends only
    
    **Important Notes:**
    - Predictions are estimates
    - Based on current patterns
    - External factors not included
    - Consult healthcare providers
    """)
    
    st.markdown("---")
    st.header("📈 Forecast History")
    
    if hasattr(st.session_state, 'saved_forecasts') and st.session_state.saved_forecasts:
        for i, forecast in enumerate(st.session_state.saved_forecasts[-3:]):
            st.markdown(f"**{i+1}.** {forecast['period']}")
            st.write(f"Risk trend: {forecast['avg_forecast_risk']:.1%}")
    else:
        st.info("No forecasts saved yet.")
    
    st.markdown("---")
    st.header("🎯 Quick Actions")
    if st.button("📊 View Risk Dashboard"):
        st.switch_page("pages/01_Risk_Prediction.py")
    
    if st.button("🩺 Check Symptoms"):
        st.switch_page("pages/02_Symptom_Checker.py")
