import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Student Mental Health Analytics",
    layout="wide"
)

# -----------------------------
# Global Plot Style (BLENDS WITH STREAMLIT)
# -----------------------------
plt.style.use("seaborn-v0_8-whitegrid")

# -----------------------------
# Subtle KPI Styling
# -----------------------------
st.markdown(
    """
    <style>
    div[data-testid="metric-container"] {
        background-color: #f6f7f9;
        padding: 14px;
        border-radius: 8px;
        border: 1px solid #e6e6e6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Header
# -----------------------------
st.markdown("## Student Mental Health Analytics Dashboard")
st.markdown(
    "Population-level insights derived from self-reported mental health and lifestyle indicators "
    "to support awareness and data-driven understanding."
)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data/student_mental_health.csv")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

selected_course = st.sidebar.selectbox(
    "Course Level",
    options=["All"] + sorted(df["course_level"].unique().tolist())
)

selected_gender = st.sidebar.selectbox(
    "Gender",
    options=["All"] + sorted(df["gender"].unique().tolist())
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()

if selected_course != "All":
    filtered_df = filtered_df[filtered_df["course_level"] == selected_course]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == selected_gender]

# -----------------------------
# KPI Section
# -----------------------------
st.divider()
st.subheader("Key Metrics Overview")
st.caption("Aggregated indicators based on the selected filters")

avg_stress = filtered_df["stress_score"].mean()
avg_sleep = filtered_df["sleep_hours"].mean()
avg_anxiety = filtered_df["anxiety_score"].mean()
high_stress_pct = (filtered_df["stress_score"] >= 7).mean() * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Stress Score", f"{avg_stress:.1f}")
col2.metric("Average Sleep (hrs)", f"{avg_sleep:.1f}")
col3.metric("Average Anxiety Score", f"{avg_anxiety:.1f}")
col4.metric("High Stress Records (%)", f"{high_stress_pct:.1f}%")

# -----------------------------
# Distribution Analysis
# -----------------------------
st.divider()
st.subheader("Distribution Analysis")

# Stress Distribution
fig1, ax1 = plt.subplots()
fig1.patch.set_facecolor("#f6f7f9")
ax1.set_facecolor("#f6f7f9")

ax1.hist(filtered_df["stress_score"], bins=10, edgecolor="none")
ax1.set_xlabel("Stress Score")
ax1.set_ylabel("Number of Records")
ax1.set_title("Distribution of Stress Scores")

ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

st.pyplot(fig1)

# Sleep Distribution
fig2, ax2 = plt.subplots()
fig2.patch.set_facecolor("#f6f7f9")
ax2.set_facecolor("#f6f7f9")

ax2.hist(filtered_df["sleep_hours"], bins=10, edgecolor="none")
ax2.set_xlabel("Sleep Hours")
ax2.set_ylabel("Number of Records")
ax2.set_title("Distribution of Sleep Duration")

ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

st.pyplot(fig2)

st.caption(
    "Stress scores cluster around moderate levels, while average sleep duration "
    "remains below optimal levels for many students."
)

# -----------------------------
# Relationship Analysis
# -----------------------------
st.divider()
st.subheader("Lifestyle vs Mental Health Relationships")

# Sleep vs Stress
fig3, ax3 = plt.subplots()
fig3.patch.set_facecolor("#f6f7f9")
ax3.set_facecolor("#f6f7f9")

ax3.scatter(
    filtered_df["sleep_hours"],
    filtered_df["stress_score"],
    alpha=0.4,
    s=25
)
ax3.set_xlabel("Sleep Hours")
ax3.set_ylabel("Stress Score")
ax3.set_title("Sleep Duration vs Stress Levels")

ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)

st.pyplot(fig3)

# Screen Time vs Anxiety
fig4, ax4 = plt.subplots()
fig4.patch.set_facecolor("#f6f7f9")
ax4.set_facecolor("#f6f7f9")

ax4.scatter(
    filtered_df["screen_time_hours"],
    filtered_df["anxiety_score"],
    alpha=0.4,
    s=25
)
ax4.set_xlabel("Screen Time (hours)")
ax4.set_ylabel("Anxiety Score")
ax4.set_title("Screen Time vs Anxiety Levels")

ax4.spines["top"].set_visible(False)
ax4.spines["right"].set_visible(False)

st.pyplot(fig4)

st.caption(
    "Lower sleep duration shows a negative association with stress, while "
    "higher screen time usage tends to coincide with increased anxiety levels."
)

# -----------------------------
# Ethical Disclaimer
# -----------------------------
st.divider()
st.caption(
    "Disclaimer: This dashboard is intended for educational and analytical purposes only. "
    "It does not provide medical diagnosis, mental health screening, or treatment recommendations."
)
