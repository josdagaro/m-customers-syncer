from flask import Flask, request, jsonify
import mysql.connector
import os
import json

app = Flask(__name__)

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

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)

# Simulación de un servicio de autenticación
def get_role_from_token(token):
    # Este es un ejemplo simple, en la realidad deberías verificar el token y obtener el rol de un servicio de autenticación
    token_role_map = {
        'admin-token': 'admin',
        'viewer-token': 'viewer',
        'analyst-token': 'analyst'
    }
    return token_role_map.get(token, None)

@app.route('/clientes', methods=['GET'])
def get_clientes():
    token = request.headers.get('Authorization')
    role = get_role_from_token(token)

    if not role:
        return jsonify({"error": "Unauthorized access"}), 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if role == 'admin':
        cursor.execute('SELECT * FROM usuarios')
    elif role == 'viewer':
        cursor.execute('SELECT id, user_name, direccion, avatar FROM usuarios')
    elif role == 'analyst':
        cursor.execute('SELECT id, user_name, direccion, avatar, credit_card_num FROM usuarios')
    else:
        cursor.close()
        conn.close()
        return jsonify({"error": "Unauthorized access"}), 403

    clientes = cursor.fetchall()

    if role == 'analyst':
        for cliente in clientes:
            cliente['credit_card_num'] = cliente['credit_card_num'][-4:].rjust(len(cliente['credit_card_num']), '*')

    cursor.close()
    conn.close()
    return jsonify(clientes)


@app.route('/health', methods=['GET'])
def health_check():
    return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
