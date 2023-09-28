import string
import random
import base64
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from NavyTrials import settings
DATA_KEY = "TRIALS-ADMIN-API"
DATA_IV= "TRIALS-INITIAL-V"
SECRET_KEY="V1VWTVRFOVhJRk5WUWsxQlVrbE9SUT09LFRrOUNUMFJaSUZkSlRFd2dTMDVQVnc9PQ=="
class AESify:
  def __init__(self, key=DATA_KEY, iv=DATA_IV,secret = SECRET_KEY, block_len=16, salt_len= 8):
    self.key = key
    self.iv = iv
    self.salt_len = salt_len
    self.block_len = block_len
    self.mode = AES.MODE_CBC
    if(secret):
      self.secret = secret
      self.useSecret(secret)
    else:
      self.secret = self.makeSecret(key, iv)
      if(self.secret):
        self.useSecret(self.secret)
    if(self.key is None and self.iv is None):
      raise Exception("No key , IV pair or secret provided")
      
  @staticmethod
  def makeSecret(key, iv):
    if(len(key) % 8 != 0):
      raise Exception("Key length must be a mutliple of 8")
    if(len(iv) % 8 != 0):
      raise Exception("Initial vector must be a multiple of 8")
    key64 = base64.b64encode(key.encode()).decode()
    iv64 = base64.b64encode(iv.encode()).decode()
    secret = iv64 + "," + key64
    secret64 = base64.b64encode(secret.encode()).decode()
    return secret64

  def useSecret(self, secret):
    iv64, key64 = base64.b64decode(secret).decode().split(",") # decode and convert to string
    self.iv = base64.b64decode(iv64)
    self.key = base64.b64decode(key64)
    return self

  def encrypt(self, text):
    text = self.add_salt(text, self.salt_len)
    cipher = AES.new(self.key, self.mode, self.iv)
    text = cipher.encrypt(pad(text.encode('utf-8'), self.block_len))
    return binascii.hexlify(text).decode()
  
  def decrypt(self, data):
    text = binascii.unhexlify(data) # UNHEX and convert the encrypted data to text
    cipher = AES.new(self.key, self.mode, self.iv)
    decData=unpad(cipher.decrypt(text), self.block_len).decode('utf-8')[self.salt_len:] 
    return decData[4:]
  
  def add_salt(self, text, salt_len):
    # pre-pad with random salt
    salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(salt_len))
    text = salt + text
    return text