import bcrypt

# Just Testing
'''
# Bare Bones Implementation
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

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

if bcrypt.checkpw(input("ENTER PASSWORD: ").encode("utf-8"), hash_password("SecretPassword")): print("Y")
else: print("N")