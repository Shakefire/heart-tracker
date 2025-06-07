import pandas as pd
import numpy as np
from datetime import datetime
import io
import base64
from fpdf import FPDF
import streamlit as st

class ReportGenerator:
    def __init__(self):
        self.report_data = {}
    
    def generate_prediction_report(self, input_data, prediction_result, feature_importance=None, model_comparison=None):
        """Generate comprehensive prediction report"""
        
        # Prepare report data
        self.report_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'input_data': input_data,
            'prediction': prediction_result,
            'feature_importance': feature_importance,
            'model_comparison': model_comparison
        }
        
        return self.report_data
    
    def create_pdf_report(self, report_data):
        """Create PDF report"""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=16)
            
            # Title
            pdf.cell(200, 10, txt="Heart Disease Risk Assessment Report", ln=True, align='C')
            pdf.ln(10)
            
            # Timestamp
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, txt=f"Generated on: {report_data['timestamp']}", ln=True)
            pdf.ln(5)
            
            # Prediction Results
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt="Risk Assessment Results", ln=True)
            pdf.ln(5)
            
            pdf.set_font("Arial", size=12)
            prediction = report_data['prediction']
            pdf.cell(200, 10, txt=f"Risk Level: {prediction['risk_level']}", ln=True)
            pdf.cell(200, 10, txt=f"Risk Probability: {prediction['risk_probability']:.3f}", ln=True)
            pdf.cell(200, 10, txt=f"Model Used: {prediction['model_used']}", ln=True)
            pdf.ln(10)
            
            # Input Summary
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt="Input Data Summary", ln=True)
            pdf.ln(5)
            
            pdf.set_font("Arial", size=10)
            feature_names = [
                'Age', 'Sex', 'Chest Pain Type', 'Resting BP', 'Cholesterol',
                'Fasting Blood Sugar', 'Resting ECG', 'Max Heart Rate',
                'Exercise Angina', 'ST Depression', 'Slope', 'Major Vessels', 'Thalassemia'
            ]
            
            for i, (name, value) in enumerate(zip(feature_names, report_data['input_data'])):
                pdf.cell(200, 8, txt=f"{name}: {value}", ln=True)
            
            pdf.ln(10)
            
            # Recommendations
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt="Health Recommendations", ln=True)
            pdf.ln(5)
            
            pdf.set_font("Arial", size=10)
            recommendations = self._generate_recommendations(prediction['risk_level'])
            
            for rec in recommendations:
                pdf.cell(200, 8, txt=f"• {rec}", ln=True)
            
            # Save to bytes
            pdf_output = io.BytesIO()
            pdf_string = pdf.output(dest='S').encode('latin-1')
            pdf_output.write(pdf_string)
            pdf_output.seek(0)
            
            return pdf_output
            
        except Exception as e:
            st.error(f"Error generating PDF report: {str(e)}")
            return None
    
    def create_csv_report(self, report_data):
        """Create CSV report with detailed data"""
        try:
            # Prepare CSV data
            csv_data = []
            
            # Basic information
            csv_data.append(['Report Type', 'Heart Disease Risk Assessment'])
            csv_data.append(['Generated On', report_data['timestamp']])
            csv_data.append(['', ''])
            
            # Prediction results
            prediction = report_data['prediction']
            csv_data.append(['Prediction Results', ''])
            csv_data.append(['Risk Level', prediction['risk_level']])
            csv_data.append(['Risk Probability', f"{prediction['risk_probability']:.6f}"])
            csv_data.append(['Risk Class', prediction['risk_class']])
            csv_data.append(['Model Used', prediction['model_used']])
            csv_data.append(['', ''])
            
            # Input data
            csv_data.append(['Input Features', 'Values'])
            feature_names = [
                'Age', 'Sex', 'Chest Pain Type', 'Resting BP', 'Cholesterol',
                'Fasting Blood Sugar', 'Resting ECG', 'Max Heart Rate',
                'Exercise Angina', 'ST Depression', 'Slope', 'Major Vessels', 'Thalassemia'
            ]
            
            for name, value in zip(feature_names, report_data['input_data']):
                csv_data.append([name, value])
            
            csv_data.append(['', ''])
            
            # Feature importance if available
            if report_data.get('feature_importance') is not None:
                csv_data.append(['Feature Importance', ''])
                csv_data.append(['Feature', 'Importance Score'])
                for _, row in report_data['feature_importance'].iterrows():
                    csv_data.append([row['Feature'], f"{row['Importance']:.6f}"])
                csv_data.append(['', ''])
            
            # Model comparison if available
            if report_data.get('model_comparison') is not None:
                csv_data.append(['Model Comparison', ''])
                csv_data.append(['Model', 'Risk Level', 'Risk Probability'])
                for _, row in report_data['model_comparison'].iterrows():
                    csv_data.append([row['Model'], row['Risk Level'], f"{row['Risk Probability']:.6f}"])
                csv_data.append(['', ''])
            
            # Recommendations
            csv_data.append(['Recommendations', ''])
            recommendations = self._generate_recommendations(prediction['risk_level'])
            for i, rec in enumerate(recommendations, 1):
                csv_data.append([f'Recommendation {i}', rec])
            
            # Convert to DataFrame and then to CSV
            df = pd.DataFrame(csv_data)
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, header=False)
            csv_buffer.seek(0)
            
            return csv_buffer
            
        except Exception as e:
            st.error(f"Error generating CSV report: {str(e)}")
            return None
    
    def _generate_recommendations(self, risk_level):
        """Generate health recommendations based on risk level"""
        base_recommendations = [
            "Maintain a healthy, balanced diet rich in fruits and vegetables",
            "Engage in regular physical activity (at least 150 minutes per week)",
            "Avoid smoking and limit alcohol consumption",
            "Monitor blood pressure and cholesterol levels regularly",
            "Manage stress through relaxation techniques or meditation",
            "Get adequate sleep (7-9 hours per night)",
            "Schedule regular check-ups with your healthcare provider"
        ]
        
        if risk_level == "Low":
            specific_recommendations = [
                "Continue your current healthy lifestyle habits",
                "Consider preventive measures to maintain heart health",
                "Stay informed about heart disease prevention"
            ]
        elif risk_level == "Medium":
            specific_recommendations = [
                "Consider consulting with a cardiologist for detailed evaluation",
                "Focus on dietary modifications to reduce cholesterol and blood pressure",
                "Increase physical activity intensity with medical supervision",
                "Monitor symptoms and seek immediate care if they worsen"
            ]
        else:  # High risk
            specific_recommendations = [
                "URGENT: Consult with a cardiologist immediately",
                "Consider cardiac screening tests (ECG, stress test, echocardiogram)",
                "Discuss medication options with your healthcare provider",
                "Implement strict dietary and lifestyle modifications",
                "Monitor symptoms closely and seek emergency care for chest pain or shortness of breath"
            ]
        
        return base_recommendations + specific_recommendations
    
    def get_download_link(self, file_buffer, filename, file_type):
        """Generate download link for reports"""
        try:
            if file_type == 'pdf':
                b64 = base64.b64encode(file_buffer.read()).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download PDF Report</a>'
            elif file_type == 'csv':
                b64 = base64.b64encode(file_buffer.getvalue().encode()).decode()
                href = f'<a href="data:text/csv;base64,{b64}" download="{filename}">Download CSV Report</a>'
            else:
                return None
            
            return href
            
        except Exception as e:
            st.error(f"Error creating download link: {str(e)}")
            return None
    
    def display_report_summary(self, report_data):
        """Display report summary in Streamlit"""
        st.subheader("📋 Report Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Risk Level", report_data['prediction']['risk_level'])
            st.metric("Risk Probability", f"{report_data['prediction']['risk_probability']:.3f}")
        
        with col2:
            st.metric("Model Used", report_data['prediction']['model_used'])
            st.metric("Report Generated", report_data['timestamp'])
        
        # Recommendations
        st.subheader("💡 Key Recommendations")
        recommendations = self._generate_recommendations(report_data['prediction']['risk_level'])
        
        for rec in recommendations[:5]:  # Show top 5 recommendations
            st.write(f"• {rec}")
