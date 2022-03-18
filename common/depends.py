from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer,OAuth2

OAuth2 = OAuth2()


async def jwt_auth(token=Depends(OAuth2)):
    pass
