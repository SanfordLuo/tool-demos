"""
mysql redis 的连接使用
"""
import MySQLdb
import MySQLdb.cursors
import redis


class RedisHandler(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        pool = redis.ConnectionPool(decode_responses=True)
        self.redis = redis.Redis(
            host='localhost',
            port=3306,
            db=0,
            connection_pool=pool)


class DbHandler(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.connect = MySQLdb.connect(
            host='localhost',
            user='root',
            password='jayae.22378',
            database='sanford',
            port=3306,
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            autocommit=True
        )
        self.cursor = self.connect.cursor()


class TableUser(DbHandler):
    def __init__(self):
        super().__init__()

    def get_user_by_id(self, user_id):
        sql = """select * from user where id = %s"""
        self.cursor.execute(sql, [user_id])
        return self.cursor.fetchone()

    def insert_user(self, data):
        data_keys = str(tuple(data.keys())).replace("'", "")
        data_values = data.values()
        values_num = '({})'.format('%s,' * len(data)).replace(',)', ')')
        sql = """ insert into user %s values %s """ % (data_keys, values_num)
        ret = self.cursor.execute(sql, data_values)
        return ret


if __name__ == '__main__':
    # ret = RedisHandler().redis.get('name')
    # print(ret)

    user_info = TableUser().get_user_by_id(1)
    print(user_info['username'])

    # data_1 = dict(
    #     uuid=10000005,
    #     username='jay_05',
    #     password='10000005',
    #     phone=17839194005
    # )
    # data_2 = dict(
    #     uuid=10000006,
    #     username='jay_06',
    #     password='10000006',
    #     phone=17839194006
    # )
    # table_user = TableUser()
    # try:
    #     table_user.connect.begin()
    #     table_user.insert_user(data_1)
    #     table_user.insert_user(data_2)
    # except Exception as e:
    #     print(e)
    #     table_user.connect.rollback()
    # else:
    #     table_user.connect.commit()
