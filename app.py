import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Social Media User Satisfaction Analysis",
    page_icon='📊',
    layout="wide"
)

social = pd.read_csv(r'Time-Wasters on Social Media.csv')
df = social.copy()

if 'Watch Reason' in df.columns:
    df.rename(columns={'Watch Reason': 'Watch_Reason'}, inplace=True)
if 'Video Category' in df.columns:
    df.rename(columns={'Video Category': 'Video_Category'}, inplace=True)

# Sidebar
st.sidebar.header('🔍 Filter Data')
gender = st.sidebar.multiselect("Select Gender:", options=df['Gender'].dropna().unique(), default=df['Gender'].unique())
platform = st.sidebar.multiselect("Select Platform:", options=df['Platform'].dropna().unique(), default=df['Platform'].unique())
watch_reason = st.sidebar.multiselect("Select Watch Reason:", options=df['Watch_Reason'].dropna().unique(), default=df['Watch_Reason'].unique())
video_category = st.sidebar.multiselect("Select Video Category:", options=df['Video_Category'].dropna().unique(), default=df['Video_Category'].unique())
device_type = st.sidebar.multiselect("Select Device Type:", options=df['DeviceType'].dropna().unique(), default=df['DeviceType'].unique())
connection_type = st.sidebar.multiselect("Select Connection Type:", options=df['ConnectionType'].dropna().unique(), default=df['ConnectionType'].unique())

df_selection = df.query(
    "Gender == @gender & Platform == @platform & Watch_Reason == @watch_reason & Video_Category == @video_category & DeviceType == @device_type & ConnectionType == @connection_type"
)

st.write("📂 **Filtered Social Media Usage Data**")
st.dataframe(df_selection)

# Check if data is available after filtering
if df_selection.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust your selections.")
else:
    # KPIs
    st.markdown("<h2 style='text-align: center'>📌 Key Performance Indicators</h2>", unsafe_allow_html=True)

    total_time_spent = int(df_selection['Total Time Spent'].sum())
    avg_time_spent = round(df_selection['Total Time Spent'].mean(), 1)
    
    total_sessions = int(df_selection['Number of Sessions'].sum())
    avg_sessions = round(df_selection['Number of Sessions'].mean(), 1)
    
    total_scroll_rate = int(df_selection['Scroll Rate'].sum())
    avg_scroll_rate = round(df_selection['Scroll Rate'].mean(), 1)
    
    total_time_on_video = int(df_selection['Time Spent On Video'].sum())
    avg_time_on_video = round(df_selection['Time Spent On Video'].mean(), 1)
    
    total_videos_watched = int(df_selection['Number of Videos Watched'].sum())
    avg_videos_watched = round(df_selection['Number of Videos Watched'].mean(), 1)

    # KPIs in two columns
    left_col, right_col = st.columns(2)
    with left_col:
        st.subheader('⏳ Total Time Spent:')
        st.subheader(f'📌 {total_time_spent} mins')

        st.subheader('📊 Total No. of Sessions:')
        st.subheader(f'📌 {total_sessions}')

        st.subheader('🎬 Total No. of Videos Watched:')
        st.subheader(f'📌 {total_videos_watched}')

        st.subheader('📜 Total Scroll Rate:')
        st.subheader(f'📌 {total_scroll_rate}')

    with right_col:
        st.subheader('⏳ Average Time Spent:')
        st.subheader(f'📌 {avg_time_spent} mins')

        st.subheader('📊 Average No. of Sessions:')
        st.subheader(f'📌 {avg_sessions}')

        st.subheader('🎬 Average No. of Videos Watched:')
        st.subheader(f'📌 {avg_videos_watched}')

        st.subheader('📜 Average Scroll Rate:')
        st.subheader(f'📌 {avg_scroll_rate}')
        
    # Data Distributions
    st.markdown("<h2 style='text-align: center; color: white;'>📊 Data Distributions</h2>", unsafe_allow_html=True)

    pie_col1, pie_col2, pie_col3 = st.columns(3)
    
    with pie_col1:
        st.subheader('🎓 Profession Distribution')
        fig_prof = px.pie(df_selection, values='Number of Sessions', names='Profession', title="Profession Breakdown")
        st.plotly_chart(fig_prof)

    with pie_col2:
        st.subheader('🌍 Demographics Distribution')
        fig_demo = px.pie(df_selection, values='Satisfaction', names='Demographics', title="Demographics Breakdown")
        st.plotly_chart(fig_demo)

    with pie_col3:
        st.subheader('📅 Frequency of Usage')
        fig_freq = px.pie(df_selection, values='Number of Sessions', names='Frequency', title="Usage Frequency")
        st.plotly_chart(fig_freq)
