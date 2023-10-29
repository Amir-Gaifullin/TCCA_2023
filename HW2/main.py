import hashlib
import json
import rsa
import psycopg2
import os
import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import binascii
import requests
from dotenv import load_dotenv

# Функция для подсчета хеша блока
def calculate_hash(block_data):
    sha = hashlib.sha256()
    sha.update(block_data.encode('utf-8'))
    return sha

# Функция для подписи данных и хеша блока
def sign_data(block_hash):
    json = requests.get('http://itislabs.ru/ts?digest=' + block_hash.hexdigest()).json()
    sign = bytes.fromhex(json['timeStampToken']['signature'])
    ts = (json['timeStampToken']['ts'])    
    return sign, ts

# Функция для добавления нового блока в блокчейн
def add_block(data):
    # Получение предыдущего блока
    previous_block = get_previous_block()
    previous_hash = previous_block[5] if previous_block else None

    # Формирование данных для нового блока
    block_data = json.dumps(data)
    block_hash = calculate_hash(block_data)
    sign, ts = sign_data(block_hash)

    # make key object from bytes

    token = ts.encode('utf-8') + binascii.unhexlify(block_hash.hexdigest())
    hasher = SHA256.new()
    
    # msg -> hash
    hasher.update(token) #bytearray(msg, 'utf-8'))


    add_employee = ("INSERT INTO blocks "
               "(signature, timestamp, data, previous_hash, hash) "
               "VALUES (%s, %s, %s, %s, %s)")

    data_employee = (sign, ts, block_data, previous_hash, block_hash.hexdigest())

    # Вставка нового блока в базу данных
    cursor.execute(add_employee, data_employee)
    conn.commit()

    print("Блок добавлен успешно!")

# Функция для получения предыдущего блока
def get_previous_block():
    cursor.execute('SELECT * FROM blocks ORDER BY id DESC LIMIT 1')
    return cursor.fetchone()

# Функция для проверки подлинности данных и хеша блока
def verify_data(block_hash, sign):
    signer = pkcs1_15.new(key)

    try:
        signer.verify(sign, block_hash)
    except:
        return True

load_dotenv()

public_key = "30819f300d06092a864886f70d010101050003818d0030818902818100a811365d2f3642952751029edf87c8fa2aeb6e0feafcf800190a7dd2cf750c63262f6abd8ef52b251c0e10291d5e2f7e6682de1aae1d64d4f9b242050f898744ca300a44c4d8fc8af0e7a1c7fd9b606d7bde304b29bec01fbef554df6ba1b7b1ec355e1ff68bd37f3d40fb27d1aa233fe3dd6b63f7241e734739851ce8c590f70203010001";
pkey_hex = binascii.unhexlify(public_key)
key = RSA.import_key(pkey_hex)


try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect(dbname='blockhain', user='postgres', password=os.environ["DATABASE_PASSWORD"], host="/tmp")
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Can`t establish connection to database')

cursor = conn.cursor()

# Пример использования

# # Добавление блоков в блокчейн
# add_block({'user': 'Alice', 'amount': 1})
# add_block({'user': 'Bob', 'amount': 2})
# add_block({'user': 'Charlie', 'amount': 3})

# Вывод информации о блоках
cursor.execute('SELECT * FROM blocks')
blocks = cursor.fetchall()
for block in blocks:
    print(f'Блок {block[0]}: {block[1]}')

# Проверка достоверности информации в выбранном блоке
selected_block = blocks[1]
selected_hash = selected_block[5]
selected_signature = selected_block[4]
print(f'Достоверность информации в блоке {selected_block[0]}:',
      verify_data(selected_hash, selected_signature))
# Закрытие соединения с базой данных
conn.close()

