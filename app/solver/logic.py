import re
import pandas as pd

def compute_answer(question: str, extracted_data: dict):
 
    # If CSV is present
    if "csv" in extracted_data:
        df = pd.DataFrame(extracted_data["csv"])

        # SUM
        m = re.search(r"sum of the ['\"]?(\w+)['\"]? column", question, re.I)
        if m:
            col = m.group(1)
            return float(df[col].astype(float).sum())

        # AVERAGE
        m = re.search(r"average of ['\"]?(\w+)['\"]?", question, re.I)
        if m:
            col = m.group(1)
            return float(df[col].astype(float).mean())

        # COUNT ROWS
        if "how many rows" in question.lower():
            return int(len(df))

        # MAX
        m = re.search(r"maximum of ['\"]?(\w+)['\"]?", question, re.I)
        if m:
            col = m.group(1)
            return float(df[col].astype(float).max())

        # MIN
        m = re.search(r"minimum of ['\"]?(\w+)['\"]?", question, re.I)
        if m:
            col = m.group(1)
            return float(df[col].astype(float).min())

    # If PDF tables exist (first table only, basic logic)
    if "pdf_tables" in extracted_data:
        tables = extracted_data["pdf_tables"]
        if tables:
            df = tables[0]

            # Attempt same operations on PDF tables
            m = re.search(r"sum of the ['\"]?(\w+)['\"]?", question, re.I)
            if m:
                col = m.group(1)
                return float(df[col].astype(float).sum())

    return "Unable to interpret question"
