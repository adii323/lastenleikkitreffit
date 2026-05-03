import db
from werkzeug.security import generate_password_hash, check_password_hash

def get_user(user_id):
    sql = """SELECT id, username
            FROM users
            WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_invitations(user_id):
    sql = """SELECT id, title, location, day, time, user_id
            FROM invitations
            WHERE user_id = ?
            ORDER BY day, time"""
    return db.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    rows = db.query(sql, [username])
    if not rows:
        return None
    result = db.query(sql, [username])[0]
    user_id = result["id"]
    password_hash = result["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None