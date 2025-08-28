import streamlit as st
import pandas as pd
import re
import preprocess, helper

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'Nirmala UI','Segoe UI Emoji'



# ---------------- Sidebar ----------------
st.sidebar.title("Whatsapp Chat Analyzer")

# Initialize state
if "show_analysis" not in st.session_state:
    st.session_state.show_analysis = False

uploaded_file = st.sidebar.file_uploader("Choose a file")

# Button that sets the state immediately
def start_analysis():
    st.session_state.show_analysis = True

if uploaded_file is not None:
    if not st.session_state.show_analysis:
        st.sidebar.button("Show Analysis", on_click=start_analysis)
else:
    st.session_state.show_analysis = False  # reset if no file uploaded

# ---------------- Instructions ----------------
if not st.session_state.show_analysis:
    st.title("📊 WhatsApp Chat Analyzer")
    st.markdown("""
    Welcome to the **WhatsApp Chat Analyzer**!  
    Follow these steps to use the tool:

    1. **Export your WhatsApp chat** (without media) from your phone.  
       - On WhatsApp:  
         `More → Export Chat → Without Media`  
    2. **Upload the exported `.txt` file** using the sidebar.  
    3. Select the **user** (or choose "Overall") for analysis.  
    4. Click on **Show Analysis** to view chat statistics, timelines, wordclouds, and more.  

    👉 Use the **sidebar** on the left to get started!
    """)

# ---------------- Analysis Section ----------------
if uploaded_file is not None and st.session_state.show_analysis:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.parse_whatsapp_chat(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # Stats Area
    num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
    st.title("Top Statistics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.header("Total Messages")
        st.title(num_messages)
    with col2:
        st.header("Total Words")
        st.title(words)
    with col3:
        st.header("Media Shared")
        st.title(num_media_messages)
    with col4:
        st.header("Links Shared")
        st.title(num_links)

    # find the most active users in group
    if selected_user == 'Overall':
        st.title("Most Busy Users")
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    # Monthly timeline
    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'], color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Daily timeline
    st.title("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Activity map
    st.title('Activity Map')
    col1, col2 = st.columns(2)
    with col1:
        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values, color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header("Most busy month")
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values, color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)

    # WordCloud
    st.title("Wordcloud")
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    ax.axis("off")   # hide axes for clean look
    st.pyplot(fig)

    # Most common words
    st.title('Most common words')
    most_common_df = helper.most_common_words(selected_user, df)
    fig, ax = plt.subplots()
    ax.barh(most_common_df['word'], most_common_df['count'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    # emoji analysis
    st.title("Emoji Analysis")
    emoji_df = helper.emoji_helper(selected_user, df)

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)

    with col2:
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            emoji_df['count'].head(),
            labels=emoji_df['emoji'].head(),
            autopct="%0.2f"
        )
        for t in texts:
            t.set_fontsize(12)
        for at in autotexts:
            at.set_fontsize(10)
        st.pyplot(fig)

        
