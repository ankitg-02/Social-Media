import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# Load Data Function
def load_data():
    try:
        df = pd.read_csv(r'Time-Wasters on Social Media.csv')
        df.rename(columns=lambda x: x.strip().replace(' ', '_'), inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Page Configuration
st.set_page_config(
    page_title="Social Media Satisfaction Analysis",
    page_icon='📊',
    layout="wide"
)

# Sidebar Features
st.sidebar.header('🔍 Filters')
mode = st.sidebar.radio("Select Mode:", ["Light", "Dark"])
data_refresh = st.sidebar.button("🔄 Refresh Data")

df = load_data()
if df.empty:
    st.stop()

# Dynamic Filters
filters = {
    "Gender": df.get('Gender', pd.Series()).dropna().unique(),
    "Platform": df.get('Platform', pd.Series()).dropna().unique(),
    "Watch_Reason": df.get('Watch_Reason', pd.Series()).dropna().unique(),
    "Video_Category": df.get('Video_Category', pd.Series()).dropna().unique(),
    "DeviceType": df.get('DeviceType', pd.Series()).dropna().unique(),
    "ConnectionType": df.get('ConnectionType', pd.Series()).dropna().unique()
}

selected_filters = {k: st.sidebar.multiselect(f"Select {k}:", options=v, default=v) for k, v in filters.items()}
total_time_range = st.sidebar.slider("Filter by Total Time Spent:", int(df["Total_Time_Spent"].min()), int(df["Total_Time_Spent"].max()), (int(df["Total_Time_Spent"].min()), int(df["Total_Time_Spent"].max())))

query_str = " & ".join([f"{key} in @selected_filters[\"{key}\"]" for key in selected_filters if selected_filters[key]])
df_selection = df.query(query_str) if query_str else df
df_selection = df_selection[(df_selection["Total_Time_Spent"] >= total_time_range[0]) & (df_selection["Total_Time_Spent"] <= total_time_range[1])]

st.write("📂 **Filtered Social Media Usage Data**")
st.dataframe(df_selection)

if df_selection.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust your selections.")
else:
    st.markdown("<h2 style='text-align: center'>📌 Key Performance Indicators</h2>", unsafe_allow_html=True)
    
    kpi_cols = st.columns(4)
    metrics = {
        '⏳ Total Time Spent': df_selection['Total_Time_Spent'].sum(),
        '📊 Total Sessions': df_selection['Number_of_Sessions'].sum(),
        '🎬 Videos Watched': df_selection['Number_of_Videos_Watched'].sum(),
        '📜 Scroll Rate': df_selection['Scroll_Rate'].sum()
    }
    
    for col, (metric, value) in zip(kpi_cols, metrics.items()):
        col.metric(label=metric, value=f"{value}")
    
    # Data Visualizations with Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📉 Trends", "🔎 Insights"])
    
    with tab1:
        chart_cols = st.columns(3)
        with chart_cols[0]:
            fig_prof = px.pie(df_selection, values='Number_of_Sessions', names='Profession', title="Profession Breakdown")
            st.plotly_chart(fig_prof)
        with chart_cols[1]:
            fig_demo = px.pie(df_selection, values='Satisfaction', names='Demographics', title="Demographics Breakdown")
            st.plotly_chart(fig_demo)
        with chart_cols[2]:
            fig_freq = px.bar(df_selection, x='Frequency', y='Number_of_Sessions', title="Usage Frequency", color='Frequency')
            st.plotly_chart(fig_freq)
    
    with tab2:
        fig_time = px.scatter(df_selection, x='Platform', y='Total_Time_Spent', color='Platform', size='Total_Time_Spent', title="Time Spent on Social Media Platforms", animation_frame='Platform')
        st.plotly_chart(fig_time)
    
    with tab3:
        fig_corr = px.imshow(df_selection.corr(), color_continuous_scale='blues', title='Feature Correlation Heatmap')
        st.plotly_chart(fig_corr)
    
    # Dark Mode Styling
    if mode == "Dark":
        st.markdown(""" <style> body { background-color: #1e1e1e; color: white; } </style> """, unsafe_allow_html=True)

st.sidebar.write("👨‍💻 Built with ❤️ using Streamlit & Plotly")
