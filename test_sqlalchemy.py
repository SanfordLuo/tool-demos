import logging
from utils.util_logger import set_logger_config
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, DECIMAL, Enum, Date, DateTime, Time, String, Text, Index
from datetime import datetime
from utils.util_mysql import SqlalchemyShell

set_logger_config('test_sqlalchemy')
logger = logging.getLogger('test_sqlalchemy')

Base = declarative_base()


class User(Base):
    """
    primary_key=True  设置主键
    autoincrement=True  自增
    default  默认值
    nullable=False  不能为空
    index=True  索引
    unique=True  唯一索引
    onupdate：在数据更新的时候会调用这个参数指定的值或者函数。在第一次插入这条数据的时候，不会用onupdate的值，只会使用default的值。常用于是update_time字段（每次更新数据的时候都要更新该字段值）。
    """
    __tablename__ = "user"
    __table_args__ = ({"comment": "用户表"})

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户id")
    username = Column(String(255), nullable=False, unique=True, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    phone = Column(String(11), nullable=False, unique=True, comment="手机号")
    email = Column(String(255), default="", comment="邮箱")
    avatar = Column(String(255), default="", comment="用户头像")
    birthday = Column(String(11), default="", comment="生日")
    id_card = Column(String(11), default="", comment="身份证")
    sex = Column(Integer, default=0, comment="性别: 0-保密 1-男 2-女")
    status = Column(Integer, default=0, comment="用户状态: 0-注册 1-认证中 2-已认证 3-注销中 4-已注销")
    create_time = Column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="修改时间")


def init_engine():
    # engine = create_engine('dialect+driver://username:password@host:port/database')
    """
    echo=False: 默认False, 为True时候会把sql语句打印出来
    pool_size=5: 连接池的大小, 默认为5个, 0表示连接数无限制。初始化时并不产生连接，当并发量上去时连接才会慢慢增多直到最高连接数。
    pool_recycle=3600: 在指定秒数内，没有任何动作的连接会被回收掉, 默认-1时mysql设置的等待时间连接8小时无动作时断开。
    pool_pre_ping: 探针检测, 为True时出现异常则连接全部回收，重新根据并发量建立连接
    """
    engine = create_engine('mysql+pymysql://root:jayae.22378@localhost:3306/sanford-test?charset=utf8')
    return engine


def create_table(engine):
    Base.metadata.create_all(engine)


def test_insert(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    # 插入数据返回id
    # user = User(username='jay', password='jay', phone='17813227930')
    # session.add(user)
    # session.flush()
    # session.commit()
    # print("======================", user.id)

    # 批量插入
    objects = [
        User(username='jay_00', password='jay', phone='17813227931'),
        User(username='jay_01', password='jay', phone='17813227932'),
        User(username='jay_02', password='jay', phone='17813227933')]
    session.add_all(objects)
    session.commit()


def test_update(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(User)

    # 单个更新
    # xm_user = query.filter(User.id == 9).first()
    # xm_user.username = 'hhhh'
    # session.commit()

    # 批量更新
    query.filter(User.create_time >= '2022-10-12 00:37:49').update({User.sex: 1})
    session.commit()


def test_query(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    # q = session.query(User)
    # print(q.count())
    # for _ in q:
    #     print(_.id)

    query = session.query(User)

    # ret = query.filter(User.create_time >= '2022-10-12 00:37:49').order_by(User.id.desc()).all()
    # for aa in ret:
    #     print(aa.id)

    # 原生sql查询
    # ret_01 = query.from_statement(text("SELECT * FROM user where sex=:sex")).params(sex=1).all()
    # for aa in ret_01:
    #     print(aa.id)

    # 分页查询 page_size=2, page_no=2
    # offset：偏移量, 第几条开始，limit：条数限制, page_size *( page_no - 1 )
    ret_02 = query.filter(User.create_time >= '2022-10-12 00:37:49').order_by(User.id.desc()).offset(2).limit(2)
    for aa in ret_02:
        print(aa.id)


def test_delete(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(User)

    # 单个删除
    # xm_user = query.filter(User.username == 'hhhh').first()
    # session.delete(xm_user)
    # session.commit()

    # 批量删除
    query.filter(User.create_time >= '2022-10-12 00:37:49').delete()
    session.commit()


def test_shiwu(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user_00 = User(username='luo_00', password='luo_00', phone='17813227934')
        session.add(user_00)
        user_01 = User(username='luo_00', password='luo_01', phone='17813227935')
        session.add(user_01)
        session.commit()
        # raise False
    except Exception as e:
        session.rollback()


def test_aa(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    ret = session.execute("select * from user where id = :id", {"id": 1})
    for ii in ret:
        print(ii.id)


def test_with(engine):
    Session = sessionmaker(bind=engine)

    with SqlalchemyShell(Session()) as session:
        ret_00 = session.query(User).filter(User.id == 1).update({User.sex: 2})

        new_user = User(username='jay_03', password='jay_03', phone='17813227934')
        ret_01 = session.add(new_user)
        session.flush()

        ret_02 = session.query(User).filter(User.id == 1).update({User.sex: 2})

        print(111)


if __name__ == '__main__':
    engine = init_engine()
    # create_table(engine)
    # test_insert(engine)
    # test_update(engine)
    # test_query(engine)
    # test_delete(engine)
    # test_shiwu(engine)
    # test_aa(engine)
    test_with(engine)
