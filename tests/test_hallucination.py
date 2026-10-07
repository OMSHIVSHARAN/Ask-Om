"""Task 7 — Hallucination test: run 5 predefined questions and print answers."""

import os
import sys

from dotenv import load_dotenv
from groq import Groq

from backend.candidate import load_candidate
from backend.prompts import build_system_prompt

load_dotenv()

TEST_QUESTIONS = [
    "Tell me about Om.",
    "What are Om's technical skills?",
    "Tell me about Om's projects.",
    "What programming languages does Om know?",
    "Does Om have experience with Kubernetes?",
]


def main() -> None:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "YOUR_GROQ_API_KEY":
        print("ERROR: Set a valid GROQ_API_KEY in your .env file.")
        sys.exit(1)

    candidate = load_candidate()
    system_prompt = build_system_prompt(candidate)
    client = Groq(api_key=api_key)

    print("=" * 60)
    print("HALLUCINATION TEST — 5 Questions")
    print("=" * 60)

    for i, question in enumerate(TEST_QUESTIONS, 1):
        print(f"\n--- Question {i} ---")
        print(f"Q: {question}\n")

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.3,
            max_tokens=1024,
        )

        answer = response.choices[0].message.content
        print(f"A: {answer}\n")

    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
