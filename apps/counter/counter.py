import sqlite3


# Connect with the database
conn = sqlite3.connect('bot_data.db', check_same_thread=False)
cursor = conn.cursor()

# Creation of tables if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_counts (
        user_id INTEGER PRIMARY KEY,
        count INTEGER NOT NULL
    )
''')
conn.commit()


def update_count(user_id):
    """ 
    
        We update the user by receiving the user_id as a parameter
        
    """
    cursor.execute('SELECT count FROM user_counts WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        count = result[0] + 1
        cursor.execute('UPDATE user_counts SET count = ? WHERE user_id = ?', (count, user_id))
    else:
        count = 1
        cursor.execute('INSERT INTO user_counts (user_id, count) VALUES (?, ?)', (user_id, count))
    
    conn.commit()

# Función para obtener el contador actual
def get_count(user_id):
    """
    
    We obtain the number of touches made in the database, receiving the user_id by parameters
    
    """
    cursor.execute('SELECT count FROM user_counts WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        return 0
    