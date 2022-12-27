#!C:/Python/python.exe

import logging
import dao
import errors
import base64
import db_connect
import check_auth
import genral_header
import asyncio
import datetime

# Authorization Server

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


async def connect_to_db():
    '''Connect to DataBase'''
    return db_connect.connect()


async def check_auth_header():
    '''Check authedification header'''
    return check_auth.check_auth()


async def check_auth_scheme(auth_header):
    '''Check authedification scheme BASIC'''
    if auth_header.startswith('Basic'):
        return auth_header[6:]
    else:
        errors.send401("Authorization scheme Basic required")
        raise Exception("Authorization scheme Basic required")


async def parse_base64(credentials):
    '''Convert string from base64 to utf8'''
    try:
        return base64.b64decode(credentials, validate=True).decode('utf-8')
    except:
        errors.send401("Credentials invalid: Base64 string required")
        raise Exception("Credentials invalid: Base64 string required")


async def check_data_format(data):
    '''Chech credentials format'''
    if not ':' in data:
        errors.send401("Credentials invalid: Login:Password format expected")
        raise Exception("Credentials invalid: Base64 string required")

    user_login, user_password = data.split(':', maxsplit=1)
    return [user_login, user_password]


async def dao_connect(connection):
    '''Connecting to DAO services'''
    user_dao = dao.UserDAO(connection)
    access_token_dao = dao.AccessTokenDAO(connection)
    return [user_dao, access_token_dao]


async def get_user_by_credentials(user_dao, user_login, user_password):
    '''Get user from DataBase'''
    user = user_dao.auth_user(user_login, user_password)
    if user is None:
        errors.send401("Credentials rejected")
        raise Exception("Credentials rejected")

    return user


async def generate_token(access_token_dao, user):
    '''Generate or return access token from DataBase'''
    access_token = access_token_dao.get_by_user(user)

    '''
    deltatime = (datetime.datetime.now() -
                 datetime.timedelta(days=access_token.expires.day, hours=access_token.expires.hour, minutes=access_token.expires.minute))

    logging.warning(datetime.datetime.now())
    logging.warning(access_token.expires)
    logging.warning(datetime.datetime.now() - access_token.expires)
    logging.warning(deltatime)
    # use timedelta to set the different between data
    # date_time_obj = datetime.strptime(access_token.expires, '%Y-%m-%d %H:%M:%S')
    # logging.warning(access_token.expires)
    # access_token.expires, "%Y-%m-%d %H:%M:%S").date())
    '''

    if access_token == None:
        access_token = access_token_dao.create(user)
    if not access_token:
        errors.send401("Token creation error")
        raise Exception("Token creation error")

    return access_token


async def send_finally_headers(access_token):
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
    connect = asyncio.create_task(connect_to_db())
    check_auth = asyncio.create_task(check_auth_header())

    try:
        connection = await connect
        auth_header = await check_auth

        scheme = asyncio.create_task(check_auth_scheme(auth_header))
        credentials = await scheme

        parse = asyncio.create_task(parse_base64(credentials))
        data = await parse

        check_format = asyncio.create_task(check_data_format(data))
        datas = await check_format

        dao_connection = asyncio.create_task(dao_connect(connection))
        daos = await dao_connection

        get_user = asyncio.create_task(
            get_user_by_credentials(daos[0], datas[0], datas[1]))
        user = await get_user

        gen_token = asyncio.create_task(
            generate_token(daos[1], user))
        access_token = await gen_token

        asyncio.create_task(
            send_finally_headers(access_token))

        # logging.warning(send_headers) !!! learn how to log
    except:
        exit()
    finally:
        pass

asyncio.run(main())

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
