import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="National Park Attendance Explorer", layout="wide")
st.title("National Park Attendance & Activities Explorer")

# Page selector
page = st.sidebar.radio(
    "Choose a page:",
    ["Yearly Attendance Explorer", "Activity-Based Park Explorer"]
)

# Load data
def load_data():
    df = pd.read_csv('final.csv')
    # Clean up numeric columns
    for col in ['total visits', 'annual visits']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '')
            df[col] = pd.to_numeric(df[col], errors='coerce')
    if 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
    return df

df = load_data()


activity_cols = [col for col in df.columns if col.startswith('activity_')]
activity_names = [col.replace('activity_', '').replace('_', ' ').title() for col in activity_cols]
activity_map = dict(zip(activity_names, activity_cols))

selected_activities = []  # Default to empty list to avoid NameError


if page == "Yearly Attendance Explorer":
    # Year selector for annual visits
    st.sidebar.header("Year Filter")
    if 'year' in df.columns:
        years = sorted(df['year'].dropna().unique().astype(int))
        selected_year = st.sidebar.selectbox('Select year for annual visits analysis:', years, index=len(years)-1)
        df_year = df[df['year'] == selected_year]
    else:
        selected_year = None
        df_year = df

    # Show top 10 most visited parks for selected year (annual visits)
    if selected_year is not None:
        st.header(f"Top 10 Most Visited Parks in {selected_year}")
        top10_year = df_year.drop_duplicates(subset='fullName').sort_values('annual visits', ascending=False).head(10)
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        sns.barplot(x=top10_year['fullName'], y=top10_year['annual visits'], palette='crest', ax=ax3)
        ax3.set_ylabel('Annual Visitors')
        ax3.set_xlabel('National Park')
        ax3.set_title(f'Top 10 Most Visited National Parks in {selected_year}')
        plt.xticks(rotation=30, ha='right')
        st.pyplot(fig3)

    # Show overall top 10 most visited parks (total visits)
    st.header("Top 10 Most Visited Parks (All Years)")
    top10 = df.drop_duplicates(subset='fullName').sort_values('total visits', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=top10['fullName'], y=top10['total visits'], palette='viridis', ax=ax)
    ax.set_ylabel('Total Visitors')
    ax.set_xlabel('National Park')
    ax.set_title('Top 10 Most Visited National Parks (All Years)')
    plt.xticks(rotation=30, ha='right')
    st.pyplot(fig)

elif page == "Activity-Based Park Explorer":
    st.sidebar.header("Activity Filter")
    selected_activities = st.sidebar.multiselect(
        "Select activities (parks must have all):",
        activity_names
    )
    df_filtered = df.copy()
    if selected_activities:
        for act in selected_activities:
            df_filtered = df_filtered[df_filtered[activity_map[act]] == 1]
    st.header("Top 10 Most Visited Parks (Filtered by Activities)")
    if not df_filtered.empty:
        top10_act = df_filtered.drop_duplicates(subset='fullName').sort_values('total visits', ascending=False).head(10)
        fig_act, ax_act = plt.subplots(figsize=(12, 6))
        sns.barplot(x=top10_act['fullName'], y=top10_act['total visits'], palette='viridis', ax=ax_act)
        ax_act.set_ylabel('Total Visitors')
        ax_act.set_xlabel('National Park')
        ax_act.set_title('Top 10 Most Visited Parks (Filtered by Activities)')
        plt.xticks(rotation=30, ha='right')
        st.pyplot(fig_act)
    else:
        st.info("No parks match the selected activities.")


