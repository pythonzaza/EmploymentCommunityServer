from typing import Optional
from geoip2.database import Reader

from common.logger import logger
from schema_models.common_models import IpDetailsModel

reader = Reader('./db/GeoLite2-City.mmdb', locales=['zh-CN'])


async def query_ip(ip: str) -> IpDetailsModel:
    """
    查询IP地址
    :param ip:
    :return:
    """
    if ip[:4] in ["127.", "192.", "10.", "172."]:
        return IpDetailsModel(ip=ip)

    response = reader.city(ip)

    data = {
        "ip": ip,
        "city": f'{response.country.names["zh-CN"]}{response.subdivisions.most_specific.names["zh-CN"]}{response.city.names["zh-CN"]}',
        # "coordinates": f"{response.location.latitude},{response.location.longitude}",
        "coordinates": f"{response.location.longitude},{response.location.latitude}",
    }

    return IpDetailsModel(**data)

