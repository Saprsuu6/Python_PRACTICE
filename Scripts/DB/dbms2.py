# работа с таблицей Users
import hashlib
import mysql.connector
import random
import uuid


class User:
    def __init__(self, row=None, tuple=None) -> None:
        if tuple != None:
            self.id = tuple.id
            self.login = tuple.login
            self.passw = tuple.passw
            self.name = tuple.passw
            self.salt = tuple.salt
            self.avatar = tuple.avatar
            self.email = tuple.email
            self.email_code = tuple.email_code
            self.email_code_attempts = tuple.email_code_attempts
            return

        if row == None:
            self.id = ''
            self.login = ''
            self.passw = ''
            self.name = ''
            self.salt = ''
            self.avatar = ''
            self.email = ''
            self.email_code = ''
            self.email_code_attempts = ''
        else:
            if row:
                self.id = row[0]
                self.login = row[1]
                self.passw = row[2]
                self.name = row[3]
                self.salt = row[4]
                self.avatar = row[5]
                self.email = row[6]
                self.email_code = row[7]
                self.email_code_attempts = row[8]

    def print_user(self) -> None:
        info = f"ID: {self.id},\nLOGIN: {self.login},\nPASSWORD: {self.passw}\nNAME: {self.name}\nSALT: {self.salt}\nAVATAR: {self.avatar}\nEAMIL: {self.email}\nEMAIL_CODE: {self.email_code}\nnEMAIL_CODE_ATTEMPTS: {self.email_code_attempts}"
        print(info)


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

        # print(user.__dict__)

        user.id = str(uuid.uuid4())
        user.email_code_attempts = 0

        keys = user.__dict__.keys()
        fields = ','.join(f"`{x}`" for x in keys).replace('passw', 'pass')
        placeholders = ','.join(f"%({x})s" for x in keys)

        sql = f"INSERT INTO Users({fields}) VALUES({placeholders})"
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, user.__dict__)
            self.db.commit()
        except mysql.connector.Error as err:
            print('ADD_USER ERROR: ', err)
            return False
        else:
            return True
        finally:
            cursor.close()

    def get_users(self) -> tuple | None:
        ''' Get all users from DB table '''
        sql = 'SELECT * FROM Users'
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
        except mysql.connector.Error as err:
            print('GET_USER ERROR: ', err)
            return None
        else:
            return tuple(User(row) for row in cursor)
        finally:
            cursor.close()
        return


def main(db: mysql.connector.MySQLConnection) -> None:
    user = User()
    user.login = "admin"
    user.passw = "123"
    user.name = "Root Administrator"
    user.avatar = None
    user.email = "admin@ukr.net"

    userDao = UserDAO(db)
    # userDao.add_user(user)

    print('USERS: ->\n')
    for item in list(userDao.get_users()):
        tupleUser = User(None, item)
        tupleUser.print_user()
        print('-----------------------------------')


if __name__ == "__main__":
    pars = {
        "host":     "localhost",
        "port":     3306,
        "database": "py191",
        "user":     "py191_user",
        "password": "pass_191",

        "charset":  "utf8mb4",
        "use_unicode": True,
        "collation": "utf8mb4_general_ci"
    }
    try:
        connection = mysql.connector.connect(**pars)
    except mysql.connector.Error as err:
        print("Connection:", err)
        exit()
    else:
        main(connection)   # точка инъекции
    finally:
        connection.close()


'''
CREATE TABLE `users` (
  `id`                  char(36)    NOT NULL       COMMENT 'UUID',
  `login`               varchar(32) NOT NULL,
  `pass`                char(40)    NOT NULL       COMMENT 'SHA-160 hash',
  `name`                tinytext    NOT NULL,
  `salt`                char(40)    DEFAULT NULL   COMMENT 'SHA-160 of random',
  `avatar`              varchar(64) DEFAULT NULL   COMMENT 'Avatar filename',
  `email`               varchar(64) DEFAULT NULL   COMMENT 'User E-mail',
  `email_code`          char(6)     DEFAULT NULL   COMMENT 'E-mail confirm code',
  `email_code_attempts` int(11)     DEFAULT 0      COMMENT 'Count of invalid E-mail confirmations',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;


Python              ~socket              DBMS
db.cursor() <-------------------------->
cur.execute(sql) -----(SELECT)---------> PLAN - схема выполнения
cur.fetchone()  -----------------------> получение одной строки (одно выполнение PLAN)
                <----------------------- отправка рез-та


Python              ~socket              DBMS
db.cursor() <-------------------------->
cur.execute(sql) -----(SELECT)---------> PLAN - схема выполнения + выполнение несколько раз
                        (буфер)<-------- для заполнения буфера     
cur.fetchone()  ----->(буфер)                  
               <------ получение одной строки 
                        (буфер) <------- Если опустошается, то заполнить

Подготовленный запрос
Python              ~socket              DBMS
db.cursor() <-------------------------->
                подготовка запроса
cur.prepare(sql) -----(SELECT ?)-------> PLAN - схема выполнения (создается временная хранимая процедура с параметром)
                выполнение запроса
cur.execute(data1) -----(data1)--------> выполнение (EXEC) хранимой процедуры с аргументом data1
cur.fetchone()  -----------------------> получение одной строки (одно выполнение PLAN)
                <----------------------- отправка рез-та
         повторное выполнение не посылает повторного SQL (SELECT)
cur.execute(data2) -----(data2)--------> выполнение (EXEC) хранимой процедуры с аргументом data2
cur.fetchone()  -----------------------> получение одной строки (одно выполнение PLAN)
                <----------------------- отправка рез-та
         возможно многократное выполнение       
cur.close()    ------------------------> разрушение временной процедуры

Транзакция
Python              ~socket              DBMS
db.cursor() <-------------------------->
cur.query("CREATE TRANSACTION") -------> Начало транзакции (присваивается id транзакции)
cur.query(sql1)                          на время транзакции каждая команда сохраняет
cur.query(sql2)                          предыдущее состояние для возможности отмены транзакции
cur.query(sql3)                          а также блокирует таблицу/строки для других запросов (не из этой транзакции)
cur.query("COMMIT TRANSACTION") -------> конец транзакции
                       либо
cur.query("ROLLBACK TRANSACTION") -----> отмена транзакции

'''
