from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr


class AuthToken(BaseModel):
    access_token: str
    token_type: str

    class Config:
        schema_extra = dict(
            example=dict(
                access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJUeGVtYSBCZXJtdWRleiIsIm5hbWUiOiJoaSEgd2h"
                             "hdCBhcmUgeW91IGxvb2tpbmcgZm9yPyB4RCJ9.JTDlDRcW4IXTFihK_wkNL-pDHBBTzsF2hVVKa7P1qik",
                token_type="Bearer"
            )
        )


class AuthTokenPayload(BaseModel):
    sub: Optional[EmailStr] = None
