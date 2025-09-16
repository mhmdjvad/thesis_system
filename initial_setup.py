from data_handler import load_json, save_json
from user_auth import hash_password

def initialize_defaults():
    """Create sample JSON files if missing."""
    users = load_json("users.json", None)
    if users is None:
        users = [
            {"id": "S1001", "type": "student", "name": "Ali Rezaei", "password_hash": hash_password("pass123")},
            {"id": "S1002", "type": "student", "name": "Sara Mohammadi", "password_hash": hash_password("pass123")},
            {"id": "T2001", "type": "supervisor", "name": "Dr. Ahmadi", "password_hash": hash_password("drpass"), "supervise_count": 0, "review_count": 0},
            {"id": "T2002", "type": "supervisor", "name": "Dr. Hosseini", "password_hash": hash_password("drpass"), "supervise_count": 0, "review_count": 0},
            {"id": "T3001", "type": "reviewer", "name": "Dr. Karimi", "password_hash": hash_password("revpass"), "supervise_count": 0, "review_count": 0},
        ]
        save_json("users.json", users)
    courses = load_json("courses.json", None)
    if courses is None:
        courses = [
            {"course_id": "TH1404-01", "title": "Thesis - Machine Learning", "supervisor_id": "T2001", "year": 1404, "semester": "First", "capacity": 2, "resources": ["Ref A"], "sessions": 10, "units": 6},
            {"course_id": "TH1404-02", "title": "Thesis - Computer Vision", "supervisor_id": "T2002", "year": 1404, "semester": "First", "capacity": 1, "resources": ["Ref B"], "sessions": 10, "units": 6},
        ]
        save_json("courses.json", courses)
    for fn, default in [("requests.json", []), ("theses.json", []), ("defenses.json", [])]:
        if load_json(fn, None) is None:
            save_json(fn, default)