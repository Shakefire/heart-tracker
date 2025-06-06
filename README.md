# Heart Health Tracker User Manual

## Overview
Heart Health Tracker is a comprehensive application designed to help users assess, monitor, and improve their heart health through advanced AI models, simulations, and educational resources. The system includes multiple modules:

- Risk Prediction
- Symptom Checker
- Educational Hub
- Digital Twin Heart Simulation
- Event Forecasting
- Recommendations
- Emergency SOS

This manual provides detailed instructions on how to use each module, interpret results, and utilize the system effectively.

---

## 1. Getting Started

### Accessing the Application
The application can be accessed via the main interface. Ensure that all models are trained and loaded before using prediction or forecasting features.

### Navigation
Use the sidebar or main menu to navigate between modules:
- Risk Prediction
- Symptom Checker
- Educational Hub
- Digital Twin
- Event Forecasting
- Recommendations
- Emergency SOS

---

## 2. Risk Prediction Module

### Purpose
Predict your heart disease risk using AI models based on your health data.

### Input Data
Enter your health information in the provided form:
- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate
- Exercise Induced Angina
- ST Depression
- Slope of Peak Exercise ST Segment
- Number of Major Vessels
- Thalassemia

### Model Selection
Choose from available models (CNN, LSTM, CNN-LSTM, DNN) or use the Ensemble model for combined predictions.

### Prediction
Click "Predict Risk" to generate risk assessment results including:
- Risk Level (Low, Medium, High)
- Risk Probability
- Model Used

### Feature Importance
Optionally, view feature importance analysis using LIME explanations to understand key factors influencing your risk.

### Model Comparison
Compare predictions across all models to see differences in risk assessments.

### Report Generation
Generate and download detailed PDF or CSV reports summarizing your input data, prediction results, feature importance, and model comparisons.

---

## 3. Symptom Checker Module

### Purpose
Evaluate your symptoms to identify potential heart-related issues.

### Usage
Enter your symptoms and receive guidance on possible conditions and recommended actions.

---

## 4. Educational Hub

### Purpose
Access educational materials about heart health, disease prevention, and lifestyle tips.

### Usage
Browse articles, videos, and resources to increase your knowledge and awareness.

---

## 5. Digital Twin Heart Simulation

### Purpose
Simulate how lifestyle changes and medical interventions might affect your heart health over time.

### Setup
Provide baseline profile data including age, gender, height, weight, BMI, and current health metrics.

### Lifestyle and Medical Interventions
Adjust parameters such as diet improvement, exercise increase, stress reduction, and medication usage.

### Simulation
Run the simulation to see projected changes in risk score, blood pressure, cholesterol, cardiovascular age, and other metrics over the selected period.

### Visualization
View interactive charts showing risk trends, vital signs, fitness metrics, and BMI over time.

### Save Simulation
Save your simulation results for future reference.

---

## 6. Event Forecasting

### Purpose
Forecast your heart health risk trends over the next 3-12 months using time-aware deep learning models.

### Input
Provide current health profile data and lifestyle factors.

### Forecast Parameters
Select forecast period and choose whether to include planned interventions.

### Results
View forecasted risk scores, trends, and detailed metric forecasts.

### Visualization
Interactive charts display risk trends, timeline views, and predicted risk events.

### Save Forecast
Save your forecast results for later review.

---

## 7. Recommendations

### Purpose
Receive personalized health recommendations based on your risk assessments and simulations.

### Usage
Review actionable advice to improve your heart health and reduce risk.

---

## 8. Emergency SOS

### Purpose
Quickly access emergency services and guidance in case of heart-related emergencies.

### Usage
Use the SOS feature to contact emergency responders or follow recommended steps.

---

## 9. Additional Features

### Prediction History
View recent predictions and forecasts in the sidebar for quick access.

### Input Validation
Ensure all input data is accurate and within valid ranges to get reliable results.

### User Interface
The app provides an intuitive and responsive interface with clear instructions and feedback.

---

## Troubleshooting

- **Module Import Errors:** Ensure all required Python packages are installed in your environment.
- **Prediction Errors:** Verify input data and model availability.
- **Report Generation Issues:** Use the provided buttons to generate and download reports; check for any error messages.
- **Simulation or Forecasting Errors:** Confirm input parameters and try again; report issues if persistent.

---

## Support

For further assistance, please contact the development team or consult the documentation repository.

---

*End of User Manual*
