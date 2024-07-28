import requests
import mysql.connector
import os
from datetime import datetime
from dateutil import parser
from dateutil.parser import ParserError
from cryptography.fernet import Fernet
import json

# Obtener las credenciales de la base de datos desde las variables de entorno o AWS Secrets Manager
def get_db_credentials():
    aws_mode = os.getenv('AWS_MODE', 'disabled')
    if aws_mode == 'enabled':
        secret = os.getenv('DB_SECRET_NAME')
        secret_dict = json.loads(secret)
        db_user = secret_dict['username']
        db_password = secret_dict['password']
    else:
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')

    return db_user, db_password

# Obtener las credenciales de la base de datos
DB_USER, DB_PASSWORD = get_db_credentials()
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# Generar una clave para el cifrado
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Función para cifrar datos sensibles
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

# Función para convertir las fechas al formato MySQL
def convert_datetime_format(date_str):
    try:
        dt = parser.parse(date_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ParserError, ValueError) as e:
        print(f"Error parsing date: {date_str} - {e}")
        return None

# Función para obtener los datos de la API de forma segura
def fetch_data_from_api():
    url = "https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios"
    response = requests.get(url, verify=True)
    response.raise_for_status()
    return response.json()

# Función para almacenar los datos en la base de datos MySQL
def store_data_in_db(data):
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
    cursor = cnx.cursor()
    add_user = (
        "INSERT INTO usuarios "
        "(id, fec_alta, user_name, codigo_zip, credit_card_num, credit_card_ccv, cuenta_numero, direccion, geo_latitud, geo_longitud, color_favorito, foto_dni, ip, auto, auto_modelo, auto_tipo, auto_color, cantidad_compras_realizadas, avatar, fec_birthday) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    for user in data:
        fec_alta = convert_datetime_format(user['fec_alta'])
        fec_birthday = convert_datetime_format(user['fec_birthday'])
        if fec_alta and fec_birthday:
            user_data = (
                user['id'], fec_alta, user['user_name'], user['codigo_zip'], encrypt_data(user['credit_card_num']),
                encrypt_data(user['credit_card_ccv']), encrypt_data(user['cuenta_numero']), user['direccion'],
                user['geo_latitud'], user['geo_longitud'], user['color_favorito'], user['foto_dni'], user['ip'],
                user['auto'], user['auto_modelo'], user['auto_tipo'], user['auto_color'], user['cantidad_compras_realizadas'],
                user['avatar'], fec_birthday
            )
            cursor.execute(add_user, user_data)

    cnx.commit()
    cursor.close()
    cnx.close()


# Crear la tabla en la base de datos si no existe
def create_table_if_not_exists():
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
    cursor = cnx.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT PRIMARY KEY,
        fec_alta DATETIME,
        user_name VARCHAR(255),
        codigo_zip VARCHAR(10),
        credit_card_num VARCHAR(255),
        credit_card_ccv VARCHAR(255),
        cuenta_numero VARCHAR(255),
        direccion VARCHAR(255),
        geo_latitud VARCHAR(20),
        geo_longitud VARCHAR(20),
        color_favorito VARCHAR(50),
        foto_dni VARCHAR(255),
        ip VARCHAR(15),
        auto VARCHAR(50),
        auto_modelo VARCHAR(50),
        auto_tipo VARCHAR(50),
        auto_color VARCHAR(50),
        cantidad_compras_realizadas INT,
        avatar VARCHAR(255),
        fec_birthday DATETIME
    )
    """
    cursor.execute(create_table_query)
    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    create_table_if_not_exists()
    data = fetch_data_from_api()
    store_data_in_db(data)
    print("Application executed successfully")
