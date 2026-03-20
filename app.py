import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new_invitation")
def new_invitation():
    return render_template("new_invitation.html")

@app.route("/create_invitation", methods=["POST"])
def create_invitation():
    title = request.form["title"]
    location = request.form["location"]
    time = request.form["time"]
    age = request.form["age"]
    print("Create invitation session useride = ", session["user_id"])
    user_id = session["user_id"]

    sql = """INSERT INTO invitations (title, location, time, age, user_id) 
    VALUES (?, ? ,?, ?, ?)"""
    db.execute(sql, [title, location, time, age, user_id])

    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/check", methods=["POST"])
def check():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])[0]
    #print(result["id"])
    user_id = result["id"]
    #print(user_id)
    password_hash = result["password_hash"]
    #print(password_hash)

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        #print(session["user_id"])
        session["username"] = username
        #print(session["username"])
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    #del session["user_id"]
    del session["username"]
    return redirect("/")