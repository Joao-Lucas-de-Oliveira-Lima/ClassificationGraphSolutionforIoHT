import mysql.connector
from mysql.connector import Error
import pandas as pd
from utils import cesarDecriptor

connection = None
connection_db = None
db_name = "db"  # nome do banco definido no docker-compose MYSQL_DATABASE

# Configurações de conexão
host_name = 'localhost'
user_name = 'root'
password = 'secret'  # sua senha decodificada

# Criar conexão com o servidor MySQL (sem banco específico)
def create_server_connection(host_name, user_name, user_password, port=3306):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port=port
        )
        print("Conexão com MySQL Server bem sucedida")
    except Error as err:
        print(f"Erro ao conectar no servidor MySQL: '{err}'")
    return connection

# Criar banco de dados
def create_database(connection, database_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Banco de dados '{database_name}' criado (ou já existia).")
    except Error as err:
        print(f"Erro ao criar banco de dados: '{err}'")

# Dropar banco de dados
def drop_database(connection, database_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")
        print(f"Banco de dados '{database_name}' removido.")
    except Error as err:
        print(f"Erro ao dropar banco de dados: '{err}'")

# Criar conexão com banco específico
def create_db_connection(host_name, user_name, user_password, db_name, port=3306):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=port
        )
        print(f"Conexão com banco '{db_name}' bem sucedida")
    except Error as err:
        print(f"Erro ao conectar no banco '{db_name}': '{err}'")
    return connection

def initServerConnection():
    return create_server_connection(host_name, user_name, password)

def initDBConnection():
    return create_db_connection(host_name, user_name, password, db_name)
