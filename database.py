import sqlite3 as sq


def connect_to_database(name: str):
    connection = sq.connect(name)
    return connection


def get_all_users(connection) -> tuple:
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM bot_users')
    return cursor.fetchall()


def add_user(connection, user: tuple) -> bool:
    try:
        print(user)
        add_user_query = f'''
            INSERT INTO bot_users (telegram_id,chat_id, first_name, last_name, nickname, joining_date) VALUES (?, ?, ?, ?, ?, ?)
        '''
        cursor = connection.cursor()
        cursor.execute(add_user_query, user)
        connection.commit()
        cursor.close()
        return True
    except:
        return False


if __name__ == "__main__":
    connection = connect_to_database('bot_users.db')
    create_table_query = '''CREATE TABLE IF NOT EXISTS bot_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT NOT NULL UNIQUE,
    chat_id TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    nickname TEXT,
    joining_date datetime);'''
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    print('+')
    cursor.close()
    # add_user(connection, (3453, 'Tom', 'Hels', 'Ndlkj', datetime.datetime.now()))
