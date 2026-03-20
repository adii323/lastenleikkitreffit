import db

def add_invitation(title, name, location, day, time, age, user_id):
    sql = """INSERT INTO invitations (title, name, location, day, time, age, user_id) 
    VALUES (?, ? ,?, ?, ?, ?, ?)"""
    db.execute(sql, [title, name, location, day, time, age, user_id])