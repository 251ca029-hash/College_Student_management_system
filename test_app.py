"""
System Verification Test Script
Tests all core routes, authentication, analytics, and chatbot API.
"""
from app import app
from db import db_manager

def run_tests():
    client = app.test_client()
    app.config["TESTING"] = True
    
    print("[1/6] Testing Login Page...")
    res = client.get("/login")
    assert res.status_code == 200, f"Login page failed: {res.status_code}"
    assert "Sri Ramakrishna College" in res.get_data(as_text=True)
    print("  -> Passed!")

    print("[2/6] Testing Student Authentication and Dashboard...")
    with client.session_transaction() as sess:
        user = db_manager.get_user_by_username("cs001")
        sess["user"] = user

    res = client.get("/student/dashboard")
    assert res.status_code == 200, f"Student dashboard failed: {res.status_code}"
    assert "Ananya Krishnan" in res.get_data(as_text=True)
    assert "Python Programming" in res.get_data(as_text=True)
    print("  -> Passed!")

    print("[3/6] Testing Marks Management & Report Card...")
    res = client.get("/marks")
    assert res.status_code == 200, f"Marks page failed: {res.status_code}"
    
    res = client.get("/report-card/CS001")
    assert res.status_code == 200, f"Report card failed: {res.status_code}"
    assert "Statement of Marks" in res.get_data(as_text=True)
    print("  -> Passed!")

    print("[4/6] Testing Guidelines and FAQs...")
    res = client.get("/guidelines")
    assert res.status_code == 200
    res = client.get("/faqs?q=attendance")
    assert res.status_code == 200
    print("  -> Passed!")

    print("[5/6] Testing Machine Learning & Analytics Route...")
    with client.session_transaction() as sess:
        sess["user"] = db_manager.get_user_by_username("faculty1")
    res = client.get("/analytics")
    assert res.status_code == 200, f"Analytics page failed: {res.status_code}"
    assert "K-Means" in res.get_data(as_text=True)
    print("  -> Passed!")

    print("[6/6] Testing ChatGPT-4 mini Humanoid Chatbot Endpoint...")
    chat_payload = {"message": "What is the minimum attendance required?"}
    res = client.post("/api/chat", json=chat_payload)
    assert res.status_code == 200, f"Chat API failed: {res.status_code}"
    json_data = res.get_json()
    assert "75%" in json_data["reply"]
    print("  -> Bot Response Sample:", json_data["reply"][:90], "...")
    print("  -> Passed!")

    print("\nALL 6 TEST SUITES PASSED FLAWLESSLY!")

if __name__ == "__main__":
    run_tests()
