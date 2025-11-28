import time
import requests
from .solve_quiz import solve_quiz


MAX_TIME = 180   # 3 minutes


async def solve_quiz_chain(start_url: str, email: str, secret: str):
    """
    Solves multi-step IITM quizzes:
    - solve first quiz
    - submit the answer
    - read next URL
    - loop until no more URLs
    """

    start_time = time.time()
    current_url = start_url
    steps = []

    while True:
        elapsed = time.time() - start_time
        if elapsed > MAX_TIME:
            return {"error": "Time limit exceeded (3 minutes)", "steps": steps}

        print(f"\n=== Solving quiz: {current_url} ===")

        # Solve one quiz page
        result = await solve_quiz(
            url=current_url,
            email=email,
            secret=secret
        )

        steps.append({
            "url": current_url,
            "result": result
        })

        submit_url = result.get("submit_url")
        final_answer = result.get("final_answer")

        # If no submission URL → end
        if not submit_url:
            print("No submit URL found — finishing chain.")
            return {"finished": True, "steps": steps}

        # Submit answer
        try:
            resp = requests.post(submit_url, json={
                "email": email,
                "secret": secret,
                "url": current_url,
                "answer": final_answer
            })

            print("Submission response:", resp.text)
            resp_json = resp.json()

        except Exception as e:
            print("Error submitting:", e)
            return {"error": str(e), "steps": steps}

        # Server may provide next quiz URL
        next_url = resp_json.get("url")

        if not next_url:
            print("Reached last quiz — ending.")
            return {"finished": True, "steps": steps}

        # Continue solving next quiz
        current_url = next_url
