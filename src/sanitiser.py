name_characters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " "]
email_characters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "."]
integers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

class Contact_Information:
    def __init__(self, name, email, phone, tfn, cc):
        self.name = name
        self.email = email
        self.phone = phone 

    def Sanitise_Name(self, name):
        # It will be similar for every sanitisation
        bad_letters = []
        
        for letter in range(len(name)):
            # casefold converts any uppercase into lowercase
            # accepted characters are all in lowercase
            if name[letter].casefold() not in name_characters:
                bad_letters.append(name[letter])
        
        for item in bad_letters:
            name = name.replace(item, "")

        name = name.strip()
        self.name = name

    def Validate_Name(self):
        if len(self.name) < 100: return True
        else: return False

    def Sanitise_Email(self, email):
        bad_letters = []
        for letter in range(len(email)):
            # casefold converts any uppercase into lowercase
            # accepted characters are all in lowercase
            if email[letter].casefold() not in email_characters:
                bad_letters.append(email[letter])

        for item in bad_letters:
            email = email.replace(item, "")

        self.email = email

    # Validation for email
    def Validate_Email(self):
        check_1 = False
        check_2 = False
        check_3 = False
        # check for full stop and @
            # uses count and rfind. Count will count the amount of times a specified variable is used,and rfind finds the last instance of a repeated object.
        if "." and "@" in self.email and self.email.count("@") == 1: 
            if self.email.rfind(".") > self.email.find("@"): check_1 = True
        else: check_1 = False

        # ensure full stop and @ not at start or end
        # using index can return exceptions
        try:
            if self.email[0] != "." and self.email[0] != "@" and self.email[-1] != "." and self.email[-1] != "@":
                check_2 = True
        except: return False

        # ensure length of email is right

        if len(self.email) > 4 and len(self.email) < 255: check_3 = True

        if check_1 == True and check_2 == True and check_3 == True: return True
        else: return False
                    
    def Sanitise_Phone(self, phone):
        bad_letters = []
        for letter in range(len(phone)):
            # casefold converts any uppercase into lowercase
            # accepted characters are all in lowercase
            if phone[letter].casefold() not in integers and phone[letter] != "+":
                bad_letters.append(phone[letter])
        
        for item in bad_letters:
            phone = phone.replace(item, "")
        
        self.phone = phone
    
    def Validate_phone(self):
        # There are two sets of try exception, because it uses index, which can return an exception.
        try:
            if len(self.phone) == 10 and self.phone[0] == "0": return True
            else:
                try:
                    if self.phone[2] == "+" and len(self.phone) == 12: return True
                    else: return False
                except: return False
        except: return False

    # These return the name, email, phone, tfn and credit card numbers respectively.
    def get_Name(self):
        return self.name

    def get_Email(self):
        return self.email
    
    def get_Phone(self):
        return self.phone