import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import invitations
from datetime import date

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_invitations = invitations.get_invitations()
    return render_template("index.html", invitations = all_invitations)

@app.route("/find_invitations")
def find_invitations():
    query = request.args.get("query")
    if query:
        results = invitations.find_invitations(query)
    else:
        query = ""
        results = []
    return render_template("find_invitations.html", query=query, results=results)

@app.route("/invitation/<int:invitation_id>")
def show_invitation(invitation_id):
    invitation = invitations.get_invitation(invitation_id)
    if not invitation:
        abort(404)
    return render_template("show_invitation.html", invitation = invitation)

@app.route("/new_invitation")
def new_invitation():
    require_login()
    return render_template("new_invitation.html", min_day=date.today().isoformat())

@app.route("/create_invitation", methods=["POST"])
def create_invitation():
    require_login()

    title = request.form["title"]
    if len(title) > 50:
        abort(403)
    name = request.form["name"]
    if not name or len(name) > 50:
        abort(403)
    location = request.form["location"]
    if not location or len(location) > 50:
        abort(403)
    day = request.form["day"]
    if not day or day < date.today().isoformat():
        abort(403)
    time = request.form["time"]
    age_raw = request.form["age"]
    try:
        age = int(age_raw)
    except (TypeError, ValueError):
        # Not an integer
        abort(403)
    if not age or age < 1 or age > 18:
        abort(403)
    childs_name = request.form["childs_name"]
    if not childs_name or len(childs_name) > 50:
        abort(403)
    info = request.form["info"]
    if not info or len(info) > 1000:
        abort(403)
    #print("Create invitation session useride = ", session["user_id"])
    user_id = session["user_id"]

    invitations.add_invitation(title, name, location, day, time, childs_name, age, info, user_id)

    return redirect("/")

@app.route("/edit_invitation/<int:invitation_id>")
def edit_invitation(invitation_id):
    require_login()
    invitation = invitations.get_invitation(invitation_id)
    if not invitation:
        abort(404)
    if invitation["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_invitation.html", min_day=date.today().isoformat(), invitation=invitation)

@app.route("/update_invitation", methods=["POST"])
def update_invitation():
    require_login()
    invitation_id = request.form["invitation_id"]
    invitation = invitations.get_invitation(invitation_id)
    if not invitation:
        abort(404)
    if invitation["user_id"] != session["user_id"]:
        abort(403)
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    name = request.form["name"]
    if not name or len(name) > 50:
        abort(403)
    location = request.form["location"]
    if not location or len(location) > 50:
        abort(403)
    day = request.form["day"]
    if not day or day < date.today().isoformat():
        abort(403)
    time = request.form["time"]
    childs_name = request.form["childs_name"]
    if not childs_name or len(childs_name) > 50:
        abort(403)
    age_raw = request.form["age"]
    try:
        age = int(age_raw)
    except (TypeError, ValueError):
        # Not an integer
        abort(403)
    if not age or age < 1 or age > 18:
        abort(403)
    info = request.form["info"]
    if not info or len(info) > 1000:
        abort(403)

    invitations.update_invitation(invitation_id, title, name, location, day, time, childs_name, age, info)

    return redirect("/invitation/" + str(invitation_id))

@app.route("/remove_invitation/<int:invitation_id>", methods=["GET", "POST"])
def remove_invitation(invitation_id):
    require_login()
    invitation = invitations.get_invitation(invitation_id)
    if not invitation:
        abort(404)    
    if invitation["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_invitation.html", invitation=invitation)
      
    if request.method == "POST":
        if "remove" in request.form:
            invitations.remove_invitation(invitation_id)
            return redirect("/")
        else:
            return redirect("/invitation/" + str(invitation_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("register.html", error_password="Salasanat eivät täsmää", username=username), 400
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("register.html", error_username="Tunnus on jo käytössä", username=username), 400

    return render_template("login.html", message="Tunnus luotu! Kirjaudu sisään sovellukseen:")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/check", methods=["POST"])
def check():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    rows = db.query(sql, [username])
    if not rows:
        return render_template("login.html", error="Väärä käyttäjänimi tai salasana"), 400
    #print(result["id"])
    result = db.query(sql, [username])[0]
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
        return render_template("login.html", error="Väärä käyttäjänimi tai salasana"), 400

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")