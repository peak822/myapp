"""
Module for generating Plotly charts for National Environmental Board Meeting Dashboard
"""
from typing import List, Optional
import pandas as pd
import plotly.graph_objects as go
from src.data_cleaning import THAI_MONTHS

# Harmonious environmental color palette
COLOR_CONSIDER = "#0068c9"    # Dark blue (เรื่องเพื่อพิจารณา)
COLOR_INFORM = "#00d4ff"      # Cyan/light blue (เรื่องเพื่อทราบ)
COLOR_ONSITE = "#0068c9"      # Blue (on site)
COLOR_ONLINE = "#00d4ff"      # Bright Cyan (online)
COLOR_DOMAIN = "#00b4d8"      # Teal/Cyan
COLOR_MONTH = "#0077b6"       # Ocean Blue


def get_empty_figure(message: str = "ไม่พบข้อมูลตามเงื่อนไขที่เลือก") -> go.Figure:
    """Returns an empty figure with a clear message."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16),
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=350,
    )
    return fig


def create_yearly_trend_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates stacked bar chart of meeting agendas by fiscal year and agenda type.
    """
    if df.empty:
        return get_empty_figure()

    pivot = (
        df.groupby(["ปีงบประมาณ พ.ศ.", "ประเภทวาระ"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    fig = go.Figure()

    if "เรื่องเพื่อพิจารณา" in pivot.columns:
        fig.add_trace(
            go.Bar(
                x=pivot["ปีงบประมาณ พ.ศ."],
                y=pivot["เรื่องเพื่อพิจารณา"],
                name="เรื่องเพื่อพิจารณา",
                marker_color=COLOR_CONSIDER,
                hovertemplate="<b>ปี %{x}</b><br>เพื่อพิจารณา: %{y:,} วาระ<extra></extra>",
            )
        )

    if "เรื่องเพื่อทราบ" in pivot.columns:
        fig.add_trace(
            go.Bar(
                x=pivot["ปีงบประมาณ พ.ศ."],
                y=pivot["เรื่องเพื่อทราบ"],
                name="เรื่องเพื่อทราบ",
                marker_color=COLOR_INFORM,
                hovertemplate="<b>ปี %{x}</b><br>เพื่อทราบ: %{y:,} วาระ<extra></extra>",
            )
        )

    fig.update_layout(
        title=dict(text="แนวโน้มจำนวนวาระการประชุมตามปีงบประมาณ", font=dict(size=16)),
        barmode="stack",
        xaxis=dict(title="ปีงบประมาณ พ.ศ.", type="category", showgrid=False),
        yaxis=dict(title="จำนวนวาระ", showgrid=True),
        legend=dict(orientation="v", x=1.02, y=1),
        margin=dict(l=40, r=40, t=50, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=450,
    )
    return fig


def create_topic_donut_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates donut chart showing distribution of meeting topics.
    """
    if df.empty:
        return get_empty_figure()

    topic_counts = df["ประเภทเรื่อง"].value_counts().reset_index()
    topic_counts.columns = ["ประเภทเรื่อง", "จำนวน"]

    palette = ["#0077b6", "#0096c7", "#00b4d8", "#48cae4", "#90e0ef", "#caf0f8"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=topic_counts["ประเภทเรื่อง"],
                values=topic_counts["จำนวน"],
                hole=0.5,
                marker=dict(colors=palette),
                textinfo="percent",
                direction="clockwise",
                sort=False,
                hovertemplate="<b>%{label}</b><br>จำนวน: %{value:,} วาระ (%{percent})<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title=dict(text="สัดส่วนประเภทเรื่องการประชุม", font=dict(size=15)),
        showlegend=True,
        legend=dict(orientation="v", x=1.02, y=0.5),
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=380,
    )
    return fig


def create_domain_bar_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates horizontal bar chart for environmental domains (ด้าน).
    """
    if df.empty:
        return get_empty_figure()

    domain_counts = df["ด้าน"].value_counts().reset_index()
    domain_counts.columns = ["ด้าน", "จำนวน"]
    domain_counts = domain_counts.sort_values(by="จำนวน", ascending=True)

    fig = go.Figure(
        go.Bar(
            x=domain_counts["จำนวน"],
            y=domain_counts["ด้าน"],
            orientation="h",
            marker_color=COLOR_DOMAIN,
            hovertemplate="<b>%{y}</b><br>จำนวน: %{x:,} วาระ<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="การจำแนกวาระตามด้านสิ่งแวดล้อม", font=dict(size=15)),
        xaxis=dict(title="จำนวนวาระ", showgrid=True),
        yaxis=dict(title="ด้าน", tickfont=dict(size=11)),
        margin=dict(l=20, r=20, t=40, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=380,
    )
    return fig


def create_meeting_format_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates grouped bar chart showing On-site vs Online meeting formats across years.
    """
    if df.empty:
        return get_empty_figure()

    pivot = (
        df.groupby(["ปีงบประมาณ พ.ศ.", "รูปแบบการประชุม"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    fig = go.Figure()

    if "on site" in pivot.columns:
        fig.add_trace(
            go.Bar(
                x=pivot["ปีงบประมาณ พ.ศ."],
                y=pivot["on site"],
                name="On-site",
                marker_color=COLOR_ONSITE,
                hovertemplate="<b>ปี %{x}</b><br>On-site: %{y:,} วาระ<extra></extra>",
            )
        )

    if "online" in pivot.columns:
        fig.add_trace(
            go.Bar(
                x=pivot["ปีงบประมาณ พ.ศ."],
                y=pivot["online"],
                name="Online",
                marker_color=COLOR_ONLINE,
                hovertemplate="<b>ปี %{x}</b><br>Online: %{y:,} วาระ<extra></extra>",
            )
        )

    fig.update_layout(
        title=dict(text="เปรียบเทียบรูปแบบการประชุมตามปีงบประมาณ (On-site vs Online)", font=dict(size=16)),
        barmode="group",
        xaxis=dict(title="ปีงบประมาณ พ.ศ.", type="category", showgrid=False),
        yaxis=dict(title="จำนวนวาระ", showgrid=True),
        legend=dict(orientation="v", x=1.02, y=1),
        margin=dict(l=40, r=40, t=50, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=420,
    )
    return fig


def create_monthly_meeting_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates bar chart of agenda count per Thai calendar month.
    """
    if df.empty:
        return get_empty_figure()

    month_counts = df["เดือน"].value_counts().reset_index()
    month_counts.columns = ["เดือน", "จำนวน"]

    month_df = pd.DataFrame({"เดือน": THAI_MONTHS})
    merged = pd.merge(month_df, month_counts, on="เดือน", how="left").fillna(0)

    fig = go.Figure(
        go.Bar(
            x=merged["เดือน"],
            y=merged["จำนวน"],
            marker_color=COLOR_MONTH,
            hovertemplate="<b>%{x}</b><br>จำนวนวาระ: %{y:,.0f} วาระ<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="จำนวนวาระการประชุมจำแนกตามเดือน", font=dict(size=16)),
        xaxis=dict(title="เดือน", showgrid=False),
        yaxis=dict(title="จำนวนวาระ", showgrid=True),
        margin=dict(l=40, r=40, t=50, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=400,
    )
    return fig


def create_top_agencies_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates horizontal bar chart for top agencies proposing agendas (เจ้าของวาระ).
    """
    if df.empty:
        return get_empty_figure()

    agency_counts = (
        df[df["เจ้าของวาระ"] != "ไม่ระบุ"]["เจ้าของวาระ"]
        .value_counts()
        .head(7)
        .reset_index()
    )
    agency_counts.columns = ["เจ้าของวาระ", "จำนวน"]
    agency_counts = agency_counts.sort_values(by="จำนวน", ascending=True)

    fig = go.Figure(
        go.Bar(
            x=agency_counts["จำนวน"],
            y=agency_counts["เจ้าของวาระ"],
            orientation="h",
            marker_color=COLOR_CONSIDER,
            hovertemplate="<b>%{y}</b><br>จำนวนวาระ: %{x:,} วาระ<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="หน่วยงานเจ้าของวาระสูงสุด", font=dict(size=15)),
        xaxis=dict(title="จำนวนวาระ", showgrid=True),
        yaxis=dict(title="หน่วยงาน", tickfont=dict(size=11)),
        margin=dict(l=20, r=20, t=40, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=380,
    )
    return fig
