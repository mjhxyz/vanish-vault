DEBUG = True

# 获取递增key的redis key
REDIS_INC_KEY = 'vv_next_id'
REDIS_PREFIX = 'vv_'

# 允许设置的过期时间
VALIDE_TIME_MINUTES = [
    5,
    10,
    30,
    60,
]

# session 过期时间
REMEMBER_COOKIE_DURATION = 3600 * 24 * 3
