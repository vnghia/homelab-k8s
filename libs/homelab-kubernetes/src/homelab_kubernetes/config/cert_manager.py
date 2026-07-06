from . import app


class Config(app.Config):
    chart: str
    version: str
    issuer: str
    email: str
