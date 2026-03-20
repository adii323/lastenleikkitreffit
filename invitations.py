import db

def add_invitation(title, name, location, day, time, age, user_id):
    sql = """INSERT INTO invitations (title, name, location, day, time, age, user_id) 
    VALUES (?, ? ,?, ?, ?, ?, ?)"""
    db.execute(sql, [title, name, location, day, time, age, user_id])

def get_invitations():
    sql = "SELECT id, title FROM invitations ORDER BY id DESC"
    return db.query(sql)

def get_invitation(invitation_id):
    sql = """SELECT invitations.title, 
                    invitations.name,
                    invitations.day,
                    invitations.time, 
                    users.username
            FROM invitations, users
            WHERE invitations.user_id = users.id AND
            invitations.id = ?"""
    return db.query(sql, [invitation_id])[0]