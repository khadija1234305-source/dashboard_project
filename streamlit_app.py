
import streamlit as st
st.set_page_config(
    page_title="Police Dashboard",
    layout="wide",
    page_icon="📊"
)                        

st.set_page_config(
    page_title="Police Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.sidebar.markdown("## 🎛 Dashboard Controls")
st.sidebar.markdown("---")
# =========================
# PASTEL ANIMATED UI STYLE
# =========================

st.markdown("""
<style>

/* Smooth animated gradient background */
.stApp {
    background: linear-gradient(-45deg, #a1c4fd, #c2e9fb, #fbc2eb, #f5f7fa);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
    color: #1f2937;
}

/* Animation keyframes */
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #ffffffcc;
    backdrop-filter: blur(10px);
}

/* KPI cards styling */
div[data-testid="metric-container"] {
    background-color: #ffffffaa;
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}

/* Dataframe styling */
.stDataFrame {
    background-color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PAGE TITLE
# =========================

st.markdown("""
<h1 style='text-align: center; color: #6C63FF;'>
🚨 Fatal Police Shootings Dashboard
</h1>
<p style='text-align: center; font-size:18px;'>
📊 Interactive Analytics | 🌍 Visual Insights | 🔥 Real Data Exploration
</p>
""", unsafe_allow_html=True)

# =========================
# LOAD DATASET
# =========================

df = pd.read_csv("fatal-police-shootings-data.csv")

# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.header("Filters")

# Gender Filter
gender_filter = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + list(df["gender"].dropna().unique())
)

# Race Filter
race_filter = st.sidebar.multiselect(
    "Select Race",
    df["race"].dropna().unique()
)

# Age Slider
age_filter = st.sidebar.slider(
    "Select Age Range",
    int(df["age"].min()),
    int(df["age"].max()),
    (
        int(df["age"].min()),
        int(df["age"].max())
    )
)

# =========================
# APPLY FILTERS
# =========================

filtered_df = df.copy()

if gender_filter != "All":
    filtered_df = filtered_df[
        filtered_df["gender"] == gender_filter
    ]

if race_filter:
    filtered_df = filtered_df[
        filtered_df["race"].isin(race_filter)
    ]

filtered_df = filtered_df[
    (filtered_df["age"] >= age_filter[0]) &
    (filtered_df["age"] <= age_filter[1])
]
# State Filter
state_filter = st.sidebar.multiselect(
    "Select State",
    df["state"].dropna().unique()
)

# Manner of Death Filter
death_filter = st.sidebar.multiselect(
    "Manner of Death",
    df["manner_of_death"].dropna().unique()
)

# Search Filter
search = st.sidebar.text_input("Search Keyword")

# Date Filter
df["date"] = pd.to_datetime(df["date"])

date_filter = st.sidebar.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
)
# State Filter
if state_filter:
    filtered_df = filtered_df[
        filtered_df["state"].isin(state_filter)
    ]

# Death Filter
if death_filter:
    filtered_df = filtered_df[
        filtered_df["manner_of_death"].isin(death_filter)
    ]

# Search Filter
if search:
    filtered_df = filtered_df[
        filtered_df.astype(str)
        .apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
    ]

# Date Filter
filtered_df = filtered_df[
    (filtered_df["date"] >= pd.to_datetime(date_filter[0])) &
    (filtered_df["date"] <= pd.to_datetime(date_filter[1]))
]
# =========================
# KPI SECTION
# =========================

total_cases = len(filtered_df)

average_age = round(filtered_df['age'].mean(), 1)

most_common_gender = (
    filtered_df['gender'].mode()[0]
    if not filtered_df.empty else "N/A"
)

most_common_race = (
    filtered_df['race'].mode()[0]
    if not filtered_df.empty else "N/A"
)


col1, col2, col3, col4 = st.columns(4)

col1.metric("🔥 Total Cases", total_cases)

col2.metric("📊 Average Age", average_age)

col3.metric("👥 Common Gender", most_common_gender)

col4.metric("🌍 Common Race", most_common_race)
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)

# =========================
# CHART LAYOUT
# =========================

col_chart1, col_chart2 = st.columns(2)

# =========================
# PIE CHART
# =========================

with col_chart1:

    st.subheader("Manner of Death Distribution")

    fig1, ax1 = plt.subplots(figsize=(5,5))

    death_counts = filtered_df["manner_of_death"].value_counts()

    ax1.pie(
        death_counts,
        labels=death_counts.index,
        autopct='%1.1f%%'
    )

    st.pyplot(fig1)

# =========================
# HISTOGRAM
# =========================

with col_chart2:

    st.subheader("Age Distribution")

    fig2, ax2 = plt.subplots(figsize=(6,5))

    ax2.hist(
        filtered_df["age"].dropna(),
        bins=20
    )

    ax2.set_xlabel("Age")

    ax2.set_ylabel("Frequency")

    ax2.set_title("Distribution of Age")

    st.pyplot(fig2)

# =========================
# BAR CHART
# =========================

st.subheader("Top 10 States by Shootings")

state_counts = (
    filtered_df["state"]
    .value_counts()
    .head(10)
)

fig3, ax3 = plt.subplots(figsize=(10,5))

ax3.bar(
    state_counts.index,
    state_counts.values
)

ax3.set_xlabel("State")

ax3.set_ylabel("Cases")

ax3.set_title("Top 10 States")

st.pyplot(fig3)

# =========================
# SHOW DATA
# =========================

# =========================
# BEAUTIFUL DATA TABLE
# =========================

st.subheader("📋 Filtered Data Table")

styled_df = filtered_df.copy()

# Clean column names (optional improvement)
styled_df.columns = [col.replace("_", " ").title() for col in styled_df.columns]

st.dataframe(
    styled_df,
    use_container_width=True,
    height=400
)

# =========================
# LINE CHART (TIME TREND)
# =========================

st.subheader("Trend Over Time")

df["date"] = pd.to_datetime(df["date"], errors="coerce")

trend = df.groupby(df["date"].dt.year).size()

fig4, ax4 = plt.subplots(figsize=(10,5))

ax4.plot(trend.index, trend.values, marker="o")

ax4.set_xlabel("Year")

ax4.set_ylabel("Number of Cases")

ax4.set_title("Shootings Over Time")

st.pyplot(fig4)
# =========================
# ROW 1
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("Manner of Death")
    st.pyplot(fig1)

with col2:
    st.subheader("Age Distribution")
    st.pyplot(fig2)

# =========================
# ROW 2
# =========================

col3, col4 = st.columns(2)

with col3:
    st.subheader("Top States")
    st.pyplot(fig3)

with col4:
    st.subheader("Yearly Trends")
    st.pyplot(fig4)
# =========================
col5, col6 = st.columns([1,1])

with col5:
    st.subheader("🌍 Incident Map")
    st.map(map_df[["latitude", "longitude"]])

with col6:
    st.subheader("📋 Data Table")
    st.dataframe(filtered_df.head(100))
# SCATTER PLOT
# =========================

st.subheader("Age vs Cases Relationship")

scatter_df = filtered_df.dropna(subset=["age"])

fig5, ax5 = plt.subplots(figsize=(8,5))

ax5.scatter(
    scatter_df["age"],
    range(len(scatter_df)),
    alpha=0.5
)

ax5.set_xlabel("Age")

ax5.set_ylabel("Cases Index")

ax5.set_title("Age Distribution Scatter Plot")

st.pyplot(fig5)
# =========================
# HEATMAP
# =========================

st.subheader("Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include=["number"])

fig6, ax6 = plt.subplots(figsize=(8,5))

import seaborn as sns

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    ax=ax6
)

st.pyplot(fig6)
# =========================
# INSIGHTS SECTION
# =========================

st.subheader("Key Insights")

st.markdown("""
- This dashboard analyzes fatal police shooting incidents.
- You can filter data by gender, race, and age.
- Charts automatically update based on filters.
- Trends show how incidents change over time.
""")

# =========================
# SHOW CLEAN DATA (OPTIONAL)
# =========================

with st.expander("View Raw Dataset"):
    st.dataframe(filtered_df)
    st.subheader("🗺️ Incident Map (Latitude vs Longitude)")

map_df = filtered_df.dropna(subset=["latitude", "longitude"])

st.map(map_df[["latitude", "longitude"]])
st.markdown("---")
