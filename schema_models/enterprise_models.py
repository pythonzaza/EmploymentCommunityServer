from pydantic import BaseModel, Field, root_validator
from datetime import datetime, date, timedelta
from typing import List, Optional, Any
from fastapi import Query

from schema_models.base_model import RespModel


class CreateEnterPriseModel(BaseModel):
    """  `create_date` date DEFAULT NULL COMMENT '企业创建时间',
  `register_capital` int DEFAULT NULL COMMENT '注册资本, 单位:万',"""
    name: str = Field(..., description="公司名称", min_length=4, max_length=30)
    legal_person: Optional[str] = Field(None, description="公司法人", min_length=2, max_length=30)
    address: str = Field("", description="公司地址", max_length=30)
    details: str = Field("", description="公司详情", max_length=1000)
    code: Optional[str] = Field(None, description="公司统一社会信用码,可在天眼查查询,未填写时请输入null或省略该字段", max_length=30)
    TYX_url: str = Field("", description="天眼查中的公司链接")
    create_date: date = Field(date.fromisoformat("1970-01-01"), description="企业创建时间")
    register_capital: int = Field(0, ge=0, description="注册资本, 单位:万")

    @root_validator
    def check_create_date(cls, values: dict):
        """
        检查企业创建时间
        """
        if values.get("create_date") and values.get("create_date") > datetime.now().date():
            raise ValueError("create_date不能大于今天")
        return values


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
        exclude = {"details", "create_date", "register_capital", "TYX_url"}


class EnterPriseDetailsModel(RespModel):
    data: Optional[EnterPriseModelDetails] = Field({})


class EnterPriseListModel(RespModel):
    total: Optional[int] = Field(0, description="总条数")
    data: List[EnterPriseModelList] = Field([])
