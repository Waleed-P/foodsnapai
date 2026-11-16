from enum import Enum


class TokenVariants(str, Enum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"


# Legacy alias
TokenVarients = TokenVariants
