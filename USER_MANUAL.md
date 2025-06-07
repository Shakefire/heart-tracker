# System Functions Overview

This section lists all the main system functions available in the Heart Health Tracker project, along with their descriptions.

## app.py

- **main()**  
  Entry point of the application. Sets up the Streamlit interface, including page configuration, sidebar navigation, main content sections, and model training controls.

## src/utils.py

- **initialize_session_state()**  
  Initialize session state variables used throughout the application.

- **load_custom_css()**  
  Load custom CSS styling for the Streamlit app.

- **create_risk_gauge(risk_probability, risk_level)**  
  Create a risk gauge visualization using Plotly based on risk probability and risk level.

- **get_risk_color(risk_level)**  
  Get the color code corresponding to a given risk level.

- **create_feature_importance_plot(importance_df)**  
  Create a bar plot visualization of feature importances.

- **create_model_comparison_plot(comparison_df)**  
  Create a bar plot comparing model risk probabilities.

- **format_input_data(input_data)**  
  Format raw input data for display, including mapping categorical values to readable strings.

- **validate_input_data(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)**  
  Validate user input data for acceptable ranges and return a list of errors if any.

- **generate_health_tips()**  
  Generate daily health tips, returning a tip based on the current day.

- **calculate_health_score(input_data)**  
  Calculate a simple health score based on input parameters.

- **create_trend_chart(history_data)**  
  Create a line chart showing risk probability trends over time.

- **add_prediction_to_history(prediction_result, input_data)**  
  Add a prediction result to the user's prediction history, maintaining a maximum of 50 entries.

- **get_emergency_contacts()**  
  Return a dictionary of emergency contact information.

- **generate_workout_plan(risk_level)**  
  Generate a workout plan tailored to the user's risk level.

---

This overview helps developers and users understand the key functions that drive the Heart Health Tracker system.
