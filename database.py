import sqlite3
from contextlib import closing

DB_PATH = 'analysis.db'

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                '''CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    article TEXT NOT NULL,
                    stance TEXT,
                    missing_perspectives TEXT,
                    balance_score INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )'''
            )

def log_analysis(article: str, result: dict):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                'INSERT INTO analyses (article, stance, missing_perspectives, balance_score) VALUES (?,?,?,?)',
                (
                    article,
                    result.get('stance'),
                    '\n'.join(result.get('missing_perspectives', [])),
                    result.get('balance_score'),
                ),
            )
