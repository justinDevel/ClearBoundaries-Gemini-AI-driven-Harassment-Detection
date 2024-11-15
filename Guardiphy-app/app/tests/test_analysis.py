from app.main import app

from fastapi.testclient import TestClient


client = TestClient(app)

def test_analyze():
    validRequest = {
                    "messages": [
                        {
                            "subject": "Immediate Performance Concerns",
                            "body": "I don’t know how many times I have to tell you this, but your work is way below acceptable standards. It’s honestly baffling how you’ve made it this far without getting fired. Every task you take on seems to turn into a disaster, and I’m getting tired of cleaning up your messes. You’re dragging the team down, and I’m seriously questioning why we even keep you on board. This is your last chance to prove you’re not a complete waste of time, or I’ll personally see to it that you’re replaced by someone competent. We don’t have room for someone who can’t handle basic responsibilities.",
                            "sender": "manager@example.com",
                            "recipient": "employee@example.com",
                            "created_at": "2024-11-13T11:00:00Z",
                            "modified_at": "2024-11-13T11:15:00Z",
                            "email_thread_id": "thread56789",
                            "language": "English"
                        }
                    ],
                    "data": {
                        "context": "workplace communication analysis"
                    }
                    }


    response = client.post("/api/analyze", json=validRequest)
    assert response.status_code == 200
    data = response.json()
    assert "flagged_phrases" in data
    assert "tone" in data
    assert "sentiment" in data
