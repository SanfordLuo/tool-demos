from pydantic import BaseModel, ValidationError, conint, constr, validator, conlist, EmailStr
from typing import List


class UserModel(BaseModel):
    """
    conint：
        strict: bool = False: 控制类型强制
        gt: int = None: 强制整数大于设定值
        ge: int = None: 强制整数大于或等于设定值
        lt: int = None: 强制整数小于设定值
        le: int = None: 强制整数小于或等于设定值
        multiple_of: int = None: 强制整数为设定值的倍数
    constr：
        strip_whitespace: bool = False: 删除前尾空格
        to_lower: bool = False: 将所有字符转为小写
        strict: bool = False: 控制类型强制
        min_length: int = None: 字符串的最小长度
        max_length: int = None: 字符串的最大长度
        regex: str = None: 正则表达式来验证字符串
    conlist：
        item_type: Type[T]: 列表项的类型
        min_items: int = None: 列表中的最小项目数
        max_items: int = None: 列表中的最大项目数
    EmailStr:
        邮箱
    validator:
        自定义校验
    """
    id: int
    id_a: conint(gt=5, le=100, multiple_of=5)
    name: str
    name_a: constr(min_length=2, max_length=255, regex='a.*')
    age: int
    friends: List[int]
    friends_a: conlist(item_type=int, min_items=2, max_items=5)
    email: EmailStr

    @validator('age')
    def check_age(cls, v):
        if v < 18:
            raise ValueError('age < 18')
        return v


def test_01():
    params = {
        'id': 5,
        'id_a': 10,
        'name': 'a',
        'name_a': 'ab',
        'age': 18,
        'friends': [1],
        'friends_a': [1, 2],
        'email': 'aaa@123.com'
    }
    try:
        data = UserModel(**params)
    except ValidationError as e:
        print(e.json())
    else:
        print(data.dict())


if __name__ == '__main__':
    test_01()
