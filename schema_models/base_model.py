from pydantic import BaseModel, Field
from typing import Any


class RespModel(BaseModel):
    status: int = Field(1, description='状态码,1为成功,其余均失败')
    message: str = Field('成功', description='响应备注,默认成功')
    data: Any = Field([], description='响应体,返回值为obj')



