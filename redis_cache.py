import redis
import hashlib
import json


r = redis.Redis(host='localhost', port=6379, db=0)


def cache_get(key: str):
    value = r.get(key)
    if value:
        return json.loads(value)
    return None


def cache_set(key: str, value, ex=300):
    r.set(key, json.dumps(value), ex=ex)


def make_cache_key(sql: str):
    return hashlib.sha256(sql.encode()).hexdigest() 