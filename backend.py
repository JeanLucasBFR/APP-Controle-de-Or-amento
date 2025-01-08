import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd

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


#Funções de inserir

#inserir Categoria
def inserir_categoria(nome):
    with conexao:
        cursor = conexao.cursor()
        query = "INSERT INTO Categoria (nome) VALUES (%s)"
        cursor.execute(query, (nome,))  #Passa o nome como tuplo


#inserir Receitas
def inserir_receitas(nome, adicionando_em,valor):
    with conexao:
        cursor = conexao.cursor()
        query = "INSERT INTO Receitas (categoria, adicionando_em,valor) VALUES (%s,%s,%s)"
        cursor.execute(query, (nome,adicionando_em,valor))  


#Inserir Gastos
def inserir_gastos(nome, retirado_em,valor):
    with conexao:
        cursor = conexao.cursor()
        query = "INSERT INTO Gastos (categoria, retirado_em,valor) VALUES (%s,%s,%s)"
        cursor.execute(query, (nome,retirado_em,valor))  




#Funções de deletar

#Deletar Receitas
def deletar_receitas(id):
    with conexao:
        cursor = conexao.cursor()
        query = "DELETE FROM Receitas WHERE id = (%s)"
        cursor.execute(query, (id))


#Deletar Gastos
def deletar_gastos(id):
    with conexao:
        cursor = conexao.cursor()
        query = "DELETE FROM Gastos WHERE id = (%s)"
        cursor.execute(query, (id))





#Funções para ver os dados

#Ver categoria
def ver_categoria():
    lista_itens = []

    with conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Categoria")
        linha = cursor.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens


#Ver receitas
def ver_receitas():
    lista_itens = []

    with conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Receitas")
        linha = cursor.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens


#Ver Gastos
def ver_gastos():
    lista_itens = []

    with conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Gastos")
        linha = cursor.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens


#Fungão para mexer na tabela
def tabela():
    gastos = ver_gastos()
    receitas = ver_receitas()

    tabela_lista = []
    for i in gastos:
        tabela_lista.append(i)
    
    for i in receitas:
        tabela_lista.append(i)
    
    return tabela_lista


#Função para mexer com o grafico em barras
def barra_valores():
    #Receita Total
    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)

    #Despesas total
    despesas = ver_gastos()
    despesas_lista = []
    for i in despesas:
        despesas_lista.append(i[3])
    despesas_total = sum(despesas_lista)

    #Saldo total
    saldo_total = receita_total - despesas_total
    return[receita_total,despesas_total,saldo_total]


#Funçção para mexer com o grafico pizza
def pizza_valores():
    gastos = ver_gastos()
    tabela_lista = []
    for i in gastos:
        tabela_lista.append(i)
    
    dataframe = pd.DataFrame(tabela_lista, columns = ['id','categoria','data','valor'])
    dataframe = dataframe.groupby('categoria')['valor'].sum()

    lista_quantias = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append(i)
    
    return([lista_categorias, lista_quantias])