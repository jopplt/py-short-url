from bootstrap import app
from entrypoints.fastapi import ApiFactory

api = ApiFactory().create(application=app)
