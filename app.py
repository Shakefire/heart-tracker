import streamlit as st
import pandas as pd
import numpy as np
from src.utils import initialize_session_state, load_custom_css
from src.data_preprocessor import DataPreprocessor
from src.model_trainer import ModelTrainer
import os

# Page configuration
st.set_page_config(
    page_title="Heart Disease Risk Prediction",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Main app
def main():
    st.title("❤️ Heart Disease Risk Prediction & Health Support")
    st.markdown("---")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        st.markdown("Use the pages in the sidebar to navigate through different features:")
        st.markdown("- **Risk Prediction**: Get your heart disease risk assessment")
        st.markdown("- **Symptom Checker**: Check your symptoms")
        st.markdown("- **Educational Hub**: Learn about heart health")
        st.markdown("- **Digital Twin**: Simulate heart health scenarios")
        st.markdown("- **Event Forecasting**: Predict future health trends")
        st.markdown("- **Recommendations**: Get personalized health advice")
        st.markdown("- **Emergency SOS**: Emergency assistance")
        st.markdown("- **Community**: Connect with others")
    
    # Main content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🔍 Risk Assessment")
        st.write("Advanced machine learning models to predict heart disease risk using clinical data.")
        if st.button("Start Risk Prediction", key="risk_pred"):
            st.switch_page("pages/01_Risk_Prediction.py")
    
    with col2:
        st.subheader("🩺 Health Monitoring")
        st.write("Comprehensive health monitoring tools including symptom checker and health forecasting.")
        if st.button("Check Symptoms", key="symptom_check"):
            st.switch_page("pages/02_Symptom_Checker.py")
    
    with col3:
        st.subheader("📚 Education & Support")
        st.write("Learn about heart health, get personalized recommendations, and connect with community.")
        if st.button("Learn More", key="education"):
            st.switch_page("pages/03_Educational_Hub.py")
    
    st.markdown("---")
    
    # App overview
    st.subheader("🎯 Application Features")
    
    features = [
        "**Multi-Model ML Pipeline**: CNN, LSTM, CNN-LSTM, and Deep Neural Networks",
        "**Model Interpretability**: LIME-powered feature importance analysis",
        "**Comprehensive Health Tools**: Risk prediction, symptom checking, and health forecasting",
        "**Personalized Recommendations**: AI-driven lifestyle and health suggestions",
        "**Educational Resources**: Curated content for heart health awareness",
        "**Emergency Support**: Quick access to emergency services",
        "**Community Features**: Social health goals and gamification",
        "**Report Generation**: Downloadable PDF and CSV reports"
    ]
    
    for feature in features:
        st.markdown(f"✅ {feature}")
    
    st.markdown("---")
    
    # Model training section
    st.subheader("🤖 Model Training Status")
    
    if st.button("Initialize/Train Models", key="train_models"):
        with st.spinner("Training models... This may take a few minutes."):
            try:
                # Initialize data preprocessor
                preprocessor = DataPreprocessor()
                
                # Load and preprocess data
                X_train, X_test, y_train, y_test = preprocessor.load_and_preprocess_data()
                
                # Initialize model trainer
                trainer = ModelTrainer()
                
                # Train models
                models, results = trainer.train_all_models(X_train, y_train, X_test, y_test)
                
                # Store in session state
                st.session_state.models = models
                st.session_state.model_results = results
                st.session_state.preprocessor = preprocessor
                
                st.success("✅ All models trained successfully!")
                
                # Display results
                st.subheader("Model Performance")
                results_df = pd.DataFrame(results).T
                st.dataframe(results_df, use_container_width=True)
                
                # Best model
                best_model = max(results.keys(), key=lambda x: results[x]['accuracy'])
                st.info(f"🏆 Best performing model: **{best_model}** (Accuracy: {results[best_model]['accuracy']:.3f})")
                
            except Exception as e:
                st.error(f"❌ Error during model training: {str(e)}")
                st.error("Please ensure you have the required data files and dependencies installed.")
    
    # Display current model status
    if hasattr(st.session_state, 'models') and st.session_state.models:
        st.success("🎉 Models are ready for prediction!")
        
        # Show model performance summary
        if hasattr(st.session_state, 'model_results'):
            st.subheader("Current Model Performance")
            results_df = pd.DataFrame(st.session_state.model_results).T
            st.dataframe(results_df, use_container_width=True)
    else:
        st.warning("⚠️ Models not trained yet. Please click 'Initialize/Train Models' to get started.")
    
    st.markdown("---")
    st.markdown("**Note**: This application uses the Cleveland Heart Disease Dataset and implements state-of-the-art deep learning models for accurate risk prediction.")

if __name__ == "__main__":
    main()
