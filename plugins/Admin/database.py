import redis

from config.Admin import REDIS


r = redis.Redis(**REDIS)
