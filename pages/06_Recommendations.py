import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Smart Recommendations", page_icon="💡", layout="wide")

st.title("💡 Smart Health Recommendations")
st.markdown("Get personalized recommendations for workouts, nutrition, stress management, and lifestyle improvements based on your health profile and trends.")

st.markdown("---")

# Initialize recommendation system
class SmartRecommendationEngine:
    def __init__(self):
        self.user_profile = {}
        self.recommendations = {
            'exercise': [],
            'nutrition': [],
            'stress_management': [],
            'lifestyle': [],
            'medical': []
        }
    
    def analyze_user_profile(self, health_data, lifestyle_data, preferences):
        """Analyze user data to generate personalized recommendations"""
        self.user_profile = {
            'health_data': health_data,
            'lifestyle_data': lifestyle_data,
            'preferences': preferences
        }
        
        # Generate recommendations based on analysis
        self._generate_exercise_recommendations()
        self._generate_nutrition_recommendations()
        self._generate_stress_management_recommendations()
        self._generate_lifestyle_recommendations()
        self._generate_medical_recommendations()
        
        return self.recommendations
    
    def _generate_exercise_recommendations(self):
        """Generate personalized exercise recommendations"""
        health = self.user_profile['health_data']
        lifestyle = self.user_profile['lifestyle_data']
        prefs = self.user_profile['preferences']
        
        fitness_level = lifestyle.get('fitness_level', 'beginner')
        available_time = lifestyle.get('exercise_time', 30)
        preferred_activities = prefs.get('exercise_preferences', [])
        
        recommendations = []
        
        # Cardio recommendations
        if health.get('bp_systolic', 120) > 140:
            recommendations.append({
                'type': 'Cardiovascular',
                'activity': 'Brisk Walking',
                'duration': '30-45 minutes',
                'frequency': '5 days/week',
                'intensity': 'Moderate',
                'benefits': 'Helps lower blood pressure and improve heart health',
                'priority': 'High'
            })
        
        if health.get('cholesterol', 200) > 240:
            recommendations.append({
                'type': 'Cardiovascular',
                'activity': 'Swimming or Cycling',
                'duration': '25-40 minutes',
                'frequency': '4-5 days/week',
                'intensity': 'Moderate to Vigorous',
                'benefits': 'Helps improve cholesterol profile and cardiovascular fitness',
                'priority': 'High'
            })
        
        # Strength training
        if fitness_level != 'advanced':
            recommendations.append({
                'type': 'Strength Training',
                'activity': 'Bodyweight Exercises',
                'duration': '20-30 minutes',
                'frequency': '2-3 days/week',
                'intensity': 'Moderate',
                'benefits': 'Builds muscle strength and improves metabolism',
                'priority': 'Medium'
            })
        
        # Flexibility and balance
        if health.get('age', 40) > 50 or lifestyle.get('stress_level', 50) > 60:
            recommendations.append({
                'type': 'Flexibility',
                'activity': 'Yoga or Tai Chi',
                'duration': '20-30 minutes',
                'frequency': '3-4 days/week',
                'intensity': 'Light to Moderate',
                'benefits': 'Improves flexibility, balance, and reduces stress',
                'priority': 'Medium'
            })
        
        # Time-based adjustments
        if available_time < 30:
            recommendations.append({
                'type': 'High-Intensity',
                'activity': 'HIIT Workouts',
                'duration': '15-20 minutes',
                'frequency': '3 days/week',
                'intensity': 'High',
                'benefits': 'Maximizes benefits in minimal time',
                'priority': 'Medium'
            })
        
        self.recommendations['exercise'] = recommendations
    
    def _generate_nutrition_recommendations(self):
        """Generate personalized nutrition recommendations"""
        health = self.user_profile['health_data']
        lifestyle = self.user_profile['lifestyle_data']
        prefs = self.user_profile['preferences']
        
        recommendations = []
        
        # Blood pressure management
        if health.get('bp_systolic', 120) > 130:
            recommendations.append({
                'category': 'Blood Pressure',
                'recommendation': 'Reduce sodium intake to less than 2,300mg daily',
                'foods_to_include': ['Leafy greens', 'Berries', 'Bananas', 'Beets', 'Oats'],
                'foods_to_limit': ['Processed foods', 'Canned soups', 'Deli meats', 'Restaurant meals'],
                'priority': 'High'
            })
            
            recommendations.append({
                'category': 'Blood Pressure',
                'recommendation': 'Follow the DASH diet pattern',
                'foods_to_include': ['Whole grains', 'Lean proteins', 'Low-fat dairy', 'Nuts', 'Seeds'],
                'foods_to_limit': ['Refined sugars', 'Saturated fats', 'Red meat'],
                'priority': 'High'
            })
        
        # Cholesterol management
        if health.get('cholesterol', 200) > 200:
            recommendations.append({
                'category': 'Cholesterol',
                'recommendation': 'Increase omega-3 fatty acids and soluble fiber',
                'foods_to_include': ['Salmon', 'Mackerel', 'Walnuts', 'Flaxseeds', 'Oatmeal', 'Beans'],
                'foods_to_limit': ['Trans fats', 'Fried foods', 'Full-fat dairy', 'Fatty meats'],
                'priority': 'High'
            })
        
        # Weight management
        bmi = health.get('bmi', 25)
        if bmi > 25:
            recommendations.append({
                'category': 'Weight Management',
                'recommendation': 'Focus on portion control and calorie-dense nutrients',
                'foods_to_include': ['Vegetables', 'Lean proteins', 'Whole fruits', 'Legumes'],
                'foods_to_limit': ['Sugary drinks', 'Processed snacks', 'Large portions', 'High-calorie desserts'],
                'priority': 'Medium'
            })
        
        # Heart-healthy general
        recommendations.append({
            'category': 'Heart Health',
            'recommendation': 'Follow a Mediterranean-style eating pattern',
            'foods_to_include': ['Olive oil', 'Fish', 'Nuts', 'Whole grains', 'Fruits', 'Vegetables'],
            'foods_to_limit': ['Processed meats', 'Refined carbs', 'Added sugars', 'Excess alcohol'],
            'priority': 'Medium'
        })
        
        self.recommendations['nutrition'] = recommendations
    
    def _generate_stress_management_recommendations(self):
        """Generate stress management recommendations"""
        lifestyle = self.user_profile['lifestyle_data']
        prefs = self.user_profile['preferences']
        
        stress_level = lifestyle.get('stress_level', 50)
        available_time = lifestyle.get('relaxation_time', 15)
        
        recommendations = []
        
        if stress_level > 60:
            recommendations.append({
                'technique': 'Deep Breathing Exercises',
                'description': '4-7-8 breathing technique for immediate stress relief',
                'duration': '5-10 minutes',
                'frequency': '2-3 times daily',
                'difficulty': 'Easy',
                'benefits': 'Activates parasympathetic nervous system, lowers heart rate'
            })
            
            recommendations.append({
                'technique': 'Progressive Muscle Relaxation',
                'description': 'Systematic tensing and relaxing of muscle groups',
                'duration': '15-20 minutes',
                'frequency': 'Daily before bed',
                'difficulty': 'Easy',
                'benefits': 'Reduces physical tension and promotes better sleep'
            })
        
        if available_time >= 20:
            recommendations.append({
                'technique': 'Mindfulness Meditation',
                'description': 'Focused attention on present moment awareness',
                'duration': '10-20 minutes',
                'frequency': 'Daily',
                'difficulty': 'Medium',
                'benefits': 'Reduces anxiety, improves emotional regulation'
            })
        
        recommendations.append({
            'technique': 'Nature Exposure',
            'description': 'Spend time outdoors in natural settings',
            'duration': '20-30 minutes',
            'frequency': '3-4 times weekly',
            'difficulty': 'Easy',
            'benefits': 'Reduces cortisol levels, improves mood'
        })
        
        if stress_level > 70:
            recommendations.append({
                'technique': 'Professional Support',
                'description': 'Consider counseling or stress management programs',
                'duration': 'Varies',
                'frequency': 'As recommended',
                'difficulty': 'Varies',
                'benefits': 'Develops coping strategies, addresses root causes'
            })
        
        self.recommendations['stress_management'] = recommendations
    
    def _generate_lifestyle_recommendations(self):
        """Generate general lifestyle recommendations"""
        health = self.user_profile['health_data']
        lifestyle = self.user_profile['lifestyle_data']
        
        recommendations = []
        
        # Sleep recommendations
        sleep_hours = lifestyle.get('sleep_hours', 7)
        if sleep_hours < 7:
            recommendations.append({
                'area': 'Sleep Hygiene',
                'recommendation': 'Aim for 7-9 hours of quality sleep nightly',
                'specific_actions': [
                    'Establish consistent bedtime routine',
                    'Avoid screens 1 hour before bed',
                    'Keep bedroom cool and dark',
                    'Limit caffeine after 2 PM'
                ],
                'priority': 'High'
            })
        
        # Social connections
        recommendations.append({
            'area': 'Social Health',
            'recommendation': 'Maintain strong social connections',
            'specific_actions': [
                'Schedule regular social activities',
                'Join community groups or clubs',
                'Volunteer for meaningful causes',
                'Stay connected with family and friends'
            ],
            'priority': 'Medium'
        })
        
        # Preventive care
        recommendations.append({
            'area': 'Preventive Healthcare',
            'recommendation': 'Stay up-to-date with health screenings',
            'specific_actions': [
                'Annual physical exams',
                'Blood pressure monitoring',
                'Cholesterol screening every 5 years',
                'Diabetes screening if at risk'
            ],
            'priority': 'High'
        })
        
        # Smoking cessation
        if lifestyle.get('smoking_status') == 'current':
            recommendations.append({
                'area': 'Smoking Cessation',
                'recommendation': 'Quit smoking immediately for heart health',
                'specific_actions': [
                    'Consult healthcare provider about cessation aids',
                    'Join smoking cessation programs',
                    'Use nicotine replacement therapy if appropriate',
                    'Identify and avoid triggers'
                ],
                'priority': 'Critical'
            })
        
        self.recommendations['lifestyle'] = recommendations
    
    def _generate_medical_recommendations(self):
        """Generate medical follow-up recommendations"""
        health = self.user_profile['health_data']
        
        recommendations = []
        
        # Blood pressure follow-up
        if health.get('bp_systolic', 120) > 140:
            recommendations.append({
                'type': 'Cardiology Consultation',
                'urgency': 'High',
                'reason': 'Elevated blood pressure requires medical evaluation',
                'suggested_tests': ['24-hour BP monitoring', 'ECG', 'Echocardiogram'],
                'timeframe': 'Within 2 weeks'
            })
        
        # Cholesterol follow-up
        if health.get('cholesterol', 200) > 240:
            recommendations.append({
                'type': 'Lipid Management',
                'urgency': 'Medium',
                'reason': 'High cholesterol may require medication',
                'suggested_tests': ['Comprehensive lipid panel', 'Coronary calcium score'],
                'timeframe': 'Within 1 month'
            })
        
        # General cardiac risk assessment
        age = health.get('age', 40)
        if age > 50 or health.get('family_history', False):
            recommendations.append({
                'type': 'Cardiac Risk Assessment',
                'urgency': 'Medium',
                'reason': 'Age or family history indicates need for screening',
                'suggested_tests': ['Stress test', 'Coronary calcium score', 'Carotid ultrasound'],
                'timeframe': 'Within 3 months'
            })
        
        self.recommendations['medical'] = recommendations

# User input section
st.subheader("👤 Your Health Profile")

# Health data input
with st.expander("🩺 Health Metrics", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age", 20, 100, 45)
        height = st.number_input("Height (cm)", 140, 220, 170)
        weight = st.number_input("Weight (kg)", 40, 150, 70)
        bmi = weight / ((height/100) ** 2)
        
    with col2:
        bp_systolic = st.number_input("Systolic BP (mmHg)", 90, 200, 120)
        bp_diastolic = st.number_input("Diastolic BP (mmHg)", 60, 120, 80)
        cholesterol = st.number_input("Total Cholesterol (mg/dL)", 120, 400, 200)
        
    with col3:
        resting_hr = st.number_input("Resting Heart Rate (bpm)", 50, 120, 70)
        family_history = st.checkbox("Family History of Heart Disease")
        diabetes = st.checkbox("Diabetes")

# Lifestyle data input
with st.expander("🎯 Lifestyle Information"):
    col1, col2 = st.columns(2)
    
    with col1:
        fitness_level = st.selectbox("Current Fitness Level", ["Beginner", "Intermediate", "Advanced"])
        exercise_frequency = st.slider("Exercise Days per Week", 0, 7, 3)
        exercise_time = st.slider("Available Exercise Time (minutes/day)", 15, 120, 30)
        stress_level = st.slider("Stress Level (0-100)", 0, 100, 40)
        
    with col2:
        sleep_hours = st.slider("Average Sleep Hours", 4, 12, 7)
        smoking_status = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
        alcohol_consumption = st.selectbox("Alcohol Consumption", ["None", "Light", "Moderate", "Heavy"])
        relaxation_time = st.slider("Available Relaxation Time (minutes/day)", 5, 60, 15)

# Preferences
with st.expander("⚙️ Preferences"):
    col1, col2 = st.columns(2)
    
    with col1:
        exercise_preferences = st.multiselect("Preferred Exercise Types", 
                                            ["Walking", "Running", "Swimming", "Cycling", "Yoga", "Weight Training", "Sports", "Dancing"])
        dietary_restrictions = st.multiselect("Dietary Restrictions", 
                                            ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Low-Sodium", "Diabetic"])
        
    with col2:
        time_availability = st.selectbox("When do you prefer to exercise?", 
                                       ["Morning", "Afternoon", "Evening", "Flexible"])
        support_preference = st.selectbox("Preferred Support Type", 
                                        ["Self-guided", "Group classes", "Personal trainer", "Online programs"])

# Generate recommendations
if st.button("🚀 Generate Personalized Recommendations", type="primary"):
    
    # Prepare data
    health_data = {
        'age': age,
        'bmi': bmi,
        'bp_systolic': bp_systolic,
        'bp_diastolic': bp_diastolic,
        'cholesterol': cholesterol,
        'resting_hr': resting_hr,
        'family_history': family_history,
        'diabetes': diabetes
    }
    
    lifestyle_data = {
        'fitness_level': fitness_level.lower(),
        'exercise_frequency': exercise_frequency,
        'exercise_time': exercise_time,
        'stress_level': stress_level,
        'sleep_hours': sleep_hours,
        'smoking_status': smoking_status.lower(),
        'alcohol_consumption': alcohol_consumption.lower(),
        'relaxation_time': relaxation_time
    }
    
    preferences = {
        'exercise_preferences': exercise_preferences,
        'dietary_restrictions': dietary_restrictions,
        'time_availability': time_availability.lower(),
        'support_preference': support_preference.lower()
    }
    
    # Generate recommendations
    with st.spinner("Analyzing your profile and generating personalized recommendations..."):
        engine = SmartRecommendationEngine()
        recommendations = engine.analyze_user_profile(health_data, lifestyle_data, preferences)
        
        # Store in session state
        st.session_state.current_recommendations = recommendations
        st.session_state.recommendation_timestamp = datetime.now()
    
    # Display recommendations
    st.markdown("---")
    st.subheader("🎯 Your Personalized Recommendations")
    
    # Create tabs for different recommendation categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💪 Exercise", "🥗 Nutrition", "🧘 Stress Management", "🌟 Lifestyle", "🩺 Medical"])
    
    with tab1:
        st.header("💪 Exercise Recommendations")
        
        if recommendations['exercise']:
            for i, rec in enumerate(recommendations['exercise']):
                priority_color = "🔴" if rec['priority'] == 'High' else "🟡" if rec['priority'] == 'Medium' else "🟢"
                
                with st.expander(f"{priority_color} {rec['activity']} ({rec['type']})", expanded=(rec['priority'] == 'High')):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Duration:** {rec['duration']}")
                        st.markdown(f"**Frequency:** {rec['frequency']}")
                        st.markdown(f"**Intensity:** {rec['intensity']}")
                    
                    with col2:
                        st.markdown(f"**Priority:** {rec['priority']}")
                        st.markdown(f"**Benefits:** {rec['benefits']}")
            
            # Weekly workout plan
            st.markdown("---")
            st.subheader("📅 Suggested Weekly Plan")
            
            # Generate a sample weekly plan based on recommendations
            weekly_plan = {
                'Monday': 'Cardio (30 min) + Stretching (10 min)',
                'Tuesday': 'Strength Training (25 min)',
                'Wednesday': 'Active Recovery - Walking (20 min)',
                'Thursday': 'Cardio (30 min) + Core Work (10 min)',
                'Friday': 'Strength Training (25 min)',
                'Saturday': 'Flexibility/Yoga (30 min)',
                'Sunday': 'Rest or Light Activity'
            }
            
            for day, activity in weekly_plan.items():
                st.write(f"**{day}:** {activity}")
        
        else:
            st.info("No specific exercise recommendations generated. Consult with a fitness professional for personalized guidance.")
    
    with tab2:
        st.header("🥗 Nutrition Recommendations")
        
        if recommendations['nutrition']:
            for rec in recommendations['nutrition']:
                priority_color = "🔴" if rec['priority'] == 'High' else "🟡" if rec['priority'] == 'Medium' else "🟢"
                
                with st.expander(f"{priority_color} {rec['category']}", expanded=(rec['priority'] == 'High')):
                    st.markdown(f"**Recommendation:** {rec['recommendation']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Foods to Include:**")
                        for food in rec['foods_to_include']:
                            st.write(f"✅ {food}")
                    
                    with col2:
                        st.markdown("**Foods to Limit:**")
                        for food in rec['foods_to_limit']:
                            st.write(f"❌ {food}")
            
            # Meal planning suggestions
            st.markdown("---")
            st.subheader("🍽️ Sample Meal Ideas")
            
            meal_ideas = {
                'Breakfast': [
                    'Oatmeal with berries and walnuts',
                    'Greek yogurt with flaxseeds and fruit',
                    'Whole grain toast with avocado'
                ],
                'Lunch': [
                    'Grilled salmon with quinoa and vegetables',
                    'Lentil soup with whole grain bread',
                    'Mediterranean salad with olive oil dressing'
                ],
                'Dinner': [
                    'Baked chicken with sweet potato and broccoli',
                    'Vegetable stir-fry with brown rice',
                    'Grilled fish with roasted vegetables'
                ],
                'Snacks': [
                    'Handful of nuts',
                    'Apple with almond butter',
                    'Hummus with vegetable sticks'
                ]
            }
            
            for meal, ideas in meal_ideas.items():
                with st.expander(f"🍽️ {meal} Ideas"):
                    for idea in ideas:
                        st.write(f"• {idea}")
        
        else:
            st.info("No specific nutrition recommendations generated. Consider consulting with a registered dietitian.")
    
    with tab3:
        st.header("🧘 Stress Management")
        
        if recommendations['stress_management']:
            for rec in recommendations['stress_management']:
                difficulty_icon = "🟢" if rec['difficulty'] == 'Easy' else "🟡" if rec['difficulty'] == 'Medium' else "🔴"
                
                with st.expander(f"{difficulty_icon} {rec['technique']}", expanded=True):
                    st.markdown(f"**Description:** {rec['description']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Duration:** {rec['duration']}")
                        st.markdown(f"**Frequency:** {rec['frequency']}")
                    
                    with col2:
                        st.markdown(f"**Difficulty:** {rec['difficulty']}")
                        st.markdown(f"**Benefits:** {rec['benefits']}")
            
            # Quick stress relief guide
            st.markdown("---")
            st.subheader("⚡ Quick Stress Relief Techniques")
            
            quick_techniques = [
                "Take 5 deep breaths (4 seconds in, 6 seconds out)",
                "Do a 2-minute body scan from head to toe",
                "Listen to calming music for 5 minutes",
                "Step outside and take a short walk",
                "Practice gratitude - think of 3 things you're thankful for"
            ]
            
            for technique in quick_techniques:
                st.write(f"• {technique}")
        
        else:
            st.info("Consider incorporating stress management techniques into your daily routine.")
    
    with tab4:
        st.header("🌟 Lifestyle Recommendations")
        
        if recommendations['lifestyle']:
            for rec in recommendations['lifestyle']:
                priority_color = "🔴" if rec['priority'] == 'Critical' else "🟡" if rec['priority'] == 'High' else "🟢"
                
                with st.expander(f"{priority_color} {rec['area']}", expanded=(rec['priority'] in ['Critical', 'High'])):
                    st.markdown(f"**Recommendation:** {rec['recommendation']}")
                    
                    st.markdown("**Specific Actions:**")
                    for action in rec['specific_actions']:
                        st.write(f"• {action}")
            
            # Habit tracking suggestions
            st.markdown("---")
            st.subheader("📊 Habit Tracking Suggestions")
            
            habits_to_track = [
                "Daily exercise minutes",
                "Hours of sleep",
                "Stress level (1-10 scale)",
                "Servings of fruits and vegetables",
                "Minutes of relaxation/meditation",
                "Water intake (glasses)",
                "Steps taken",
                "Mood rating"
            ]
            
            st.info("Consider tracking these habits to monitor your progress:")
            for habit in habits_to_track:
                st.write(f"📈 {habit}")
        
        else:
            st.info("Continue maintaining healthy lifestyle habits.")
    
    with tab5:
        st.header("🩺 Medical Recommendations")
        
        if recommendations['medical']:
            for rec in recommendations['medical']:
                urgency_color = "🔴" if rec['urgency'] == 'High' else "🟡" if rec['urgency'] == 'Medium' else "🟢"
                
                with st.expander(f"{urgency_color} {rec['type']}", expanded=(rec['urgency'] == 'High')):
                    st.markdown(f"**Reason:** {rec['reason']}")
                    st.markdown(f"**Timeframe:** {rec['timeframe']}")
                    st.markdown(f"**Urgency:** {rec['urgency']}")
                    
                    if rec['suggested_tests']:
                        st.markdown("**Suggested Tests:**")
                        for test in rec['suggested_tests']:
                            st.write(f"• {test}")
            
            st.warning("⚠️ These are general recommendations. Always consult with your healthcare provider for personalized medical advice.")
        
        else:
            st.success("✅ No immediate medical follow-up recommendations based on current data.")
    
    # Action plan summary
    st.markdown("---")
    st.subheader("📋 Your Action Plan Summary")
    
    # Prioritized action items
    high_priority_items = []
    medium_priority_items = []
    
    # Collect high priority items from all categories
    for category, recs in recommendations.items():
        if category == 'exercise':
            high_priority_items.extend([f"Exercise: {rec['activity']}" for rec in recs if rec['priority'] == 'High'])
        elif category == 'nutrition':
            high_priority_items.extend([f"Nutrition: {rec['recommendation']}" for rec in recs if rec['priority'] == 'High'])
        elif category == 'lifestyle':
            high_priority_items.extend([f"Lifestyle: {rec['recommendation']}" for rec in recs if rec['priority'] in ['Critical', 'High']])
        elif category == 'medical':
            high_priority_items.extend([f"Medical: {rec['type']}" for rec in recs if rec['urgency'] == 'High'])
    
    # Display prioritized actions
    if high_priority_items:
        st.markdown("### 🎯 High Priority Actions (Start This Week)")
        for item in high_priority_items:
            st.write(f"🔴 {item}")
    
    # Save recommendations
    if st.button("💾 Save Recommendations"):
        if 'saved_recommendations' not in st.session_state:
            st.session_state.saved_recommendations = []
        
        recommendation_summary = {
            'timestamp': datetime.now(),
            'health_profile': health_data,
            'lifestyle_profile': lifestyle_data,
            'high_priority_actions': high_priority_items,
            'total_recommendations': sum(len(recs) for recs in recommendations.values())
        }
        
        st.session_state.saved_recommendations.append(recommendation_summary)
        st.success("✅ Recommendations saved to your profile!")

# Progress tracking section
st.markdown("---")
st.subheader("📈 Track Your Progress")

if hasattr(st.session_state, 'current_recommendations'):
    st.info("💡 Tip: Come back weekly to update your progress and get refined recommendations!")
    
    # Simple progress tracking
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Completed Actions")
        completed_actions = st.multiselect(
            "Select actions you've completed:",
            options=[f"Action {i+1}" for i in range(5)],  # Placeholder options
            help="Track your progress on recommended actions"
        )
    
    with col2:
        st.markdown("### 🎯 Weekly Goals")
        weekly_goals = st.text_area(
            "Set your goals for this week:",
            placeholder="e.g., Exercise 3 times, try Mediterranean diet, practice meditation daily"
        )

# Sidebar with additional features
with st.sidebar:
    st.header("🎯 Quick Actions")
    
    if st.button("📊 Update Health Profile"):
        st.rerun()
    
    if st.button("📱 Get Daily Tip"):
        daily_tips = [
            "Take a 5-minute walking break every hour",
            "Replace one processed snack with a piece of fruit",
            "Practice deep breathing when you feel stressed",
            "Drink a glass of water when you wake up",
            "End your day by writing down one thing you're grateful for"
        ]
        tip = random.choice(daily_tips)
        st.info(f"💡 Today's tip: {tip}")
    
    st.markdown("---")
    st.header("📈 Recommendation History")
    
    if hasattr(st.session_state, 'saved_recommendations') and st.session_state.saved_recommendations:
        for i, rec in enumerate(st.session_state.saved_recommendations[-3:]):
            st.markdown(f"**{i+1}.** {rec['timestamp'].strftime('%Y-%m-%d')}")
            st.write(f"Actions: {rec['total_recommendations']}")
    else:
        st.info("No saved recommendations yet.")
    
    st.markdown("---")
    st.header("🔗 Related Tools")
    
    if st.button("🔍 Risk Assessment"):
        st.switch_page("pages/01_Risk_Prediction.py")
    
    if st.button("🔮 Health Forecast"):
        st.switch_page("pages/05_Event_Forecasting.py")
    
    if st.button("🫀 Digital Twin"):
        st.switch_page("pages/04_Digital_Twin.py")
