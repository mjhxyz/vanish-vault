import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os
import hashlib

mode = AES.MODE_CBC


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
CHARS = "aTJ7s2hC98GifUoZDNd6LzBQmEv0MlkXKb5y4OjWxYRtPnwrVpqF1Igu3eAS0"


def to_base62(num):
    """10进制转62进制"""
    if num == 0:
        return CHARS[0]
    result = []
    while num > 0:
        num, rem = divmod(num, BASE)
        result.append(CHARS[rem])
    return "".join(result[::-1])
