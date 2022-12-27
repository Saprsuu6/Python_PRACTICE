#!C:/Python/python.exe

import dao
import db_connect
import errors
import check_auth
import genral_header
import asyncio
# API demo - доступ до ресурсу обмеженого доступу (Resource Server)


async def connect_to_db():
    '''Connect to DataBase'''
    return db_connect.connect()


async def check_auth_header():
    '''Check authedification header'''
    return check_auth.check_auth()


async def check_auth_scheme(auth_header):
    '''Check authorisation header'''
    if not auth_header:
        errors.send401("Authorization header required")
        raise Exception("Authorization header required")

    if not auth_header.startswith('Bearer'):
        errors.send401("Bearer Authorization header required")
        raise Exception("Bearer Authorization header required")


async def extract_token(auth_header):
    '''Extract the token from BEARER'''
    return auth_header[7:]


async def get_token(connection, access_token):
    '''Get token from from front-end'''
    token = dao.AccessTokenDAO(connection).get(access_token)
    if not token:
        errors.send401("Token rejected")
        raise Exception("Token rejected")

    return token


async def send_finally_headers(token):
    genral_header.send_header()
    print()
    print(f'"{token}"')


async def main():
    connect = asyncio.create_task(connect_to_db())
    check_auth = asyncio.create_task(check_auth_header())

    try:
        connection = await connect
        auth_header = await check_auth

        check_scheme = asyncio.create_task(check_auth_scheme(auth_header))
        await check_scheme

        exact = asyncio.create_task(extract_token(auth_header))
        data = await exact

        token = asyncio.create_task(get_token(connection, data))
        access_token = await token

        asyncio.create_task(
            send_finally_headers(access_token))
        # logging.warning(send_headers) !!! learn how to log
    except:
        exit()
    finally:
        pass

asyncio.run(main())

# '''
# Схеми авторизації.
# https://datatracker.ietf.org/doc/html/rfc6750

# Запит на обмежений ресурс --> Перевірка авторизації
# якщо "+", то видаємо ресурс, інакше відповідь з кодом 401

# Перевірка авторизації: аналіз заголовку Authorization
# та відповідної схеми автентифікації
#  - Basic - безпосередня передача логіну та паролю (кодованих у Base64)
#  - Bearer - за допомогою спеціальних токенів

# Токен отримується від серверу авторизації /auth
# '''
