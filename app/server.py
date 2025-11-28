from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.solver.quiz_chain import solve_quiz_chain

app = FastAPI()

SECRET = "your_secret_here"   # Same as Google Form


class Payload(BaseModel):
    email: str
    secret: str
    url: str


@app.post("/")
async def main_endpoint(payload: Payload):
    # Secret validation
    if payload.secret != SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")

    try:
        # Solve full quiz chain
        result = await solve_quiz_chain(
            start_url=payload.url,
            email=payload.email,
            secret=payload.secret
        )

        return {"status": "OK", "answer": result}

    except ValueError as ve:
        # Known user errors
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception:
        # UNKNOWN errors should NOT leak stack traces
        raise HTTPException(status_code=400, detail="Internal error")
