"""
Unit and integration tests for data loading, data cleaning, and chart generation
"""
import pytest
import pandas as pd
from pathlib import Path

from src.data_loader import load_raw_data, COLUMN_RENAME_MAP
from src.data_cleaning import clean_data, THAI_MONTHS, NUMERIC_COLUMNS
from src.charts import (
    create_monthly_trend_chart,
    create_department_comparison_chart,
    create_waste_management_donut_chart,
    create_top10_departments_chart,
    create_monthly_staff_chart,
    get_empty_figure,
)


def test_data_loader_reads_raw_data():
    """Verify raw data loads without errors and contains expected columns."""
    df = load_raw_data()
    assert not df.empty, "DataFrame should not be empty"
    assert "ปี" in df.columns
    assert "หน่วยงาน" in df.columns
    assert "ขยะที่เกิดขึ้น (กก.)" in df.columns
    assert "นำไปใช้ประโยชน์ (กก.)" in df.columns
    assert "ขยะที่ส่งกำจัด (กก.)" in df.columns


def test_data_cleaning_preserves_rows_and_types():
    """Verify cleaning converts numbers and strips strings."""
    raw_df = load_raw_data()
    cleaned = clean_data(raw_df)
    assert len(cleaned) == len(raw_df)

    for col in NUMERIC_COLUMNS:
        assert pd.api.types.is_numeric_dtype(cleaned[col]), f"{col} should be numeric"

    assert pd.api.types.is_integer_dtype(cleaned["ปี"]) or pd.api.types.is_numeric_dtype(cleaned["ปี"])
    assert 2568 in cleaned["ปี"].values
    assert 2569 in cleaned["ปี"].values


def test_calculations_match_prototype_2569():
    """
    Verify calculation of 2569 totals match prototype web metrics exactly:
    - ขยะที่เกิดขึ้น: ~43,950.65
    - นำไปใช้ประโยชน์: ~9,090.31
    - ขยะที่ส่งกำจัด: ~27,691.10
    """
    raw_df = load_raw_data()
    cleaned = clean_data(raw_df)
    df_2569 = cleaned[cleaned["ปี"] == 2569]

    total_gen = df_2569["ขยะที่เกิดขึ้น (กก.)"].sum()
    total_rec = df_2569["นำไปใช้ประโยชน์ (กก.)"].sum()
    total_disp = df_2569["ขยะที่ส่งกำจัด (กก.)"].sum()

    assert pytest.approx(total_gen, 0.01) == 43950.65
    assert pytest.approx(total_rec, 0.01) == 9090.31
    assert pytest.approx(total_disp, 0.01) == 27691.10


def test_charts_generate_successfully():
    """Verify all chart generator functions produce valid Plotly Figures."""
    raw_df = load_raw_data()
    cleaned = clean_data(raw_df)
    sample_df = cleaned[cleaned["ปี"] == 2569]

    fig1 = create_monthly_trend_chart(sample_df)
    assert fig1 is not None
    assert len(fig1.data) == 3  # 3 lines

    fig2 = create_department_comparison_chart(sample_df)
    assert fig2 is not None
    assert len(fig2.data) == 3  # 3 bar series

    fig3 = create_waste_management_donut_chart(sample_df)
    assert fig3 is not None
    assert len(fig3.data) == 1  # 1 pie trace

    fig4 = create_top10_departments_chart(sample_df)
    assert fig4 is not None
    assert len(fig4.data) == 1

    fig5 = create_monthly_staff_chart(sample_df)
    assert fig5 is not None
    assert len(fig5.data) == 1


def test_empty_dataframe_handling():
    """Verify charts don't crash when filtered to an empty DataFrame."""
    empty_df = pd.DataFrame(columns=NUMERIC_COLUMNS + ["ปี", "สังกัด", "หน่วยงาน", "เดือน"])

    fig1 = create_monthly_trend_chart(empty_df)
    fig2 = create_department_comparison_chart(empty_df)
    fig3 = create_waste_management_donut_chart(empty_df)
    fig4 = create_top10_departments_chart(empty_df)
    fig5 = create_monthly_staff_chart(empty_df)

    assert fig1 is not None
    assert fig2 is not None
    assert fig3 is not None
    assert fig4 is not None
    assert fig5 is not None
