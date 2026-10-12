"""
Module for cleaning and transforming waste management dataset
"""
from pathlib import Path
from typing import Optional, List
import pandas as pd

DEFAULT_PROCESSED_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "waste_data_combined.csv"

THAI_MONTHS: List[str] = [
    "มกราคม",
    "กุมภาพันธ์",
    "มีนาคม",
    "เมษายน",
    "พฤษภาคม",
    "มิถุนายน",
    "กรกฎาคม",
    "สิงหาคม",
    "กันยายน",
    "ตุลาคม",
    "พฤศจิกายน",
    "ธันวาคม",
]

NUMERIC_COLUMNS = [
    "คนเฉลี่ย",
    "วันทำงาน",
    "โฟมบรรจุอาหาร (ใบ)",
    "ขยะที่เกิดขึ้น (กก.)",
    "นำไปใช้ประโยชน์ (กก.)",
    "ขยะที่ส่งกำจัด (กก.)",
    "ร้อยละขยะส่งกำจัดลดลง",
]


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw DataFrame:
    - Strips whitespace in text fields
    - Casts numeric fields safely with coerce
    - Standardizes Year and Month
    - Returns clean DataFrame
    """
    df_clean = df.copy()

    # Strip string columns
    string_cols = ["สังกัด", "หน่วยงาน", "เดือน"]
    for col in string_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()

    # Clean year
    if "ปี" in df_clean.columns:
        df_clean["ปี"] = pd.to_numeric(df_clean["ปี"], errors="coerce").fillna(0).astype(int)

    # Clean numeric columns
    for col in NUMERIC_COLUMNS:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce").fillna(0.0)

    # Sort primarily by Year descending, preserving original file order within each year
    if "ปี" in df_clean.columns:
        df_clean = df_clean.sort_values(by="ปี", ascending=False).reset_index(drop=True)

    return df_clean


def save_processed_data(df: pd.DataFrame, file_path: Optional[Path] = None) -> Path:
    """
    Saves clean DataFrame as UTF-8 with BOM for Excel/Pandas interoperability.
    """
    target_path = Path(file_path) if file_path else DEFAULT_PROCESSED_FILE
    target_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target_path, index=False, encoding="utf-8-sig")
    return target_path
