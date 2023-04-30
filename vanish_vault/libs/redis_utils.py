from redis import Redis, ConnectionPool


class RedisClient:
    def __init__(self):
        self.pool = None
        self.app = None
        self.inc_key = None

    def init_app(self, app):
        app.config.setdefault('REDIS', dict(
            host='127.0.0.1',
            port=6379,
            db=0,
        ))
        self.inc_key = app.config.setdefault('REDIS_INC_KEY', 'vv_next_id')
        self.pool = ConnectionPool(**app.config['REDIS'])
        self.app = app

    def get_redis(self):
        # TODO 判断是否已经初始化
        return Redis(connection_pool=self.pool)

    def get_next_id(self):
        return self.get_redis().incr(self.inc_key)


rclient = RedisClient()


def get_redis():
    return rclient.get_redis()
