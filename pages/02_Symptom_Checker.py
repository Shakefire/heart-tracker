import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Symptom Checker", page_icon="🩺", layout="wide")

st.title("🩺 Heart Health Symptom Checker")
st.markdown("Check your symptoms and get preliminary health guidance. **This is not a substitute for professional medical advice.**")

st.markdown("---")

# Symptom categories
st.subheader("💡 How to Use This Tool")
st.info("""
1. Select the symptoms you're currently experiencing
2. Rate their severity and frequency
3. Get preliminary guidance based on your responses
4. **Always consult a healthcare professional for proper diagnosis**
""")

st.markdown("---")

# Symptom checker form
st.subheader("📋 Symptom Assessment")

with st.form("symptom_checker_form"):
    st.markdown("### 🫀 Chest-Related Symptoms")
    col1, col2 = st.columns(2)

    with col1:
        chest_pain = st.selectbox("Chest Pain",
                                  options=["None", "Mild",
                                           "Moderate", "Severe"],
                                  help="Any discomfort, pressure, or pain in chest area")
        chest_pain_type = st.multiselect("Type of Chest Pain (if any)",
                                         options=["Sharp", "Dull", "Burning", "Pressure", "Squeezing", "Stabbing"])
        chest_tightness = st.selectbox("Chest Tightness",
                                       options=["None", "Mild", "Moderate", "Severe"])

    with col2:
        pain_radiation = st.multiselect("Pain Radiates To",
                                        options=["Left arm", "Right arm", "Both arms", "Neck", "Jaw", "Back", "Shoulder"])
        pain_triggers = st.multiselect("Pain Triggered By",
                                       options=["Physical activity", "Stress", "Cold weather", "After meals", "At rest"])
        pain_duration = st.selectbox("Pain Duration",
                                     options=["None", "Seconds", "Minutes", "Hours", "Days"])

    st.markdown("### 🫁 Breathing-Related Symptoms")
    col1, col2 = st.columns(2)

    with col1:
        shortness_breath = st.selectbox("Shortness of Breath",
                                        options=["None", "Mild", "Moderate", "Severe"])
        breath_triggers = st.multiselect("Shortness of Breath Occurs",
                                         options=["At rest", "With light activity", "With moderate activity", "With vigorous activity", "When lying down"])

    with col2:
        wheezing = st.selectbox("Wheezing", options=["No", "Yes"])
        coughing = st.selectbox("Persistent Cough", options=["No", "Yes"])
        cough_blood = st.selectbox("Coughing Blood", options=["No", "Yes"])

    st.markdown("### 💓 Heart Rhythm Symptoms")
    col1, col2 = st.columns(2)

    with col1:
        palpitations = st.selectbox("Heart Palpitations",
                                    options=["None", "Occasional", "Frequent", "Constant"])
        rapid_heartbeat = st.selectbox("Rapid Heartbeat",
                                       options=["None", "Occasional", "Frequent", "Constant"])

    with col2:
        irregular_heartbeat = st.selectbox("Irregular Heartbeat",
                                           options=["None", "Occasional", "Frequent", "Constant"])
        heart_skipping = st.selectbox("Heart Skipping Beats",
                                      options=["None", "Occasional", "Frequent", "Constant"])

    st.markdown("### 🩸 Circulation Symptoms")
    col1, col2 = st.columns(2)

    with col1:
        swelling = st.multiselect("Swelling In",
                                  options=["Feet", "Ankles", "Legs", "Hands", "Face", "Abdomen"])
        cold_extremities = st.selectbox("Cold Hands/Feet",
                                        options=["No", "Occasionally", "Frequently", "Always"])

    with col2:
        leg_pain_walking = st.selectbox("Leg Pain When Walking",
                                        options=["None", "Mild", "Moderate", "Severe"])
        blue_lips_fingers = st.selectbox("Blue Lips or Fingertips",
                                         options=["No", "Yes"])

    st.markdown("### 🧠 General Symptoms")
    col1, col2 = st.columns(2)

    with col1:
        dizziness = st.selectbox("Dizziness",
                                 options=["None", "Mild", "Moderate", "Severe"])
        fainting = st.selectbox("Fainting/Near Fainting",
                                options=["No", "Once", "Multiple times"])
        fatigue = st.selectbox("Unusual Fatigue",
                               options=["None", "Mild", "Moderate", "Severe"])

    with col2:
        nausea = st.selectbox("Nausea", options=["No", "Yes"])
        sweating = st.selectbox("Unexplained Sweating",
                                options=["No", "Mild", "Moderate", "Severe"])
        sleep_issues = st.selectbox("Difficulty Sleeping Due to Breathing",
                                    options=["No", "Occasionally", "Frequently", "Always"])

    st.markdown("### ⏰ Timing and Context")
    col1, col2 = st.columns(2)

    with col1:
        symptom_onset = st.selectbox("When Did Symptoms Start?",
                                     options=["Just now", "Today", "This week", "This month", "Longer ago"])
        symptom_frequency = st.selectbox("How Often Do You Experience These Symptoms?",
                                         options=["First time", "Rarely", "Sometimes", "Often", "Daily"])

    with col2:
        symptom_progression = st.selectbox("Are Symptoms Getting:",
                                           options=["Better", "Worse", "Same", "Fluctuating"])
        current_medications = st.text_area("Current Medications (optional)",
                                           help="List any medications you're currently taking")

    submitted = st.form_submit_button("🔍 Analyze Symptoms", type="primary")

if submitted:
    # Calculate risk score based on symptoms
    risk_score = 0
    emergency_symptoms = []
    concerning_symptoms = []

    # High-risk symptoms
    if chest_pain in ["Moderate", "Severe"]:
        risk_score += 3
        concerning_symptoms.append("Significant chest pain")

    if "Pressure" in chest_pain_type or "Squeezing" in chest_pain_type:
        risk_score += 2
        concerning_symptoms.append("Pressure-type chest pain")

    if shortness_breath in ["Moderate", "Severe"]:
        risk_score += 2
        concerning_symptoms.append("Significant shortness of breath")

    if cough_blood == "Yes":
        risk_score += 4
        emergency_symptoms.append("Coughing blood")

    if blue_lips_fingers == "Yes":
        risk_score += 4
        emergency_symptoms.append("Blue lips or fingertips")

    if fainting in ["Once", "Multiple times"]:
        risk_score += 3
        concerning_symptoms.append("Fainting episodes")

    if palpitations in ["Frequent", "Constant"]:
        risk_score += 2
        concerning_symptoms.append("Frequent heart palpitations")

    if "Left arm" in pain_radiation:
        risk_score += 2
        concerning_symptoms.append("Pain radiating to left arm")

    if swelling and len(swelling) >= 2:
        risk_score += 2
        concerning_symptoms.append("Multiple areas of swelling")

    # Display results
    st.markdown("---")
    st.subheader("📊 Symptom Analysis Results")

    # Emergency alert
    if emergency_symptoms or risk_score >= 8:
        st.error("🚨 **URGENT - SEEK EMERGENCY CARE IMMEDIATELY**")
        st.error(
            "Your symptoms may indicate a serious medical emergency. Call 112 or go to the nearest emergency room.")

        if emergency_symptoms:
            st.error("**Critical symptoms detected:**")
            for symptom in emergency_symptoms:
                st.error(f"• {symptom}")

    elif risk_score >= 5:
        st.warning(
            "⚠️ **CONCERNING SYMPTOMS - CONSULT HEALTHCARE PROVIDER TODAY**")
        st.warning(
            "Your symptoms warrant prompt medical evaluation. Contact your doctor or visit urgent care.")

        if concerning_symptoms:
            st.warning("**Concerning symptoms:**")
            for symptom in concerning_symptoms:
                st.warning(f"• {symptom}")

    elif risk_score >= 2:
        st.info("ℹ️ **MILD CONCERN - SCHEDULE DOCTOR VISIT SOON**")
        st.info(
            "While not immediately urgent, these symptoms should be evaluated by a healthcare provider.")

    else:
        st.success("✅ **LOW CONCERN - MONITOR SYMPTOMS**")
        st.success(
            "Your symptoms appear to be of low concern, but continue to monitor them.")

    # Detailed recommendations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏥 Immediate Actions")

        if risk_score >= 8:
            st.markdown("""
            - **Call 112 immediately**
            - **Do not drive yourself**
            - **Chew aspirin if not allergic**
            - **Stay calm and rest**
            """)
        elif risk_score >= 5:
            st.markdown("""
            - **Contact your doctor today**
            - **Consider urgent care visit**
            - **Avoid strenuous activity**
            - **Monitor symptoms closely**
            """)
        else:
            st.markdown("""
            - **Schedule routine check-up**
            - **Keep symptom diary**
            - **Maintain healthy lifestyle**
            - **Follow up if symptoms worsen**
            """)

    with col2:
        st.subheader("📝 General Recommendations")
        st.markdown("""
        - **Rest and avoid overexertion**
        - **Stay hydrated**
        - **Avoid smoking and alcohol**
        - **Take prescribed medications**
        - **Monitor blood pressure**
        - **Eat heart-healthy foods**
        - **Get adequate sleep**
        - **Manage stress levels**
        """)

    # When to seek immediate care
    st.markdown("---")
    st.subheader("🚨 When to Call 112")
    st.error("""
    **Call emergency services immediately if you experience:**
    - Severe chest pain or pressure
    - Shortness of breath with chest pain
    - Pain radiating to arm, neck, or jaw
    - Sudden severe headache
    - Loss of consciousness or fainting
    - Coughing up blood
    - Blue lips or fingertips
    - Severe difficulty breathing
    """)

    # Disclaimer
    st.markdown("---")
    st.warning("""
    **⚠️ Important Disclaimer:**
    This symptom checker is for informational purposes only and does not replace professional medical advice, 
    diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns. 
    In case of emergency, call 112 immediately.
    """)

    # Save symptom report
    if st.button("💾 Save Symptom Report"):
        symptom_report = {
            'timestamp': datetime.now(),
            'risk_score': risk_score,
            'emergency_symptoms': emergency_symptoms,
            'concerning_symptoms': concerning_symptoms,
            'chest_pain': chest_pain,
            'shortness_breath': shortness_breath,
            'palpitations': palpitations
        }

        if 'symptom_history' not in st.session_state:
            st.session_state.symptom_history = []

        st.session_state.symptom_history.append(symptom_report)
        st.success("✅ Symptom report saved to your history!")

# Sidebar information
with st.sidebar:
    st.header("ℹ️ Emergency Contacts")
    st.markdown("""
    **Emergency Services:** 112
    
    **Poison Control:** 1-800-222-1222
    
    **Crisis Text Line:** Text HOME to 741741
    
    **American Heart Association:** 1-800-AHA-USA1
    """)

    st.markdown("---")
    st.header("📱 Heart Attack Warning Signs")
    st.markdown("""
    - Chest discomfort
    - Discomfort in arms, back, neck, jaw
    - Shortness of breath
    - Cold sweat, nausea, lightheadedness
    """)

    if hasattr(st.session_state, 'symptom_history') and st.session_state.symptom_history:
        st.markdown("---")
        st.subheader("📈 Recent Assessments")
        for i, report in enumerate(st.session_state.symptom_history[-3:]):
            st.markdown(f"**{i+1}.** Risk Score: {report['risk_score']}")
