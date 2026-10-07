"""Ask-Om FastAPI backend and terminal chat CLI."""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq

from backend.candidate import load_candidate
from backend.models import ChatRequest, ChatResponse
from backend.prompts import build_system_prompt

load_dotenv()

app = FastAPI(
    title="Ask-Om API",
    description="AI representative of Om Shivsharan",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_groq_client() -> Groq:
    """Return a Groq client; raise HTTPException if key is missing."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "YOUR_GROQ_API_KEY":
        raise HTTPException(
            status_code=500,
            detail="Server misconfiguration: GROQ_API_KEY is not set.",
        )
    return Groq(api_key=api_key)


@app.get("/")
def health_check() -> dict:
    return {"status": "ok", "service": "Ask-Om API"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        candidate = load_candidate()
    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(status_code=500, detail=str(e))

    system_prompt = build_system_prompt(candidate)
    client = get_groq_client()

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message},
            ],
            temperature=0.3,
            max_tokens=1024,
        )
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Failed to get a response from the AI service.",
        )

    reply = completion.choices[0].message.content
    return ChatResponse(response=reply)


def cli_chat() -> None:
    """Interactive terminal chat."""
    import sys

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "YOUR_GROQ_API_KEY":
        print("ERROR: Set a valid GROQ_API_KEY in your .env file.")
        sys.exit(1)

    candidate = load_candidate()
    system_prompt = build_system_prompt(candidate)
    client = Groq(api_key=api_key)
    messages: list[dict] = [{"role": "system", "content": system_prompt}]

    print(f"Ask Om — AI Representative of {candidate.name}")
    print("Type 'quit' or 'exit' to end the conversation.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.3,
            max_tokens=1024,
        )

        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        print(f"\nAI: {reply}\n")


if __name__ == "__main__":
    cli_chat()
