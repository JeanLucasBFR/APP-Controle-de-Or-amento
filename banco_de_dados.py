import psycopg2
from dotenv import load_dotenv
import os


#Carregar as variáveis do arquivo .env
load_dotenv()


#Obter as variáveis
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")


conexao = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)


with conexao:
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE Categoria(id SERIAL, nome TEXT)")
    conexao.commit()

#tabela receitas
with conexao:
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE Receitas(id SERIAL, categoria TEXT, adicionando_em DATE, valor DECIMAL)")
    conexao.commit()

#Tabela gastos
with conexao:
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE Gastos(id SERIAL, categoria TEXT, retirado_em DATE, valor DECIMAL)")
    conexao.commit()
