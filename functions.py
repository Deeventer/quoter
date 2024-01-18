# БИБЛИОТЕКА ИМПОРТОВ
from aiogram.types import User
from config import db



# ПРОВЕРКИ ПОЛЬЗОВАТЕЛЯ

class UserService:
    '''Класс взаимодействий с пользователем'''

    async def __init__(self, user: User, *args, **kwargs):
        self.user = user


    async def check_registration(self) -> bool:
        '''Проверяет зарегистрирован ли пользователь'''

        return db.cursor().execute(f'SELECT id FROM users WHERE id = {self.user.id}').fetchone()
    

    async def register_user(self) -> None:
        '''Регистрирует нового пользователя'''
        db.cursor().execute('INSERT INTO users (id, username, full_name) VALUES (?,?,?)',
                            (self.user.id, f'@{self.user.username}', self.user.full_name))
        db.commit()