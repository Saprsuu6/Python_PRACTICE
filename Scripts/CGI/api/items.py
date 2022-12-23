#!C:/Python/python.exe

import dao
import db_connect
import errors
import check_auth
import genral_header
# API demo - доступ до ресурсу обмеженого доступу (Resource Server)


# дістаємо заголовок Authorization
auth_header = check_auth.check_auth()

# Проверяем наличие заголовка Authorization
if not auth_header:
    errors.send401("Authorization header required")
    exit()

# Проверяем схему авторизации Bearer
if not auth_header.startswith('Bearer'):
    errors.send401("Bearer Authorization header required")
    exit()

# Извлекаем токен
access_token = auth_header[7:]   # убираем 'Bearer' + space

# підключаємось до БД
connection = db_connect.connect()

token = dao.AccessTokenDAO(connection).get(access_token)
if not token:
    errors.send401("Token rejected")
    exit()

# Проверяем активность токена (срок)

# Успішне завершення
genral_header.send_header()
print()
print(f'"{token}"')


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
