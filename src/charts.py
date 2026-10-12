"""
Module for generating Plotly charts matching the prototype dashboard
"""
from typing import List, Optional
import pandas as pd
import plotly.graph_objects as go
from src.data_cleaning import THAI_MONTHS

# Color palette matching prototype
COLOR_GENERATED = "#0055b7"   # Dark blue
COLOR_RECYCLED = "#64b5f6"    # Light blue
COLOR_DISPOSED = "#e53935"    # Red
COLOR_STAFF = "#0055b7"       # Dark blue


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
        font=dict(size=16, color="#666666"),
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=350,
    )
    return fig


def create_monthly_trend_chart(df: pd.DataFrame, selected_months: Optional[List[str]] = None) -> go.Figure:
    """
    Creates monthly waste trend line chart with 3 series:
    - ขยะที่เกิดขึ้น (กก.)
    - นำไปใช้ประโยชน์ (กก.)
    - ขยะที่ส่งกำจัด (กก.)
    """
    if df.empty:
        return get_empty_figure()

    months = THAI_MONTHS

    monthly_summary = (
        df.groupby("เดือน", as_index=False)[
            ["ขยะที่เกิดขึ้น (กก.)", "นำไปใช้ประโยชน์ (กก.)", "ขยะที่ส่งกำจัด (กก.)"]
        ]
        .sum()
    )

    # Reindex to ensure all selected months are present in proper calendar order
    month_df = pd.DataFrame({"เดือน": months})
    merged = pd.merge(month_df, monthly_summary, on="เดือน", how="left").fillna(0)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=merged["เดือน"],
            y=merged["ขยะที่เกิดขึ้น (กก.)"],
            name="ขยะที่เกิดขึ้น (กก.)",
            mode="lines+markers",
            line=dict(color=COLOR_GENERATED, width=2.5),
            marker=dict(size=6),
            hovertemplate="<b>%{x}</b><br>ขยะที่เกิดขึ้น: %{y:,.2f} กก.<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=merged["เดือน"],
            y=merged["นำไปใช้ประโยชน์ (กก.)"],
            name="นำไปใช้ประโยชน์ (กก.)",
            mode="lines+markers",
            line=dict(color=COLOR_RECYCLED, width=2.5),
            marker=dict(size=6),
            hovertemplate="<b>%{x}</b><br>นำไปใช้ประโยชน์: %{y:,.2f} กก.<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=merged["เดือน"],
            y=merged["ขยะที่ส่งกำจัด (กก.)"],
            name="ขยะที่ส่งกำจัด (กก.)",
            mode="lines+markers",
            line=dict(color=COLOR_DISPOSED, width=2.5),
            marker=dict(size=6),
            hovertemplate="<b>%{x}</b><br>ขยะที่ส่งกำจัด: %{y:,.2f} กก.<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="แนวโน้มปริมาณขยะรายเดือน", font=dict(size=16, color="#262730")),
        xaxis=dict(title="เดือน", showgrid=True, gridcolor="#f0f2f6"),
        yaxis=dict(title="ปริมาณ (กก.)", showgrid=True, gridcolor="#f0f2f6", rangemode="tozero"),
        legend=dict(
            title=dict(text="ประเภทขยะ"),
            orientation="v",
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
        ),
        margin=dict(l=40, r=40, t=50, b=40),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="x unified",
        height=450,
    )
    return fig


def create_department_comparison_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates grouped bar chart comparing waste metrics across departments.
    """
    if df.empty:
        return get_empty_figure()

    dept_summary = (
        df.groupby("หน่วยงาน", as_index=False)[
            ["ขยะที่เกิดขึ้น (กก.)", "นำไปใช้ประโยชน์ (กก.)", "ขยะที่ส่งกำจัด (กก.)"]
        ]
        .sum()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=dept_summary["หน่วยงาน"],
            y=dept_summary["ขยะที่เกิดขึ้น (กก.)"],
            name="ขยะที่เกิดขึ้น (กก.)",
            marker_color=COLOR_GENERATED,
            hovertemplate="<b>%{x}</b><br>ขยะที่เกิดขึ้น: %{y:,.2f} กก.<extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            x=dept_summary["หน่วยงาน"],
            y=dept_summary["นำไปใช้ประโยชน์ (กก.)"],
            name="นำไปใช้ประโยชน์ (กก.)",
            marker_color=COLOR_RECYCLED,
            hovertemplate="<b>%{x}</b><br>นำไปใช้ประโยชน์: %{y:,.2f} กก.<extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            x=dept_summary["หน่วยงาน"],
            y=dept_summary["ขยะที่ส่งกำจัด (กก.)"],
            name="ขยะที่ส่งกำจัด (กก.)",
            marker_color=COLOR_DISPOSED,
            hovertemplate="<b>%{x}</b><br>ขยะที่ส่งกำจัด: %{y:,.2f} กก.<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="เปรียบเทียบปริมาณขยะตามหน่วยงาน", font=dict(size=16, color="#262730")),
        barmode="group",
        xaxis=dict(
            title="หน่วยงาน",
            tickangle=-45,
            showgrid=False,
            tickfont=dict(size=10),
        ),
        yaxis=dict(title="ปริมาณ (กก.)", showgrid=True, gridcolor="#f0f2f6"),
        legend=dict(
            title=dict(text="ประเภท"),
            orientation="v",
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
        ),
        margin=dict(l=40, r=40, t=50, b=120),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=500,
    )
    return fig


def create_waste_management_donut_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates donut chart showing proportion of recycled vs disposed waste.
    """
    if df.empty:
        return get_empty_figure()

    total_recycled = df["นำไปใช้ประโยชน์ (กก.)"].sum()
    total_disposed = df["ขยะที่ส่งกำจัด (กก.)"].sum()

    if (total_recycled + total_disposed) <= 0:
        return get_empty_figure("ไม่มีข้อมูลปริมาณการจัดการขยะ")

    labels = ["ส่งกำจัด", "นำไปใช้ประโยชน์"]
    values = [total_disposed, total_recycled]
    colors = [COLOR_GENERATED, COLOR_RECYCLED]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                marker=dict(colors=colors),
                textinfo="percent",
                direction="clockwise",
                sort=False,
                hovertemplate="<b>%{label}</b><br>ปริมาณ: %{value:,.2f} กก. (%{percent})<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title=dict(text="สัดส่วนการจัดการขยะ", font=dict(size=15, color="#262730")),
        showlegend=True,
        legend=dict(orientation="v", x=1.02, y=0.5),
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        height=380,
    )
    return fig


def create_top10_departments_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates horizontal bar chart of top 10 departments with highest waste generated.
    """
    if df.empty:
        return get_empty_figure()

    dept_summary = (
        df.groupby("หน่วยงาน", as_index=False)["ขยะที่เกิดขึ้น (กก.)"]
        .sum()
        .sort_values(by="ขยะที่เกิดขึ้น (กก.)", ascending=False)
        .head(10)
    )

    # Sort ascending for horizontal bar chart display so largest is at the top
    dept_summary_asc = dept_summary.sort_values(by="ขยะที่เกิดขึ้น (กก.)", ascending=True)

    fig = go.Figure(
        go.Bar(
            x=dept_summary_asc["ขยะที่เกิดขึ้น (กก.)"],
            y=dept_summary_asc["หน่วยงาน"],
            orientation="h",
            marker_color=COLOR_GENERATED,
            hovertemplate="<b>%{y}</b><br>ขยะที่เกิดขึ้น: %{x:,.2f} กก.<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="10 หน่วยงานที่มีขยะเกิดขึ้นสูงสุด", font=dict(size=15, color="#262730")),
        xaxis=dict(title="ขยะที่เกิดขึ้น (กก.)", showgrid=True, gridcolor="#f0f2f6"),
        yaxis=dict(title="หน่วยงาน", tickfont=dict(size=11)),
        margin=dict(l=20, r=20, t=40, b=40),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=380,
    )
    return fig


def create_monthly_staff_chart(df: pd.DataFrame, selected_months: Optional[List[str]] = None) -> go.Figure:
    """
    Creates bar chart of average staff per month.
    """
    if df.empty:
        return get_empty_figure()

    months = THAI_MONTHS

    staff_summary = df.groupby("เดือน", as_index=False)["คนเฉลี่ย"].mean()
    month_df = pd.DataFrame({"เดือน": months})
    merged = pd.merge(month_df, staff_summary, on="เดือน", how="left").fillna(0)

    fig = go.Figure(
        go.Bar(
            x=merged["เดือน"],
            y=merged["คนเฉลี่ย"],
            marker_color=COLOR_STAFF,
            hovertemplate="<b>%{x}</b><br>คนเฉลี่ย: %{y:,.1f} คน<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="จำนวนคนเฉลี่ยรายเดือน", font=dict(size=16, color="#262730")),
        xaxis=dict(title="เดือน", showgrid=False),
        yaxis=dict(title="คนเฉลี่ย", showgrid=True, gridcolor="#f0f2f6"),
        margin=dict(l=40, r=40, t=50, b=40),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=400,
    )
    return fig
