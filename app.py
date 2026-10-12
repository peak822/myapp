"""
Streamlit Web Application: Waste Management Dashboard
Dataset: กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช (data.go.th)
"""
from pathlib import Path
import streamlit as st
import pandas as pd

from src.data_loader import load_raw_data
from src.data_cleaning import clean_data, THAI_MONTHS
from src.charts import (
    create_monthly_trend_chart,
    create_department_comparison_chart,
    create_waste_management_donut_chart,
    create_top10_departments_chart,
    create_monthly_staff_chart,
)

# Page configuration
st.set_page_config(
    page_title="Waste Management Dashboard",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling to match prototype aesthetic and elegant Thai typography
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');

    html, body, .stApp {
        font-family: 'Prompt', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Prompt', sans-serif;
        font-weight: 600;
    }

    /* Preserve Streamlit Material Icons for collapse/expand and UI icons */
    [data-testid="stIconMaterial"],
    [data-testid*="stIcon"],
    [class*="material-symbols"],
    .material-symbols-rounded,
    .material-symbols-outlined,
    button[data-testid="stSidebarCollapseButton"] *,
    button[data-testid="stSidebarCollapsedControl"] * {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
    }

    /* Section header styling */
    .section-title {
        font-size: 1.35rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .sub-desc {
        color: #4b5563;
        font-size: 0.95rem;
        margin-bottom: 1.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_data() -> pd.DataFrame:
    """Loads and caches processed dataset."""
    processed_file = Path(__file__).parent / "data" / "processed" / "waste_data_combined.csv"
    if processed_file.exists():
        return pd.read_csv(processed_file, encoding="utf-8-sig")

    # Fallback to load and clean from raw
    raw_df = load_raw_data()
    clean_df = clean_data(raw_df)
    return clean_df


# Load dataset
try:
    df = get_data()
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
    st.stop()

# ==========================================
# Sidebar: Filters
# ==========================================
st.sidebar.title("🔎 Filter ข้อมูล")

# Year filter
available_years = sorted(df["ปี"].dropna().unique().tolist(), reverse=True)
default_years = [2569] if 2569 in available_years else available_years
selected_years = st.sidebar.multiselect("ปี", options=available_years, default=default_years)

# Filter dataframe by selected years
df_filtered_year = df[df["ปี"].isin(selected_years)] if selected_years else df

# Affiliation filter (สังกัด)
available_affiliations = sorted(df_filtered_year["สังกัด"].dropna().unique().tolist())
selected_affiliations = st.sidebar.multiselect(
    "สังกัด", options=available_affiliations, default=available_affiliations
)

# Filter dataframe by affiliations
df_filtered_affil = (
    df_filtered_year[df_filtered_year["สังกัด"].isin(selected_affiliations)]
    if selected_affiliations
    else df_filtered_year
)

# Department filter (หน่วยงาน)
available_departments = sorted(df_filtered_affil["หน่วยงาน"].dropna().unique().tolist())
selected_departments = st.sidebar.multiselect(
    "หน่วยงาน", options=available_departments, default=available_departments
)

# Filter dataframe by departments
df_filtered_dept = (
    df_filtered_affil[df_filtered_affil["หน่วยงาน"].isin(selected_departments)]
    if selected_departments
    else df_filtered_affil
)

# Month filter (เดือน)
# Only list months that are present in the dataset, ordered by Thai calendar
present_months = [m for m in THAI_MONTHS if m in df_filtered_dept["เดือน"].values]
selected_months = st.sidebar.multiselect("เดือน", options=present_months, default=present_months)

# Final filtered dataframe
filtered_df = (
    df_filtered_dept[df_filtered_dept["เดือน"].isin(selected_months)]
    if selected_months
    else pd.DataFrame(columns=df.columns)
)

# ==========================================
# Main Header
# ==========================================
st.title("♻️ Waste Management Dashboard")
st.markdown("#### Dashboard การจัดการขยะ")
st.markdown(
    "ใช้สำหรับวิเคราะห์ปริมาณขยะ การนำขยะไปใช้ประโยชน์ และปริมาณขยะที่ส่งกำจัด โดยสามารถกรองข้อมูลตามปี สังกัด หน่วยงาน และเดือนได้"
)

# ==========================================
# Section 1: KPI Metrics Summary
# ==========================================
st.markdown("### 📊 สรุปข้อมูล")

if not filtered_df.empty:
    total_waste_gen = filtered_df["ขยะที่เกิดขึ้น (กก.)"].sum()
    total_waste_rec = filtered_df["นำไปใช้ประโยชน์ (กก.)"].sum()
    total_waste_disp = filtered_df["ขยะที่ส่งกำจัด (กก.)"].sum()
    avg_reduction = filtered_df["ร้อยละขยะส่งกำจัดลดลง"].mean()
    total_foam = filtered_df["โฟมบรรจุอาหาร (ใบ)"].sum()
else:
    total_waste_gen = 0.0
    total_waste_rec = 0.0
    total_waste_disp = 0.0
    avg_reduction = 0.0
    total_foam = 0.0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("ขยะที่เกิดขึ้น", f"{total_waste_gen:,.2f} กก.")
col2.metric("นำไปใช้ประโยชน์", f"{total_waste_rec:,.2f} กก.")
col3.metric("ขยะที่ส่งกำจัด", f"{total_waste_disp:,.2f} กก.")
col4.metric("เฉลี่ยขยะส่งกำจัดลดลง", f"{avg_reduction:.2f}%")
col5.metric("โฟมบรรจุอาหาร", f"{int(total_foam):,} ใบ")

st.divider()

# ==========================================
# Section 2: Monthly Waste Trend
# ==========================================
st.markdown("### 📈 ปริมาณขยะรายเดือน")
fig_monthly = create_monthly_trend_chart(filtered_df, selected_months=selected_months if selected_months else present_months)
st.plotly_chart(fig_monthly, use_container_width=True)

# ==========================================
# Section 3: Waste by Department
# ==========================================
st.markdown("### 🏢 ปริมาณขยะตามหน่วยงาน")
fig_dept = create_department_comparison_chart(filtered_df)
st.plotly_chart(fig_dept, use_container_width=True)

# ==========================================
# Section 4: Waste Management Distribution & Top 10
# ==========================================
st.markdown("### ♻️ การจัดการขยะ")
col_donut, col_top10 = st.columns(2)

with col_donut:
    fig_donut = create_waste_management_donut_chart(filtered_df)
    st.plotly_chart(fig_donut, use_container_width=True)

with col_top10:
    fig_top10 = create_top10_departments_chart(filtered_df)
    st.plotly_chart(fig_top10, use_container_width=True)

# ==========================================
# Section 5: Monthly Average Staff
# ==========================================
st.markdown("### 👥 คนเฉลี่ยและวันทำงาน")
fig_staff = create_monthly_staff_chart(filtered_df, selected_months=selected_months if selected_months else present_months)
st.plotly_chart(fig_staff, use_container_width=True)

# ==========================================
# Section 6: Data Table
# ==========================================
st.markdown("### 📋 รายละเอียดข้อมูล")
display_cols = [
    "ปี",
    "สังกัด",
    "หน่วยงาน",
    "เดือน",
    "คนเฉลี่ย",
    "วันทำงาน",
    "โฟมบรรจุอาหาร (ใบ)",
    "ขยะที่เกิดขึ้น (กก.)",
    "นำไปใช้ประโยชน์ (กก.)",
    "ขยะที่ส่งกำจัด (กก.)",
    "ร้อยละขยะส่งกำจัดลดลง",
]
available_display_cols = [c for c in display_cols if c in filtered_df.columns]
st.dataframe(
    filtered_df[available_display_cols].reset_index(drop=True),
    use_container_width=True,
    hide_index=True,
)
