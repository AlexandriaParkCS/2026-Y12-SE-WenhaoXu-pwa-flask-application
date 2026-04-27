import re
# NAME: pattern="[a-zA-Z0-9]{2,20}$"
# EMAIL: pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2, 4}$"

class validate:
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

# TESTING
'''
print(validate.vName("yum"))
print(validate.vEmail("wenhao.xu@education.nsw.gov.au"))
print(validate.vPassword("Test1234&%"))
'''
