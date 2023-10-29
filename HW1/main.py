import hashlib
import json
import rsa
import psycopg2
import os
from dotenv import load_dotenv

# Функция для подсчета хеша блока
def calculate_hash(block_data):
    sha = hashlib.sha256()
    sha.update(block_data.encode('utf-8'))
    return sha.hexdigest()

# Функция для подписи данных и хеша блока
<<<<<<< HEAD
<<<<<<< HEAD
def sign_data(block_hash):
    signature = rsa.sign(block_hash.encode(), private_key, 'SHA-256')
=======
def sign_data(data, block_hash):
    # Здесь можно реализовать выбор и использование конкретной схемы подписи (например, RSA)
    # В данном примере для простоты будем использовать только текстовую подпись
    signature_data = f'{data}{block_hash}'
    signature = rsa.sign(signature_data.encode(), private_key, 'SHA-256')
>>>>>>> 5f957f7 (HW1)
=======
def sign_data(block_hash):
    signature = rsa.sign(block_hash.encode(), private_key, 'SHA-256')
>>>>>>> 23bf133 (fix)
    
    return signature

# Функция для добавления нового блока в блокчейн
def add_block(data):
    # Получение предыдущего блока
    previous_block = get_previous_block()
    previous_hash = previous_block[2] if previous_block else None

    # Формирование данных для нового блока
    block_data = json.dumps(data)
    block_hash = calculate_hash(block_data)
<<<<<<< HEAD
<<<<<<< HEAD
    signature = sign_data(block_hash).hex()
=======
    signature = sign_data(block_data, block_hash).hex()
>>>>>>> 5f957f7 (HW1)
=======
    signature = sign_data(block_hash).hex()
>>>>>>> 23bf133 (fix)

    add_employee = ("INSERT INTO blocks "
               "(data, hash, signature, previous_hash) "
               "VALUES (%s, %s, %s, %s)")

    data_employee = (block_data, block_hash, signature, previous_hash)

    # Вставка нового блока в базу данных
    cursor.execute(add_employee, data_employee)
    conn.commit()

    print("Блок добавлен успешно!")

# Функция для получения предыдущего блока
def get_previous_block():
    cursor.execute('SELECT * FROM blocks ORDER BY id DESC LIMIT 1')
    return cursor.fetchone()

# Функция для проверки подлинности данных и хеша блока
def verify_data(block_hash, signature):
    try:
        return rsa.verify(block_hash.encode(), signature, public_key)
    except:
        return True

# Функция для проверки целостности блокчейна
def verify_blockchain():
    cursor.execute('SELECT * FROM blocks ORDER BY id ASC')
    blocks = cursor.fetchall()

    for i in range(1, len(blocks)):
        previous_block = blocks[i - 1]
        current_block = blocks[i]

        # Проверка подлинности данных и хеша блока
<<<<<<< HEAD
<<<<<<< HEAD
        if not verify_data(previous_block[2], previous_block[3]):
=======
        if not verify_data(previous_block[1], previous_block[2], previous_block[3]):
>>>>>>> 5f957f7 (HW1)
=======
        if not verify_data(previous_block[2], previous_block[3]):
>>>>>>> 23bf133 (fix)
            return False

        # Проверка хеша предыдущего блока
        previous_block_data = json.dumps(previous_block[1])

        if calculate_hash(previous_block_data) != previous_block[2]:
            return False

        # Проверка хеша текущего блока
        current_block_data = json.dumps(current_block[1])

        if calculate_hash(current_block_data) != current_block[2]:
            print(2)
            return False

    return True

load_dotenv()

# Загрузка ключей RSA
with open('private.pem', 'r') as private_file:
    private_key = rsa.PrivateKey.load_pkcs1(private_file.read().encode())
with open('public.pem', 'r') as public_file:
    public_key = rsa.PublicKey.load_pkcs1(public_file.read().encode())


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
<<<<<<< HEAD
<<<<<<< HEAD
selected_hash = selected_block[2]
selected_signature = bytes.fromhex(selected_block[3])
print(f'Достоверность информации в блоке {selected_block[0]}:',
      verify_data(selected_hash, selected_signature))
=======
selected_data = selected_block[1]
selected_hash = selected_block[2]
selected_signature = bytes.fromhex(selected_block[3])
print(f'Достоверность информации в блоке {selected_block[0]}:',
      verify_data(selected_data, selected_hash, selected_signature))
>>>>>>> 5f957f7 (HW1)
=======
selected_hash = selected_block[2]
selected_signature = bytes.fromhex(selected_block[3])
print(f'Достоверность информации в блоке {selected_block[0]}:',
      verify_data(selected_hash, selected_signature))
>>>>>>> 23bf133 (fix)

# Проверка целостности блокчейна
print('Целостность блокчейна:', verify_blockchain())

# Закрытие соединения с базой данных
conn.close()
