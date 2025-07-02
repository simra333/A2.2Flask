from datetime import datetime
import sqlite3

class DevelopersHandler:
    def __init__(self, conn):
        self.conn=conn

    def add_developers(self, name, email):
        query = '''INSERT INTO developers (name, email)
                   VALUES (?, ?)'''
        try:
            self.conn.execute(query, (name, email))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding developer: {e}")
            return False

    def get_developers(self):
        query = "SELECT * FROM developers"
        try:
            cursor = self.conn.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving developers: {e}")
            return False
    
    def update_developers(self, dev_id, name, email):
        query = '''UPDATE developers
                   SET name = ?, email = ?
                   WHERE id = ?'''
        try:
            self.conn.execute(query, (name, email, dev_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating developer: {e}")
            return False

    def delete_developers(self, dev_id):
        query = "DELETE FROM developers WHERE id = ?"
        try:
            self.conn.execute(query, (dev_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting developer: {e}")
            return False