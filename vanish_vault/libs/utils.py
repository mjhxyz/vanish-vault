import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os
import hashlib
from datetime import datetime, timedelta

from vanish_vault.libs.redis_utils import rclient
from vanish_vault.models.message import Message
from vanish_vault.models.base import db

mode = AES.MODE_CBC


# 转换为剩余时间字符串
def to_remaining_time(expire_at):
    remaining_time = expire_at - datetime.now()
    if remaining_time < timedelta(seconds=0):
        return '已过期'
    if remaining_time.days > 0:
        return f'{remaining_time.days}天{remaining_time.seconds // 3600}小时{remaining_time.seconds // 60 % 60}分钟'
    if remaining_time.seconds > 3600:
        return f'{remaining_time.seconds // 3600}小时{remaining_time.seconds // 60 % 60}分钟'
    if remaining_time.seconds > 60:
        return f'{remaining_time.seconds // 60}分钟'
    return f'{remaining_time.seconds}秒'


def encrypt(plaintext, key):
    key = hashlib.md5(key.encode('utf-8')).hexdigest().encode('utf-8')
    iv = os.urandom(16)
    cipher = AES.new(key, mode, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode('utf-8')


def decrypt(ciphertext, key):
    key = hashlib.md5(key.encode('utf-8')).hexdigest().encode('utf-8')
    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:16]
    cipher = AES.new(key, mode, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)
    return plaintext.decode('utf-8')


BASE = 62
# 打乱的 62 个字符
CHARS = "LWVqiarAS7bnHv2olf9d1Jeh6QYNmPRyksz3KBGU4xcEp0jItCXOgTuZwF5D8M"
# CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def random_str(n):
    import random
    return ''.join([random.choice(CHARS) for i in range(n)])


def to_base62(num):
    """10进制转62进制"""
    if num == 0:
        return CHARS[0]
    result = []
    while num > 0:
        num, rem = divmod(num, BASE)
        result.append(CHARS[rem])
    return "".join(result[::-1])


def is_id_exist(id):
    from vanish_vault.libs.redis_utils import rclient
    app = rclient.app
    prefix = app.config.setdefault('REDIS_PREFIX', 'vv_')
    client = rclient.get_redis()
    return client.exists(f'{prefix}{id}')


def is_key_exist(key):
    record = Message.query.filter_by(key=key, status=1).first()
    if record and record.expire_at < datetime.now():
        record.delete()
        db.session.commit()
        return False
    return record is not None


def delete_content2(id):
    record = Message.query.filter_by(id=id).first()
    if record is None:
        return None
    db.session.delete(record)
    db.session.commit()
    return True


def delete_content(id):
    from vanish_vault.libs.redis_utils import rclient
    app = rclient.app
    prefix = app.config.setdefault('REDIS_PREFIX', 'vv_')
    client = rclient.get_redis()
    return client.delete(f'{prefix}{id}')


def get_decrypted_content2(id, key):
    record = Message.query.filter_by(key=id).first()
    if record is None:
        return None
    if record.expire_at < datetime.now():
        record.delete()
        db.session.commit()
        return None
    try:
        return decrypt(record.content, key)
    except Exception:
        return None


def get_decrypted_content(id, key):
    from vanish_vault.libs.redis_utils import rclient
    app = rclient.app
    prefix = app.config.setdefault('REDIS_PREFIX', 'vv_')
    client = rclient.get_redis()
    encrypted_content = client.get(f'{prefix}{id}')
    if not encrypted_content:
        return None
    try:
        return decrypt(encrypted_content, key)
    except Exception:
        return None


def get_next_id():
    from vanish_vault.libs.redis_utils import rclient
    redis_next_id = to_base62(rclient.get_next_id())
    return f'{redis_next_id}{random_str(2)}'


def save_content(content, key, expire=10 * 60):
    app = rclient.app
    encrypted_content = encrypt(content, key)
    prefix = app.config.setdefault('REDIS_PREFIX', 'vv_')
    next_id = get_next_id()
    client = rclient.get_redis()
    client.setex(f'{prefix}{next_id}', expire, encrypted_content)
    return next_id


def save_content_using_mysql(content, key, user_id, expire=10 * 60):
    encrypted_content = encrypt(content, key)
    next_id = get_next_id()
    message = Message(key=next_id, content=encrypted_content, expire_at=datetime.now(
    ) + timedelta(seconds=expire), title='消息x', user_id=user_id)
    db.session.add(message)
    db.session.commit()
    return next_id
