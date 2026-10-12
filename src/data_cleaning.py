"""
Module for cleaning and transforming National Environmental Board Meeting dataset
"""
from pathlib import Path
from typing import Optional, List
import pandas as pd

DEFAULT_PROCESSED_FILE = (
    Path(__file__).resolve().parent.parent / "data" / "processed" / "neb_meeting_processed.csv"
)

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

MONTH_REGEX_PATTERN = r"(" + "|".join(THAI_MONTHS) + r")"


def clean_meeting_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw meeting dataset:
    - Strips whitespace
    - Casts fiscal year as int
    - Extracts Thai month from date
    - Fills missing values with meaningful defaults
    """
    df_clean = df.copy()

    # Strip text columns
    for col in df_clean.select_dtypes(include=["object", "string"]).columns:
        df_clean[col] = df_clean[col].astype(str).str.strip()

    # Clean fiscal year
    if "ปีงบประมาณ พ.ศ." in df_clean.columns:
        df_clean["ปีงบประมาณ พ.ศ."] = (
            pd.to_numeric(df_clean["ปีงบประมาณ พ.ศ."], errors="coerce").fillna(0).astype(int)
        )

    # Extract month from date
    if "วันที่" in df_clean.columns:
        extracted_months = df_clean["วันที่"].str.extract(MONTH_REGEX_PATTERN)[0]
        df_clean["เดือน"] = extracted_months.fillna("ไม่ระบุ")
    else:
        df_clean["เดือน"] = "ไม่ระบุ"

    # Fill and standardize categorical fields
    if "รูปแบบการประชุม" in df_clean.columns:
        df_clean["รูปแบบการประชุม"] = (
            df_clean["รูปแบบการประชุม"]
            .replace({"nan": "ไม่ระบุ", "": "ไม่ระบุ", "None": "ไม่ระบุ"})
            .fillna("ไม่ระบุ")
        )

    if "ด้าน" in df_clean.columns:
        df_clean["ด้าน"] = (
            df_clean["ด้าน"]
            .replace({"nan": "ด้านอื่น ๆ", "": "ด้านอื่น ๆ", "None": "ด้านอื่น ๆ"})
            .fillna("ด้านอื่น ๆ")
        )

    if "ประเภทเรื่อง" in df_clean.columns:
        df_clean["ประเภทเรื่อง"] = (
            df_clean["ประเภทเรื่อง"]
            .replace({"nan": "อื่น ๆ", "": "อื่น ๆ", "None": "อื่น ๆ"})
            .fillna("อื่น ๆ")
        )

    if "เจ้าของโครงการ" in df_clean.columns:
        df_clean["เจ้าของโครงการ"] = (
            df_clean["เจ้าของโครงการ"]
            .replace({"nan": "-", "": "-", "None": "-"})
            .fillna("-")
        )

    if "เจ้าของวาระ" in df_clean.columns:
        df_clean["เจ้าของวาระ"] = (
            df_clean["เจ้าของวาระ"]
            .replace({"nan": "ไม่ระบุ", "": "ไม่ระบุ", "None": "ไม่ระบุ"})
            .fillna("ไม่ระบุ")
        )

    # Sort by Fiscal Year descending, then Meeting round
    sort_cols = [c for c in ["ปีงบประมาณ พ.ศ.", "ครั้งที่"] if c in df_clean.columns]
    if sort_cols:
        df_clean = df_clean.sort_values(by=sort_cols, ascending=[False, True]).reset_index(drop=True)

    return df_clean


def save_processed_meeting_data(df: pd.DataFrame, file_path: Optional[Path] = None) -> Path:
    """
    Saves clean DataFrame as UTF-8 with BOM for Excel/Pandas interoperability.
    """
    target_path = Path(file_path) if file_path else DEFAULT_PROCESSED_FILE
    target_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target_path, index=False, encoding="utf-8-sig")
    return target_path
