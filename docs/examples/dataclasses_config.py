from pydantic import ConfigDict
from pydantic.dataclasses import dataclass


# 方式 1 - 直接使用字典
# 注意: `mypy` 仍然会引发拼写错误
@dataclass(config=dict(validate_assignment=True))
class MyDataclass1:
    a: int


# 方式 2 - 使用`ConfigDict`
# （在运行时与之前相同，因为它是一个 TypedDict 但具有智能感知）
@dataclass(config=ConfigDict(validate_assignment=True))
class MyDataclass2:
    a: int


# Option 3 - 使用类似于 BaseModel 的 `Config` 类 
class Config:
    validate_assignment = True


@dataclass(config=Config)
class MyDataclass3:
    a: int
