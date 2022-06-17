import sqlite3

DB_PATH = '../models/features.db'

def get_db_connexion(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def save_feature(image, category, description, name, price, feature):
    conn = get_db_connexion()
    conn.execute('INSERT INTO features (image, category, description, name, price, features) VALUES (?, ?, ?, ?, ?, ?)', (image, category, description, name, price, feature))
    conn.commit()
    conn.close()

def get_features():
    conn = get_db_connexion()
    features = conn.execute('SELECT * FROM features').fetchall()
    conn.close()
    return features

def get_features_category(path, category):
    conn = get_db_connexion(path)
    features = conn.execute('SELECT * FROM features WHERE category=?', (category,)).fetchall()
    conn.close()
    return features

