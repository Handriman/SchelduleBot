import sqlite3 as sq


def connect_to_database(name: str):
    connection = sq.connect(name)
    return connection


def get_all_users(connection) -> tuple:
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM bot_users')
    return cursor.fetchall()


def change_user_group_by_id(id: int, group: int):
    connection = connect_to_database('bot_users.db')
    cursor = connection.cursor()
    cursor.execute(f"""
    UPDATE bot_users
    SET group_number = {str(group)}
    WHERE telegram_id = {str(id)}
    """)
    connection.commit()
    cursor.close()
    return True


def get_user_by_id(id: int):
    connection = connect_to_database('bot_users.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT group_number FROM bot_users WHERE telegram_id = {id}")
    return cursor.fetchall()
def add_user(connection, user: tuple) -> bool:
    try:
        print(user)
        add_user_query = f'''
            INSERT INTO bot_users (telegram_id,chat_id, first_name, last_name, nickname, group_number, joining_date) VALUES (?, ?, ?, ?, ?,?, ?)
        '''
        cursor = connection.cursor()
        cursor.execute(add_user_query, user)
        connection.commit()
        cursor.close()
        return True
    except:
        return False


if __name__ == "__main__":
    # connection = connect_to_database('bot_users.db')
    # create_table_query = '''CREATE TABLE IF NOT EXISTS bot_users (
    # id INTEGER PRIMARY KEY AUTOINCREMENT,
    # telegram_id TEXT NOT NULL UNIQUE,
    # chat_id TEXT NOT NULL,
    # first_name TEXT,
    # last_name TEXT,
    # nickname TEXT,
    # group_number TEXT,
    # joining_date datetime);'''
    # cursor = connection.cursor()
    # cursor.execute(create_table_query)
    # connection.commit()
    # print('+')
    # cursor.close()

    change_user_group_by_id(384573724, 120811)
    # add_user(connection, (3453, 'Tom', 'Hels', 'Ndlkj', datetime.datetime.now()))
