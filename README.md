# Git-Gazer: The GitHub Profile Analyzer

## Project Overview

Git-Gazer is an interactive web application built with Streamlit that allows users to analyze any public GitHub profile. By entering a username, the app fetches data from the official GitHub API and generates a dashboard with insightful visualizations about the user's coding habits, repository popularity, and activity over time.

This project showcases skills in API integration, data manipulation with Pandas, and building interactive, user-facing data products with Streamlit and Plotly.

## Key Features

- **Authenticated API Integration:** Securely connects to the GitHub REST API using a personal access token managed via environment variables.
- **Dynamic User Interface:** Users can input any GitHub username to generate a new report on the fly.
- **Comprehensive Profile Summary:** Displays key user statistics, including bio, follower count, and a direct link to their profile.
- **Insightful Visualizations:**
    - **Language Distribution:** An interactive pie chart showing the breakdown of primary programming languages used.
    - **Repository Popularity:** A bar chart of the top 10 most-starred repositories.
    - **Creation Timeline:** A line chart illustrating the user's repository creation activity year over year.
- **Efficient Data Handling:** Uses Streamlit's caching (`@st.cache_data`) to minimize redundant API calls and improve app performance.

## Screenshot of the Dashboard

![Dashboard Screenshot](<img width="1348" height="654" alt="github_analyzer_screenshot2" src="https://github.com/user-attachments/assets/0e5a0d25-76cf-4d63-8ac2-8363e4d70f0b" />
) 
<img width="825" height="572" alt="github_analyzer_screenshot" src="https://github.com/user-attachments/assets/6d7f7e2e-afac-4dbd-8798-4074bf00b03d" />

## Tech Stack

- **Language:** Python
- **Web Framework:** Streamlit
- **Data Manipulation:** Pandas
- **API Interaction:** Requests
- **Data Visualization:** Plotly Express
- **Secret Management:** python-dotenv

## How to Run Locally

1.  Clone this repository.
2.  Create a virtual environment and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Create a `.env` file in the root directory.
4.  Add your GitHub Personal Access Token to the `.env` file:
    ```
    GITHUB_TOKEN=your_personal_access_token_here
    ```
5.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
