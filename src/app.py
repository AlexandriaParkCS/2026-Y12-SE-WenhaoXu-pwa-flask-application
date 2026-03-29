import logging

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
from datetime import timedelta

from sqldb import SqlDb

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
app.permanent_session_lifetime = timedelta(minutes=2) # 2 minutes for testing purposes
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


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")

'''
@app.route("/form.html", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        email = request.form["email"]
        text = request.form["text"]
        print(f"<From(email={email}, text='{text}')>")
        return render_template("/form.html")
    else:
        return render_template("/form.html")
'''

@app.route("/login.html", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form["email"]
        password = request.form["password"]
        #print(f"<From(email={email}, password={password})>")
        session["user"] = email
        return redirect(url_for("user"))
    else:
        # add code to 
        return render_template("/login.html")

@app.route("/signup.html", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        username = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        #print(f"<From(email={email}, password={password}, username={username})>")
        return render_template("/signup.html")
    else:
        return render_template("/signup.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        user = session["user"]
        return render_template("userpage.html")
    else:
        redirect(url_for("login.html"))


# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data)
    return "done"


if __name__ == "__main__":
    # app.logger.debug("Started")
    app.run(debug=True, host="0.0.0.0", port=5000)
