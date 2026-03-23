import db

def add_invitation(title, name, location, day, time, age, user_id):
    sql = """INSERT INTO invitations (title, name, location, day, time, age, user_id) 
    VALUES (?, ? ,?, ?, ?, ?, ?)"""
    db.execute(sql, [title, name, location, day, time, age, user_id])

def get_invitations():
    sql = "SELECT id, title FROM invitations ORDER BY id DESC"
    return db.query(sql)

def get_invitation(invitation_id):
    sql = """SELECT invitations.id,
                    invitations.title,
                    invitations.location, 
                    invitations.name,
                    invitations.day,
                    invitations.time, 
                    invitations.age,
                    users.id user_id,
                    users.username
            FROM invitations, users
            WHERE invitations.user_id = users.id AND
            invitations.id = ?"""
    return db.query(sql, [invitation_id])[0]

def update_invitation(invitation_id, title, name, location, day, time, age):
    sql = """UPDATE invitations SET title = ?,
                                    name = ?,
                                    location = ?,
                                    day = ?,
                                    time = ?,
                                    age = ?
                                WHERE id = ?"""
    db.execute(sql, [title, name, location, day, time, age, invitation_id])


def remove_invitation(invitation_id):
    sql = "DELETE FROM invitations WHERE id = ?"""
    db.execute(sql, [invitation_id])