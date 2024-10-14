from typing import Annotated

from fastapi import Header

from app.common import constants, exceptions


async def api_key_required(x_api_key: Annotated[str, Header()]):
    if x_api_key != constants.API_KEY:
        raise exceptions.UnauthorizedException("Invalid API Key")
    return None
