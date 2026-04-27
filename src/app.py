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
from sanitiser import sanitise
from validater import validate
from encrypt import hash_password

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
    return render_template("/index.html")


@app.route("/privacy", methods=["GET"])
def privacy():
    return render_template("/privacy.html")

# Perhaps change to two screens; login by email or login by username
# Unfinished, need to add the user information onto the database
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form["email"]
        password = request.form["password"]
        '''
        try:
            sql_db.get_user_by_email(email)
        except:
            pass
        '''
        session["user"] = email
        return redirect(url_for("user"))
    else:
        # add code to 
        return render_template("/login.html")

@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        # Sanitise/Validate
        NameValid = validate.vName(username)
        if NameValid != True:
            flash(NameValid, "error")
            return render_template("/signup.html")
        
        EmailValid = validate.vEmail(email)
        if EmailValid != True:
            flash(EmailValid, "error")
            return render_template("/signup.html")
        
        PwdValid = validate.vPassword(password)
        if PwdValid != True:
            flash(PwdValid, "error")
            return render_template("/signup.html")

        # hash password (TEST PASSWORD: Test1234&%)
        pwd_hash = hash_password(password)
        try:
            sql_db.create_user(username, email, pwd_hash)
            return redirect(url_for("login")) # change to a confirmation screen of sorts
        except Exception as e:
            flash(f"Something went wrong!", "error") # flash a failure msg
            return render_template("/signup.html")
    else:
        return render_template("/signup.html")

@app.route("/confirmation", methods=["POST", "GET"])
def sgnconfirm():
    return render_template("/signup2.html")

# THIS NEEDS WORK
@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        user = session["user"]
        return render_template("userpage.html")
    else:
        redirect(url_for("login"))


# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data)
    return "done"


if __name__ == "__main__":
    # app.logger.debug("Started")
    app.run(debug=True, host="0.0.0.0", port=5000)
