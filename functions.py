# БИБЛИОТЕКА ИМПОРТОВ
import sqlite3



# ПРОВЕРКИ ПОЛЬЗОВАТЕЛЯ

class CheckUser:
    '''Класс проверки пользователя'''

    async def registration(userid: int) -> bool:
        '''Проверяет зарегистрирован ли пользователь'''

        db = sqlite3.connect('database.db')
        all_users = db.cursor().execute('SELECT id FROM users').fetchall()
        registred_users = [user[0] for user in all_users]
        db.close()

        return userid in registred_users