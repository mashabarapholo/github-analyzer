# In app.py (Final Version with Charts)

import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Git-Gazer: GitHub Profile Analyzer",
    page_icon="🔭",
    layout="wide"
)

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# --- API CALLER FUNCTION ---
@st.cache_data(ttl=3600) # Cache data for 1 hour to avoid hitting API limits
def get_github_data(username):
    if not username:
        return None, None
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    user_url = f"https://api.github.com/users/{username}"
    user_response = requests.get(user_url, headers=headers)
    if user_response.status_code != 200:
        return {"error": "User not found or API rate limit exceeded."}, None
    user_data = user_response.json()

    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    all_repos = []
    page = 1
    while True:
        repos_response = requests.get(f"{repos_url}&page={page}", headers=headers)
        if repos_response.status_code != 200: break
        repos_data = repos_response.json()
        if not repos_data: break
        all_repos.extend(repos_data)
        page += 1
    return user_data, all_repos

# --- MAIN APP LAYOUT ---
st.title("🔭 Git-Gazer")
st.subheader("Analyze any public GitHub profile!")

username = st.text_input("Enter a GitHub Username:", "streamlit")

if st.button("Analyze Profile"):
    with st.spinner("Fetching data from GitHub API... This might take a moment."):
        user_data, repos_data = get_github_data(username)

    if user_data and "error" in user_data:
        st.error(user_data["error"])
    elif user_data and repos_data is not None:
        st.success(f"Successfully fetched data for {user_data.get('name', username)}!")

        # --- DISPLAY USER PROFILE ---
        st.header("User Profile")
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(user_data['avatar_url'], width=150)
        with col2:
            st.write(f"**Name:** {user_data.get('name', 'N/A')}")
            st.write(f"**Bio:** {user_data.get('bio', 'N/A')}")
            st.write(f"**Followers:** {user_data.get('followers', 0)} | **Following:** {user_data.get('following', 0)}")
            st.write(f"**Public Repos:** {user_data.get('public_repos', 0)}")
            st.link_button("View Profile on GitHub", user_data['html_url'])

        st.markdown("---")

        if repos_data:
            repos_df = pd.DataFrame(repos_data)
            
            # --- START OF NEW ANALYSIS AND VISUALIZATION CODE ---

            st.header("Language Analysis")
            
            # 1. Analyze Programming Language Usage
            lang_stats = repos_df['language'].value_counts().dropna()
            if not lang_stats.empty:
                fig_langs = px.pie(
                    lang_stats,
                    values=lang_stats.values,
                    names=lang_stats.index,
                    title="Primary Languages Used in Repositories"
                )
                fig_langs.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_langs, use_container_width=True)
            else:
                st.write("No language data available for repositories.")

            st.header("Repository Popularity")
            
            # 2. Analyze Top 10 Most Starred Repositories
            top_starred_repos = repos_df.sort_values(by='stargazers_count', ascending=False).head(10)
            if not top_starred_repos.empty:
                fig_stars = px.bar(
                    top_starred_repos,
                    x='name',
                    y='stargazers_count',
                    title='Top 10 Most Starred Repositories',
                    labels={'name': 'Repository', 'stargazers_count': 'Number of Stars ⭐'}
                )
                st.plotly_chart(fig_stars, use_container_width=True)
            else:
                st.write("No starred repositories found.")

            st.header("Repository Creation Timeline")
            
            # 3. Analyze Activity Over Time
            repos_df['created_at'] = pd.to_datetime(repos_df['created_at'])
            repos_over_time = repos_df.set_index('created_at').resample('Y').size().reset_index(name='count')
            repos_over_time['year'] = repos_over_time['created_at'].dt.year
            
            if not repos_over_time.empty:
                fig_timeline = px.line(
                    repos_over_time,
                    x='year',
                    y='count',
                    title='Repositories Created Over Time',
                    labels={'year': 'Year', 'count': 'Number of Repositories Created'}
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
            else:
                st.write("No repository creation data available.")
            
            # --- END OF NEW ANALYSIS AND VISUALIZATION CODE ---

            st.header("All Repositories")
            display_df = repos_df[['name', 'language', 'stargazers_count', 'forks_count', 'created_at']]
            display_df = display_df.rename(columns={
                'name': 'Repository Name', 'language': 'Primary Language',
                'stargazers_count': 'Stars ⭐', 'forks_count': 'Forks 🍴',
                'created_at': 'Creation Date'
            })
            st.dataframe(display_df.sort_values(by='Stars ⭐', ascending=False))
        else:
            st.write("No public repositories found for this user.")