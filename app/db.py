# Spin The Wheel -- Matthew Chen, Sakina Raza, Caroline Tham, Efaz Khan
# SoftDev  P00 -- Scenario Sigma
# Target ship date: 2026-11-18

import sqlite3

DB_FILE = "storytelling.db"

def init_db():
    # Creates the users, stories, and contributions tables if they don't exist yet
    pass


def add_user(username, password):
    # Adds a user. Returns false if the username is already taken, returns true otherwise
    print("Fake add_user:", username)
    return True


def check_login(username, password):
    # Returns true if the username/password match a user, returns false otherwise
    print("Fake check_login:", username)
    return False


def create_story(username, title, body):
    # Adds a story and its first contribution (the opening text). Returns the new story_id
    print("Fake create_story:", username, title, body)
    return 1


def get_story(story_id):
    # Returns the story (story_id and title), or None if it doesn't exist
    print("Fake get_story:", story_id)
    return None


def get_latest_contribution(story_id):
    # Returns the text of the newest contribution to a story
    print("Fake get_latest_contribution:", story_id)
    return ""


def get_browsable_stories(username):
    # Returns a list of (story_id, title) for stories this user hasn't contributed to
    print("Fake get_browsable_stories:", username)
    return []


def get_user_stories(username):
    # Returns every story this user contributed to, with full text, as a list of
    # dictionaries like {"story_id": 1, "title": "My Story", "parts": ["piece 1", "piece 2"]}
    print("Fake get_user_stories:", username)
    return []


def has_contributed(username, story_id):
    # Returns True if this user already added to this story, else False
    print("Fake has_contributed:", username, story_id)
    return False


def add_contribution(username, story_id, body):
    # Adds a contribution. Returns True, or False if this user already added to this story
    print("Fake add_contribution:", username, story_id)
    return True
