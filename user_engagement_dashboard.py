# ===============================
# User Engagement Analysis Dashboard
# ===============================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# -------------------------------
# Streamlit page configuration
# -------------------------------
st.set_page_config(page_title="User Engagement Dashboard", layout="wide")
st.title("📊 User Engagement Analysis Across Courses")

# -------------------------------
# Step 1: Load Dataset
# -------------------------------
 # <-- Update your path
df = pd.read_csv("data/e_learning_dataset_with_course_names.csv")

# -------------------------------
# Step 2: Clean Column Names
# -------------------------------
# Make all column names lowercase and strip spaces
df.rename(columns=lambda x: x.strip().lower(), inplace=True)

# Preview dataset
st.subheader("Dataset Preview")
st.dataframe(df.head())

# -------------------------------
# Step 3: Clean numeric columns
# -------------------------------
# Only keep numeric columns that exist in the dataset
all_numeric_cols = ['sessionsperweek', 'coursecompletion', 'usersatisfaction', 'quizscore']
numeric_cols = [col for col in all_numeric_cols if col in df.columns]

# Fill missing values for available numeric columns
for col in numeric_cols:
    df[col].fillna(df[col].mean(), inplace=True)

df.drop_duplicates(inplace=True)

# -------------------------------
# Step 4: Course filter dropdown
# -------------------------------
st.subheader("Filter by Course")
courses = df['coursename'].unique()
selected_courses = st.multiselect(
    "Select Course(s) to Analyze:",
    options=courses,
    default=list(courses)  # All courses selected by default
)

# Filter dataset
if selected_courses:
    filtered_df = df[df['coursename'].isin(selected_courses)]
else:
    filtered_df = df.copy()

st.write(f"Showing data for: {', '.join(selected_courses) if selected_courses else 'All Courses'}")
st.dataframe(filtered_df.head())

# -------------------------------
# Step 5: Average engagement metrics per course
# -------------------------------
if 'sessionsperweek' in numeric_cols:
    avg_sessions = filtered_df.groupby('coursename')['sessionsperweek'].mean().sort_values(ascending=False)
    st.subheader("Average Sessions Per Week by Course")
    st.bar_chart(avg_sessions)

if 'coursecompletion' in numeric_cols:
    avg_completion = filtered_df.groupby('coursename')['coursecompletion'].mean().sort_values(ascending=False)
    st.subheader("Average Course Completion by Course")
    st.bar_chart(avg_completion)

# -------------------------------
# Step 6: Correlation heatmap
# -------------------------------
st.subheader("Correlation Heatmap")
if numeric_cols:
    plt.figure(figsize=(8,6))
    sns.heatmap(filtered_df[numeric_cols].corr(), annot=True, cmap='Blues')
    st.pyplot(plt)
else:
    st.info("No numeric columns available for correlation heatmap.")

# -------------------------------
# -------------------------------
# -------------------------------
# Step 7: Dynamic Visualization - User Satisfaction vs Course Completion
# -------------------------------
st.subheader("Visualize User Satisfaction vs Course Completion")

# Chart type selector
chart_type = st.selectbox(
    "Select Chart Type:",
    options=["Scatter Plot", "Line Chart", "Pie Chart"]
)

if 'usersatisfaction' in numeric_cols and 'coursecompletion' in numeric_cols:
    
    # -------------------------------
    # SCATTER PLOT
    # -------------------------------
    if chart_type == "Scatter Plot":
        plt.figure(figsize=(10,6))
        sns.scatterplot(
            data=filtered_df,
            x='coursecompletion',
            y='usersatisfaction',
            hue='coursename',
            palette='tab10',
            s=150,
            edgecolor='black'
        )
        plt.xlabel("Course Completion (%)", fontsize=12)
        plt.ylabel("User Satisfaction", fontsize=12)
        plt.title("User Satisfaction vs Course Completion (Scatter Plot)", fontsize=14)
        plt.legend(title='Course', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)

    # -------------------------------
    # LINE CHART
    # -------------------------------
    elif chart_type == "Line Chart":
        plt.figure(figsize=(10,6))
        for course in filtered_df['coursename'].unique():
            course_data = filtered_df[filtered_df['coursename'] == course]
            course_data = course_data.sort_values('coursecompletion')
            plt.plot(
                course_data['coursecompletion'],
                course_data['usersatisfaction'],
                marker='o',
                linewidth=2,
                label=course
            )
        plt.xlabel("Course Completion (%)", fontsize=12)
        plt.ylabel("User Satisfaction", fontsize=12)
        plt.title("User Satisfaction vs Course Completion (Line Chart)", fontsize=14)
        plt.legend(title='Course', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(plt)

    # -------------------------------
    # PIE CHART
    # -------------------------------
    elif chart_type == "Pie Chart":
        avg_completion = filtered_df.groupby('coursename')['coursecompletion'].mean()
        plt.figure(figsize=(8,8))
        plt.pie(
            avg_completion,
            labels=avg_completion.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=sns.color_palette('tab10', len(avg_completion))
        )
        plt.title("Proportion of Average Course Completion by Course (Pie Chart)", fontsize=14)
        st.pyplot(plt)

else:
    st.info("Required numeric columns ('usersatisfaction' and 'coursecompletion') are not available for visualization.")


# -------------------------------
# Step 8: Key Insights
# -------------------------------
if not filtered_df.empty:
    st.subheader("Key Insights")
    if 'sessionsperweek' in numeric_cols:
        top_course_sessions = filtered_df.groupby('coursename')['sessionsperweek'].mean().idxmax()
        st.markdown(f"🔥 **Course with Highest Average Sessions Per Week:** {top_course_sessions}")
    if 'coursecompletion' in numeric_cols:
        top_course_completion = filtered_df.groupby('coursename')['coursecompletion'].mean().idxmax()
        st.markdown(f"✅ **Course with Highest Average Completion:** {top_course_completion}")
    st.markdown("📊 Time spent and course completion correlate with user satisfaction where data is available.")
else:
    st.warning("No data available for the selected course(s).")
