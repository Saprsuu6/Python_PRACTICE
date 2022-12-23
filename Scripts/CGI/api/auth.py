#!C:/Python/python.exe

import logging
import dao  # User, UserDAO
import db   # config for db connection
import mysql.connector
import base64
import os
import sys
import db
from datetime import datetime

# Authorization Server

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


def send401(message: str = None) -> None:
    print("Status: 401 Unauthorized")
    print('WWW-Authenticate: Basic realm "Authorization required" ')
    print()
    if message:
        print(message)
    return


# дістаємо заголовок Authorization
if 'HTTP_AUTHORIZATION' in os.environ.keys():
    auth_header = os.environ['HTTP_AUTHORIZATION']
else:
    # відправляємо 401
    send401()
    exit()

# Перевіряємо схему авторизації - має бути Basic
if auth_header.startswith('Basic'):
    credentials = auth_header[6:]
else:
    send401("Authorization scheme Basic required")
    exit()

# credentials (параметр заголовку) - це Base64 кодований рядок "логін:пароль"
# у скрипті info підготуємо зразок для "admin:123"  --> YWRtaW46MTIz
# декодуємо credentials

try:
    data = base64.b64decode(credentials, validate=True).decode('utf-8')
except:
    send401("Credentials invalid: Base64 string required")
    exit()

# Перевіряємо формат (у data має бути :)
if not ':' in data:
    send401("Credentials invalid: Login:Password format expected")
    exit()


user_login, user_password = data.split(':', maxsplit=1)


# підключаємось до БД
try:
    db = mysql.connector.connect(**db.conf)
except mysql.connector.Error as err:
    send401(err)
    exit()


# підключаємо userdao
user_dao = dao.UserDAO(db)
access_token_dao = dao.AccessTokenDAO(db)


# получаем пользователя по логину и паролю
user = user_dao.auth_user(user_login, user_password)
if user is None:
    send401("Credentials rejected")
    exit()

# генерируем токен для пользователя

access_token = access_token_dao.get_by_user(user)
# use timedelta to set the different between data
#date_time_obj = datetime.strptime(access_token.expires, '%Y-%m-%d %H:%M:%S')
#logging.warning(access_token.expires)
   #access_token.expires, "%Y-%m-%d %H:%M:%S").date())

if access_token == None:
    access_token = access_token_dao.create(user)

if not access_token:
    send401("Token creation error")
    exit()

# Успішне завершення
print("Status: 200 OK")
print("Content-Type: application/json; charset=UTF-8")
print("Cache-Control: no-store")
print("Pragma: no-cache")
print()
print(f'''{{
    "access_token": "{access_token.token}",
    "token_type": "Bearer",
    "expires_in": "{access_token.expires}"
}}''', end='')

# An example of such a (https://datatracker.ietf.org/doc/html/rfc6750 page 9)
#    response is:

#      HTTP/1.1 200 OK
#      Content-Type: application/json;charset=UTF-8
#      Cache-Control: no-store
#      Pragma: no-cache
#      {
#        "access_token":"mF_9.B5f-4.1JqM",
#        "token_type":"Bearer",
#        "expires_in":3600,
#        "refresh_token":"tGzv3JOkF0XG5Qx2TlKWIA"
#      }
