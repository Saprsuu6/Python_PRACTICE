import dao
import db
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import sys
# sys.path.clear()
# sys.path.insert(0,'C:/Users/Sapr_suu6/AppData/Roaming/Python/Python37/site-packages/')
import mysql.connector
import asyncio
import re
import json


class DbService:
    __connection: mysql.connector.MySQLConnection = None

    def get_connection(self) -> mysql.connector.MySQLConnection:
        if DbService.__connection is None or not DbService.__connection.is_connected():
            # print( db.conf )
            try:
                DbService.__connection = mysql.connector.connect(**db.conf)
            except mysql.connector.Error as err:
                print(err)
                DbService.__connection = None
        return DbService.__connection


class DaoService:

    def __init__(self, db_service) -> None:
        self.__db_service: DbService = db_service
        # угода іменування: до полів з "__" додається назва класу:
        self.__user_dao: dao.UserDAO = None
        # "DaoService._DaoService__user_dao". Це аналог "private"
        self.__access_token_dao: dao.AccessTokenDAO = None
        return

    def get_user_dao(self) -> dao.UserDAO:
        if self.__user_dao is None:
            self.__user_dao = dao.UserDAO(self.__db_service.get_connection())
        return self.__user_dao

    def get_access_token_dao(self) -> dao.AccessTokenDAO:
        if self.__access_token_dao is None:
            self.__access_token_dao = dao.AccessTokenDAO(
                self.__db_service.get_connection())
        return self.__access_token_dao

    def get_clear_connection(self) -> mysql.connector.MySQLConnection:
        return self.__db_service.get_connection()


# print( DaoService.__user_dao )  # AttributeError: type object 'DaoService' has no attribute '__user_dao'
# print( DaoService._DaoService__user_dao )  # OK


dao_service: DaoService = None


class MainHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server) -> None:
        # RequestScoped - створюється при кожному запиті
        super().__init__(request, client_address, server)
        # print( 'init', self.command )    # self.command - метод запиту (GET, POST, ...)

    def do_GET(self) -> None:
        # вывод в консоль (не в ответ сервера)
        print("path:", self.path)
        # разделенный на части запрос, path_parts[0] - пустой, т.к. path начинается со "/"
        path_parts = self.path.split("/")
        # if path_parts[1] == "":
        #     path_parts[1] = "static/index.html"
        if self.path == '/':
            self.path = '/static/index.html'
        # print(os.getcwd())
        fname = "./http" + self.path
        # print(fname)
        if os.path.isfile(fname):              # запрос - существующий файл
            print(fname)
            # print( fname, "file" )
            self.flush_file(fname)
        elif path_parts[1] == "auth":            # запрос - /auth
            self.auth()
        elif path_parts[1] == "items":            # запрос - /items
            self.items()
        else:
            # print( fname, "not file" )
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write("<h1>404</h1>".encode())
        return

    def auth(self) -> None:
        try:
            # дістаємо заголовок Authorization
            auth_header = self.check_auth()

            # Перевіряємо схему авторизації - має бути Basic
            credentials = self.check_auth_scheme(auth_header)

            # декодуємо credentials
            data = self.parse_base64(credentials)

            # Перевіряємо формат (у data має бути :), розділяємо логін та пароль за ":"
            datas = self.check_data_format(data)

            # підключаємо userdao
            user_dao = dao_service.get_user_dao()
            user = self.get_user_by_credentials(user_dao, datas[0], datas[1])

            # get user access token
            access_token_dao = dao_service.get_access_token_dao()
            access_token = self.generate_token(access_token_dao, user)

            # send finally sucessull headers with token
            self.send_200(message=f'''{{
                    "access_token": "{access_token.token}",
                    "token_type": "Bearer",
                    "expires_in": "{access_token.expires}"
                }}''')
        except Exception as error:
            print(error)
        finally:
            exit()

    def check_auth_scheme_BASIC(self, auth_header):
        '''Check authedification scheme BASIC'''
        if auth_header.startswith('Basic'):
            return auth_header[6:]
        else:
            self.send401("Authorization scheme Basic required")
            raise Exception("Authorization scheme Basic required")

    def check_auth(self):
        '''Check authedification header'''
        auth_header = self.headers.get("Authorization")
        if auth_header is None:
            self.send_401("Authorization header required")
            return Exception("Authorization header required")

        return auth_header

    def parse_base64(self, credentials):
        '''Convert string from base64 to utf8'''
        try:
            return base64.b64decode(credentials, validate=True).decode('utf-8')
        except:
            self.send401("Credentials invalid: Base64 string required")
            raise Exception("Credentials invalid: Base64 string required")

    def check_data_format(self, data):
        '''Chech credentials format'''
        if not ':' in data:
            self.send401("Credentials invalid: Login:Password format expected")
            raise Exception(
                "Credentials invalid: Login:Password format expected")

        user_login, user_password = data.split(':', maxsplit=1)
        return [user_login, user_password]

    def get_user_by_credentials(self, user_dao, user_login, user_password):
        '''Get user from DataBase'''
        user = user_dao.auth_user(user_login, user_password)
        if user is None:
            self.send401("Credentials rejected")
            raise Exception("Credentials rejected")

        return user

    def generate_token(self, access_token_dao, user) -> str:
        '''Generate or return access token from DataBase'''
        access_token = access_token_dao.get_by_user(user)

        if access_token == None:
            access_token = access_token_dao.create(user)
        if not access_token:
            self.send401("Token creation error")
            raise Exception("Token creation error")

        return access_token

    def items(self) -> None:
        try:
            # дістаємо заголовок Authorization
            auth_header = self.check_auth()

            # extect token
            data = self.extract_token(auth_header)

            # get token by user credentials
            connection = dao_service.get_clear_connection()
            token_obj = self.get_token(connection, data)

            # check_valid
            self.validate_token(self, token_obj.token)

            user_dao = dao_service.get_user_dao()
            #user = user_dao.get_user(id=token_obj.user_id)
            users = user_dao.get_users(ignore_deleted=False)
            jsonObj = json.dumps(users)

            self.send_200(message=jsonObj ,type="json")
        except Exception as error:
            print(error)
        finally:
            exit()

    def check_auth_scheme_BEARER(self, auth_header):
        '''Check authorisation header'''
        if not auth_header:
            self.send401("Authorization header required")
            raise Exception("Authorization header required")

        if not auth_header.startswith('Bearer'):
            self.send401("Bearer Authorization header required")
            raise Exception("Bearer Authorization header required")

    def extract_token(auth_header):
        '''Extract the token from BEARER'''
        return auth_header[7:]

    def get_token(self, connection, access_token):
        '''Get token from from front-end'''
        token = dao.AccessTokenDAO(connection).get(access_token)
        if not token:
            self.send401("Token rejected")
            raise Exception("Token rejected")

        return token

    def validate_token(self, token):
        result = re.findall(r'^[0-9a-f]{40}$', token)
        
        if len(result) == 0:
            self.send401("Token rejected")
            raise Exception("Token rejected")



    def send_401(self, message: str = None) -> None:
        self.send_response(401, "Unauthorized")
        if message:
            self.send_header("Content-Type", "text/plain")
        self.end_headers()
        if message:
            self.wfile.write(message.encode())
        return

    def send_200(self, message: str = None, type: str = "text") -> None:
        self.send_response(200)
        if type == 'json':
            content_type = 'application/json; charset=UTF-8'
        else:
            content_type = 'text/plain; charset=UTF-8'
        self.send_header("Content-Type", content_type)
        self.end_headers()
        if message:
            self.wfile.write(message.encode())
        return

    def flush_file(self, filename) -> None:
        # Визначаємо розширення файлу
        extension = filename[filename.rindex(".") + 1:]
        # print( extension )
        # Встановлюємо тип (Content-Type)
        if extension == 'ico':
            content_type = 'image/x-icon'
        elif extension in ('html', 'htm'):
            content_type = 'text/html'
        elif extension == 'css':
            content_type = "text/css"
        elif extension == 'js':
            content_type = "application/javascript"
        else:
            content_type = 'application/octet-stream'

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        # Копіюємо вміст файлу у тіло відповіді
        with open(filename, "rb") as f:
            self.wfile.write(f.read())
        return

    # Override
    def log_request(self, code: int or str = ..., size: int or str = ...) -> None:
        # логування запиту у консоль
        # return super().log_request(code, size)
        return

    def check_auth_scheme(self, auth_header):
        '''Check authorisation header'''
        if not auth_header:
            self.send401("Authorization header required")
            raise Exception("Authorization header required")

        if not auth_header.startswith('Bearer'):
            self.send401("Bearer Authorization header required")
            raise Exception("Bearer Authorization header required")


def main() -> None:
    global dao_service
    http_server = HTTPServer(
        ('127.0.0.1', 88),     # host + port = endpoint
        MainHandler)
    try:
        print("Server started")
        dao_service = DaoService(DbService())   # ~ Inject
        http_server.serve_forever()
    except:
        print("Server stopped")


if __name__ == "__main__":
    main()

'''
Інший спосіб створення серверних додатків (поруч з CGI) - утворення
"власного" сервера, який прослуховує порт та запускає оброблення запитів.
Засоби:
 http.server - модуль
 HTTPServer - клас для старту сервера
 BaseHTTPRequestHandler - базовий клас для обробників запитів (~ Servlet)
Особливості (у порівнянні з CGI)
- сервер запускається засобами Python з консолі, відповідно print діє 
    як у скриптах - виводить у консоль (не у відповідь сервера)
- обробник запитів (Handler) - це клас нащадок BaseHTTPRequestHandler,
    його методи відповідають формі do_GET, do_POST, ... ,
    методи не приймають параметрів, усі дані про requestorresponse
    проходять як поля/методи self.(send_response, send_header)
- формування тіла здійснюється за файловим протоколом через запис
    у self.wfile Особливість - він пише не рядки, а бінарні дані
- успішні запити логуються у консоль (127.0.0.1 - - [27/Dec/2022 12:45:15] "GET / HTTP/1.1" 200 - )
    за це відповідає метод log_request, який можна переозначити
- запити не маршрутизуються (всі потрапляють у do_GET), наявність 
    файлів не перевіряється (запити на файли також потрапляють у do_GET)
    Необхідно самостійно опрацьовувати запити на файли
'''
