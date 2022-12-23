#!C:/Python/python.exe

import logging
import dao
import errors
import base64
import db_connect
import check_auth
import genral_header
import asyncio

# Authorization Server

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


def connect_to_db():
    '''Connect to DataBase'''
    return db_connect.connect()


def check_auth_header():
    '''Check authedification header'''
    return check_auth.check_auth()


def check_auth_scheme(auth_header):
    '''Check authedification scheme'''
    if auth_header.startswith('Basic'):
        return auth_header[6:]
    else:
        errors.send401("Authorization scheme Basic required")
        raise Exception("Authorization scheme Basic required")


def parse_base64(credentials):
    '''Convert string from base64 to utf8'''
    try:
        return base64.b64decode(credentials, validate=True).decode('utf-8')
    except:
        errors.send401("Credentials invalid: Base64 string required")
        raise Exception("Credentials invalid: Base64 string required")


def check_data_format(data):
    '''Chech credentials format'''
    if not ':' in data:
        errors.send401("Credentials invalid: Login:Password format expected")
        raise Exception("Credentials invalid: Base64 string required")

    user_login, user_password = data.split(':', maxsplit=1)
    return [user_login, user_password]


def dao_connect(connection):
    '''Connecting to DAO services'''
    user_dao = dao.UserDAO(connection)
    access_token_dao = dao.AccessTokenDAO(connection)
    return [user_dao, access_token_dao]


def get_user_by_credentials(user_dao, user_login, user_password):
    '''Get user from DataBase'''
    user = user_dao.auth_user(user_login, user_password)
    if user is None:
        errors.send401("Credentials rejected")
        raise Exception("Credentials rejected")

    return user


def generate_token(access_token_dao, user):
    '''Generate or return access token from DataBase'''
    access_token = access_token_dao.get_by_user(user)
    # use timedelta to set the different between data
    #date_time_obj = datetime.strptime(access_token.expires, '%Y-%m-%d %H:%M:%S')
    # logging.warning(access_token.expires)
    # access_token.expires, "%Y-%m-%d %H:%M:%S").date())

    if access_token == None:
        access_token = access_token_dao.create(user)

    if not access_token:
        errors.send401("Token creation error")
        raise Exception("Token creation error")


def send_finally_headers(access_token):
    genral_header.send_header()
    print("Cache-Control: no-store")
    print("Pragma: no-cache")
    print()
    print(f'''{{
        "access_token": "{access_token.token}",
        "token_type": "Bearer",
        "expires_in": "{access_token.expires}"
    }}''', end='')


async def main():
    # exit() in except
    pass


asyncio.run(main())

# дістаємо заголовок Authorization
auth_header = check_auth.check_auth()

# Перевіряємо схему авторизації - має бути Basic
if auth_header.startswith('Basic'):
    credentials = auth_header[6:]
else:
    errors.send401("Authorization scheme Basic required")
    exit()

# credentials (параметр заголовку) - це Base64 кодований рядок "логін:пароль"
# у скрипті info підготуємо зразок для "admin:123"  --> YWRtaW46MTIz
# декодуємо credentials

try:
    data = base64.b64decode(credentials, validate=True).decode('utf-8')
except:
    errors.send401("Credentials invalid: Base64 string required")
    exit()

# Перевіряємо формат (у data має бути :)
if not ':' in data:
    errors.send401("Credentials invalid: Login:Password format expected")
    exit()


user_login, user_password = data.split(':', maxsplit=1)


# підключаємось до БД
connection = db_connect.connect()


# підключаємо userdao
user_dao = dao.UserDAO(connection)
access_token_dao = dao.AccessTokenDAO(connection)


# получаем пользователя по логину и паролю
user = user_dao.auth_user(user_login, user_password)
if user is None:
    errors.send401("Credentials rejected")
    exit()

# генерируем токен для пользователя

access_token = access_token_dao.get_by_user(user)
# use timedelta to set the different between data
#date_time_obj = datetime.strptime(access_token.expires, '%Y-%m-%d %H:%M:%S')
# logging.warning(access_token.expires)
# access_token.expires, "%Y-%m-%d %H:%M:%S").date())

if access_token == None:
    access_token = access_token_dao.create(user)

if not access_token:
    errors.send401("Token creation error")
    exit()

# Успішне завершення
genral_header.send_header()
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
