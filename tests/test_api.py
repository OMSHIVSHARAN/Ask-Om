"""Tests for the Ask-Om FastAPI backend."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def _mock_groq_response(content: str) -> MagicMock:
    """Build a fake Groq chat completion response."""
    choice = MagicMock()
    choice.message.content = content
    completion = MagicMock()
    completion.choices = [choice]
    return completion


def test_health_check():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "Ask-Om API"


@patch("backend.main.get_groq_client")
def test_chat_valid_question(mock_get_client):
    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value = _mock_groq_response(
        "Om is a Computer Engineering student."
    )
    mock_get_client.return_value = fake_client

    resp = client.post("/chat", json={"message": "Tell me about Om."})
    assert resp.status_code == 200
    data = resp.json()
    assert "response" in data
    assert "Om" in data["response"]


def test_chat_empty_message():
    resp = client.post("/chat", json={"message": ""})
    assert resp.status_code == 422


def test_chat_whitespace_message():
    resp = client.post("/chat", json={"message": "   "})
    assert resp.status_code == 422


def test_chat_missing_message():
    resp = client.post("/chat", json={})
    assert resp.status_code == 422


@patch("backend.main.get_groq_client")
def test_kubernetes_hallucination(mock_get_client):
    """The AI must NOT claim Om knows Kubernetes."""
    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value = _mock_groq_response(
        "The candidate profile does not contain information about Kubernetes."
    )
    mock_get_client.return_value = fake_client

    resp = client.post(
        "/chat",
        json={"message": "Does Om have experience with Kubernetes?"},
    )
    assert resp.status_code == 200
    data = resp.json()
    answer = data["response"].lower()
    assert "kubernetes" in answer
    assert any(
        phrase in answer
        for phrase in ["not", "no ", "don't", "does not", "unavailable"]
    )
