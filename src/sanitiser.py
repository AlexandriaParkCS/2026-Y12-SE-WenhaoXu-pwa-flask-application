name_characters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " "]
email_characters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "."]
integers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
import re
class sanitise:
    def __init__(self, name, email, phone):
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
    
    # These return the name, email, phone respectively
    def get_Name(self):
        return self.name

    def get_Email(self):
        return self.email
    
    def get_Phone(self):
        return self.phone