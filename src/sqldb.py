import sqlite3

class SqlDb(object):

    def __init__(self, db_path="db/app.db"):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("""BEGIN""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL)
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                user_id INTEGER,
                task_completion INTEGER DEFAULT 0,
                weekday INTEGER,
                time_hour INTEGER,
                time_minute INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()

# User functions
    def create_user(self, username, email, password_hash):
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return {"id": user_id, "username": username, "email": email, "password_hash": password_hash}
        except sqlite3.IntegrityError:
            print("Error: Username or email already exists.")
        except sqlite3.Error as e:
            print(f"Database error during user creation: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()

    def get_user_by_id(self, uid):
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email, password_hash FROM users WHERE id = ?",
                (uid,)
            )
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "username": row[1], "email": row[2], "password_hash": row[3]}
        except sqlite3.Error as e:
            print(f"Database error during user retrieval: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()

    def get_user_by_username(self, username):
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email, password_hash FROM users WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "username": row[1], "email": row[2], "password_hash": row[3]}
        except sqlite3.Error as e:
            print(f"Database error during user retrieval: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()

    def get_user_by_email(self, email):
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email, password_hash FROM users WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "username": row[1], "email": row[2], "password_hash": row[3]}
        except sqlite3.Error as e:
            print(f"Database error during user retrieval: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()

    def update_user_email(self, new_email, username):
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET email = ? WHERE username = ?",
                (new_email, username)
            )
            conn.commit()
            if cursor.rowcount:
                return self.get_user_by_username(username)
            else:
                print("User not found.")
        except sqlite3.IntegrityError:
            print("Error: Email already in use.")
        except sqlite3.Error as e:
            print(f"Database error during update: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()

    def update_user_username(self, new_username, username):
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET username = ? WHERE username = ?",
                (new_username, username)
            )
            conn.commit()
            if cursor.rowcount:
                return self.get_user_by_username(username)
            else:
                print("User not found.")
        except sqlite3.IntegrityError:
            print("Error: Email already in use.")
        except sqlite3.Error as e:
            print(f"Database error during update: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()        

    def update_user_password(self, new_password, username):
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET password_hash = ? WHERE username = ?",
                (new_password, username)
            )
            conn.commit()
            if cursor.rowcount:
                return self.get_user_by_username(username)
            else:
                print("User not found.")
        except sqlite3.IntegrityError:
            print("Error: Email already in use.")
        except sqlite3.Error as e:
            print(f"Database error during update: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()

    def delete_user_by_user(self, username):
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM users WHERE username = ?",
                (username,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error during deletion: {e}")
            return False
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()

    def delete_user_by_email(self, email):
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM users WHERE email = ?",
                (email,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error during deletion: {e}")
            return False
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()

# Chore sheet
    def create_chore(self, name, description, weekday, time_hour, time_minute, user_id):
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chores (name, description, weekday, time_hour, time_minute, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                (name, description, weekday, time_hour, time_minute, user_id)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return {"id": user_id, "username": name, "description": description}
        except sqlite3.IntegrityError:
            print("Error: chore already exists.")
        except sqlite3.Error as e:
            print(f"Database error during chore creation: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()

    def get_all_chores(self, user_id):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, description, weekday, time_hour, time_minute, id FROM chores WHERE user_id= ? ORDER BY weekday, time_hour, time_minute",
                (user_id,)
            )
            row = cursor.fetchall()
            return row
        except sqlite3.Error as e:
            print(f"Database error during chore retrieval: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()

    def get_all_chores_by_day(self, user_id, weekday):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, description, weekday, time_hour, time_minute FROM chores WHERE user_id = ? AND weekday = ?",
                (user_id, weekday)
            )
            row = cursor.fetchall()
            return row
        except sqlite3.Error as e:
            print(f"Database error during chore retrieval: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn: 
                conn.close()

    def delete_chore(self, chore_id, user_id):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM chores WHERE id = ? AND user_id = ?",
                (chore_id, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error during chore deletion: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn: 
                conn.close()        

'''
# Example usage
if __name__ == "__main__":
    db = SqlDb("runtime/db/test.db")

    # Create
    user = db.create_user("emiltech", "emil@example.com", bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()))
    print("Created:", user)

    # Read
    user = db.get_user_by_username("emiltech")
    print("Retrieved:", user)

    # Update
    updated_user = db.update_user_email("emiltech", "emil_updated@example.com")
    print("Updated:", updated_user)

    # Delete
    success = db.delete_user_by_user("emiltech")
    print("Deleted:", success)

    chore = db.create_chore("Do Software work", "I have software due soon!")
    print("Created:", chore)
'''