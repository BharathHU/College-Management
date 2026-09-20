from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def login(username, password):
    response = client.post("/api/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["data"]["access_token"]


def test_login_success():
    response = client.post("/api/auth/login", json={"username": "student.com", "password": "student123"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "access_token" in response.json()["data"]


def test_login_invalid_password():
    response = client.post("/api/auth/login", json={"username": "student.com", "password": "wrong-pass"})
    assert response.status_code == 401


def test_protected_route_requires_auth():
    response = client.get("/api/students/me")
    assert response.status_code == 401


def test_role_restrictions():
    student_token = login("student.com", "student123")
    teacher_token = login("teacher.com", "teacher123")
    assert client.get("/api/teachers/me", headers={"Authorization": f"Bearer {student_token}"}).status_code == 403
    assert client.get("/api/students/me", headers={"Authorization": f"Bearer {teacher_token}"}).status_code == 403


def test_duplicate_attendance_rejected():
    token = login("teacher.com", "teacher123")
    payload = {"subject_id": 1, "student_id": 1, "date": (datetime.utcnow() + timedelta(days=30)).isoformat(), "status": "present"}
    headers = {"Authorization": f"Bearer {token}"}
    assert client.post("/api/attendance/mark", json=payload, headers=headers).status_code == 200
    assert client.post("/api/attendance/mark", json=payload, headers=headers).status_code == 409


def test_marks_range_validation():
    token = login("teacher.com", "teacher123")
    response = client.post("/api/marks/upsert", json={"subject_id": 1, "student_id": 1, "internal_marks": 31, "assignment_marks": 10, "exam_marks": 40}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422


def test_assignment_submission_status():
    teacher_token = login("teacher.com", "teacher123")
    create_response = client.post("/api/assignments/create", json={"subject_id": 1, "title": "Test assignment", "description": "Complete the test task", "due_date": (datetime.utcnow() + timedelta(days=14)).isoformat()}, headers={"Authorization": f"Bearer {teacher_token}"})
    assert create_response.status_code == 200
    assignment_id = create_response.json()["data"]["id"]
    student_token = login("student.com", "student123")
    submission = client.post(f"/api/assignments/{assignment_id}/submit", json={"content": "Completed"}, headers={"Authorization": f"Bearer {student_token}"})
    assert submission.status_code == 200
    duplicate = client.post(f"/api/assignments/{assignment_id}/submit", json={"content": "Submitted twice"}, headers={"Authorization": f"Bearer {student_token}"})
    assert duplicate.status_code == 409
    assignments = client.get(f"/api/assignments/student?q=Test%20assignment&limit=100", headers={"Authorization": f"Bearer {student_token}"})
    assert any(item["id"] == assignment_id and item["status"] == "Submitted" for item in assignments.json()["data"]["items"])


def test_invalid_attendance_and_marks_are_rejected():
    teacher_token = login("teacher.com", "teacher123")
    headers = {"Authorization": f"Bearer {teacher_token}"}
    invalid_attendance = client.post("/api/attendance/mark", json={"subject_id": 1, "student_id": 1, "date": datetime.utcnow().isoformat(), "status": "late"}, headers=headers)
    assert invalid_attendance.status_code == 422
    negative_marks = client.post("/api/marks/upsert", json={"subject_id": 1, "student_id": 1, "internal_marks": -1, "assignment_marks": 10, "exam_marks": 40}, headers=headers)
    assert negative_marks.status_code == 422


def test_teacher_ownership_is_enforced_for_mutations():
    teacher_token = login("teacher.com", "teacher123")
    headers = {"Authorization": f"Bearer {teacher_token}"}
    response = client.post("/api/assignments/create", json={"subject_id": 9999, "title": "Unauthorized", "description": "Should fail", "due_date": (datetime.utcnow() + timedelta(days=14)).isoformat()}, headers=headers)
    assert response.status_code == 404
    announcements = client.post("/api/announcements/create", json={"subject_id": 9999, "title": "Unauthorized", "message": "Should fail"}, headers=headers)
    assert announcements.status_code == 404


def test_teacher_can_review_owned_assignment_submissions():
    teacher_token = login("teacher.com", "teacher123")
    student_token = login("student.com", "student123")
    create_response = client.post("/api/assignments/create", json={"subject_id": 1, "title": "Reviewable", "description": "Review this", "due_date": (datetime.utcnow() + timedelta(days=14)).isoformat()}, headers={"Authorization": f"Bearer {teacher_token}"})
    assignment_id = create_response.json()["data"]["id"]
    client.post(f"/api/assignments/{assignment_id}/submit", json={"content": "Ready for review"}, headers={"Authorization": f"Bearer {student_token}"})
    response = client.get(f"/api/assignments/{assignment_id}/submissions", headers={"Authorization": f"Bearer {teacher_token}"})
    assert response.status_code == 200
    assert response.json()["data"][0]["student_id"] == "STU-1001"
    submission_id = response.json()["data"][0]["id"]
    update = client.patch(f"/api/assignments/{assignment_id}/submissions/{submission_id}", json={"status": "graded"}, headers={"Authorization": f"Bearer {teacher_token}"})
    assert update.status_code == 200
    assert update.json()["data"]["status"] == "graded"


def test_announcement_audience_and_creation():
    teacher_token = login("teacher.com", "teacher123")
    student_token = login("student.com", "student123")
    response = client.post("/api/announcements/create", json={"subject_id": 1, "title": "Student notice", "message": "Bring your lab record."}, headers={"Authorization": f"Bearer {teacher_token}"})
    assert response.status_code == 200
    announcements = client.get("/api/students/announcements", headers={"Authorization": f"Bearer {student_token}"})
    assert announcements.status_code == 200
    assert any(item["title"] == "Student notice" for item in announcements.json()["data"])


def test_search_and_pagination_contracts():
    student_token = login("student.com", "student123")
    teacher_token = login("teacher.com", "teacher123")
    subjects = client.get("/api/students/subjects?q=Python&page=1&limit=1", headers={"Authorization": f"Bearer {student_token}"})
    assert subjects.status_code == 200
    assert subjects.json()["data"]["page"] == 1
    assert subjects.json()["data"]["total"] >= 1
    assignments = client.get("/api/assignments/student?status=submitted&page=1&limit=1", headers={"Authorization": f"Bearer {student_token}"})
    assert assignments.status_code == 200
    assert assignments.json()["data"]["total"] >= 1
    roster = client.get("/api/teachers/students?q=Rahul&page=1&limit=1", headers={"Authorization": f"Bearer {teacher_token}"})
    assert roster.status_code == 200
    assert roster.json()["data"]["total"] >= 1


def test_dashboard_pending_assignments_excludes_submitted():
    student_token = login("student.com", "student123")
    dashboard = client.get("/api/dashboard/student", headers={"Authorization": f"Bearer {student_token}"})
    assert dashboard.status_code == 200
    data = dashboard.json()["data"]
    assignments = client.get("/api/assignments/student?limit=100", headers={"Authorization": f"Bearer {student_token}"}).json()["data"]["items"]
    expected = sum(1 for assignment in assignments if assignment["status"].lower() not in {"submitted", "graded"})
    assert data["stats"]["pending_assignments"] == expected
    assert "upcoming_classes" in data
    assert "grade_distribution" in data


def test_teacher_roster_returns_real_subject_metrics_and_pending_review():
    teacher_token = login("teacher.com", "teacher123")
    roster = client.get("/api/teachers/students?subject_id=1", headers={"Authorization": f"Bearer {teacher_token}"})
    assert roster.status_code == 200
    student = next(item for item in roster.json()["data"]["items"] if item["student_id"] == "STU-1001")
    assert student["attendance"] is not None
    assert 0 <= student["attendance"] <= 100
    assert student["performance"] == 88
    assignment = client.get("/api/assignments/teacher?limit=100", headers={"Authorization": f"Bearer {teacher_token}"}).json()["data"]["items"][0]
    review = client.get(f"/api/assignments/{assignment['id']}/submissions", headers={"Authorization": f"Bearer {teacher_token}"})
    assert review.status_code == 200
    assert all(item["student_id"] == "STU-1001" for item in review.json()["data"])
