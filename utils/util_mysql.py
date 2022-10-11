"""
@Author  :   luoyafei
@Time    :   2022/09/22 17:58:54
@Desc    :   None
"""
import time
import pymysql
import logging
from DBUtils.PooledDB import PooledDB

logger = logging.getLogger('server')


class SqlalchemyShell(object):
    """
    Sqlalchemy 的上下文管理器
    """

    def __init__(self, db_session):
        self.db_session = db_session

    def __enter__(self, *args):
        return self.db_session

    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            self.db_session.commit()
        except Exception as e:
            logger.info(e)
            self.db_session.rollback()


class MysqlShell():
    """
    mysql上下文管理器
    """

    def __init__(self, db_core):
        self.__db_core = db_core

    def __enter__(self, *args):
        [self.connect, self.cursor] = self.__db_core._get_connect_cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_traceback is None:
            self.__db_core._recycle_connect_cursor(self.connect, self.cursor)
        else:
            self.__db_core._recycle_connect_cursor_with_rollback(self.connect, self.cursor)


class MysqlClient(object):

    def __init__(self, mysql_config):
        self.inner_db = None
        self.maxconnections = 100
        self.maxcached = 5
        self.mysql_config = mysql_config
        # host, user, passwd, db, port, charset

    def _get_connect_cursor(self):
        """
        从 DB 连接池中获取一个连接以及其对应的游标
        :return:
        """
        try:
            connection = self.inner_db.connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            return [connection, cursor]
        except BaseException as et:
            try:
                del self.inner_db
                self.inner_db = None
            except BaseException as edd:
                pass

            conn_times = 0
            while not self.inner_db:
                try:
                    self.inner_db = PooledDB(pymysql,
                                             maxconnections=self.maxconnections,
                                             maxcached=self.maxcached, **self.mysql_config)
                    connection = self.inner_db.connection()
                    cursor = connection.cursor(pymysql.cursors.DictCursor)
                    return [connection, cursor]
                except BaseException as ec:
                    try:
                        del self.inner_db
                    except BaseException as ed:
                        pass
                    time.sleep(0.5)
                    self.inner_db = None
                    conn_times += 1
                    if conn_times > 4:
                        raise BaseException('__get_connect_cursor: '
                                            'MySQL db get connection exception[{exp}] ERROR!!'
                                            .format(exp=str(ec)))

    @staticmethod
    def _recycle_connect_cursor(connect, cursor):
        try:
            if cursor:
                cursor.close()
            if connect:
                #  mysql 数据库没有配置 auto-commit 时，会出现连接池不同连接，数据状态不一致的问题
                #  所以回收前先 commit()
                #  参见 http://everet.org/python-mysqldb-autocommit-transaction-misunderstood.html
                connect.commit()
                connect.close()
        except BaseException as e:
            pass

    @staticmethod
    def _recycle_connect_cursor_with_rollback(connect, cursor):
        try:
            if cursor:
                cursor.close()
            if connect:
                connect.rollback()
                connect.close()
        except Exception as e:
            raise BaseException('Recycle DB-Connection error[{e}]'.format(e=e))

    def execute(self, sql, args=None):
        try:
            [conn, cursor] = self._get_connect_cursor()
        except BaseException as e:
            raise BaseException('get_poem_data: exception[{exp}]'.format(exp=str(e)))

        cursor.execute(sql, args)
