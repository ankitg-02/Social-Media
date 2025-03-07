import streamlit as st
import pandas as pd
import plotly.express as py

social=pd.read_csv(r'Time-Wasters on Social Media.csv')
df=pd.DataFrame(social)
df_1=df.copy()
st.set_page_config(page_title="Social Media User Satisfaction Analysis",
                page_icon='bar_chart')

df_1['Watch_Reason']=df_1['Watch Reason']
df_1['Video_Category']=df_1['Video Category']

#

st.write("Social Media Usage Dataset")
st.sidebar.header('Please give the correct values:')
gender=st.sidebar.multiselect(
    "Select the Gender",
    options=df_1['Gender'].unique(),
    default=df_1['Gender'].unique()
)

platform=st.sidebar.multiselect(
    "Select the Platform:",
    options=df_1['Platform'].unique(),
    default=df_1['Platform'].unique()
)

watch_reason=st.sidebar.multiselect(
    "Select the Watch Reason:",
    options=df_1['Watch_Reason'].unique(),
    default=df_1['Watch_Reason'].unique()
)

video_category=st.sidebar.multiselect(
    "Select the Video Category:",
    options=df_1['Video_Category'].unique(),
    default=df_1['Video_Category'].unique()
)

device_type=st.sidebar.multiselect(
    "Select the Device Type:",
    options=df_1['DeviceType'].unique(),
    default=df_1['DeviceType'].unique()
)

connection_type=st.sidebar.multiselect(
    "Select the Connection Type:",
    options=df_1['ConnectionType'].unique(),
    default=df_1['ConnectionType'].unique()
)

df_selection=df_1.query(
    "Gender==@gender & Platform==@platform  & Watch_Reason==@watch_reason & Video_Category==@video_category & DeviceType==@device_type & ConnectionType==@connection_type"
)
st.dataframe(df_selection)

####################################################################################################

title = "<u><b><h1 style='text-align: center; color: white;'>Key Performance Indicators</h1></u></b>"
st.markdown(title, unsafe_allow_html=True)

####################################################################################################

total_time_spent=round(int(df_selection['Total Time Spent'].sum()),1)
avg_time_spent=round(int(df_selection['Total Time Spent'].mean()),1)
####################################
total_session=round(int(df_selection['Number of Sessions'].sum()),1)
avg_session=round(int(df_selection['Number of Sessions'].mean()),1)
####################################
total_scroll_rate=round(int(df_selection['Scroll Rate'].sum()),1)
avg_scroll_rate=round(int(df_selection['Scroll Rate'].mean()),1)
####################################
total_time_spent_on_video=round(int(df_selection['Time Spent On Video'].sum()),1)
avg_time_spent_on_video=round(int(df_selection['Time Spent On Video'].mean()),1)
###################################
total_no_of_videos_watched=round(int(df_selection['Number of Videos Watched'].sum()),1)
avg_no_of_videos_watched=round(int(df_selection['Number of Videos Watched'].mean()),1)

####################################################################################################

left_colummn , right_column =st.columns(2)
with left_colummn:
    st.subheader('Total Time Spend:')
    st.subheader(f'{total_time_spent}mins')
    #---------------------------------------
    st.subheader('Total No. of Sessions:')
    st.subheader(f'{total_session}')
    #---------------------------------------
    st.subheader('Total No. of Videos Watched:')
    st.subheader(f'{total_no_of_videos_watched}')
    #----------------------------------------
    st.subheader('Total No. of Scroll Rate:')
    st.subheader(f'{total_scroll_rate}')
with right_column:
    st.subheader('Average Time Spend:')
    st.subheader(f'{avg_time_spent}mins')
    #---------------------------------------
    st.subheader('Average No. of Session:')
    st.subheader(f'{avg_session}')
    #------------------------------------
    st.subheader('Average No. of Videos Watched:')
    st.subheader(f'{avg_no_of_videos_watched}')
    #------------------------------------
    st.subheader('Average No. of Scroll Rate:')
    st.subheader(f'{avg_scroll_rate}')
    
####################################################################################################
    fig = py.line(df_selection,x="Total Time Spend",y="Satisfaction")
    st.plotly_chart(fig)