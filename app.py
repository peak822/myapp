"""
Streamlit Web Application: National Environmental Board Meeting Dashboard
Dataset: การประชุมคณะกรรมการสิ่งแวดล้อมแห่งชาติ (data.go.th)
สำนักงานนโยบายและแผนทรัพยากรธรรมชาติและสิ่งแวดล้อม (สผ.)
"""
from pathlib import Path
import streamlit as st
import pandas as pd

from src.data_loader import load_raw_meeting_data
from src.data_cleaning import clean_meeting_data, THAI_MONTHS
from src.charts import (
    create_yearly_trend_chart,
    create_topic_donut_chart,
    create_domain_bar_chart,
    create_meeting_format_chart,
    create_monthly_meeting_chart,
    create_top_agencies_chart,
)

# Page configuration
st.set_page_config(
    page_title="National Environmental Board Meeting Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for elegant Thai typography and icon preservation
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
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_data() -> pd.DataFrame:
    """Loads and caches processed meeting dataset."""
    processed_file = (
        Path(__file__).parent / "data" / "processed" / "neb_meeting_processed.csv"
    )
    if processed_file.exists():
        return pd.read_csv(processed_file, encoding="utf-8-sig")

    # Fallback to load and clean from raw
    raw_df = load_raw_meeting_data()
    clean_df = clean_meeting_data(raw_df)
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
available_years = sorted(df["ปีงบประมาณ พ.ศ."].dropna().unique().tolist(), reverse=True)
selected_years = st.sidebar.multiselect(
    "ปีงบประมาณ พ.ศ.", options=available_years, default=available_years
)
df_filtered = df[df["ปีงบประมาณ พ.ศ."].isin(selected_years)] if selected_years else df

# Agenda Type filter (ประเภทวาระ)
available_types = sorted(df_filtered["ประเภทวาระ"].dropna().unique().tolist())
selected_types = st.sidebar.multiselect(
    "ประเภทวาระ", options=available_types, default=available_types
)
df_filtered = (
    df_filtered[df_filtered["ประเภทวาระ"].isin(selected_types)]
    if selected_types
    else df_filtered
)

# Domain filter (ด้าน)
available_domains = sorted(df_filtered["ด้าน"].dropna().unique().tolist())
selected_domains = st.sidebar.multiselect(
    "ด้านสิ่งแวดล้อม", options=available_domains, default=available_domains
)
df_filtered = (
    df_filtered[df_filtered["ด้าน"].isin(selected_domains)]
    if selected_domains
    else df_filtered
)

# Format filter (รูปแบบการประชุม)
available_formats = sorted(df_filtered["รูปแบบการประชุม"].dropna().unique().tolist())
selected_formats = st.sidebar.multiselect(
    "รูปแบบการประชุม", options=available_formats, default=available_formats
)
df_filtered = (
    df_filtered[df_filtered["รูปแบบการประชุม"].isin(selected_formats)]
    if selected_formats
    else df_filtered
)

# Month filter (เดือน)
present_months = [m for m in THAI_MONTHS if m in df_filtered["เดือน"].values]
selected_months = st.sidebar.multiselect("เดือน", options=present_months, default=present_months)
filtered_df = (
    df_filtered[df_filtered["เดือน"].isin(selected_months)]
    if selected_months
    else pd.DataFrame(columns=df.columns)
)

# ==========================================
# Main Header
# ==========================================
st.title("🌿 National Environmental Board Meeting Dashboard")
st.markdown("#### แดชบอร์ดข้อมูลการประชุมคณะกรรมการสิ่งแวดล้อมแห่งชาติ")
st.markdown(
    "วิเคราะห์ข้อมูลวาระการประชุม รูปแบบการประชุม และประเภทเรื่องการพิจารณา (ปีงบประมาณ พ.ศ. 2561 - 2567) "
    "แหล่งข้อมูลจาก สำนักงานนโยบายและแผนทรัพยากรธรรมชาติและสิ่งแวดล้อม (สผ.) ผ่าน data.go.th"
)

# ==========================================
# Section 1: KPI Metrics Summary
# ==========================================
st.markdown("### 📊 สรุปข้อมูล")

total_agendas = len(filtered_df)
total_consider = (filtered_df["ประเภทวาระ"] == "เรื่องเพื่อพิจารณา").sum() if not filtered_df.empty else 0
total_inform = (filtered_df["ประเภทวาระ"] == "เรื่องเพื่อทราบ").sum() if not filtered_df.empty else 0
total_onsite = (filtered_df["รูปแบบการประชุม"] == "on site").sum() if not filtered_df.empty else 0
total_online = (filtered_df["รูปแบบการประชุม"] == "online").sum() if not filtered_df.empty else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("วาระทั้งหมด", f"{total_agendas:,} วาระ")
col2.metric("เรื่องเพื่อพิจารณา", f"{total_consider:,} วาระ")
col3.metric("เรื่องเพื่อทราบ", f"{total_inform:,} วาระ")
col4.metric("การประชุม On-site", f"{total_onsite:,} วาระ")
col5.metric("การประชุม Online", f"{total_online:,} วาระ")

st.divider()

# ==========================================
# Section 2: Yearly Trend Chart
# ==========================================
st.markdown("### 📈 แนวโน้มวาระการประชุมตามปีงบประมาณ")
fig_yearly = create_yearly_trend_chart(filtered_df)
st.plotly_chart(fig_yearly, width="stretch")

# ==========================================
# Section 3: Topic & Domain Breakdown
# ==========================================
st.markdown("### 📑 สัดส่วนเรื่องและด้านสิ่งแวดล้อม")
col_topic, col_domain = st.columns(2)

with col_topic:
    fig_topic = create_topic_donut_chart(filtered_df)
    st.plotly_chart(fig_topic, width="stretch")

with col_domain:
    fig_domain = create_domain_bar_chart(filtered_df)
    st.plotly_chart(fig_domain, width="stretch")

# ==========================================
# Section 4: Format Comparison & Top Proposing Agencies
# ==========================================
st.markdown("### 💻 รูปแบบการประชุมและหน่วยงานเจ้าของวาระ")
col_format, col_agency = st.columns(2)

with col_format:
    fig_format = create_meeting_format_chart(filtered_df)
    st.plotly_chart(fig_format, width="stretch")

with col_agency:
    fig_agency = create_top_agencies_chart(filtered_df)
    st.plotly_chart(fig_agency, width="stretch")

# ==========================================
# Section 5: Monthly Distribution
# ==========================================
st.markdown("### 📅 การประชุมรายเดือน")
fig_monthly = create_monthly_meeting_chart(filtered_df)
st.plotly_chart(fig_monthly, width="stretch")

# ==========================================
# Section 6: Data Table
# ==========================================
st.markdown("### 📋 รายละเอียดวาระการประชุม")
display_cols = [
    "ปีงบประมาณ พ.ศ.",
    "ครั้งที่",
    "วันที่",
    "เดือน",
    "ประเภทวาระ",
    "วาระที่",
    "ชื่อวาระ",
    "ประเภทเรื่อง",
    "ด้าน",
    "เจ้าของวาระ",
    "รูปแบบการประชุม",
    "สถานที่",
]
available_display_cols = [c for c in display_cols if c in filtered_df.columns]
st.dataframe(
    filtered_df[available_display_cols].reset_index(drop=True),
    width="stretch",
    hide_index=True,
)
