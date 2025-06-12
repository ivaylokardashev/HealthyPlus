import sqlite3

class QRDatabase:
    def __init__(self, db_path="qr_data.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS qr_items (
                qrcode TEXT PRIMARY KEY,
                name TEXT,
                ingredients TEXT
            )
        ''')
        self.conn.commit()

    def get_item(self, qrcode):
        c = self.conn.cursor()
        c.execute("SELECT name, ingredients FROM qr_items WHERE qrcode = ?", (qrcode,))
        return c.fetchone()

    def add_item(self, qrcode, name, ingredients):
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO qr_items (qrcode, name, ingredients) VALUES (?, ?, ?)",
                  (qrcode, name, ingredients))
        self.conn.commit()
