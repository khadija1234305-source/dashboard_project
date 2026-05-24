import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Fatal Police Shootings Dashboard",
    page_icon="🚨",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main {
    background-color: #f8f6ff;
}

h1 {
    color: #6c63ff;
    text-align: center;
    font-size: 45px;
}

h2, h3 {
    color: #444;
}

[data-testid="stSidebar"] {
    background-color: #efeaff;
}

.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

div[data-testid="stPlotlyChart"] {
    background-color: white;
    border-radius: 15px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.title("🚨 Fatal Police Shootings Dashboard")

st.markdown("""
### Interactive dashboard for analyzing fatal police shooting incidents across the United States.
""")

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/fatal-police-shootings-data.csv")

# =========================
# DATA CLEANING
# =========================

df["date"] = pd.to_datetime(df["date"], errors="coerce")

df = df.dropna(subset=["date"])

# =========================
# SIDEBAR
# =========================

st.sidebar.title("🎛 Dashboard Filters")

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

# State Filter
state_filter = st.sidebar.multiselect(
    "Select State",
    df["state"].dropna().unique()
)

# Manner of Death
death_filter = st.sidebar.multiselect(
    "Manner of Death",
    df["manner_of_death"].dropna().unique()
)

# Age Slider
min_age = int(df["age"].min())
max_age = int(df["age"].max())

age_filter = st.sidebar.slider(
    "Select Age Range",
    min_age,
    max_age,
    (min_age, max_age)
)

# Search Filter
search = st.sidebar.text_input("🔍 Search Keyword")

# Date Filter
min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_filter = st.sidebar.date_input(
    "📅 Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# =========================
# FILTER DATA
# =========================

filtered_df = df.copy()

# Gender
if gender_filter != "All":
    filtered_df = filtered_df[
        filtered_df["gender"] == gender_filter
    ]

# Race
if race_filter:
    filtered_df = filtered_df[
        filtered_df["race"].isin(race_filter)
    ]

# State
if state_filter:
    filtered_df = filtered_df[
        filtered_df["state"].isin(state_filter)
    ]

# Manner of Death
if death_filter:
    filtered_df = filtered_df[
        filtered_df["manner_of_death"].isin(death_filter)
    ]

# Age
filtered_df = filtered_df[
    (filtered_df["age"] >= age_filter[0]) &
    (filtered_df["age"] <= age_filter[1])
]

# Search
if search:
    filtered_df = filtered_df[
        filtered_df.astype(str)
        .apply(
            lambda row: row.str.contains(
                search,
                case=False
            ).any(),
            axis=1
        )
    ]

# Date
start_date = pd.to_datetime(date_filter[0])
end_date = pd.to_datetime(date_filter[1])

filtered_df = filtered_df[
    (filtered_df["date"] >= start_date) &
    (filtered_df["date"] <= end_date)
]

# =========================
# KPI CARDS
# =========================

total_cases = len(filtered_df)

average_age = round(filtered_df["age"].mean(), 1)

most_common_gender = (
    filtered_df["gender"]
    .mode()[0]
    if not filtered_df["gender"].mode().empty
    else "N/A"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔥 Total Cases", total_cases)

with col2:
    st.metric("📊 Average Age", average_age)

with col3:
    st.metric("👥 Common Gender", most_common_gender)

# =========================
# CHARTS ROW 1
# =========================

col4, col5 = st.columns(2)

with col4:

    st.subheader("🥧 Manner of Death Distribution")

    fig1, ax1 = plt.subplots(figsize=(6,6))

    filtered_df["manner_of_death"] \
        .value_counts() \
        .plot.pie(
            autopct='%1.1f%%',
            ax=ax1
        )

    ax1.set_ylabel("")

    st.pyplot(fig1)

with col5:

    st.subheader("📈 Age Distribution")

    fig2, ax2 = plt.subplots(figsize=(7,5))

    sns.histplot(
        filtered_df["age"].dropna(),
        bins=20,
        kde=True,
        ax=ax2
    )

    st.pyplot(fig2)

# =========================
# CHARTS ROW 2
# =========================

col6, col7 = st.columns(2)

with col6:

    st.subheader("📊 Top States")

    top_states = filtered_df["state"] \
        .value_counts() \
        .head(10)

    fig3, ax3 = plt.subplots(figsize=(7,5))

    sns.barplot(
        x=top_states.values,
        y=top_states.index,
        ax=ax3
    )

    st.pyplot(fig3)

with col7:

    st.subheader("📉 Yearly Trends")

    yearly = filtered_df.groupby(
        filtered_df["date"].dt.year
    ).size()

    fig4, ax4 = plt.subplots(figsize=(7,5))

    yearly.plot(
        kind="line",
        marker="o",
        ax=ax4
    )

    st.pyplot(fig4)

# =========================
# HEATMAP
# =========================

st.subheader("🔥 Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include=np.number)

fig5, ax5 = plt.subplots(figsize=(10,6))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    ax=ax5
)

st.pyplot(fig5)

# =========================
# MAP + TABLE
# =========================

col8, col9 = st.columns(2)

with col8:

    st.subheader("🌍 Incident Map")

    if "latitude" in filtered_df.columns and "longitude" in filtered_df.columns:

        map_data = filtered_df.dropna(
            subset=["latitude", "longitude"]
        )

        if not map_data.empty:
            st.map(map_data[["latitude", "longitude"]])

        else:
            st.warning("No map data available.")

with col9:

    st.subheader("📋 Data Table")

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True,
        height=400
    )

# =========================
# DOWNLOAD BUTTON
# =========================

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

# =========================
# FOOTER
# =========================

st.markdown("---")

st.markdown(
    "<center>Made with ❤️ using Streamlit</center>",
    unsafe_allow_html=True
)
