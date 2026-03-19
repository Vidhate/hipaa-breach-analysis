import os
import pandas as pd

DATA_DIR = os.path.realpath(os.path.dirname(__file__))
ACTIVE_FILEPATH = os.path.join(DATA_DIR, "breach_report_hhs_active.csv")
RESOLVED_FILEPATH = os.path.join(DATA_DIR, "breach_report_hhs_resolved.csv")

def process_ocr_breach_data():
    """
    Predefined processing to clean up the OCR breach raw data.

    Following steps are applied to both the files:
    1. column "Breach Submission Date" is casted to datetime


    Following steps are applied to `breach_report_hhs_active.csv`:
    1. column name `javax.faces.component.UIPanel@4aeff997` is renamed to "Covered Entity Name" as found on website  
    2. column name `javax.faces.component.UIPanel@30064d1d` is renamed to "Business Associate Present" as found on website

    Following steps are applied to `breach_report_hhs_resolved.csv`:
    1. column name `javax.faces.component.UIPanel@401ebe35` is renamed to "Covered Entity Name" as found on website
    2. column name `javax.faces.component.UIPanel@55cba586` is renamed to "Business Associate Present" as found on website
    3. column "Individuals Affected" is casted to int; one row with a NaN value is dropped because it's "web description" notes that the case has been consolidated with another
    4. column "Web Description" where values are "\\N" are replaced with NaN
    """

    active = pd.read_csv(ACTIVE_FILEPATH)
    resolved = pd.read_csv(RESOLVED_FILEPATH)

    active = active.rename(columns={
        "javax.faces.component.UIPanel@4aeff997": "Covered Entity Name",
        "javax.faces.component.UIPanel@30064d1d": "Business Associate Present"
    })

    active["Breach Submission Date"] = pd.to_datetime(active["Breach Submission Date"])


    resolved = resolved.rename(columns={
        "javax.faces.component.UIPanel@401ebe35": "Covered Entity Name",
        "javax.faces.component.UIPanel@55cba586": "Business Associate Present"
    })

    resolved["Breach Submission Date"] = pd.to_datetime(resolved["Breach Submission Date"])
    resolved = resolved.dropna(subset=["Individuals Affected"])
    resolved["Individuals Affected"] = resolved["Individuals Affected"].astype(int)
    resolved["Web Description"] = resolved["Web Description"].replace("\\N", pd.NA)

    active.to_csv(ACTIVE_FILEPATH, index=False)
    resolved.to_csv(RESOLVED_FILEPATH, index=False)

    pass


if __name__ == "__main__":
    process_ocr_breach_data()