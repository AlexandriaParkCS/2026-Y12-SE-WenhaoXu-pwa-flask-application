import logging

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
from datetime import timedelta

from sqldb import SqlDb
from validation import validate
from encrypt import hash_password, check_password

# OR
# from ormdb import OrmDb

log = logging.getLogger(__name__)
logging.basicConfig(
    filename="runtime/log/app.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format=" %(asctime)s %(message)s",
)

sql_db = SqlDb("runtime/db/sql.db")

app = Flask(__name__)
app.secret_key = b"FtI7fPmZ5Gw4xFg3"  # To get a unique basic 16 key: https://acte.ltd/utils/randomkeygen
csrf = CSRFProtect(app)


# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["POST", "GET"])
@csp_header(
    {
        # Server Side CSP is consistent with meta CSP in layout.html
        "base-uri": "'self'",
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self'",
        "img-src": "'self' data:",
        "media-src": "'self'",
        "font-src": "'self'",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'",
    }
)
def index():
    if "user" not in session:
        return render_template("/index.html")
    else:
        return redirect(url_for("home"))

# find someway to deal w/ this
@app.route("/privacy", methods=["GET"])
def privacy():
    return render_template("/privacy.html")

# Perhaps change to two screens; login by email or login by username
@app.route("/login", methods=["POST", "GET"])
def login():
    if "user" not in session:
        if request.method == "POST":
            session.permanent = True
            email = request.form["email"]
            password = request.form["password"] #(TEST PASSWORD: Test1234&%)
            try:
                credentials = sql_db.get_user_by_email(email)
                if check_password(password, credentials["password_hash"]) == True:
                    session["user"] = email
                    return redirect(url_for("home")) # homepage / userpage
                else:
                    flash("Incorrect password.", "error")
                    return render_template("/login.html")
            except Exception as e:
                print(f"Login Error: {e}")
                flash("Something went wrong.", "error")
                return render_template("/login.html")
        else:
            return render_template("/login.html")
    else: return redirect(url_for("home"))

@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    if "user" not in session:
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

            # Repeat check
            try:
                cred_by_name = sql_db.get_user_by_username(username)
                cred_by_email = sql_db.get_user_by_email(email)
                if cred_by_name["username"] == username:
                    print("Error: Username already exists!")
                    flash("Error: Username is already taken!", "error")
                    return render_template("/signup.html")
                elif cred_by_email["email"] == email:
                    print("Error: Email already exists!")
                    flash("Error: Email already in use!", "error")
                    return render_template("/signup.html")
            except Exception as e:
                print(f"Error: {e}, HENCE no user or email has previously existed")
                pass

            # Validate
            NameValid = validate.vName(username)
            if NameValid != True:
                print(f"Name Error: {NameValid}")
                flash(NameValid, "error")
                return render_template("/signup.html")
            
            EmailValid = validate.vEmail(email)
            if EmailValid != True:
                print(f"Email Error: {EmailValid}")
                flash(EmailValid, "error")
                return render_template("/signup.html")
            
            PwdValid = validate.vPassword(password)
            if PwdValid != True:
                print(f"Password Error: {PwdValid}")
                flash(PwdValid, "error")
                return render_template("/signup.html")
            
            # sanitise
            username = validate.sanitise(username)
            email = validate.sanitise(email)
            password = validate.sanitise(password)

            # hash password (TEST PASSWORD: Test1234&%)
            pwd_hash = hash_password(password)
            # creation of user
            try:
                sql_db.create_user(username, email, pwd_hash)
                return redirect("/confirmation") # confirmation screen
            except Exception as e:
                print(e)
                flash(f"Something went wrong!", "error") # flash a failure msg
                return render_template("/signup.html")
        else:
            return render_template("/signup.html")
    else: return redirect(url_for("home"))

@app.route("/confirmation", methods=["POST", "GET"])
def sgnconfirm():
    return render_template("/signup2.html")

# THIS NEEDS WORK
@app.route("/home", methods=["POST", "GET"]) #user page / homepage
def home():
    if "user" in session:
        return render_template("userpage.html")
    else:
        redirect(url_for("login"))

@app.route("/settings", methods=["POST", "GET"])
def settings():
    if "user" in session:
        return render_template("settings.html")
    else:
        return redirect(url_for("login"))

# Example Logout; Change maybe?

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

# REMEMBER TO CHANGE LOGIC IN TRYEXCEPT IF LOGIN GETS CHANGED TO EITHER BY USER/EMAIL
@app.route("/deleteAccount", methods=["POST", "GET"])
def deleteAccount():
    if "user" in session:
        if request.method == "POST":
            username = request.form["deleteAcc"]
            password = request.form["password"]
            email = session["user"] # change later
            try:
                userCheck = False
                pwdCheck = False
                credentials = sql_db.get_user_by_email(email) # Ensure no delete other ppl password if guessed
                # Check password, username
                if credentials["username"] == username: 
                    userCheck = True
                if check_password(password, credentials["password_hash"]) == True: 
                    pwdCheck = True

                if userCheck == False: # match username w/ database
                    flash("Error: Incorrect Username!", "error")
                    return render_template("delete_account.html")
                elif pwdCheck == False:
                    flash("Error: Incorrect Password!", "error")
                    return render_template("delete_account.html")
                else:
                    print(f"User:{credentials["username"]} deleted!")
                    session.pop("user", None)
                    sql_db.delete_user_by_email(email)
                    return redirect(url_for("index"))
            except Exception as e:
                print(f"Error deleting account: {e}")
                flash(f"Error deleting account: {e}", "error")
                return render_template("delete_account.html")
        else:
            return render_template("delete_account.html") # In session
    else: 
        return redirect(url_for("index")) # Not in session 

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data)
    return "done"


if __name__ == "__main__":
    # app.logger.debug("Started")
    app.run(debug=True, host="0.0.0.0", port=5000)
