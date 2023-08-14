import sqlite3
class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()