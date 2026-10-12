"""
Unit and integration tests for National Environmental Board Meeting Dashboard
"""
import pytest
import pandas as pd
from pathlib import Path

from src.data_loader import load_raw_meeting_data
from src.data_cleaning import clean_meeting_data, THAI_MONTHS
from src.charts import (
    create_yearly_trend_chart,
    create_topic_donut_chart,
    create_domain_bar_chart,
    create_meeting_format_chart,
    create_monthly_meeting_chart,
    create_top_agencies_chart,
    get_empty_figure,
)


def test_data_loader_reads_meeting_data():
    """Verify raw meeting data loads without errors and contains expected columns."""
    df = load_raw_meeting_data()
    assert not df.empty, "DataFrame should not be empty"
    assert "ปีงบประมาณ พ.ศ." in df.columns
    assert "ครั้งที่" in df.columns
    assert "ชื่อวาระ" in df.columns
    assert "ประเภทวาระ" in df.columns


def test_data_cleaning_preserves_rows_and_extracts_month():
    """Verify cleaning preserves row count and correctly extracts months."""
    raw_df = load_raw_meeting_data()
    cleaned = clean_meeting_data(raw_df)
    assert len(cleaned) == len(raw_df)
    assert "เดือน" in cleaned.columns
    assert cleaned["เดือน"].notna().all()
    assert pd.api.types.is_integer_dtype(cleaned["ปีงบประมาณ พ.ศ."])


def test_charts_generate_successfully():
    """Verify all chart generator functions produce valid Plotly Figures."""
    raw_df = load_raw_meeting_data()
    cleaned = clean_meeting_data(raw_df)

    fig1 = create_yearly_trend_chart(cleaned)
    assert fig1 is not None
    assert len(fig1.data) >= 1

    fig2 = create_topic_donut_chart(cleaned)
    assert fig2 is not None
    assert len(fig2.data) == 1

    fig3 = create_domain_bar_chart(cleaned)
    assert fig3 is not None
    assert len(fig3.data) == 1

    fig4 = create_meeting_format_chart(cleaned)
    assert fig4 is not None
    assert len(fig4.data) >= 1

    fig5 = create_monthly_meeting_chart(cleaned)
    assert fig5 is not None
    assert len(fig5.data) == 1

    fig6 = create_top_agencies_chart(cleaned)
    assert fig6 is not None
    assert len(fig6.data) == 1


def test_empty_dataframe_handling():
    """Verify charts don't crash when filtered to an empty DataFrame."""
    empty_df = pd.DataFrame(
        columns=[
            "ปีงบประมาณ พ.ศ.",
            "ครั้งที่",
            "วันที่",
            "เดือน",
            "ประเภทวาระ",
            "ประเภทเรื่อง",
            "ด้าน",
            "รูปแบบการประชุม",
            "เจ้าของวาระ",
        ]
    )

    fig1 = create_yearly_trend_chart(empty_df)
    fig2 = create_topic_donut_chart(empty_df)
    fig3 = create_domain_bar_chart(empty_df)
    fig4 = create_meeting_format_chart(empty_df)
    fig5 = create_monthly_meeting_chart(empty_df)
    fig6 = create_top_agencies_chart(empty_df)

    assert fig1 is not None
    assert fig2 is not None
    assert fig3 is not None
    assert fig4 is not None
    assert fig5 is not None
    assert fig6 is not None
