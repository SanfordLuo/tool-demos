import logging
from utils.util_logger import set_logger_config
from utils.util_mysql import MysqlShell, MysqlClient

set_logger_config('test')
logger = logging.getLogger('test')


def test_log():
    logger.info("test info message")
    logger.error("test error message")


def test_mysql():
    mysql_config = {'host': 'localhost',
                    'user': 'root',
                    'passwd': 'jayae.22378',
                    'db': 'sanford',
                    'port': 3306,
                    'charset': 'utf8'}

    with MysqlShell(MysqlClient(mysql_config)) as conn:
        sql = "SELECT * FROM USER WHERE id = %s;"
        args = [22]
        conn.cursor.execute(sql, args)
        ret = conn.cursor.fetchone()
        print(ret)


if __name__ == '__main__':
    test_log()
    test_mysql()
