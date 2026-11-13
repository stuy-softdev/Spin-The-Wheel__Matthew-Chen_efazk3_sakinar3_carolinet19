# Spin The Wheel -- Matthew Chen, Sakina Raza, Caroline Tham, Efaz Khan
# SoftDev  P00 -- Scenario Sigma
# Target ship date: 2026-11-18

import sqlite3

DB_FILE = "storytelling.db"

def init_db():
    # Creates the users, stories, and contributions tables if they don't exist yet
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS stories (story_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(user_id))")
    c.execute("CREATE TABLE IF NOT EXISTS contributions (contribution_id INTEGER PRIMARY KEY AUTOINCREMENT, story_id INTEGER, user_id INTEGER, body TEXT, FOREIGN KEY (story_id) REFERENCES stories(story_id), FOREIGN KEY (user_id) REFERENCES users(user_id))")
    db.commit()
    db.close()

def get_user_id(username):
    """Helper function to fetch a user_id given a username."""
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    c = db.cursor()
    c.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    db.close()
    return row["user_id"] if row else None

def add_user(username, password):
    # Adds a user. Returns false if the username is already taken, returns true otherwise
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        db.close()

def check_login(username, password):
    # Returns true if the username/password match a user, returns false otherwise
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    c = db.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    db.close()
    
    if row and row["password"] == password:
        return True
    return False

def create_story(username, title, body):
    # Adds a story and its first contribution (the opening text). Returns the new story_id
    user_id = get_user_id(username)
    if not user_id:
        return None

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    # Save the story tied to the creator's user_id[cite: 1]
    c.execute("INSERT INTO stories (title, user_id) VALUES (?, ?)", (title, user_id))
    story_id = c.lastrowid
    
    # Save the opening text as the first contribution (preventing the creator from contributing twice)[cite: 1]
    c.execute("INSERT INTO contributions (story_id, user_id, body) VALUES (?, ?, ?)", (story_id, user_id, body))
    db.commit()
    db.close()
    return story_id

def get_story(story_id):
    # Returns the story (story_id and title), or None if it doesn't exist
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    c = db.cursor()
    c.execute("SELECT story_id, title FROM stories WHERE story_id = ?", (story_id,))
    row = c.fetchone()
    db.close()
    
    if row:
        return {"story_id": row["story_id"], "title": row["title"]}
    return None

def get_latest_contribution(story_id):
    # Returns the text of the newest contribution to a story
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    c = db.cursor()
    c.execute("SELECT body FROM contributions WHERE story_id = ? ORDER BY contribution_id DESC LIMIT 1", (story_id,))
    row = c.fetchone()
    db.close()
    
    if row:
        return row["body"]
    return ""

def get_browsable_stories(username):
    # Returns a list of (story_id, title) for stories this user hasn't contributed to
    user_id = get_user_id(username)
    if not user_id:
        return []

    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    c = db.cursor()
    c.execute("""
        SELECT story_id, title FROM stories 
        WHERE story_id NOT IN (
            SELECT story_id FROM contributions WHERE user_id = ?
        )
    """, (user_id,))
    rows = c.fetchall()
    db.close()
    
    return [(row["story_id"], row["title"]) for row in rows]

def get_user_stories(username):
    # Returns every story this user contributed to, with full text, as a list of
    # dictionaries like {"story_id": 1, "title": "My Story", "parts": ["piece 1", "piece 2"]}
    user_id = get_user_id(username)
    if not user_id:
        return []

    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    c = db.cursor()
    c.execute("""
        SELECT DISTINCT s.story_id, s.title 
        FROM stories s
        JOIN contributions co ON s.story_id = co.story_id
        WHERE s.story_id IN (SELECT story_id FROM contributions WHERE user_id = ?)
    """, (user_id,))
    story_rows = c.fetchall()
    
    result = []
    for s_row in story_rows:
        s_id = s_row["story_id"]
        c.execute("SELECT body FROM contributions WHERE story_id = ?", (s_id,))
        parts = [part["body"] for part in c.fetchall()]
        result.append({
            "story_id": s_id,
            "title": s_row["title"],
            "parts": parts
        })
        
    db.close()
    return result

def has_contributed(username, story_id):
    # Returns True if this user already added to this story, else False
    user_id = get_user_id(username)
    if not user_id:
        return False

    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    c = db.cursor()
    c.execute("SELECT 1 FROM contributions WHERE user_id = ? AND story_id = ?", (user_id, story_id))
    row = c.fetchone()
    db.close()
    
    return row is not None

def add_contribution(username, story_id, body):
    # Adds a contribution. Returns True, or False if this user already added to this story
    if has_contributed(username, story_id):
        return False
        
    user_id = get_user_id(username)
    if not user_id:
        return False

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO contributions (story_id, user_id, body) VALUES (?, ?, ?)", (story_id, user_id, body))
    db.commit()
    db.close()
    return True
