import streamlit as st
import numpy as np
import lime
import lime.lime_tabular
import pandas as pd
from src.predictor import HeartDiseasePredictor
from src.report_generator import ReportGenerator
from src.utils import (
    create_risk_gauge, create_feature_importance_plot, create_model_comparison_plot,
    format_input_data, validate_input_data, add_prediction_to_history
)

st.set_page_config(page_title="Risk Prediction", page_icon="🔍", layout="wide")

st.title("🔍 Heart Disease Risk Prediction")
st.markdown(
    "Get an accurate assessment of your heart disease risk using advanced AI models.")

# Check if models are loaded
if not hasattr(st.session_state, 'models') or st.session_state.models is None:
    st.error(
        "⚠️ Models not loaded! Please go to the main page and train the models first.")
    if st.button("Go to Main Page"):
        st.switch_page("app.py")
    st.stop()

# Initialize predictor
predictor = HeartDiseasePredictor(
    st.session_state.models, st.session_state.preprocessor)
report_generator = ReportGenerator()

st.markdown("---")

# Input form
st.subheader("📝 Enter Your Health Information")

with st.form("risk_prediction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", min_value=20, max_value=120,
                              value=50, help="Your age in years")
        sex = st.selectbox("Sex", options=[
                           0, 1], format_func=lambda x: "Female" if x == 0 else "Male", help="Biological sex")
        cp = st.selectbox("Chest Pain Type", options=[0, 1, 2, 3],
                          format_func=lambda x: [
                              "Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"][x],
                          help="Type of chest pain experienced")
        trestbps = st.number_input("Resting Blood Pressure", min_value=70, max_value=250, value=120,
                                   help="Resting blood pressure in mmHg")
        chol = st.number_input("Cholesterol", min_value=100, max_value=600, value=200,
                               help="Serum cholesterol in mg/dL")

    with col2:
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", options=[0, 1],
                           format_func=lambda x: "No" if x == 0 else "Yes",
                           help="Is fasting blood sugar greater than 120 mg/dL?")
        restecg = st.selectbox("Resting ECG", options=[0, 1, 2],
                               format_func=lambda x: [
                                   "Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"][x],
                               help="Resting electrocardiographic results")
        thalach = st.number_input("Maximum Heart Rate", min_value=60, max_value=220, value=150,
                                  help="Maximum heart rate achieved during exercise")
        exang = st.selectbox("Exercise Induced Angina", options=[0, 1],
                             format_func=lambda x: "No" if x == 0 else "Yes",
                             help="Exercise induced angina")
        oldpeak = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=1.0, step=0.1,
                                  help="ST depression induced by exercise relative to rest")

    with col3:
        slope = st.selectbox("Slope of Peak Exercise ST Segment", options=[0, 1, 2],
                             format_func=lambda x: [
                                 "Upsloping", "Flat", "Downsloping"][x],
                             help="Slope of the peak exercise ST segment")
        ca = st.selectbox("Number of Major Vessels", options=[0, 1, 2, 3],
                          help="Number of major vessels colored by fluoroscopy (0-3)")
        thal = st.selectbox("Thalassemia", options=[0, 1, 2, 3],
                            format_func=lambda x: [
                                "Normal", "Fixed Defect", "Reversible Defect", "Not Described"][x],
                            help="Thalassemia type")

    # Model selection
    st.subheader("🤖 Model Selection")
    available_models = list(st.session_state.models.keys())
    selected_model = st.selectbox("Choose Model", options=available_models + ["Ensemble"],
                                  help="Select which model to use for prediction")

    show_explanation = st.checkbox("Show Feature Importance Analysis", value=True,
                                   help="Generate LIME explanation for the prediction")
    show_comparison = st.checkbox("Compare All Models", value=False,
                                  help="Show predictions from all available models")

    submitted = st.form_submit_button("🔍 Predict Risk", type="primary")

if submitted:
    # Validate input
    input_data = [age, sex, cp, trestbps, chol, fbs,
                  restecg, thalach, exang, oldpeak, slope, ca, thal]
    errors = validate_input_data(*input_data)

    if errors:
        st.error("❌ Please correct the following errors:")
        for error in errors:
            st.error(f"• {error}")
    else:
        with st.spinner("Analyzing your data..."):
            # Make prediction
            if selected_model == "Ensemble":
                prediction_result = predictor.get_ensemble_prediction(
                    input_data)
            else:
                prediction_result = predictor.predict_risk(
                    input_data, selected_model)

            if prediction_result:
                # Add to history
                add_prediction_to_history(prediction_result, input_data)

                # Display results
                st.markdown("---")
                st.subheader("📊 Risk Assessment Results")

                col1, col2 = st.columns([1, 2])

                with col1:
                    # Risk gauge
                    risk_gauge = create_risk_gauge(
                        prediction_result['risk_probability'], prediction_result['risk_level'])
                    st.plotly_chart(risk_gauge, use_container_width=True)

                with col2:
                    # Risk metrics
                    st.markdown(f"""
                    <div class="metric-card risk-{prediction_result['risk_level'].lower()}">
                        <h3>Risk Assessment</h3>
                        <p><strong>Risk Level:</strong> {prediction_result['risk_level']}</p>
                        <p><strong>Risk Probability:</strong> {prediction_result['risk_probability']:.1%}</p>
                        <p><strong>Model Used:</strong> {prediction_result['model_used']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Risk interpretation
                    if prediction_result['risk_level'] == "Low":
                        st.success(
                            "✅ Your risk of heart disease appears to be low. Continue maintaining a healthy lifestyle!")
                    elif prediction_result['risk_level'] == "Medium":
                        st.warning(
                            "⚠️ You have a moderate risk of heart disease. Consider lifestyle modifications and consult your doctor.")
                    else:
                        st.error(
                            "🚨 You have a high risk of heart disease. Please consult with a healthcare professional immediately.")

                # Feature importance analysis
                if show_explanation:
                    st.markdown("---")
                    st.subheader("🔍 Feature Importance Analysis")

                    with st.spinner("Generating explanation..."):
                        explanation = predictor.explain_prediction(
                            input_data, selected_model if selected_model != "Ensemble" else "DNN")

                        if explanation:
                            importance_df = predictor.get_feature_importance(
                                explanation)

                            if importance_df is not None:
                                col1, col2 = st.columns(2)

                                with col1:
                                    # Feature importance plot
                                    importance_plot = create_feature_importance_plot(
                                        importance_df)
                                    if importance_plot:
                                        st.plotly_chart(
                                            importance_plot, use_container_width=True)

                                with col2:
                                    # Feature importance table
                                    st.subheader("Top Contributing Factors")
                                    st.dataframe(importance_df.head(
                                        10), use_container_width=True)
                        else:
                            st.info(
                                "Feature importance analysis is not available for this prediction.")

                # Model comparison
                if show_comparison:
                    st.markdown("---")
                    st.subheader("🤖 Model Comparison")

                    comparison_df = predictor.get_model_comparison(input_data)

                    if comparison_df is not None:
                        col1, col2 = st.columns(2)

                        with col1:
                            comparison_plot = create_model_comparison_plot(
                                comparison_df)
                            if comparison_plot:
                                st.plotly_chart(
                                    comparison_plot, use_container_width=True)

                        with col2:
                            st.dataframe(
                                comparison_df, use_container_width=True)

                # Report generation
                st.markdown("---")
                st.subheader("📄 Generate Report")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("📄 Generate PDF Report", type="secondary"):
                        with st.spinner("Generating PDF report..."):
                            # Prepare report data
                            feature_importance = predictor.get_feature_importance(
                                explanation) if show_explanation and explanation else None
                            model_comparison = comparison_df if show_comparison else None

                            report_data = report_generator.generate_prediction_report(
                                input_data, prediction_result, feature_importance, model_comparison
                            )

                            # Generate PDF
                            pdf_buffer = report_generator.create_pdf_report(
                                report_data)

                            if pdf_buffer:
                                st.download_button(
                                    label="📥 Download PDF Report",
                                    data=pdf_buffer.read(),
                                    file_name=f"heart_risk_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                    mime="application/pdf"
                                )

                with col2:
                    if st.button("📊 Generate CSV Report", type="secondary"):
                        with st.spinner("Generating CSV report..."):
                            # Prepare report data
                            feature_importance = predictor.get_feature_importance(
                                explanation) if show_explanation and explanation else None
                            model_comparison = comparison_df if show_comparison else None

                            report_data = report_generator.generate_prediction_report(
                                input_data, prediction_result, feature_importance, model_comparison
                            )

                            # Generate CSV
                            csv_buffer = report_generator.create_csv_report(
                                report_data)

                            if csv_buffer:
                                st.download_button(
                                    label="📥 Download CSV Report",
                                    data=csv_buffer.getvalue(),
                                    file_name=f"heart_risk_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv"
                                )

                # Display report summary
                feature_importance = predictor.get_feature_importance(
                    explanation) if show_explanation and explanation else None
                model_comparison = comparison_df if show_comparison else None

                report_data = report_generator.generate_prediction_report(
                    input_data, prediction_result, feature_importance, model_comparison
                )
                report_generator.display_report_summary(report_data)

            else:
                st.error("❌ Error occurred during prediction. Please try again.")

# Sidebar information
with st.sidebar:
    st.header("ℹ️ Information")
    st.markdown("""
    **Risk Levels:**
    - 🟢 **Low Risk (< 30%)**: Continue healthy habits
    - 🟡 **Medium Risk (30-70%)**: Consider lifestyle changes
    - 🔴 **High Risk (> 70%)**: Consult healthcare provider
    
    **Model Types:**
    - **CNN**: Convolutional Neural Network
    - **LSTM**: Long Short-Term Memory
    - **CNN-LSTM**: Hybrid model
    - **DNN**: Deep Neural Network
    - **Ensemble**: Average of all models
    """)

    if hasattr(st.session_state, 'prediction_history') and st.session_state.prediction_history:
        st.markdown("---")
        st.subheader("📈 Recent Predictions")
        for i, pred in enumerate(st.session_state.prediction_history[-3:]):
            st.markdown(
                f"**{i+1}.** {pred['risk_level']} ({pred['risk_probability']:.1%})")
