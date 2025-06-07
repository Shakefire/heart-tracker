import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="Emergency SOS", page_icon="🚨", layout="wide")

st.title("🚨 Emergency SOS")
st.markdown(
    "Quick access to emergency assistance and critical health information.")

# Emergency alert banner
st.error("""
🚨 **MEDICAL EMERGENCY?**
**Call 112 immediately** if you're experiencing:
- Severe chest pain or pressure
- Difficulty breathing
- Loss of consciousness
- Severe bleeding
- Signs of stroke (facial drooping, arm weakness, speech difficulty)
""")

st.markdown("---")

# Emergency contacts section
st.subheader("🏥 Health & Emergency Services in Biu, Borno State, Nigeria")

st.markdown("### 🔹 1. Abbott Health Clinic, Zarawuyaku")
st.markdown("""
* **Type:** Private Primary Health Care Centre
* **Services:** General surgery, obstetrics, antenatal care, immunization, HIV/AIDS services, family planning, etc.
* **Operating Hours:** 24/7
* **Address:** Zarawuyaku, Biu LGA, Borno State
* **Phone:** 0803-810-3132
* **Source:** [thehospitalbook.com](https://thehospitalbook.com/abbott-health-clinic/)
""")

st.markdown("---")

st.markdown("### 🔹 2. Abbott Clinic & Maternity")
st.markdown("""
* **Type:** Private Clinic
* **Address:** Damaturu Road, Biu, Borno State
* **Phone:** 0803-810-3132
* **Source:** [directory.org.ng](https://www.directory.org.ng/abbott_clinic_maternity_biu/)
""")

st.markdown("---")

st.markdown("### 🔹 3. Hirku Health Clinic, Dugja")
st.markdown("""
* **Type:** Private Primary Health Care Centre
* **Services:** Cardiology, general surgery, obstetrics, HIV/AIDS services, etc.
* **Operating Hours:** 24/7
* **Address:** Dugja, Biu LGA, Borno State
* **Source:** [thehospitalbook.com](https://thehospitalbook.com/hirku-health-clinic/)
""")

st.markdown("---")

st.markdown("### 🔹 4. Biu Town Dispensary, Sul-Umthla")
st.markdown("""
* **Type:** Public Primary Health Care Centre
* **Services:** Antenatal care, immunization, HIV/AIDS services, family planning, etc.
* **Operating Hours:** 24/7
* **Address:** Sul-Umthla, Biu LGA, Borno State
* **Phone:** 0806-530-2934
* **Source:** [thehospitalbook.com](https://thehospitalbook.com/biu-town-dispensary/)
""")

st.markdown("---")

st.markdown("### 🔹 5. Army Barrack Health Clinic, Yawi Ward")
st.markdown("""
* **Type:** Military Health Facility
* **Services:** Outpatient/inpatient services, surgery, obstetrics, gynecology, pediatrics, and more
* **Address:** Yawi Ward, Biu LGA, Borno State
* **Phone:** 0081-002-0027
* **Source:** [branches.com.ng](https://branches.com.ng/branch-detail/Hospitals-and-Clinics-in-Nigeria-Army-Barrack-Health-Clinic-Borno)
""")

st.markdown("---")

st.subheader("🚑 Emergency Medical Services in Borno State")

st.markdown(
    "### 🔸 Borno State Emergency Medical Services and Ambulance System (SEMSAS)")
st.markdown("""
* **Overview:** Provides rescue and ambulance services across Borno State, with trained paramedics and dispatch system
* **Coverage:** Expanding to rural LGAs like Biu
* **Official Website:** [semsas.bornohealthdata.com.ng](https://semsas.bornohealthdata.com.ng/)
""")

st.markdown("---")

st.subheader("📞 Nationwide & Local Emergency Contacts in Nigeria")

st.markdown(
    "### ✅ Toll-Free & Emergency Numbers (Available in Biu and Nationwide)")

st.markdown("""
| **Service** | **Number** |
| ----------------------------- | ----------------- |
| **General Emergency (NEMA)** | `112` (Toll-Free) |
| **Ambulance Services** | `112` |
| **Fire Service** | `112` |
| **Police Emergency** | `112` or `112` |
| **Federal Road Safety Corps** | `122` |
| **Red Cross (Emergency)** | `0803-960-7023` |
| **NCDC / Health Call Center** | `0800 9700 0010` |
""")

st.info("🔔 **Note:** Dialing `112` connects you to the national control room, and they'll dispatch the appropriate emergency unit (ambulance, police, or fire). This number is **toll-free across all networks** and works even without airtime or data.")

# Quick health info sharing
st.markdown("---")
st.subheader("📋 Share Critical Health Information")

col1, col2 = st.columns(2)

with col1:
    if st.button("📤 Send Health Summary to Emergency Contact", type="secondary", use_container_width=True):
        st.success("📱 Health summary sent to emergency contacts.")
        st.info("""
        **Sent Information:**
        - Current medications
        - Known allergies
        - Recent vital signs
        - Emergency contact numbers
        - Location information
        """)

with col2:
    if st.button("📍 Share Current Location", type="secondary", use_container_width=True):
        st.success("📍 Location shared with emergency contacts.")
        st.info("""
        **Location Information Shared:**
        - GPS coordinates
        - Nearest hospital
        - Emergency services contacted
        - Real-time health status
        """)

# Heart attack recognition and response
st.markdown("---")
st.subheader("❤️ Heart Attack Recognition & Response")

tab1, tab2, tab3 = st.tabs(
    ["⚠️ Warning Signs", "🚨 What to Do", "💊 Medications"])

with tab1:
    st.header("🚨 Heart Attack Warning Signs")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Common Symptoms")
        symptoms = [
            "Chest pain, pressure, or discomfort",
            "Pain radiating to arms, neck, jaw, or back",
            "Shortness of breath",
            "Cold sweat",
            "Nausea or vomiting",
            "Lightheadedness or sudden dizziness",
            "Unusual fatigue (especially in women)"
        ]

        for symptom in symptoms:
            st.write(f"⚠️ {symptom}")

    with col2:
        st.markdown("### 👩 Women's Symptoms")
        women_symptoms = [
            "More likely to have atypical symptoms",
            "Jaw, neck, or upper back pain",
            "Nausea and vomiting",
            "Extreme fatigue",
            "Shortness of breath without chest pain",
            "Dizziness",
            "Pressure in lower chest or upper abdomen"
        ]

        for symptom in women_symptoms:
            st.write(f"👩 {symptom}")

    st.error("🚨 **If you experience ANY of these symptoms, call 112 immediately!**")

with tab2:
    st.header("🚨 What to Do During a Heart Attack")

    st.markdown("### ⚡ Immediate Actions (F.A.S.T.)")

    actions = [
        ("🚨 **Call 112**", "Don't wait - call immediately, even if symptoms seem mild"),
        ("💊 **Chew Aspirin**", "If not allergic, chew 325mg aspirin (or 4 baby aspirin)"),
        ("🧘 **Stay Calm**", "Sit down, rest, and try to remain calm"),
        ("🚗 **Don't Drive**", "Never drive yourself - wait for emergency services"),
        ("👥 **Get Help**", "Alert others nearby who can assist"),
        ("💊 **Take Nitroglycerin**", "If prescribed, take as directed by your doctor")
    ]

    for i, (action, description) in enumerate(actions, 1):
        st.markdown(f"**{i}. {action}**")
        st.write(f"   {description}")
        st.markdown("---")

    st.info("💡 **Remember:** Time is muscle. The faster treatment begins, the better the outcome.")

with tab3:
    st.header("💊 Emergency Medications")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💊 Aspirin")
        st.write("**Dosage:** 325mg (or 4 baby aspirin)")
        st.write("**Action:** Chew, don't swallow whole")
        st.write("**Purpose:** Reduces blood clotting")
        st.write("**Caution:** Only if not allergic to aspirin")

        if st.button("ℹ️ Aspirin Instructions", key="aspirin_instructions"):
            st.info("""
            **How to take aspirin during heart attack:**
            1. Chew 325mg aspirin (or 4 baby aspirin)
            2. Chewing helps faster absorption
            3. Take with small amount of water
            4. Tell emergency responders you took aspirin
            """)

    with col2:
        st.markdown("### 🫀 Nitroglycerin")
        st.write("**Use:** Only if prescribed by doctor")
        st.write("**Dosage:** As prescribed (usually under tongue)")
        st.write("**Purpose:** Improves blood flow to heart")
        st.write("**Important:** Don't use if taking ED medications")

        if st.button("ℹ️ Nitroglycerin Instructions", key="nitroglycerin_instructions"):
            st.info("""
            **How to use nitroglycerin:**
            1. Sit down before taking
            2. Place tablet under tongue
            3. May repeat every 5 minutes (max 3 doses)
            4. Call 112 if no improvement after first dose
            """)

# CPR Instructions
st.markdown("---")
st.subheader("🫁 CPR Instructions (For Bystanders)")

cpr_tab1, cpr_tab2 = st.tabs(["👨‍⚕️ CPR Steps", "📱 CPR Assistant"])

with cpr_tab1:
    st.header("🫁 How to Perform CPR")

    st.warning(
        "⚠️ Use CPR only if person is unresponsive and not breathing normally")

    cpr_steps = [
        ("1. 📞 **Call 112**", "Or have someone else call while you start CPR"),
        ("2. 🫁 **Check Responsiveness**", "Tap shoulders and shout 'Are you okay?'"),
        ("3. 💨 **Check Breathing**",
         "Look for normal breathing for no more than 10 seconds"),
        ("4. 🤲 **Position Hands**",
         "Place heel of hand on center of chest, between nipples"),
        ("5. 💪 **Push Hard & Fast**",
         "Push at least 2 inches deep, 100-120 compressions/minute"),
        ("6. ⚡ **Allow Complete Recoil**",
         "Let chest return to normal position between compressions"),
        ("7. 🔄 **Continue Until Help Arrives**",
         "Don't stop until emergency services take over")
    ]

    for step, description in cpr_steps:
        st.markdown(f"**{step}**")
        st.write(f"   {description}")
        st.markdown("---")

    st.info("💡 **Remember:** Even imperfect CPR is better than no CPR!")

with cpr_tab2:
    st.header("📱 CPR Metronome Assistant")

    st.write("Use this to maintain the correct compression rate of 100-120 per minute")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶️ Start CPR Metronome", type="primary", key="start_cpr_metronome"):
            st.session_state.cpr_metronome_playing = True
            st.success("🎵 CPR Metronome Started!")
            st.info(
                "🎵 Count: 1-2-3-4... Playing 'Bee Gees - Stayin' Alive'")
            st.markdown("**Compression Rate:** 110 beats per minute")
            st.markdown("**Depth:** At least 2 inches")
            st.markdown("**Recoil:** Allow complete chest recoil")

    with col2:
        if st.button("⏹️ Stop Metronome", key="stop_cpr_metronome"):
            st.session_state.cpr_metronome_playing = False
            st.info("🔇 Metronome stopped")

    if 'cpr_metronome_playing' not in st.session_state:
        st.session_state.cpr_metronome_playing = False

    if st.session_state.cpr_metronome_playing:
        audio_file_path = "attached_assets/Bee Gees - Stayin' Alive (Official Music Video).mp3"
        audio_file = open(audio_file_path, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3', start_time=0)
        audio_file.close()

    st.markdown("### 🎵 CPR Songs (to keep rhythm)")
    songs = [
        "🎵 'Stayin' Alive' by Bee Gees",

    ]

    for song in songs:
        st.write(song)

# Location and medical info
st.markdown("---")
st.subheader("📍 Location & Medical Information")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📍 Current Location Information")

    # Simulated location data
    location_data = {
        "Address": "123 Main Street, City, State 12345",
        "Nearest Hospital": "Central Medical Center (0.8 miles)",
        "Emergency Room": "Central Medical ER - (555) 999-0000",
        "Nearest Fire Station": "Station 5 (0.3 miles)",
        "GPS Coordinates": "40.7128° N, 74.0060° W"
    }

    for key, value in location_data.items():
        st.write(f"**{key}:** {value}")

    if st.button("🗺️ Get Directions to Nearest Hospital"):
        st.success("🗺️ Opening directions to Central Medical Center...")
        st.info("In a real app, this would open GPS navigation")

with col2:
    st.markdown("### 🩺 Critical Medical Information")

    # This would be user-configured in a real app
    medical_info = {
        "Blood Type": "O+",
        "Allergies": "Penicillin, Shellfish",
        "Current Medications": "Lisinopril, Metformin",
        "Medical Conditions": "Hypertension, Diabetes Type 2",
        "Emergency Contact": "Jane Doe - (555) 111-2222",
        "Insurance": "HealthCare Plus - Policy #123456"
    }

    for key, value in medical_info.items():
        st.write(f"**{key}:** {value}")

    if st.button("📋 Update Medical Information", key="update_medical_info"):
        st.info("Medical profile editor opened.")

# Medical ID and ICE information
st.markdown("---")
st.subheader("🆔 Medical ID & ICE (In Case of Emergency)")

tab1, tab2 = st.tabs(["🆔 Medical ID", "📱 ICE Setup"])

with tab1:
    st.header("🆔 Medical ID Information")

    st.info("This information would be accessible even when your phone is locked")

    medical_id = {
        "Name": "John Doe",
        "Date of Birth": "January 1, 1980",
        "Medical Conditions": "Hypertension, High Cholesterol",
        "Medications": "Lisinopril 10mg daily, Atorvastatin 20mg daily",
        "Allergies": "Penicillin (severe reaction), Shellfish",
        "Blood Type": "O Positive",
        "Organ Donor": "Yes",
        "Emergency Contact 1": "Jane Doe (Wife) - (555) 111-2222",
        "Emergency Contact 2": "Dr. Smith (PCP) - (555) 123-4567",
        "Insurance": "HealthCare Plus - Policy #123456789"
    }

    for key, value in medical_id.items():
        st.write(f"**{key}:** {value}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📱 Show QR Code for Medical ID"):
            st.success("📱 QR Code Generated!")
            st.info(
                "Scannable QR code with medical information has been generated.")

    with col2:
        if st.button("✏️ Edit Medical ID"):
            st.info("Medical ID editor opened.")

with tab2:
    st.header("📱 ICE (In Case of Emergency) Setup")

    st.markdown("### 📞 Emergency Contacts Configuration")

    # Emergency contacts form (in real app, this would save to user profile)
    with st.form("ice_contacts"):
        st.markdown("**Primary Emergency Contact:**")
        primary_name = st.text_input("Name", value="Jane Doe")
        primary_relationship = st.selectbox(
            "Relationship", ["Spouse", "Parent", "Child", "Sibling", "Friend", "Other"])
        primary_phone = st.text_input("Phone Number", value="(555) 111-2222")

        st.markdown("**Secondary Emergency Contact:**")
        secondary_name = st.text_input("Name ", value="John Doe Sr.")
        secondary_relationship = st.selectbox("Relationship ", [
                                              "Spouse", "Parent", "Child", "Sibling", "Friend", "Other"], index=1)
        secondary_phone = st.text_input(
            "Phone Number ", value="(555) 333-4444")

        if st.form_submit_button("💾 Save ICE Contacts"):
            st.success("✅ Emergency contacts saved!")

    st.markdown("### ⚠️ Important ICE Setup Tips")
    tips = [
        "Add 'ICE' before contact names in your phone",
        "Include multiple contacts in case one is unavailable",
        "Keep contacts updated with current information",
        "Inform your ICE contacts that they're listed",
        "Include medical contacts (doctor, pharmacy)",
        "Test that your contacts work from time to time"
    ]

    for tip in tips:
        st.write(f"💡 {tip}")

# Emergency preparedness
st.markdown("---")
st.subheader("🎒 Emergency Preparedness")

prep_tab1, prep_tab2 = st.tabs(["🏠 Home Preparedness", "📦 Emergency Kit"])

with prep_tab1:
    st.header("🏠 Home Emergency Preparedness")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Emergency Checklist")
        checklist_items = [
            "Emergency contact list posted by phones",
            "First aid kit accessible and stocked",
            "Emergency medications readily available",
            "Flashlights and batteries available",
            "Emergency water supply (1 gallon per person per day)",
            "Non-perishable food for 3 days",
            "Battery-powered or hand-crank radio",
            "Cell phone chargers (car and portable)",
            "Important documents in waterproof container"
        ]

        for item in checklist_items:
            st.checkbox(item, key=f"prep_{item}")

    with col2:
        st.markdown("### 📋 Family Emergency Plan")
        plan_elements = [
            "Meeting places (local and out-of-area)",
            "Emergency contact outside your area",
            "Evacuation routes from home and work",
            "Important phone numbers memorized",
            "Location of emergency supplies",
            "How to turn off utilities (gas, water, electricity)",
            "Emergency plans for pets",
            "Special needs considerations",
            "Insurance and financial information"
        ]

        for element in plan_elements:
            st.write(f"📝 {element}")

with prep_tab2:
    st.header("📦 Personal Emergency Kit Contents")

    kit_categories = {
        "🩺 Medical Supplies": [
            "Prescription medications (7-day supply)",
            "First aid kit",
            "Thermometer",
            "Blood pressure monitor (if needed)",
            "Blood glucose monitor (if diabetic)",
            "Emergency medications (EpiPen, inhaler)",
            "Medical alert bracelet/necklace",
            "Copies of medical records and prescriptions"
        ],
        "📱 Communication": [
            "Cell phone with chargers",
            "Battery-powered radio",
            "Emergency contact information",
            "Whistle for signaling help",
            "Paper and pencil",
            "Maps of local area"
        ],
        "🥤 Food and Water": [
            "Water (1 gallon per person per day for 3 days)",
            "Non-perishable food (3-day supply)",
            "Can opener (manual)",
            "Disposable plates, cups, utensils",
            "Garbage bags and plastic ties"
        ],
        "🔦 Tools and Supplies": [
            "Flashlight and extra batteries",
            "Multi-tool or Swiss Army knife",
            "Duct tape and plastic sheeting",
            "Matches in waterproof container",
            "Cash in small bills",
            "Credit cards",
            "Emergency blanket"
        ]
    }

    for category, items in kit_categories.items():
        with st.expander(category, expanded=False):
            for item in items:
                st.checkbox(item, key=f"kit_{item}")

# Sidebar with emergency summary
with st.sidebar:
    st.header("🚨 Emergency Quick Reference")

    st.markdown("### 📞 Key Numbers")
    st.markdown("**🚑 Emergency:** 112")
    st.markdown("**☠️ Poison Control:** 1-800-222-1222")
    st.markdown("**💬 Crisis Line:** Text HOME to 741741")

    st.markdown("---")
    st.header("❤️ Heart Attack Signs")
    st.markdown("""
    - Chest pain/pressure
    - Arm, neck, jaw pain
    - Shortness of breath
    - Cold sweat
    - Nausea
    """)

    st.markdown("---")
    st.header("🚨 When to Call 112")
    st.markdown("""
    - Chest pain lasting >5 minutes
    - Severe shortness of breath
    - Loss of consciousness
    - Severe bleeding
    - Signs of stroke
    """)

    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.switch_page("app.py")
