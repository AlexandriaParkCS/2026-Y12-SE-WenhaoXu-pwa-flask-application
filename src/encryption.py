import bcrypt

# Just Testing
# Bare bones implementation
'''
password1 = b"admin"

salt = bcrypt.gensalt()

hash = bcrypt.hashpw(password1, salt)

# 'utf-8' is encode for str (or something like that)
x = input("ENTER PASSWORD: ").encode('utf-8')

if bcrypt.checkpw(x, hash):
    print("True")
else:
    print("False")
'''
class encrypt:
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(password, hashed):
        if bcrypt.checkpw(password.encode("utf-8"), hashed):
            return True
        else:
            return False

# if bcrypt.checkpw(input("ENTER PASSWORD: ").encode("utf-8"), hash_password("SecretPassword")): print("Y")
# else: print("N")