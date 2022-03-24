from pydantic import BaseModel, Field
from typing import Any


class RespModel(BaseModel):
    status: int = Field(1, description='状态码,1为成功,其余均失败')
    message: str = Field('Success', description='响应备注,默认成功')
    data: Any = Field([], description='响应体,返回值为obj')

    # def json(self, *args, **kwargs):
    #     super().json(ensure_ascii=False, *args, **kwargs)


class RespModel422(RespModel):
    status = 422
    message = "数据格式异常"
    data: str = ""
