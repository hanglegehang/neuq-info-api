# coding:utf-8
# Created by lihang on 2017/3/23.

from Crypto.Cipher import AES
import binascii

class AESCipher(object):

    def __init__(self):
        self.bs = 16
        self.iv = '0123456789123456'
        self.key = '1234567890123456'
    # 加密
    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return binascii.hexlify(cipher.encrypt(raw))
    # 解密
    def decrypt(self, enc):
        enc = binascii.unhexlify(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.decrypt(enc).decode('utf-8').rstrip("\0")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * '\0'


# crypt = AESCipher()
#
# print crypt.encrypt('12345')
# print crypt.decrypt('90b2c15e84cb78e5161f42867807c4bc')