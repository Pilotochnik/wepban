import sqlite3

try:
    conn = sqlite3.connect('backend/project_manager.db')
    cursor = conn.cursor()
    
    # Проверим таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print('Tables:', tables)
    
    # Проверим пользователей
    cursor.execute("SELECT * FROM users WHERE telegram_id = 434532312")
    user = cursor.fetchone()
    print('Creator user:', user)
    
    # Все пользователи
    cursor.execute("SELECT id, telegram_id, username, first_name, role, is_active FROM users")
    users = cursor.fetchall()
    print('All users:', users)
    
    conn.close()
except Exception as e:
    print('Error:', e)
