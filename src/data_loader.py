"""
Module for loading National Environmental Board Meeting dataset from data.go.th
"""
from pathlib import Path
from typing import Optional
import pandas as pd

DEFAULT_RAW_FILE = Path(__file__).resolve().parent.parent / "data" / "raw" / "neb_board_meeting.csv"


def load_raw_meeting_data(file_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Loads raw meeting CSV file and removes unneeded unnamed trailing columns.
    """
    target_file = Path(file_path) if file_path else DEFAULT_RAW_FILE
    if not target_file.exists():
        raise FileNotFoundError(f"File not found: {target_file}")

    encodings_to_try = ["utf-8-sig", "utf-8", "cp874", "tis-620"]
    last_err: Optional[Exception] = None
    df: Optional[pd.DataFrame] = None

    for enc in encodings_to_try:
        try:
            df = pd.read_csv(target_file, encoding=enc)
            break
        except Exception as e:
            last_err = e
            continue

    if df is None:
        raise RuntimeError(f"Cannot read {target_file} with tested encodings: {last_err}")

    # Drop unnamed empty columns
    valid_cols = [c for c in df.columns if not str(c).startswith("Unnamed:")]
    df = df[valid_cols].copy()

    return df
