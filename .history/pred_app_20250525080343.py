import streamlit as st
import numpy as np
import pickle


with open('random_forest.pkl', 'rb') as f:
    model = pickle.load(f)

with open('standard_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

st.set_page_config(page_title="Social Media Satisfaction Predictor")
st.title("📱 Social Media Satisfaction Prediction")

st.markdown("""
Provide your basic information and preferences below.  
The model will predict how satisfied you are likely to be with your social media experience.
""")


gender_options = ['Male', 'Female', 'Other']
profession_options = ['Student', 'Working Professional', 'Unemployed', 'Others']
demographic_options = ['Urban', 'Rural', 'Suburban']
platform_options = ['Instagram', 'Facebook', 'Twitter', 'LinkedIn', 'Snapchat', 'Other']
video_category_options = ['Entertainment', 'Education', 'News', 'Gaming', 'Lifestyle', 'Other']


age = st.slider('Age', 13, 65, 25)
gender = st.selectbox('Gender', gender_options)
profession = st.selectbox('Profession', profession_options)
demographic = st.selectbox('Demographic Location', demographic_options)
platform = st.selectbox('Preferred Social Media Platform', platform_options)
video_time = st.slider("Time Spent Watching Videos (minutes/day)", 0, 300, 60)
video_category = st.selectbox("Primary Video Category Watched", video_category_options)


gender_map = {'Male': 0, 'Female': 1, 'Other': 2}
profession_map = {'Student': 0, 'Working Professional': 1, 'Unemployed': 2, 'Others': 3}
demographic_map = {'Urban': 0, 'Rural': 1, 'Suburban': 2}
platform_map = {'Instagram': 0, 'Facebook': 1, 'Twitter': 2, 'LinkedIn': 3, 'Snapchat': 4, 'Other': 5}
video_category_map = {
    'Entertainment': 0,
    'Education': 1,
    'News': 2,
    'Gaming': 3,
    'Lifestyle': 4,
    'Other': 5
}

user_features = [
    age,
    gender_map[gender],
    profession_map[profession],
    demographic_map[demographic],
    platform_map[platform],
    video_time,
    video_category_map[video_category]
]

dummy_values = [0] * (19 - len(user_features))
final_input = np.array(user_features + dummy_values).reshape(1, -1)

scaled_input = scaler.transform(final_input)

if st.button('🔮 Predict Satisfaction Score'):
    prediction = model.predict(scaled_input)
    st.success(f"📊 Predicted Satisfaction Score: **{prediction[0]:.2f}** (out of 10)")
