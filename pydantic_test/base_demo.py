from pydantic import BaseModel, ValidationError
from typing import List, Optional
from datetime import datetime


class FriendModel(BaseModel):
    friend_name: str = 'oker'
    friend_age: int
    # Optional 可选参数，默认None，也可指定默认，
    # Optional[int] 等价于 Union[int, None]，既可以传指定的类型 int，也可以传 None
    # add_time: Optional[str]
    add_time: Optional[str] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class UserModel(BaseModel):
    id: int
    name: str
    friends: List[FriendModel]


def test_01():
    """
    返回结果:
        {
            'id': 111,
            'name': 'sanford',
            'friends': [{
                'friend_name': 'jay',
                'friend_age': 22,
                'add_time': '2022-03-22 18:29:34'
            }, {
                'friend_name': 'oker',
                'friend_age': 23,
                'add_time': '2022-03-22 18:29:34'
            }, {
                'friend_name': 'chou',
                'friend_age': 24,
                'add_time': '2022-03-22 18:00:00'
            }]
        }
    """
    params = {
        'id': 111,
        'name': 'sanford',
        'friends': [
            {'friend_name': 'jay', 'friend_age': '22'},  # friend_age定义的是int型，输入是str时输出结果会转换int
            {'friend_age': 23},
            {'friend_name': 'chou', 'friend_age': 24, 'add_time': '2022-03-22 18:00:00'},
        ],
        'invalid': 777  # 未定义invalid，输出结果会筛选掉
    }
    data = UserModel(**params)
    # print(data.name)  # 获取指定参数
    print(data.dict())  # 返回参数转换为字典


def test_02():
    """
    捕获异常：
        [
          {
            "loc": [
              "id"
            ],
            "msg": "field required",
            "type": "value_error.missing"
          },
          {
            "loc": [
              "friends"
            ],
            "msg": "value is not a valid list",
            "type": "type_error.list"
          }
        ]
    """
    err_params = {
        'name': 'sanford',
        'friends': {'friend_age': 23}
    }
    try:
        data = UserModel(**err_params)
    except ValidationError as e:
        # print(e.json())
        print(e.errors())
    else:
        print(data.dict())


if __name__ == '__main__':
    # test_01()
    test_02()
