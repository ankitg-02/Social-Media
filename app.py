import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Social Media User Satisfaction Analysis",
    page_icon='📊',
    layout="wide"
)

# Load Data with Caching
@st.cache_data
def load_data():
    df = pd.read_csv('Time-Wasters on Social Media.csv')
    df.rename(columns=lambda x: x.strip(), inplace=True)
    if 'Watch Reason' in df.columns:
        df.rename(columns={'Watch Reason': 'Watch_Reason'}, inplace=True)
    if 'Video Category' in df.columns:
        df.rename(columns={'Video Category': 'Video_Category'}, inplace=True)
    df.drop(columns=['UserID', 'Video ID'], errors='ignore', inplace=True)
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header('🔍 Filter Data')
gender = st.sidebar.multiselect("Select Gender:", options=df['Gender'].dropna().unique(), default=df['Gender'].unique())
platform = st.sidebar.multiselect("Select Platform:", options=df['Platform'].dropna().unique(), default=df['Platform'].unique())
watch_reason = st.sidebar.multiselect("Select Watch Reason:", options=df['Watch_Reason'].dropna().unique(), default=df['Watch_Reason'].unique())
video_category = st.sidebar.multiselect("Select Video Category:", options=df['Video_Category'].dropna().unique(), default=df['Video_Category'].unique())

# Data Filtering
df_selection = df.query(
    "Gender == @gender & Platform == @platform & Watch_Reason == @watch_reason & Video_Category == @video_category"
)

st.write("📂 **Filtered Social Media Usage Data**")
st.dataframe(df_selection)

if df_selection.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust your selections.")
else:
    # KPIs Section
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

    left_col, right_col = st.columns(2)
    with left_col:
        st.subheader(f'⏳ Total Time Spent: 📌 {total_time_spent} mins')
        st.subheader(f'📊 Total Sessions: 📌 {total_sessions}')
        st.subheader(f'🎬 Total Videos Watched: 📌 {total_videos_watched}')
        st.subheader(f'📜 Total Scroll Rate: 📌 {total_scroll_rate}')

    with right_col:
        st.subheader(f'⏳ Average Time Spent: 📌 {avg_time_spent} mins')
        st.subheader(f'📊 Average Sessions: 📌 {avg_sessions}')
        st.subheader(f'🎬 Average Videos Watched: 📌 {avg_videos_watched}')
        st.subheader(f'📜 Average Scroll Rate: 📌 {avg_scroll_rate}')

   #General Data Distribution
st.markdown("<h2 style='text-align: center;'>📊Data Distribution</h2>", unsafe_allow_html=True)
    
dist_col1, dist_col2 = st.columns(2)
with dist_col1:
        st.subheader('📊 Time Spent Distribution')
        fig_time = px.histogram(df_selection, x='Total Time Spent', title='Time Spent Distribution')
        st.plotly_chart(fig_time)
        
        st.subheader('📊 Scroll Rate Distribution')
        fig_scroll = px.histogram(df_selection, x='Scroll Rate', title='Scroll Rate Distribution')
        st.plotly_chart(fig_scroll)
        
with dist_col2:
        st.subheader('📊 Time Spent on Video Distribution')
        fig_video_time = px.histogram(df_selection, x='Time Spent On Video', title='Time Spent on Video Distribution')
        st.plotly_chart(fig_video_time)
        
        st.subheader('📊 Videos Watched Distribution')
        fig_video = px.histogram(df_selection, x='Number of Videos Watched', title='Videos Watched Distribution')
        st.plotly_chart(fig_video)
        
    # Data Distribution Charts
st.markdown("<h2 style='text-align: center;'>📊 Data Distributions</h2>", unsafe_allow_html=True)
    
pie_col1, pie_col2, pie_col3 = st.columns(3)
    
with pie_col1:
        st.subheader('🎓 Profession Distribution')
        fig_prof = px.pie(df_selection, values='Number of Sessions', names='Profession', title="Profession Breakdown")
        st.plotly_chart(fig_prof)
        
        fig_prof1 = px.pie(df_selection, values='Satisfaction', names='Profession', title="Satisfaction by Profession")
        st.plotly_chart(fig_prof1)
    
with pie_col2:
        st.subheader('🌍 Demographics Distribution')
        fig_demo = px.pie(df_selection, values='Number of Sessions', names='Demographics', title="Demographics Breakdown")
        st.plotly_chart(fig_demo)
        
        fig_demo1 = px.pie(df_selection, values='Satisfaction', names='Demographics', title="Satisfaction by Demographics")
        st.plotly_chart(fig_demo1)
    
with pie_col3:
        st.subheader('📅 Frequency of Usage')
        fig_freq = px.pie(df_selection, values='Number of Sessions', names='Frequency', title="Usage Frequency")
        st.plotly_chart(fig_freq)
        
        fig_freq1 = px.pie(df_selection, values='Satisfaction', names='Frequency', title="Satisfaction by Frequency")
        st.plotly_chart(fig_freq1)

        
    # Count Analysis for Gender, Watch Reason, Platform, and Video Category
st.markdown("<h2 style='text-align: center;'>📊 Count Analysis</h2>", unsafe_allow_html=True)

count_col1, count_col2 = st.columns(2)

with count_col1:
    st.subheader('🧑‍🤝‍🧑 Gender Count')
    gender_count = df['Gender'].value_counts().reset_index()
    gender_count.columns = ['Category', 'Count']  # Renaming columns
    fig_gender = px.bar(gender_count, x='Category', y='Count', labels={'Category': 'Gender', 'Count': 'Count'})
    st.plotly_chart(fig_gender)

    st.subheader('📱 Platform Count')
    platform_count = df['Platform'].value_counts().reset_index()
    platform_count.columns = ['Category', 'Count']
    fig_platform = px.bar(platform_count, x='Category', y='Count', labels={'Category': 'Platform', 'Count': 'Count'})
    st.plotly_chart(fig_platform)


with count_col2:
    st.subheader('📌 Watch Reason Count')
    watch_reason_count = df['Watch_Reason'].value_counts().reset_index()
    watch_reason_count.columns = ['Category', 'Count']
    fig_watch_reason = px.bar(watch_reason_count, x='Category', y='Count', labels={'Category': 'Watch Reason', 'Count': 'Count'})
    st.plotly_chart(fig_watch_reason)
    
    st.subheader('🎥 Video Category Count')
    video_category_count = df['Video_Category'].value_counts().reset_index()
    video_category_count.columns = ['Category', 'Count']
    fig_video_category = px.bar(video_category_count, x='Category', y='Count', labels={'Category': 'Video Category', 'Count': 'Count'})
    st.plotly_chart(fig_video_category)

        
 
st.subheader("📊 Scroll Rate vs. Time Spent")
fig_scatter = px.scatter(df, x='Scroll Rate', y='Total Time Spent', 
                         color='Platform', 
                         title='Scroll Rate vs. Total Time Spent',
                         labels={'Scroll Rate': 'Scrolling Rate', 'Total Time Spent': 'Time Spent (mins)'},
                         size='Number of Sessions', hover_data=['Gender', 'Watch_Reason'])
st.plotly_chart(fig_scatter)

st.header("📱Platform-Wise Analysis")

st.subheader("📊 Time Spent across Platforms")
fig_box = px.box(df, x='Platform', y='Total Time Spent', 
                 color='Platform', 
                 title='Time Spent Distribution across Platforms')
st.plotly_chart(fig_box)

st.subheader("📊 Scrolling rate across Platforms")
fig_scroll_rate = px.bar(
    df.groupby('Platform', as_index=False)['Scroll Rate'].mean(),
    x='Platform',
    y='Scroll Rate',
    title="📌 Average Scroll Rate by Platform",
    color='Platform',
    text_auto=True
)
st.plotly_chart(fig_scroll_rate)

st.subheader("📊 No.of Sessions across Platforms")
fig_sessions = px.box(
    df,
    x="Platform",
    y="Number of Sessions",
    title="📌 Distribution of Number of Sessions by Platform",
    color="Platform"
)
st.plotly_chart(fig_sessions)

st.header("🧑‍🤝‍🧑 Gender-Wise Analysis")
st.subheader("📊 Average Time Spent on Video by Gender")
gender_time = df.groupby('Gender')['Total Time Spent'].mean().reset_index()
fig_bar = px.bar(gender_time, x='Gender', y='Total Time Spent', 
                 title="Average Time Spent on Social Media by Gender", 
                 labels={'Total Time Spent': 'Avg Time Spent (mins)'}, color='Gender')
st.plotly_chart(fig_bar)

st.subheader("📊 Average Scrolling Rate by Gender")
fig_scroll_rate = px.bar(
    df.groupby('Gender', as_index=False)['Scroll Rate'].mean(),
    x='Gender',
    y='Scroll Rate',
    title="📌 Average Scroll Rate by Gender",
    color='Gender',
    text_auto=True
)
st.plotly_chart(fig_scroll_rate)

st.subheader("📊 No. of Sessions by Gender")
fig_sessions = px.box(
    df,
    x="Gender",
    y="Number of Sessions",
    title="📌 Distribution of Number of Sessions by Gender",
    color="Gender"
)
st.plotly_chart(fig_sessions)

st.subheader("📊 Time Spend on Video by Gender")
fig_video_time = px.box(
    df,
    x="Gender",
    y="Time Spent On Video",
    title="📌 Distribution of Time Spent on Videos by Gender",
    color="Gender"
)
st.plotly_chart(fig_video_time)

st.subheader("📊 Time Spent on Video vs. Scroll Rate")
fig_scatter = px.scatter(df, x='Time Spent On Video', y='Scroll Rate',
                         color='Platform', 
                         title='Time Spent on Video vs. Scroll Rate',
                         labels={'Time Spent On Video': 'Time Spent on Video (mins)', 'Scroll Rate': 'Scrolling Rate'},
                         size='Number of Sessions')
st.plotly_chart(fig_scatter)

st.subheader("📊 Watch Reason vs. Time Spent")
watch_reason_time = df.groupby('Watch_Reason')['Total Time Spent'].mean().reset_index()
fig_watch_reason = px.bar(watch_reason_time, x='Watch_Reason', y='Total Time Spent', 
                          title="Average Time Spent per Watch Reason", 
                          labels={'Total Time Spent': 'Avg Time Spent (mins)'}, 
                          color='Watch_Reason')
st.plotly_chart(fig_watch_reason)


# Footer
st.markdown("""
    <div style="text-align: center; padding: 10px; font-size: 14px;">
        © Ankit Gochhayat | Built with Streamlit
    </div>
""", unsafe_allow_html=True)
