import re
# NAME: pattern="[a-zA-Z0-9]{2,20}$"
# EMAIL: pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2, 4}$"

class validate:
    def sanitise(s):
        if s is None:
            return ""
        # possible malicous commands
        patterns = [
        r"'[^']*'",    # Single quotes
        r"`[^`]*`",    # Backticks
        r"\{[^}]*\}",  # Curly braces
        r"\[[^\]]*\]", # Square brackets
        r"\([^)]*\)",  # Parentheses
        r"<[^>]*>",    # Angle brackets
        r'"[^"]*"'     # Double quotes
        ]
        for pattern in patterns:
            s = re.sub(pattern, '', s)
        # remove any whitespace at front or back of string
        s = s.strip() 
        # replace any characters outside of the ASCII with a blank
        return re.sub(r"[^\x20-\x7E()]", "", s) 

    def vName(name):
        nameNotNull = True
        nameValid = True

        if not name:
            nameNotNull = False
        # All characters must be an uppercase, lowercase or integer
        if not re.fullmatch(r"[A-Za-z0-9']{2,20}", name):
            nameValid = False
        
        if nameNotNull == False: return "Name cannot be empty."
        elif nameValid == False: return "Name has to be only integers and letters between 2-20 letters."
        else: return True

    
    def vEmail(email):
        emailNotNull = True
        emailValid = True

        if not email:
            emailNotNull = False
        
        # Email
        if not re.fullmatch(r"[A-Za-z0-9._+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", email):
            emailValid = False
        
        if emailNotNull == False: return "Email cannot be empty."
        elif emailValid == False: return "Invalid email format."
        else: return True

    def vPassword(password):
        pwdNotNull = True
        pwdValid = True

        if not password:
            pwdNotNull = False
        # Password
        if not re.fullmatch(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}", password):
            pwdValid = False
        
        if pwdNotNull == False: return "Password cannot be empty."
        elif pwdValid == False: return "Password must include 8 characters, one lowercase, one uppercase, one number and one special character"
        else: return True

    def vTask(task):
        taskNotNull = True
        taskValid = True

        if not task:
            taskNotNull = False

        if not re.fullmatch(r"[\x20-\x7E]{1,50}", task):
            taskValid = False
        
        if taskNotNull == False: return "Task name cannot be empty!"
        elif taskValid == False: return "Task name has to be only letters and integers between 1-50 letters."
        else: return True

    def vDesc(desc):
        if not desc:
            return True
        
        if not re.fullmatch(r"[\x20-\x7E]{1,300}", desc):
            return "Description must only include letters, integers and be within 300 characters."
        
        return True

# TESTING
'''
print(validate.vName("yum"))
print(validate.vEmail("wenhao.xu@education.nsw.gov.au"))
print(validate.vPassword("Test1234&%"))
'''
