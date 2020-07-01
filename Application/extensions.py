from flask_wtf import CSRFProtect
from redis import Redis

redis = Redis()
csrf = CSRFProtect()
