"""Load and validate candidate profile from JSON."""

import json
from pathlib import Path

from pydantic import ValidationError

from backend.models import Candidate

CANDIDATE_JSON_PATH = Path(__file__).resolve().parent.parent / "data" / "candidate.json"


def load_candidate() -> Candidate:
    """Load data/candidate.json and return a validated Candidate object."""
    try:
        raw = CANDIDATE_JSON_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Candidate profile not found at {CANDIDATE_JSON_PATH}"
        )

    data = json.loads(raw)

    try:
        candidate = Candidate(**data)
    except ValidationError as e:
        raise ValueError(
            f"Candidate profile validation failed:\n{e}"
        )

    return candidate
