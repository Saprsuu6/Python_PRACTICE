# работа с таблицей Users
from datetime import datetime, timedelta
import hashlib
import mysql.connector
import random
import uuid
import re


class User:
    def __init__(self, row=None) -> None:
        if row == None:
            self.id = None
            self.login = None
            self.passw = None
            self.name = None
            self.salt = None
            self.avatar = None
            self.email = None
            self.email_code = None
            self.email_code_attempts = None
            self.del_dt = None
        elif isinstance(row, tuple):
            self.id = row[0]
            self.login = row[1]
            self.passw = row[2]
            self.name = row[3]
            self.salt = row[4]
            self.avatar = row[5]
            self.email = row[6]
            self.email_code = row[7]
            self.email_code_attempts = row[8]
            self.del_dt = row[9]
        elif isinstance(row, dict):
            self.id = row["id"]
            self.login = row["login"]
            self.passw = row["pass"]
            self.name = row["name"]
            self.salt = row["salt"]
            self.avatar = row["avatar"]
            self.email = row["email"]
            self.email_code = row["email_code"]
            self.email_code_attempts = row["email_code_attempts"]
            self.del_dt = row["del_dt"]
        else:
            raise ValueError("row format unsupported")

    def __str__(self) -> str:
        return str(self.__dict__)

    __repr__ = __str__


class UserDAO:
    def __init__(self, db: mysql.connector.MySQLConnection) -> None:
        self.db = db

    def add_user(self, user: User) -> bool:
        ''' Appends user to DB table '''
        # предполагаем, что в поле passw приходит открытый пароль, генерируем хеш здесь
        user.salt = random.randbytes(20).hex()
        user.passw = hashlib.sha1(
            (user.salt + user.passw).encode()).hexdigest()
        # генерируем код подтверждения почты
        user.email_code = random.randbytes(3).hex()

        user.id = str(uuid.uuid4())
        user.email_code_attempts = 0

        names = user.__dict__.keys()
        fields = ','.join(f"`{name}`" for name in names).replace(
            'passw', 'pass')
        placeholders = ','.join(f"%({name})s" for name in names)
        sql = f"INSERT INTO users({fields}) VALUES({placeholders})"

        try:
            cursor = self.db.cursor()
            # подстановка значений именованных параметров
            cursor.execute(sql, user.__dict__)
            self.db.commit()
        except mysql.connector.Error as err:
            print(err)
            return False
        else:
            return True
        finally:
            cursor.close()

    def get_users(self, ignore_deleted=True) -> tuple | None:
        sql = "SELECT * FROM users"
        if ignore_deleted:
            sql += " WHERE del_dt IS NULL"
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(sql)
        except mysql.connector.Error as err:
            print('get_users:', err)
            return None
        else:
            return tuple(User(row) for row in cursor)
        finally:
            cursor.close()
        return

    def get_user(self, id=None, login=None, ignore_deleted=True) -> User | None:
        sql = "SELECT u.* FROM Users u WHERE "
        params = []
        if id:
            sql += "u.id = %s "
            params.append(id)
        if login:
            sql += ("AND " if id else "") + "u.login = %s"
            params.append(login)
        if ignore_deleted:
            sql += "AND del_dt IS NULL"
        if len(params) == 0:
            return None

        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(sql, params)
            row = cursor.fetchone()
            if row:
                return User(row)
        except mysql.connector.Error as err:
            print('get_user:', err)
        finally:
            try:
                cursor.close()
            except:
                pass
        return None

    def update(self, user: User) -> bool:
        ''' Обновление данных о пользователе. user.id используется как ключ, остальные поля
            обновляют значения в БД. !!! Если меняется пароль получить хеш нужно до вызова метода'''

        sql = 'UPDATE users u SET ' + \
            ','.join(f"u.`{x.replace('passw','pass')}`=%({x})s" for x in user.__dict__.keys() if x != 'id') + \
            ' WHERE u.`id`=%(id)s'

        try:
            cursor = self.db.cursor()
            # подстановка значений именованных параметров
            cursor.execute(sql, user.__dict__)
            self.db.commit()
        except mysql.connector.Error as err:
            print(err)
            return False
        else:
            return True
        finally:
            try:
                cursor.close()
            except:
                pass

    def delete(self, user: User) -> bool:
        '''Удаление пользователя - это не удаление записи из БД, это установка поля del_dt'''
        if not user:
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "UPDATE users u SET u.del_dt = CURRENT_TIMESTAMP WHERE u.id = %s", (user.id,))
            self.db.commit()
        except mysql.connector.Error as err:
            print(err)
            return False
        else:
            return True
        finally:
            try:
                cursor.close()
            except:
                pass

    def is_login_free(self, login: str) -> bool:
        return True if self.get_user(login=login, ignore_deleted=False) != None else False

    def auth_user(self, login: str, password: str) -> User | None:
        '''User authentication'''
        user = self.get_user(login=login, ignore_deleted=False)

        # проверка на наличие пользователя по логину в базе
        if user == None:
            raise Exception('User were not registered')
        else:
            hash_pass = hashlib.sha1(
                (user.salt + password).encode()).hexdigest()

            if hash_pass == user.passw:
                return user
            else:
                raise Exception('Passwords missmatch')


def login_validation(login: str, pattern='^[a-zA-Z](.[a-zA-Z0-9_-]*)$') -> None:
    result = re.match(login, pattern)

    if result == None:
        raise Exception("Login are not equals with pattern")


def password_validation(password: str, pattern='/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^\w\s]).{6,}/') -> None:
    result = re.match(password, pattern)

    if result == None:
        raise Exception("Password are not equals with pattern")


class AccessToken:
    def __init__(self, row=None) -> None:
        if row == None:
            self.token = None
            self.user_id = None
            self.expires = None
        elif isinstance(row, tuple) or isinstance(row, list):
            self.token = row[0]
            self.user_id = row[1]
            self.expires = row[2]
        elif isinstance(row, dict):
            self.token = row["token"]
            self.user_id = row["user_id"]
            self.expires = row["expires"]


class AccessTokenDAO:
    def __init__(self, db: mysql.connector.MySQLConnection) -> None:
        self.db = db

    def create(self, user: str | User) -> AccessToken | None:
        ''' user - user_id only OR User instance object '''
        user_id = None
        if isinstance(user, str):   # str - user_id only
            user_id = user
        elif isinstance(user, User):
            user_id = user.id

        if not user_id:
            return None
        access_token = AccessToken()
        # 20 bytes = 40 hex-digits = 160 bit
        access_token.token = random.randbytes(20).hex()
        access_token.user_id = user_id
        access_token.expires = (datetime.now() + timedelta(days=1)  # 1 day from now
                                ).strftime("%Y-%m-%d %H:%M:%S")  # SQL-format
        sql = "INSERT INTO access_tokens VALUES( %(token)s, %(user_id)s, %(expires)s )"
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, access_token.__dict__)
            self.db.commit()
        except:
            return None
        else:
            return access_token
        finally:
            try:
                cursor.close()
            except:
                pass

    def get(self, access_token: str) -> AccessToken | None:
        sql = "SELECT * FROM access_tokens WHERE token = %s"
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(sql, (access_token, ))
            row = cursor.fetchone()
            if row:
                return AccessToken(row)
        except:
            pass
        finally:
            try:
                cursor.close()
            except:
                pass
        return None

    def get_by_user(self, user: User) -> AccessToken | None:
        sql = "SELECT * FROM access_tokens WHERE user_id = %s"
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(sql, (user.id, ))
            row = cursor.fetchone()
            if row:
                return AccessToken(row)
        except:
            pass
        finally:
            try:
                cursor.close()
            except:
                pass
        return None
