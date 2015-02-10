import json
import os
import redis
import requests

github_user = os.environ.get('GITHUB_USER')
github_pass = os.environ.get('GITHUB_PASS')

redis_conn = redis.from_url(os.environ.get('REDISTOGO_URL'))


def cached_http_get(key, ttl=None):
    data = redis_conn.get(key)
    if data:
        return json.loads(data)

    print "Data not cached. Getting it now..."
    data = requests.get(key, auth=(github_user, github_pass)).json()

    if ttl:
        redis_conn.setex(key, json.dumps(data), ttl)
    else:
        redis_conn.set(key, json.dumps(data))
    return data

def cache_until_changed(key, last_updated, fetch_method):
    data = redis_conn.get(key)
    if data:
        data = json.loads(data)
        if last_updated == data['updated_at']:
            return data['data']
        # else its out of date
    # It hasn't been cached
    new_data = fetch_method()

    redis_conn.set(key, json.dumps({"updated_at": last_updated, "data": new_data}))
    return new_data
