import bcrypt
from data_handler import load_json, save_json
from typing import Dict, Optional

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    """Checks a password against a hashed password."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        return False # Handles case where hash is not a valid bcrypt hash

def find_user_by_id(user_id: str) -> Optional[Dict]:
    """Finds a user by their ID."""
    users = load_json("users.json", [])
    for u in users:
        if u["id"] == user_id:
            return u
    return None

def upgrade_user_password(user: Dict):
    """Hashes the user's plaintext password and saves the updated user list."""
    if 'password' in user:
        user['password_hash'] = hash_password(user['password'])
        del user['password']
        users = load_json("users.json", [])
        for i, u in enumerate(users):
            if u.get('id') == user.get('id'):
                users[i] = user
                break
        save_json("users.json", users)

def authenticate_user(user_id: str, password: str) -> Optional[Dict]:
    """Authenticates a user with their ID and password, handling both hashed and plaintext passwords."""
    user = find_user_by_id(user_id)
    if not user:
        return None

    # Check for hashed password
    if 'password_hash' in user:
        if check_password(password, user['password_hash']):
            return user
    
    # Fallback to plaintext password (for first-time login)
    elif 'password' in user:
        if user['password'] == password:
            upgrade_user_password(user)
            return user

    return None