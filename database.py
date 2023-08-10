import sqlite3 as sq


def connect_to_database(name: str):
    connection = sq.connect(name)
    return connection

if __name__ == "__main__":
    connection = connect_to_database('bot_users.db')
    create_table_query = '''
    CREATE TABLE IF NOT EXIST bot_users (
    id INTEGER PRIMARY KEY,
    telegram_id TEXT NOT NULL UNIQUE, 
    '''
