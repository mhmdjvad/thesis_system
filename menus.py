import getpass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from data_handler import load_json, save_json
from user_auth import find_user_by_id

# ----------------------------------------------------------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------------------------------------------------------

def now_iso():
    """Return current datetime in ISO format."""
    return datetime.now().isoformat(timespec='seconds')

def get_next_id(data: List[Dict], prefix: str) -> str:
    """Generate the next available ID based on prefix."""
    max_id = 0
    for item in data:
        try:
            current_id = int(item[f"{prefix.lower()}_id"].strip(prefix))
            if current_id > max_id:
                max_id = current_id
        except (ValueError, KeyError):
            pass
    return f"{prefix}{max_id + 1}"

def find_course_by_id(course_id: str) -> Optional[Dict]:
    """Finds a course by its ID."""
    courses = load_json("courses.json", [])
    for c in courses:
        if c["course_id"] == course_id:
            return c
    return None

def find_request_by_id(request_id: str) -> Optional[Dict]:
    """Finds a request by its ID."""
    requests = load_json("requests.json", [])
    for r in requests:
        if r["request_id"] == request_id:
            return r
    return None

def find_thesis_by_id(thesis_id: str) -> Optional[Dict]:
    """Finds a thesis by its ID."""
    theses = load_json("theses.json", [])
    for t in theses:
        if t["thesis_id"] == thesis_id:
            return t
    return None

def find_defense_by_id(defense_id: str) -> Optional[Dict]:
    """Finds a defense by its ID."""
    defenses = load_json("defenses.json", [])
    for d in defenses:
        if d["defense_id"] == defense_id:
            return d
    return None

def search_theses(query: str) -> List[Dict]:
    """Searches theses by title, abstract, or keywords."""
    theses = load_json("theses.json", [])
    query = query.lower()
    results = []
    for t in theses:
        if query in t.get("title", "").lower() or \
           query in t.get("abstract", "").lower() or \
           any(query in k.lower() for k in t.get("keywords", [])):
            results.append(t)
    return results

# ----------------------------------------------------------------------------------------------------------------------
# Student Menu
# ----------------------------------------------------------------------------------------------------------------------

def student_menu(user: Dict):
    """Main menu for students."""
    while True:
        print("\n--- Student Menu ---")
        print("1) Request a Thesis")
        print("2) View Request Status")
        print("3) Re-submit a Request")
        print("4) Request a Defense")
        print("5) Search Thesis Archive")
        print("0) Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            courses = load_json("courses.json", [])
            for c in courses:
                supervisor = find_user_by_id(c['supervisor_id'])
                supervisor_name = supervisor['name'] if supervisor else 'Unknown'
                print(f"ID: {c['course_id']} - Title: {c['title']} - Supervisor: {supervisor_name} - Capacity: {c['capacity']}")
            
            course_id = input("Enter course ID: ").strip()
            course = find_course_by_id(course_id)

            if course is None:
                print("Course not found.")
                continue
            
            if course['capacity'] <= 0:
                print("This course is at full capacity.")
                continue

            requests = load_json("requests.json", [])
            existing_request = next((r for r in requests if r['student_id'] == user['id'] and r['status'] in ['Pending', 'Accepted']), None)

            if existing_request:
                print("You already have a pending or accepted request.")
                continue

            proposal = input("Short proposal (optional): ").strip()
            
            new_request = {
                "request_id": get_next_id(requests, "R"),
                "student_id": user['id'],
                "course_id": course['course_id'],
                "proposal": proposal,
                "status": "Pending",
                "date_submitted": now_iso(),
                "history": [{"status": "Pending", "date": now_iso(), "note": "Submitted by student"}]
            }
            requests.append(new_request)
            save_json("requests.json", requests)
            print(f"Request {new_request['request_id']} submitted successfully.")

        elif choice == "2":
            requests = load_json("requests.json", [])
            student_requests = [r for r in requests if r['student_id'] == user['id']]
            if not student_requests:
                print("No requests found.")
                continue
            for req in student_requests:
                print(f"Request ID: {req['request_id']} - Course Title: {find_course_by_id(req['course_id'])['title']} - Status: {req['status']}")
                print("History:")
                for h in req['history']:
                    print(f"  - Status: {h['status']} - Date: {h['date']} - Note: {h.get('note', '')}")

        elif choice == "3":
            requests = load_json("requests.json", [])
            student_requests = [r for r in requests if r['student_id'] == user['id'] and r['status'] == 'Rejected']
            if not student_requests:
                print("You do not have any rejected requests to re-submit.")
                continue
            
            for req in student_requests:
                course = find_course_by_id(req['course_id'])
                print(f"Request ID: {req['request_id']} - Course Title: {course['title']} - Status: {req['status']}")
            
            request_id = input("Enter the ID of the rejected request to re-submit: ").strip()
            req = find_request_by_id(request_id)
            if not req or req['student_id'] != user['id'] or req['status'] != 'Rejected':
                print("Invalid request or cannot be re-submitted.")
                continue

            req['status'] = 'Pending'
            req['date_submitted'] = now_iso()
            req['history'].append({"status": "Pending", "date": now_iso(), "note": "Re-submitted by student"})
            save_json("requests.json", requests)
            print(f"Request {req['request_id']} re-submitted successfully.")

        elif choice == "4":
            theses = load_json("theses.json", [])
            thesis = next((t for t in theses if t['student_id'] == user['id']), None)
            
            if not thesis or thesis['status'] != 'Ongoing':
                print("You do not have an active thesis or it's not ready for defense.")
                continue
            
            if thesis['ready_for_defense']:
                print("You have already requested a defense. It is currently under review.")
                continue
            
            thesis['ready_for_defense'] = True
            save_json("theses.json", theses)
            print("Defense request sent to your supervisor. Please wait for approval.")

        elif choice == "5":
            query = input("Enter keywords to search: ").strip()
            results = search_theses(query)
            if not results:
                print("No results found.")
            else:
                for t in results:
                    print(f"Thesis: {t.get('title','')} - Student: {t['student_id']} - Status: {t.get('status')}")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

# ----------------------------------------------------------------------------------------------------------------------
# Supervisor Menu
# ----------------------------------------------------------------------------------------------------------------------

def supervisor_menu(user: Dict):
    """Main menu for supervisors."""
    while True:
        print("\n--- Supervisor Menu ---")
        print("1) View new requests")
        print("2) View supervised theses")
        print("3) Schedule a defense")
        print("0) Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            requests = load_json("requests.json", [])
            supervisor_requests = [r for r in requests if find_course_by_id(r['course_id'])['supervisor_id'] == user['id'] and r['status'] == 'Pending']
            if not supervisor_requests:
                print("No new requests.")
                continue
            
            for req in supervisor_requests:
                student = find_user_by_id(req['student_id'])
                print(f"Request ID: {req['request_id']} - Student: {student['name']} - Course Title: {find_course_by_id(req['course_id'])['title']}")
            
            request_id = input("Enter request ID to review: ").strip()
            req = find_request_by_id(request_id)
            if not req or find_course_by_id(req['course_id'])['supervisor_id'] != user['id'] or req['status'] != 'Pending':
                print("Invalid request.")
                continue

            status = input("Accept or reject? (accept/reject): ").strip().lower()
            if status == "accept":
                req['status'] = "Accepted"
                req['history'].append({"status": "Accepted", "date": now_iso(), "note": "Approved by supervisor"})
                
                # Create a new thesis entry
                theses = load_json("theses.json", [])
                new_thesis = {
                    "thesis_id": get_next_id(theses, "T"),
                    "student_id": req['student_id'],
                    "course_id": req['course_id'],
                    "supervisor_id": user['id'],
                    "title": "",
                    "abstract": "",
                    "keywords": [],
                    "files": {},
                    "ready_for_defense": False,
                    "status": "Ongoing",
                    "date_submitted": now_iso()
                }
                theses.append(new_thesis)
                save_json("theses.json", theses)
                
                # Update supervisor's supervise count
                users = load_json("users.json", [])
                supervisor_user = next(u for u in users if u['id'] == user['id'])
                supervisor_user['supervise_count'] += 1
                save_json("users.json", users)
                
                print("Request accepted and new thesis created.")
                
            elif status == "reject":
                req['status'] = "Rejected"
                req['history'].append({"status": "Rejected", "date": now_iso(), "note": "Rejected by supervisor"})
                print("Request rejected.")
            else:
                print("Invalid input.")
            
            save_json("requests.json", requests)

        elif choice == "2":
            theses = load_json("theses.json", [])
            my_theses = [t for t in theses if t['supervisor_id'] == user['id']]
            if not my_theses:
                print("You are not supervising any theses.")
                continue
            for t in my_theses:
                student = find_user_by_id(t['student_id'])
                print(f"ID: {t['thesis_id']} - Student: {student['name']} - Status: {t['status']}")
        
        elif choice == "3":
            theses = load_json("theses.json", [])
            ready_for_defense = [t for t in theses if t['supervisor_id'] == user['id'] and t.get('ready_for_defense')]
            if not ready_for_defense:
                print("No theses are ready for defense.")
                continue

            for t in ready_for_defense:
                student = find_user_by_id(t['student_id'])
                print(f"ID: {t['thesis_id']} - Student: {student['name']}")

            thesis_id = input("Enter thesis ID to schedule defense: ").strip()
            thesis = find_thesis_by_id(thesis_id)
            if not thesis or thesis['supervisor_id'] != user['id'] or not thesis.get('ready_for_defense'):
                print("Invalid thesis.")
                continue

            defense_date = input("Defense date (YYYY-MM-DD): ").strip()
            internal_reviewer = input("Internal reviewer ID: ").strip()
            external_reviewer = input("External reviewer ID: ").strip()
            
            # Simple validation for reviewers
            reviewer1 = find_user_by_id(internal_reviewer)
            reviewer2 = find_user_by_id(external_reviewer)
            if not reviewer1 or reviewer1['type'] not in ['reviewer', 'supervisor'] or not reviewer2 or reviewer2['type'] not in ['reviewer', 'supervisor']:
                print("Invalid reviewer IDs.")
                continue

            defense_data = {
                "date": defense_date,
                "internal_reviewer": internal_reviewer,
                "external_reviewer": external_reviewer,
                "attendance": [],
                "scores": {}
            }
            
            thesis['defense'] = defense_data
            thesis['status'] = "Scheduled"
            save_json("theses.json", theses)
            print("Defense scheduled successfully.")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

# ----------------------------------------------------------------------------------------------------------------------
# Reviewer Menu
# ----------------------------------------------------------------------------------------------------------------------

def reviewer_menu(user: Dict):
    """Main menu for reviewers."""
    while True:
        print("\n--- Reviewer Menu ---")
        print("1) View defenses awaiting scores")
        print("0) Exit")
        choice = input("Choice: ").strip()
        
        if choice == "1":
            theses = load_json("theses.json", [])
            my_defenses = [t for t in theses if t.get('defense') and (t['defense'].get('internal_reviewer') == user['id'] or t['defense'].get('external_reviewer') == user['id'])]
            
            if not my_defenses:
                print("No defenses to review.")
                continue
            
            for t in my_defenses:
                student = find_user_by_id(t['student_id'])
                print(f"Thesis ID: {t['thesis_id']} - Student: {student['name']} - Defense Date: {t['defense']['date']}")
            
            thesis_id = input("Enter thesis ID to record score: ").strip()
            thesis = find_thesis_by_id(thesis_id)

            if not thesis or not thesis.get('defense') or (thesis['defense'].get('internal_reviewer') != user['id'] and thesis['defense'].get('external_reviewer') != user['id']):
                print("Invalid thesis.")
                continue
            
            try:
                score = float(input("Final score (0 to 20): "))
                if not 0 <= score <= 20:
                    print("Score must be between 0 and 20.")
                    continue
                
                thesis['defense']['scores'][user['id']] = score
                save_json("theses.json", theses)
                print("Score recorded successfully.")
            except ValueError:
                print("Invalid score.")
        
        elif choice == "0":
            break
        else:
            print("Invalid choice.")