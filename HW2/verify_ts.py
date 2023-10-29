#pip install pycryptodome #(pip install pycryptodomex - Windows)
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import binascii
import requests

publicKeyStr = "30819f300d06092a864886f70d010101050003818d0030818902818100a811365d2f3642952751029edf87c8fa2aeb6e0feafcf800190a7dd2cf750c63262f6abd8ef52b251c0e10291d5e2f7e6682de1aae1d64d4f9b242050f898744ca300a44c4d8fc8af0e7a1c7fd9b606d7bde304b29bec01fbef554df6ba1b7b1ec355e1ff68bd37f3d40fb27d1aa233fe3dd6b63f7241e734739851ce8c590f70203010001";

msg = 'asdjf'.encode('utf-8')
h = SHA256.new(msg)
# sign
print(h.hexdigest())
json = requests.get('http://itislabs.ru/ts?digest=' + h.hexdigest()).json()
print(json)
sign = bytes.fromhex(json['timeStampToken']['signature'])
ts = (json['timeStampToken']['ts'])
print(ts)

# message as string
# convert hex string to bytes
pkey_hex = binascii.unhexlify(publicKeyStr)
# make key object from bytes
key = RSA.import_key(pkey_hex)

token = ts.encode('utf-8') + binascii.unhexlify(h.hexdigest())

# new hasher and signer object for RSAwithSHA256 algorithm
hasher = SHA256.new()
signer = pkcs1_15.new(key)

# msg -> hash
hasher.update( token) #bytearray(msg, 'utf-8'))
# si
# gn hash
try:
    signer.verify(hasher, sign)
    print('подпись действительна')
except ValueError:
    print('подпись недействительна')