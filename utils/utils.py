import logging
import os
import sys

from pymysql.connections import CLIENT
import pymysql.cursors


def resource_path(rel):
    """
    获取资源的路径
    :param rel: 相对路径
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel)
    return os.path.join(os.path.dirname(__file__), "../", rel)

def exec_sql_file(sql_filepath, host, port, user, passwd, database, charset, collate):
    """
    execute sql file
    :param sql_filepath: sql filepath
    :param host: db host
    :param port: db port
    :param user: db user
    :param passwd: db passwd
    :param database: db database
    :param charset: db default charset
    :param collate: db default collate
    """
    ret = True
    # stmts = parse_sql_file(sql_filepath=sql_filepath)
    connection = pymysql.connect(host=host,
                                 port=port,
                                 user=user,
                                 password=passwd,
                                 cursorclass=pymysql.cursors.DictCursor,
                                 client_flag=CLIENT.MULTI_STATEMENTS)
    try:
        with connection.cursor() as cursor:
            logging.info("DROP DATABASE IF EXISTS {}".format(database))
            cursor.execute("DROP DATABASE IF EXISTS {}".format(database))
            logging.info("CREATE DATABASE {} CHARACTER SET {} COLLATE {}".format(database, charset, collate))
            cursor.execute("CREATE DATABASE {} CHARACTER SET {} COLLATE {}".format(database, charset, collate))
            logging.info("USE {}".format(database))
            cursor.execute("USE {}".format(database))
            logging.info("exec {}".format(sql_filepath))
            with open(sql_filepath, "r", encoding="utf-8") as f:
                sql_scripts = f.read()
                cursor.execute(sql_scripts)
    except pymysql.Error as e:
        logging.error("failed exec sql, {}".format(e))
        connection.rollback()
        ret = False
    finally:
        connection.close()
    return ret
