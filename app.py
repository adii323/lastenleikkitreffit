import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
import config
import db
import invitations
import users
from datetime import date
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    all_invitations = invitations.get_invitations()
    return render_template("index.html", invitations = all_invitations)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    my_invitations = users.get_invitations(user_id)
    invitation_ids = []
    for invitation in my_invitations:
        invitation_ids.append(invitation["id"])
    answers = []
    for invitation_id in invitation_ids:
        answers.append(invitations.get_answers(invitation_id))
    return render_template("show_user.html", user = user, invitations=my_invitations, answers=answers)

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
    classes = invitations.get_classes(invitation_id)
    answers = invitations.get_answers(invitation_id)

    return render_template("show_invitation.html", invitation = invitation, classes=classes, answers=answers)

@app.route("/new_invitation")
def new_invitation():
    require_login()
    classes = invitations.get_all_classes()
    return render_template("new_invitation.html", min_day=date.today().isoformat(), classes=classes)


@app.route("/create_invitation", methods=["POST"])
def create_invitation():
    require_login()
    check_csrf()

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

    #print("Create invitation session useride = ", session["user_id"])
    user_id = session["user_id"]

    all_classes = invitations.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))
    
    invitations.add_invitation(title, name, location, day, time, childs_name, age, info, user_id, classes)

    return redirect("/")

@app.route("/create_answer", methods=["POST"])
def create_answer():
    require_login()
    check_csrf()

    childs_name = request.form["childs_name"]
    if not childs_name or len(childs_name) > 50:
        abort(403)
    age_raw = request.form["age"]
    try:
        age = int(age_raw)
    except (TypeError, ValueError):
        # Not an integer
        abort(403)
    message = request.form["message"]
    if not message or len(message) > 1000:
        abort(403)
    invitation_id = request.form["invitation_id"]
    invitation = invitations.get_invitation(invitation_id)
    if not invitation:
        abort(403)
    user_id = session["user_id"]

    invitations.add_answer(invitation_id, user_id, childs_name, age, message)

    return redirect("/invitation/" + str(invitation_id))

@app.route("/edit_invitation/<int:invitation_id>")
def edit_invitation(invitation_id):
    require_login()
    invitation = invitations.get_invitation(invitation_id)
    if not invitation:
        abort(404)
    if invitation["user_id"] != session["user_id"]:
        abort(403)

    all_classes = invitations.get_all_classes()
    print(all_classes)
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    print(classes)
    for entry in invitations.get_classes(invitation_id):
        classes[entry["title"]] = entry["value"]
    print(classes)

    return render_template("edit_invitation.html", min_day=date.today().isoformat(), invitation=invitation, 
                           classes=classes, all_classes=all_classes)

@app.route("/update_invitation", methods=["POST"])
def update_invitation():
    require_login()
    check_csrf()

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

    all_classes = invitations.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))
    
    if "update" in request.form:
        invitations.update_invitation(invitation_id, title, name, location, day, time, childs_name, age, info, classes)
        return redirect("/invitation/" + str(invitation_id))
    else:
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
        check_csrf()
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
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return render_template("register.html", error_username="Tunnus on jo käytössä", username=username) 
                                  
    return render_template("login.html", message="Tunnus luotu! Kirjaudu sisään sovellukseen:")

@app.route("/login")
def login():
    return render_template("login.html", next_page=request.referrer)

@app.route("/check", methods=["POST"])
def check():
    username = request.form["username"]
    password = request.form["password"]
    next_page = request.form["next_page"]

    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect(next_page)
    else:
        return render_template("login.html", error="Väärä käyttäjänimi tai salasana", next_page=next_page), 400


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")