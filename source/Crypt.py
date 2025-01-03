from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random


class Crypt:
    def __init__(self, key: bytes):
        self._key = key

    
    def encrypt(self, data: bytes) -> tuple:
        """
        Encrypt the data in AES_GCM

        :param data in bytes
        :return tuple with (nonce, ciphertext, tag)
        """

        nonce = random.randbytes(12)

        cipher = AES.new(self._key, AES.MODE_GCM, nonce=nonce)

        ciphertext, tag = cipher.encrypt_and_digest(pad(data, AES.block_size))

        return (nonce, ciphertext, tag)
    

    def decrypt(self, nonce: bytes, data: bytes, tag: bytes) -> bytes:
        """
        Decrypt the data in AES_CBC

        :param nonce in bytes
               encrypted data in bytes
               tag in bytes
        
        :return decrypted data in bytes
        """

        cipher = AES.new(self._key, AES.MODE_GCM, nonce=nonce)

        try:
            decrypted = unpad(cipher.decrypt_and_verify(data, tag), AES.block_size)
        
        except:
            raise RuntimeError("Error decrypting the data")
        
        return decrypted