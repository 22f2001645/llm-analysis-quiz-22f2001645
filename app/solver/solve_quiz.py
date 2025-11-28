from .browser import load_page
from .parse_html import extract_question_and_submit_url, extract_file_links
from .file_utils import download_file, extract_pdf_tables, extract_csv
from .logic import compute_answer
import requests


async def solve_quiz(url: str, email: str, secret: str):
    try:
        # Load the quiz page (JS-rendered)
        html = await load_page(url)

        # Extract question & submit URL
        parsed = extract_question_and_submit_url(html)
        question = parsed["question"]
        submit_url = parsed["submit_url"]

        print("\n----- QUESTION DETECTED -----")
        print(question)
        print("-----------------------------------")

        print("\n----- SUBMIT URL DETECTED -----")
        print(submit_url)
        print("-----------------------------------\n")

        # Detect file links (PDF / CSV / XLSX etc.)
        file_links = extract_file_links(html)
        print(f"Detected file links: {file_links}")

        extracted_data = {}

        # Download & extract data from files
        for link in file_links:
            print(f"Downloading: {link}")
            local_path = download_file(link)

            if link.lower().endswith(".pdf"):
                print("Extracting PDF tables...")
                extracted_data["pdf_tables"] = extract_pdf_tables(local_path)

            elif link.lower().endswith(".csv"):
                print("Extracting CSV data...")
                extracted_data["csv"] = extract_csv(local_path).to_dict(orient="records")

        # Compute answer
        final_answer = compute_answer(question, extracted_data)

        print("\n----- FINAL ANSWER COMPUTED -----")
        print(final_answer)
        print("----------------------------------\n")

        # Submit answer (if submit_url exists)
        submit_response_text = None
        if submit_url:
            try:
                response = requests.post(submit_url, json={
                    "email": email,
                    "secret": secret,
                    "url": url,
                    "answer": final_answer
                })
                submit_response_text = response.text
                print("Submit response:", response.text)
            except Exception as e:
                print("Submission failed:", e)

        # Full response returned to server
        return {
            "question": question,
            "submit_url": submit_url,
            "files_found": file_links,
            "extracted_data": extracted_data,
            "final_answer": final_answer,
            "submit_response": submit_response_text
        }

    except Exception as e:
        print("Error loading/parsing page:", e)
        return {"error": str(e)}
