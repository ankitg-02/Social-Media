import streamlit as st
import numpy as np
import pickle

# Load model and scaler
with open('random_forest.pkl', 'rb') as f:
    model = pickle.load(f)

with open('standard_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

st.title("Social Media Satisfaction Prediction")

# Input options
gender_options = ['Male', 'Female', 'Other']
profession_options = ['Student', 'Working Professional', 'Unemployed', 'Others']
demographic_options = ['Urban', 'Rural', 'Suburban']
platform_options = ['Instagram', 'Facebook', 'Twitter', 'LinkedIn', 'Snapchat', 'Other']

# Collect user input
age = st.slider('Age', 13, 65, 25)
gender = st.selectbox('Gender', gender_options)
profession = st.selectbox('Profession', profession_options)
demographic = st.selectbox('Demographic Location', demographic_options)
platform = st.selectbox('Preferred Social Media Platform', platform_options)

# Encode categorical values (must match training encodings)
gender_map = {'Male': 0, 'Female': 1, 'Other': 2}
profession_map = {'Student': 0, 'Working Professional': 1, 'Unemployed': 2, 'Others': 3}
demographic_map = {'Urban': 0, 'Rural': 1, 'Suburban': 2}
platform_map = {'Instagram': 0, 'Facebook': 1, 'Twitter': 2, 'LinkedIn': 3, 'Snapchat': 4, 'Other': 5}

# Feature vector
features = np.array([
    age,
    gender_map[gender],
    profession_map[profession],
    demographic_map[demographic],
    platform_map[platform]
]).reshape(1, -1)

# Scale the features
scaled_features = scaler.transform(features)

# Predict
if st.button('Predict Satisfaction Score'):
    prediction = model.predict(scaled_features)
    st.success(f"Predicted Satisfaction Score: {prediction[0]:.2f}")
