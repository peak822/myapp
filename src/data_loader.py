"""
Module for loading raw waste management dataset from data.go.th / catalog.dnp.go.th
"""
from pathlib import Path
from typing import List, Optional
import pandas as pd

DEFAULT_RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

COLUMN_RENAME_MAP = {
    "ใช้ประโยชน์ (กก.)": "นำไปใช้ประโยชน์ (กก.)",
    "ร้อยละส่งกำจัดลดลง": "ร้อยละขยะส่งกำจัดลดลง",
}

EXPECTED_COLUMNS = [
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


def read_csv_with_encoding(file_path: Path) -> pd.DataFrame:
    """
    Reads a CSV file trying cp874 (standard Thai encoding) then utf-8 variants.
    """
    encodings_to_try = ["cp874", "tis-620", "utf-8-sig", "utf-8"]
    last_err: Optional[Exception] = None
    for enc in encodings_to_try:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            return df
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f"Cannot read file {file_path} with supported encodings: {last_err}")


def load_raw_data(data_dir: Optional[Path] = None) -> pd.DataFrame:
    """
    Loads all raw waste CSV files from the specified raw data directory,
    harmonizes column names, and combines them into a single DataFrame.
    """
    target_dir = Path(data_dir) if data_dir else DEFAULT_RAW_DIR
    if not target_dir.exists():
        raise FileNotFoundError(f"Directory not found: {target_dir}")

    csv_files = sorted(list(target_dir.glob("*.csv")))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {target_dir}")

    dfs: List[pd.DataFrame] = []
    for csv_file in csv_files:
        df = read_csv_with_encoding(csv_file)
        # Rename non-standard columns (e.g. from 2568 dataset)
        df = df.rename(columns=COLUMN_RENAME_MAP)
        # Ensure year column is parsed or inferred from filename if missing
        if "ปี" in df.columns:
            df["ปี"] = pd.to_numeric(df["ปี"], errors="coerce")
        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df
