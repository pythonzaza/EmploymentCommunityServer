from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from fastapi import Query

from schema_models.base_model import RespModel


class CreateEnterPriseModel(BaseModel):
    name: str = Field(..., description="公司名称", min_length=4, max_length=30)
    legal_person: Optional[str] = Field(None, description="公司法人", min_length=2, max_length=30)
    address: str = Field("", description="公司地址", max_length=30)
    details: str = Field("", description="公司详情", max_length=1000)
    code: Optional[str] = Field(None, description="公司统一社会信用码,可在天眼查查询,未填写时请输入null或省略该字段", max_length=30)
    TYX_url: str = Field("", description="天眼查中的公司链接")


class UpdateEnterPriseModel(CreateEnterPriseModel):
    name: Optional[str] = Field(None, description="公司名称", min_length=4, max_length=30)
    enterprise_id: int = Field("", description="企业id")


class EnterPriseModelDetails(CreateEnterPriseModel):
    id: int = Field(0, description="公司id")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="创建时间")
    message_count: int = Field(..., description="留言总次数")

    class Config:
        orm_mode = True


class EnterPriseModelList(EnterPriseModelDetails):
    def dict(self, *, include=None, exclude=None, by_alias: bool = False, skip_defaults: bool = None,
             exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False):
        exclude = self.Config.exclude if exclude is None else exclude

        return super().dict(include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults,
                            exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none)

    class Config:
        exclude = {"details"}


class EnterPriseDetailsModel(RespModel):
    data: Optional[EnterPriseModelDetails] = Field({})


class EnterPriseListModel(RespModel):
    total: Optional[int] = Field(0, description="总条数")
    data: List[EnterPriseModelList] = Field([])
