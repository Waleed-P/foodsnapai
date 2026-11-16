from authlib.integrations.starlette_client import OAuth
from app.core.config import settings

oauth = OAuth()

if settings.client_id and settings.client_secret:
    oauth.register(
        name="google",
        client_id=settings.client_id,
        client_secret=settings.client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile"
        },
    )
else:
    # Register anyway so startup doesn't break if env vars are configured later
    oauth.register(
        name="google",
        client_id=settings.client_id or "placeholder",
        client_secret=settings.client_secret or "placeholder",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile"
        },
    )
