import sqlite3

class MedicalDB:
    def __init__(self, db_name="data/medical.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS symptoms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            recommendation TEXT
        )
        """)
        self.conn.commit()

    def seed_data(self):
        cursor = self.conn.cursor()
        data = [
            ("fiebre", "hidratarse y descansar"),
            ("dolor", "analgésico OTC"),
            ("náuseas", "dieta blanda"),
            ("mareo", "reposo y líquidos"),
        ]
        cursor.executemany(
            "INSERT INTO symptoms (name, recommendation) VALUES (?, ?)",
            data
        )
        self.conn.commit()

    def get_recommendation(self, symptom):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT recommendation FROM symptoms WHERE name=?",
            (symptom,)
        )
        result = cursor.fetchone()
        return result[0] if result else "Consultar médico"