import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# Load data
@st.cache_data
def load_data():
    social = pd.read_csv('Time-Wasters on Social Media.csv')
    return social

data = load_data()
st.title("User Satisfaction Prediction")

# Display dataset information
st.write("### Dataset Overview")
st.write(data.describe())

# Ensure only numerical columns are used for correlation
numeric_data = data.select_dtypes(include=[np.number])
if not numeric_data.empty:
    st.write("### Correlation Heatmap")
    fig_corr = px.imshow(numeric_data.corr(), text_auto=True, title="Feature Correlation")
    st.plotly_chart(fig_corr)

# Data Preprocessing
mod_data = data.copy()
mod_data = mod_data.drop(['UserID', 'Location', 'Income', 'Debt', 'Owns Property', 'Video Length', 'Importance Score', 'OS'], axis=1, errors='ignore')
mod_data = mod_data.dropna()

encoding_mappings = {
    'Demographics': {'Rural': 0, 'Urban': 1},
    'Gender': {'Male': 1, 'Female': 2, 'Other': 3},
    'ConnectionType': {'Mobile Data': 1, 'Wi-Fi': 2},
    'Profession': {'Students': 1, 'Waiting staff': 2, 'Labor/Worker': 3, 'Driver': 4, 'Engineer': 5,
                   'Cashier': 6, 'Manager': 7, 'Artist': 8, 'Teacher': 9},
    'Platform': {'TikTok': 1, 'Instagram': 2, 'YouTube': 3, 'Facebook': 4},
    'DeviceType': {'Smartphone': 1, 'Tablet': 2, 'Computer': 3},
    'Watch Reason': {'Habit': 1, 'Boredom': 2, 'Entertainment': 3, 'Procrastination': 4},
    'CurrentActivity': {'At home': 1, 'At school': 2, 'At work': 3, 'Commuting': 4},
    'Frequency': {'Evening': 1, 'Night': 2, 'Afternoon': 3, 'Morning': 4},
    'Video Category': {'Jokes/Memes': 1, 'Life Hacks': 2, 'Gaming': 3, 'Vlogs': 4, 'Pranks': 5,
                       'Entertainment': 6, 'Trends': 7, 'ASMR': 8, 'Comedy': 9}
}

for column, mapping in encoding_mappings.items():
    if column in mod_data.columns:
        mod_data[column] = mod_data[column].map(mapping).astype(float)

mod_data = mod_data.apply(pd.to_numeric, errors='coerce')
mod_data = mod_data.dropna()

# Feature selection
target = 'Satisfaction'
if target in mod_data.columns:
    feature_options = [col for col in mod_data.columns if col != target]
else:
    feature_options = mod_data.columns.tolist()

features = st.multiselect("Select Features", feature_options, default=feature_options[:min(5, len(feature_options))])

if features and target in mod_data.columns and not mod_data.empty:
    X = mod_data[features]
    y = mod_data[target]

    if len(X) > 0:
        # Splitting data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
        
        # Standardizing data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Model selection
        model_choice = st.selectbox("Choose Model", ["Random Forest", "Gradient Boosting"])
        if model_choice == "Random Forest":
            model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=30)
        else:
            model = GradientBoostingRegressor(n_estimators=200, max_depth=5, random_state=30)
        
        # Train model
        model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = model.predict(X_test_scaled)
        
        # Model evaluation
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        st.write(f"### Model Performance: \n - Mean Squared Error: {mse:.2f} \n - R-squared: {r2:.2f}")
        
        # Feature Importance
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({'Feature': features, 'Importance': importance}).sort_values(by='Importance', ascending=False)
            
            st.write("### Feature Importance")
            fig = px.bar(feature_importance_df, x='Importance', y='Feature', orientation='h', title='Feature Importance', labels={'Importance': 'Importance Score', 'Feature': 'Feature'})
            st.plotly_chart(fig)
        
        # User inputs for prediction
        st.write("### Predict Your Satisfaction Score")
        user_inputs = [st.selectbox(f"{feature}", list(encoding_mappings[feature].keys())) if feature in encoding_mappings else st.number_input(f"{feature}") for feature in features]
        user_data = np.array([encoding_mappings[feature][user_inputs[i]] if feature in encoding_mappings else user_inputs[i] for i, feature in enumerate(features)]).astype(float)
        user_data_scaled = scaler.transform([user_data])
        
        if st.button("Predict Satisfaction"):
            prediction = model.predict(user_data_scaled)
            st.success(f'Predicted Satisfaction Score: {prediction[0]:.2f}')
    else:
        st.error("Insufficient data to split. Please select different features or check dataset content.")
