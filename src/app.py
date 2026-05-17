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
from datetime import datetime
from datehandler import timeconvert

from sqldb import SqlDb
from validation import validate
from encryption import encrypt

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
    if "user" not in session:
        return render_template("/privacy.html")
    else:
        return render_template("/privacy2.html")

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
                if encrypt.check_password(password, credentials["password_hash"]) == True:
                    session["user"] = credentials["id"]
                    print(f"Session: {credentials["id"]}")
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
                if cred_by_name["username"] == username:
                    print("Error: Username already exists!")
                    flash("Error: Username is already taken!", "error")
                    return render_template("/signup.html")
            except Exception as e:
                print(f"Error: {e}, HENCE no user has previously existed")

            try:
                cred_by_email = sql_db.get_user_by_email(email)
                if cred_by_email["email"] == email:
                    print("Error: Email already exists!")
                    flash("Error: Email already in use!", "error")
                    return render_template("/signup.html")
            except Exception as e:
                print(f"Error: {e}, HENCE no email has previously existed")

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
            pwd_hash = encrypt.hash_password(password)
            # creation of user
            try:
                sql_db.create_user(username, email, pwd_hash)
                return redirect("/confirmation") # confirmation screen
            except Exception as e:
                print(e)
                flash(f"Something went wrong!", "error")
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
        weekday = datetime.now().weekday()
        chores = sql_db.get_all_chores_by_day(session["user"], weekday)
        weekday = timeconvert.convertInt(weekday)
        chores = timeconvert.convertTupleList(chores)        

        credentials = sql_db.get_user_by_id(session["user"])
        user = credentials["username"]

        return render_template("userpage.html", chores=chores, weekday=weekday, usr=user)
    else:
        redirect(url_for("login"))

# dashboard
@app.route("/settings", methods=["POST", "GET"])
def settings():
    if "user" in session:
        return render_template("settings.html")
    else:
        return redirect(url_for("login"))

# Example Logout; Change maybe?

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "user" in session:
        session.pop("user", None)
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))

# DELETE ACCOUNT
@app.route("/deleteAccount", methods=["POST", "GET"])
def deleteAccount():
    if "user" in session:
        if request.method == "POST":
            username = request.form["deleteAcc"]
            password = request.form["password"]
            id = session["user"]
            try:
                userCheck = False
                pwdCheck = False
                credentials = sql_db.get_user_by_id(id) # Ensure no delete other ppl password if guessed
                # Check password, username
                if credentials["username"] == username: 
                    userCheck = True
                if encrypt.check_password(password, credentials["password_hash"]) == True: 
                    pwdCheck = True

                if userCheck == False: # match username w/ database
                    flash("Error: Incorrect Username!", "error")
                    return render_template("delete_account.html")
                elif pwdCheck == False:
                    flash("Error: Incorrect Password!", "error")
                    return render_template("delete_account.html")
                else:
                    session.pop("user", None)
                    sql_db.delete_user_by_email(credentials["email"])
                    print(f"User: '{credentials["username"]}' deleted!")
                    return redirect(url_for("index"))
            except Exception as e:
                print(f"Error deleting account: {e}")
                flash(f"Error deleting account: {e}", "error")
                return render_template("delete_account.html")
        else:
            return render_template("/delete_account.html") # In session
    else: 
        return redirect(url_for("index")) # Not in session 

# CHANGE USER DETAILS
@app.route("/changedetails", methods=["POST", "GET"])
def changeDetails():
    if "user" in session:
        return render_template("/change.html")
    else:
        return redirect(url_for("index"))

# CHANGE USERNAME
@app.route("/changeUsername", methods=["POST", "GET"])
def changeUsername():
    if "user" in session:
        if request.method == "POST":
            old_user = request.form["current_user"]
            new_user = request.form["new_user"]
            password = request.form["password"]
            id = session["user"]
            # CHECK IF REPEAT NAME
            try:
                cred_by_name = sql_db.get_user_by_username(new_user)
                if cred_by_name["username"] == new_user:
                    print("Error during username update: Username already exists")
                    flash("Error: Username is taken!", "error")
                    return render_template("/change_username.html")
            except:
                pass

            # VALIDATE + SANITISE NEW NAME
            NameValid = validate.vName(new_user)
            if NameValid != True:
                print(f"Name Error: {NameValid}")
                flash(NameValid, "error")
                return render_template("/signup.html")
            new_user = validate.sanitise(new_user)

            # CHECK PASSWORD
            try:
                credentials = sql_db.get_user_by_id(id)
                if encrypt.check_password(password, credentials["password_hash"]) != True:
                    print("Error during username update: Incorrect Password")
                    flash("Error: Incorrect Password", "error")
                    return render_template("/change_username.html")
            # CHECK IF OLD USERNAME IS SAME
                if credentials["username"] == old_user:
                    sql_db.update_user_username(new_user, credentials["username"])
                    print("Username updated!")
                    return redirect(url_for("home"))
                else:
                    print("Error during username update: Username not matching")
                    flash("Error: old username not matching", "error")
                    return render_template("/change_username.html")
            except Exception as e:
                print(f"Error during username update: {e}")
                flash("Something went wrong", "error")
                return render_template("/change_username.html")
        else:
            return render_template("/change_username.html")
    else:
        return redirect(url_for("index"))

# CHANGE EMAIL
@app.route("/changeEmail", methods=["POST", "GET"])
def changeEmail():
    if "user" in session:
        if request.method == "POST":
            old_email = request.form["current_email"]
            new_email = request.form["new_email"]
            password = request.form["password"]
            id = session["user"]
            # CHECK IF REPEAT EMAIL
            try:
                cred_by_email = sql_db.get_user_by_email(new_email)
                if cred_by_email["email"] == new_email:
                    print("Error during email update: Email already exists")
                    flash("Error: Email is taken!", "error")
                    return render_template("/change_email.html")
            except:
                pass

            # VALID + SANITISE NEW EMAIL
            EmailValid = validate.vEmail(new_email)
            if EmailValid != True:
                print(f"Email Error: {EmailValid}")
                flash(EmailValid, "error")
                return render_template("/signup.html")
            new_email = validate.sanitise(new_email)

            # CHECK PASSWORD
            try:
                credentials = sql_db.get_user_by_id(id)
                if encrypt.check_password(password, credentials["password_hash"]) != True:
                    print("Error during username update: Incorrect Password")
                    flash("Error: Incorrect Password", "error")
                    return render_template("/change_email.html")
            # CHECK IF OLD USERNAME IS SAME
                if credentials["email"] == old_email:
                    sql_db.update_user_email(new_email, credentials["username"])
                    print("Email Updated!")
                    return redirect(url_for("home"))
                else:
                    print("Error during email update: Email not matching")
                    flash("Error: Old email not matching")
                    return render_template("/change_email.html")
            except Exception as e:
                print(f"Error during email update: {e}")
                flash("Something went wrong", "error")
                return render_template("/change_email.html")
        else:
            return render_template("/change_email.html")
    else:
        return redirect(url_for("index"))

# CHANGE PASSWORD
@app.route("/changePassword", methods=["POST", "GET"])
def changePassword():
    if "user" in session:
        if request.method == "POST":
            old_password = request.form["current_password"]
            new_password = request.form["new_password"]
            id = session["user"]
            # VALIDATE + SANITISE PASSWORD
            PwdValid = validate.vPassword(new_password)
            if PwdValid != True:
                print(f"Email Error: {PwdValid}")
                flash(PwdValid, "error")
                return render_template("/signup.html")
            new_password = validate.sanitise(new_password)
            # CHECK OLD PASSWORD
            try:
                credentials = sql_db.get_user_by_id(id)
                if encrypt.check_password(old_password, credentials["password_hash"]) == True:
                    new_password = encrypt.hash_password(new_password)
                    sql_db.update_user_password(new_password, credentials["username"])
                    print("Password updated!")
                    return redirect(url_for("home"))
                else:
                    print("Error during password update: Password not matching")
                    flash("Error: old password not matching")
                    return render_template("/change_password.html")
            except Exception as e:
                print(f"Error during password update: {e}")
                flash("Something went wrong.", "error")
                return render_template("/change_password.html")
        else:
            return render_template("/change_password.html")
    else:
        return redirect(url_for("index"))

@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    if "user" in session:
        if request.method == "POST": # Create Chores
            # Task name and description
            task = request.form["task"]
            desc = request.form["description"]
            # Time
            weekday = request.form["weekday"]
            meridiem = request.form["meridiem"] 
            time_hour = request.form["timehour"]
            time_minute = request.form["timeminute"]
            # Conversion to 24hour time
            time_hour = timeconvert.convertMeridiem(time_hour, meridiem)

            chores = sql_db.get_all_chores(session["user"])
            chores = timeconvert.convertTupleList(chores)

            # Validations
            taskValid = validate.vTask(task)
            if taskValid != True:
                print(f"Error creating task: {taskValid}")
                flash(taskValid, "error")
                return render_template("/dashboard.html", chores=chores)
            
            descValid = validate.vDesc(desc)
            if descValid != True:
                print(f"Error creating task: {descValid}")
                flash(descValid, "error")
                return render_template("/dashboard.html", chores=chores)
            
            # Sanitisations
            weekday = timeconvert.convertDate(weekday)
            task = validate.sanitise(task)
            desc = validate.sanitise(desc)
            sql_db.create_chore(task, desc, weekday, time_hour, time_minute, session["user"])

            # Display again
            chores = sql_db.get_all_chores(session["user"]) # do this so its up to date
            chores = timeconvert.convertTupleList(chores)
            return render_template("/dashboard.html", chores=chores)
        else:
            # Display
            chores = sql_db.get_all_chores(session["user"])
            chores = timeconvert.convertTupleList(chores)
            return render_template("/dashboard.html", chores=chores) # chores=chores tells the page
    else:
        return redirect(url_for("index"))

@app.route("/delete_chore", methods=["POST"])
def delete_chore():
    if "user" in session:
        if request.method == "POST":
            choreID = request.form["chore_id"]
            sql_db.delete_chore(choreID, session["user"])
            print("CHORE ID:", choreID)
            print("SESSION USER:", session["user"])
            return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("index"))

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data)
    return "done"


if __name__ == "__main__":
    # app.logger.debug("Started")
    app.run(debug=True, host="0.0.0.0", port=5000)
