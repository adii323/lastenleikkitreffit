import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def add_invitation(title, name, location, day, time, childs_name, age, info, user_id, classes):
    sql = """INSERT INTO invitations (title, name, location, day, time, childs_name, age,
            info, user_id) VALUES (?, ? ,?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [title, name, location, day, time, childs_name, age, info, user_id])

    invitation_id = db.last_insert_id()

    sql = "INSERT INTO invitation_classes (invitation_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [invitation_id, title, value])

def add_answer(invitation_id, user_id, childs_name, age):
    sql = "INSERT INTO answers (invitation_id, user_id, childs_name, age) VALUES (?, ?, ?, ?)"
    db.execute(sql, [invitation_id, user_id, childs_name, age])

def add_message(invitation_id, user_id, content):
    sql = """INSERT INTO messages (invitation_id, user_id, sent_at, content)
            VALUES (?, ?, datetime('now'),?)"""
    db.execute(sql, [invitation_id, user_id, content])

def get_answers(invitation_id):
    sql = """SELECT answers.childs_name, answers.age, users.id user_id, users.username
            FROM answers, users
            WHERE answers.invitation_id = ? AND answers.user_id = users.id"""
    return db.query(sql, [invitation_id])

def get_messages(invitation_id):
    sql = """SELECT messages.id, messages.content, messages.sent_at, users.id user_id,
            users.username
            FROM messages, users
            WHERE messages.invitation_id = ? AND messages.user_id = users.id
            ORDER BY messages.id"""
    return db.query(sql, [invitation_id])

def get_classes(invitation_id):
    sql = "SELECT title, value FROM invitation_classes WHERE invitation_id = ?"
    return db.query(sql, [invitation_id])

def get_invitations():
    sql = """SELECT invitations.id, invitations.title, invitations.location, invitations.day,
            invitations.time,
            users.id user_id, users.username
            FROM invitations, users
            WHERE invitations.user_id = users.id
            ORDER BY invitations.day"""
    return db.query(sql)

def get_invitation(invitation_id):
    sql = """SELECT invitations.id,
                    invitations.title,
                    invitations.location,
                    invitations.name,
                    invitations.day,
                    invitations.time,
                    invitations.age,
                    invitations.childs_name,
                    invitations.info,
                    users.id user_id,
                    users.username
            FROM invitations, users
            WHERE invitations.user_id = users.id AND
            invitations.id = ?"""
    result = db.query(sql, [invitation_id])
    return result[0] if result else None

def update_invitation(invitation_id, title, name, location, day, time, childs_name, age, info, classes):
    sql = """UPDATE invitations SET title = ?,
                                    name = ?,
                                    location = ?,
                                    day = ?,
                                    time = ?,
                                    childs_name = ?,
                                    age = ?,
                                    info = ?
                                WHERE id = ?"""
    db.execute(sql, [title, name, location, day, time, childs_name, age, info, invitation_id])

    sql = "DELETE FROM invitation_classes WHERE invitation_id = ?"
    db.execute(sql, [invitation_id])

    sql = "INSERT INTO invitation_classes (invitation_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [invitation_id, title, value])


def remove_invitation(invitation_id):
    sql = "DELETE FROM invitation_classes WHERE invitation_id = ?"""
    db.execute(sql, [invitation_id])

    sql = "DELETE FROM answers WHERE invitation_id = ?"
    db.execute(sql, [invitation_id])

    sql = "DELETE FROM messages WHERE invitation_id = ?"
    db.execute(sql, [invitation_id])

    sql = "DELETE FROM invitations WHERE id = ?"""
    db.execute(sql, [invitation_id])

def delete_message(message_id):
    sql = "DELETE FROM messages WHERE id = ?"""
    db.execute(sql, [message_id])


def find_invitations(query):
    sql ="""SELECT id, title, day, time, location, user_id
            FROM invitations
            WHERE title LIKE ? OR name LIKE ?
            ORDER BY day"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])
