import os
import requests
import pdfplumber
import pandas as pd

DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_file(url: str) -> str:
    """
    Downloads file from URL and returns local file path.
    """
    filename = url.split("/")[-1]
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    response = requests.get(url)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(response.content)

    return filepath

def extract_pdf_tables(filepath: str):
    """
    Extracts tables from PDF and returns list of DataFrames.
    """
    tables = []
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                import pandas as pd
                df = pd.DataFrame(table[1:], columns=table[0])
                tables.append(df)
    return tables

def extract_csv(filepath: str):
    return pd.read_csv(filepath)
