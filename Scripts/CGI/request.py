#!C:/Python/python.exe

import os
import sys
import urllib.parse
import json

# метод запроса
method = os.environ["REQUEST_METHOD"]
query_string = urllib.parse.unquote(os.environ["QUERY_STRING"])

headers = {}

keys = os.environ.keys()

params = dict(param.split("=", maxsplit=1) if '=' in param else (param, None)
              for param in query_string.split("&"))

'''
for k in keys:
    if (k.startswith('HTTP_')):
        headers[k[5:].lower()] = os.environ[k]
    elif k in ("CONTENT_LENGTH", "CONTENT_TYPE"):
        headers[k.lower()] = os.environ[k]
'''

headers = dict(((k[5:] if k.startswith('HTTP_') else k).lower(), v)
               for k, v in os.environ.items()
               if k.startswith('HTTP_')
               or k in ["CONTENT_LENGTH", "CONTENT_TYPE"])


body = sys.stdin.read()

# Режим backend (API) - машинно-машинное взаимодействие, при котором не
# передается человеко-понятный HTML, а используется машино-понятные данные
print("")  # пустая строка, отделяющая тело
# по стандарту пуе запросы не должны иметь body
print(method, "\nHeaders:", headers,
      f"\n{json.loads(body)}" if os.environ["CONTENT_TYPE"] == "application/json" else f"\n{body}", f"\n{params}", end='')
