import mysql.connector
import errors
import db


def connect():
    try:
        return mysql.connector.connect(**db.conf)
    except mysql.connector.Error as err:
        errors.send401(err)
        exit()
