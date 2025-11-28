from bs4 import BeautifulSoup
import re

def extract_file_links(html: str):
    """
    Returns all downloadable file links (PDF, CSV, TXT, Images).
    """
    soup = BeautifulSoup(html, "lxml")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith((".pdf", ".csv", ".txt", ".xlsx")):
            links.append(href)

    return links


def extract_question_and_submit_url(html: str):
    """
    Extracts:
    - question text
    - submit URL
    """

    soup = BeautifulSoup(html, "lxml")

    # 1. Extract visible text
    text = soup.get_text(separator="\n")

    # Clean up extra whitespace
    clean_text = "\n".join([line.strip() for line in text.split("\n") if line.strip() != ""])

    # 2. Find submit URL (it will always appear as http...submit)
    submit_url_match = re.search(r"https?://[^\s'\"]+/submit[^\s'\"]*", clean_text)

    submit_url = submit_url_match.group(0) if submit_url_match else None

    # 3. The question is normally everything before the submit instructions
    if submit_url:
        question_part = clean_text.split(submit_url)[0].strip()
    else:
        question_part = clean_text

    return {
        "question": question_part,
        "submit_url": submit_url
    }
