import re
# NAME: pattern="[a-zA-Z0-9]{2,20}$"
# EMAIL: pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2, 4}$"

class validate:
    def vName(self, name):
        if not name:
            raise ValueError("Name required.")
        # All characters must be an uppercase, lowercase or integer
        if not re.fullmatch(r"[A-Za-z0-9']{2,20}", name):
            raise ValueError("Name must be 2-20 letters or numbers.")

    
    def vEmail(self, email):
        if not email:
            raise ValueError("Email required.")
        # Email
        if not re.fullmatch(r"[A-Za-z0-9._+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", email):
            raise ValueError("Invalid email format.")

    def vPassword(self, password):
        if not password:
            raise ValueError("Password required.")
        # Password
        if not re.fullmatch(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}", password):
            raise ValueError("Password must include 8 characters, one lowercase, one uppercase, one number and one special character")