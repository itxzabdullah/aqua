from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

WHO_FILE = DATA_DIR / "WHO_Drinking_Water_Quality_Standards.csv"
NSDWQ_FILE = DATA_DIR / "Pakistan_NSDWQ_Standards_Sample_Parameters.csv"


def load_who_data() -> pd.DataFrame:

    if not WHO_FILE.exists():
        raise FileNotFoundError(
            f"WHO data not found: {WHO_FILE}"
        )

    df = pd.read_csv(WHO_FILE)

    required_columns = {
        "Parameter",
        "Category",
        "Dataset_Module",
        "Unit",
        "WHO_Guideline_Value",
        "Guideline_Type",
        "Health_Implications_and_Significance",
        "Major_Sources",
        "WHO_Remarks_and_Notes",
        "Chemical_Symbol_or_Formula",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"WHO dataset is Missing columns: {sorted(missing)}")

    return df

def load_nsdwq_data() -> pd.DataFrame:

    if not NSDWQ_FILE.exists():
        raise FileNotFoundError(
            f"NSDWQ data not found: {NSDWQ_FILE}"
        )
    df = pd.read_csv(NSDWQ_FILE)

    required_columns = {
        "Sample_Feature",
        "Parameter",
        "Unit",
        "Pakistan_NSDWQ_Limit",
        "Notes",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"NSDWQ dataset is Missing columns: {sorted(missing)}")

    return df

if __name__ == "__main__":
    who = load_who_data()
    nsdwq = load_nsdwq_data()

    print("WHO dataset")
    print(f"Rows: {len(who)}")
    print(f"Columns: {len(who.columns)}")
    print()

    print("Pakistan NSDWQ dataset")
    print(f"Rows: {len(nsdwq)}")
    print(f"Columns: {len(nsdwq.columns)}")

