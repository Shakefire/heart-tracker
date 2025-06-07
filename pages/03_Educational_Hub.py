import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="Educational Hub", page_icon="📚", layout="wide")

st.title("📚 Heart Health Educational Hub")
st.markdown("Learn about heart health, prevention strategies, and lifestyle modifications to maintain a healthy heart.")

st.markdown("---")

# Navigation tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🫀 Heart Basics", "🥗 Nutrition", "🏃 Exercise", "🧘 Stress Management", "💊 Medications"])

with tab1:
    st.header("🫀 Understanding Your Heart")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("How Your Heart Works")
        st.markdown("""
        Your heart is a muscular pump that circulates blood throughout your body:
        
        **🔄 The Cardiac Cycle:**
        1. **Diastole**: Heart muscle relaxes, chambers fill with blood
        2. **Systole**: Heart muscle contracts, pumping blood out
        
        **🩸 Blood Flow Path:**
        - Right side pumps blood to lungs (pulmonary circulation)
        - Left side pumps blood to body (systemic circulation)
        - Complete cycle takes about 1 second at rest
        
        **📊 Normal Heart Rates:**
        - Resting: 60-100 beats per minute
        - During exercise: Up to 220 minus your age
        - Recovery: Should return to normal within 5-10 minutes
        """)

    with col2:
        st.subheader("Common Heart Conditions")

        conditions = {
            "Coronary Artery Disease": "Narrowing of arteries that supply blood to heart muscle",
            "Heart Attack": "Blockage of blood flow to part of heart muscle",
            "Heart Failure": "Heart cannot pump blood effectively",
            "Arrhythmia": "Irregular heart rhythm",
            "High Blood Pressure": "Force of blood against artery walls is too high",
            "Stroke": "Interruption of blood supply to the brain"
        }

        for condition, description in conditions.items():
            with st.expander(f"ℹ️ {condition}"):
                st.write(description)

                if condition == "Heart Attack":
                    st.markdown("**Warning Signs:**")
                    st.markdown("- Chest pain or discomfort")
                    st.markdown("- Pain in arms, neck, jaw, or back")
                    st.markdown("- Shortness of breath")
                    st.markdown("- Cold sweat, nausea")

    st.markdown("---")
    st.subheader("🎯 Risk Factors")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**✅ Modifiable Risk Factors:**")
        st.markdown("""
        - High blood pressure
        - High cholesterol
        - Smoking
        - Physical inactivity
        - Poor diet
        - Excess weight
        - Diabetes
        - Excessive alcohol use
        - Stress
        """)

    with col2:
        st.markdown("**⚠️ Non-Modifiable Risk Factors:**")
        st.markdown("""
        - Age (men ≥45, women ≥55)
        - Gender (men at higher risk)
        - Family history
        - Race/ethnicity
        - Previous heart attack
        - Previous stroke
        """)

with tab2:
    st.header("🥗 Heart-Healthy Nutrition")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Foods to Embrace")
        st.markdown("""
        **🐟 Omega-3 Rich Foods:**
        - Salmon, mackerel, sardines
        - Walnuts, flaxseeds, chia seeds
        - Reduces inflammation and triglycerides
        
        **🥬 Leafy Greens:**
        - Spinach, kale, arugula
        - Rich in nitrates, support blood vessel function
        
        **🫐 Berries:**
        - Blueberries, strawberries, blackberries
        - Antioxidants protect against oxidative stress
        
        **🥑 Healthy Fats:**
        - Avocados, olive oil, nuts
        - Monounsaturated fats improve cholesterol
        
        **🌾 Whole Grains:**
        - Oats, quinoa, brown rice
        - Fiber helps lower cholesterol
        """)

    with col2:
        st.subheader("Foods to Limit")
        st.markdown("""
        **🧂 High Sodium Foods:**
        - Processed meats, canned soups
        - Restaurant meals, packaged snacks
        - Aim for <2,300mg sodium daily
        
        **🍟 Trans and Saturated Fats:**
        - Fried foods, baked goods
        - Fatty cuts of meat, full-fat dairy
        - Limit saturated fat to <10% of calories
        
        **🍭 Added Sugars:**
        - Sodas, candy, desserts
        - Limit to <10% of daily calories
        
        **🍺 Excess Alcohol:**
        - Men: ≤2 drinks/day
        - Women: ≤1 drink/day
        """)

    st.markdown("---")
    st.subheader("🍽️ Sample Heart-Healthy Meal Plan")

    meal_plan = {
        "Breakfast": [
            "Oatmeal with berries and walnuts",
            "Greek yogurt with flaxseeds",
            "Whole grain toast with avocado"
        ],
        "Lunch": [
            "Grilled salmon with quinoa and vegetables",
            "Spinach salad with olive oil dressing",
            "Lentil soup with whole grain bread"
        ],
        "Dinner": [
            "Grilled chicken with sweet potato and broccoli",
            "Vegetable stir-fry with brown rice",
            "Baked cod with roasted vegetables"
        ],
        "Snacks": [
            "Handful of nuts",
            "Apple with almond butter",
            "Hummus with vegetable sticks"
        ]
    }

    for meal, options in meal_plan.items():
        with st.expander(f"🍽️ {meal} Ideas"):
            for option in options:
                st.write(f"• {option}")

with tab3:
    st.header("🏃 Exercise for Heart Health")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Exercise Guidelines")
        st.markdown("""
        **🎯 Weekly Targets:**
        - 150 minutes moderate-intensity aerobic activity
        - OR 75 minutes vigorous-intensity aerobic activity
        - 2+ days of muscle-strengthening activities
        
        **💓 Moderate Intensity Examples:**
        - Brisk walking (3-4 mph)
        - Water aerobics
        - Ballroom dancing
        - General gardening
        - Tennis (doubles)
        
        **🔥 Vigorous Intensity Examples:**
        - Running/jogging
        - Swimming laps
        - Cycling >10 mph
        - Hiking uphill
        - Tennis (singles)
        """)

    with col2:
        st.subheader("Getting Started Safely")
        st.markdown("""
        **🚀 Beginner Tips:**
        - Start with 5-10 minutes daily
        - Gradually increase duration
        - Choose activities you enjoy
        - Listen to your body
        - Stay hydrated
        
        **⚠️ When to Stop Exercising:**
        - Chest pain or pressure
        - Severe shortness of breath
        - Dizziness or lightheadedness
        - Nausea or vomiting
        - Irregular heartbeat
        
        **📋 Before Starting:**
        - Consult your doctor
        - Consider stress test if high risk
        - Start gradually
        - Warm up and cool down
        """)

    st.markdown("---")
    st.subheader("💪 Sample Workout Plans")

    workout_plans = {
        "Beginner (Week 1-4)": {
            "Monday": "10-min walk",
            "Tuesday": "Rest or gentle stretching",
            "Wednesday": "10-min walk",
            "Thursday": "Light resistance exercises",
            "Friday": "10-min walk",
            "Saturday": "Fun activity (dancing, gardening)",
            "Sunday": "Rest"
        },
        "Intermediate (Week 5-12)": {
            "Monday": "20-min brisk walk",
            "Tuesday": "Strength training (upper body)",
            "Wednesday": "25-min bike ride or swim",
            "Thursday": "Strength training (lower body)",
            "Friday": "20-min walk/jog intervals",
            "Saturday": "30-min recreational activity",
            "Sunday": "Rest or gentle yoga"
        },
        "Advanced (Week 13+)": {
            "Monday": "30-min run or vigorous activity",
            "Tuesday": "Full body strength training",
            "Wednesday": "30-min cycling or swimming",
            "Thursday": "Strength training + core work",
            "Friday": "30-min interval training",
            "Saturday": "45-min recreational activity",
            "Sunday": "Active recovery (yoga, walking)"
        }
    }

    selected_plan = st.selectbox(
        "Choose a workout plan:", list(workout_plans.keys()))

    if selected_plan:
        plan = workout_plans[selected_plan]
        cols = st.columns(7)
        days = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]

        for i, day in enumerate(days):
            with cols[i]:
                st.markdown(f"**{day}**")
                st.write(plan[day])

with tab4:
    st.header("🧘 Stress Management for Heart Health")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("How Stress Affects Your Heart")
        st.markdown("""
        **⚡ Acute Stress Response:**
        - Increases heart rate and blood pressure
        - Releases stress hormones (cortisol, adrenaline)
        - Increases blood clotting tendency
        - Usually temporary and manageable
        
        **⚠️ Chronic Stress Effects:**
        - Sustained high blood pressure
        - Increased inflammation
        - Higher risk of heart disease
        - Poor lifestyle choices (smoking, overeating)
        - Weakened immune system
        """)

        st.subheader("Stress Management Techniques")
        techniques = {
            "Deep Breathing": "4-7-8 technique: Inhale 4, hold 7, exhale 8 seconds",
            "Progressive Muscle Relaxation": "Tense and release muscle groups systematically",
            "Meditation": "5-10 minutes daily mindfulness practice",
            "Yoga": "Combines physical postures with breathing and meditation",
            "Regular Exercise": "Natural stress reliever and mood booster",
            "Adequate Sleep": "7-9 hours nightly for stress recovery"
        }

        for technique, description in techniques.items():
            with st.expander(f"🧘 {technique}"):
                st.write(description)

    with col2:
        st.subheader("Quick Stress Relief")

        if st.button("🫁 Try 4-7-8 Breathing Exercise"):
            st.info("Follow along with this breathing exercise:")

            with st.container():
                st.markdown("**Instructions:**")
                st.markdown("1. Sit comfortably with your back straight")
                st.markdown(
                    "2. Place your tongue against the roof of your mouth")
                st.markdown("3. Follow the breathing pattern below")

                # Breathing exercise simulation
                for cycle in range(1, 4):
                    st.markdown(f"**Cycle {cycle}:**")
                    st.success("🫁 Inhale through nose for 4 seconds...")
                    st.warning("⏸️ Hold your breath for 7 seconds...")
                    st.info("🫁 Exhale through mouth for 8 seconds...")
                    if cycle < 3:
                        st.markdown("---")

                st.success("✅ Exercise complete! Notice how you feel.")

        st.subheader("Lifestyle Stress Reducers")
        st.markdown("""
        **🎯 Daily Habits:**
        - Set realistic goals
        - Practice saying "no"
        - Take regular breaks
        - Maintain social connections
        - Limit caffeine and alcohol
        - Keep a gratitude journal
        - Spend time in nature
        - Listen to calming music
        - Practice mindful eating
        - Maintain work-life balance
        """)

with tab5:
    st.header("💊 Heart Medications Guide")

    st.info("ℹ️ This information is for educational purposes only. Always consult your healthcare provider about medications.")

    medications = {
        "Blood Pressure Medications": {
            "ACE Inhibitors": {
                "examples": "lisinopril, enalapril, captopril",
                "how_they_work": "Block enzyme that narrows blood vessels",
                "common_side_effects": "Dry cough, elevated potassium levels"
            },
            "Beta Blockers": {
                "examples": "metoprolol, atenolol, propranolol",
                "how_they_work": "Slow heart rate and reduce force of contractions",
                "common_side_effects": "Fatigue, cold hands/feet, depression"
            },
            "Diuretics": {
                "examples": "hydrochlorothiazide, furosemide",
                "how_they_work": "Remove excess water and sodium from body",
                "common_side_effects": "Frequent urination, electrolyte imbalances"
            }
        },
        "Cholesterol Medications": {
            "Statins": {
                "examples": "atorvastatin, simvastatin, rosuvastatin",
                "how_they_work": "Block enzyme that produces cholesterol",
                "common_side_effects": "Muscle aches, liver enzyme elevation"
            },
            "PCSK9 Inhibitors": {
                "examples": "evolocumab, alirocumab",
                "how_they_work": "Help liver remove LDL cholesterol from blood",
                "common_side_effects": "Injection site reactions, flu-like symptoms"
            }
        },
        "Blood Thinners": {
            "Antiplatelet Agents": {
                "examples": "aspirin, clopidogrel",
                "how_they_work": "Prevent blood platelets from clumping together",
                "common_side_effects": "Increased bleeding risk, stomach irritation"
            },
            "Anticoagulants": {
                "examples": "warfarin, rivaroxaban, apixaban",
                "how_they_work": "Interfere with blood clotting cascade",
                "common_side_effects": "Increased bleeding risk, bruising"
            }
        }
    }

    for category, meds in medications.items():
        st.subheader(f"💊 {category}")

        for med_name, details in meds.items():
            with st.expander(f"📋 {med_name}"):
                st.markdown(f"**Examples:** {details['examples']}")
                st.markdown(f"**How they work:** {details['how_they_work']}")
                st.markdown(
                    f"**Common side effects:** {details['common_side_effects']}")

    st.markdown("---")
    st.subheader("📋 Medication Safety Tips")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **✅ Do:**
        - Take medications as prescribed
        - Keep an updated medication list
        - Use a pill organizer
        - Set reminders
        - Ask questions about new medications
        - Report side effects to your doctor
        - Bring all medications to appointments
        """)

    with col2:
        st.markdown("""
        **❌ Don't:**
        - Stop medications without consulting doctor
        - Share medications with others
        - Take double doses if you miss one
        - Mix medications with alcohol
        - Ignore potential drug interactions
        - Take expired medications
        - Store medications in bathroom
        """)

# Sidebar with additional resources
with st.sidebar:
    st.header("📱 Quick Resources")

    st.subheader("Emergency Numbers")
    st.markdown("""
    - **Emergency:** 112
    - **Poison Control:** 1-800-222-1222
    - **American Heart Association:** 1-800-AHA-USA1
    """)

    st.subheader("Useful Apps & Websites")
    st.markdown("""
    - **MyFitnessPal:** Track nutrition
    - **Headspace:** Meditation and mindfulness
    - **Strava:** Track physical activity
    - **Heart360:** AHA's heart health tracker
    - **WebMD:** Medical information
    """)

    st.subheader("💡 Daily Tip")
    tips = [
        "Take the stairs instead of the elevator",
        "Replace one sugary drink with water today",
        "Do 5 minutes of deep breathing",
        "Take a 10-minute walk after lunch",
        "Eat one extra serving of vegetables",
        "Go to bed 15 minutes earlier tonight",
        "Practice gratitude - write down 3 things you're thankful for",
        "Do some stretches while watching TV"
    ]

    daily_tip = tips[datetime.now().day % len(tips)]
    st.info(f"💡 {daily_tip}")

    st.subheader("📚 Learn More")
    st.markdown("""
    - [American Heart Association](https://www.heart.org)
    - [CDC Heart Disease](https://www.cdc.gov/heartdisease)
    - [NIH Heart Health](https://www.nhlbi.nih.gov)
    """)
