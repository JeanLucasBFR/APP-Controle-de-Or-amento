from tkinter import *
from tkinter import ttk  
from PIL import Image, ImageTk  
#barra de progesso
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
#calendario
from tkcalendar import Calendar, DateEntry
from datetime import datetime
#messageBox
from tkinter import messagebox
#importando funções do backend
from backend import * 

#CORES

cPreta = "#2e2d2b"  #Cor preta
cBranca = "#feffff"  #Cor branca
cVerde = "#4fa882"  #Cor verde
cAzul = "#038cfc"  #Cor azul
cVermelho = "#ff0000"  #Cor vermelha
cRoxo = "#9b4d96"  #Cor roxa
cLaranja = "#e06636"  #Cor laranja
cAzulEscuro = "#38576b"  #Cor azul escuro


colors = [cVerde, cAzul, cVermelho, cRoxo, cLaranja, cAzulEscuro]

#Ciração da janela
janela = Tk()
janela.title("Controle de Orçamento")
janela.geometry("980x670")
janela.config(background=cBranca)

style = ttk.Style(janela)
style.theme_use("clam")


#Criando Frames para divisão da tela
FrameCima = Frame(janela, width=1000, height=50, bg=cBranca, relief="flat")
FrameCima.grid(row=0, column = 0)

FrameMeio = Frame(janela, width=1000, height=350, bg=cBranca,pady=20, relief="raised")
FrameMeio.grid(row=1, column = 0, pady=1)

FrameBaixo = Frame(janela, width=1200, height=300, bg=cBranca,pady=20, relief="flat")
FrameBaixo.grid(row=2, column = 0, pady=1)



#Trabalhando no Frame Cima

#Imagem
app_image = Image.open('img_logo.webp')
app_image = app_image.resize((40,40))
app_image = ImageTk.PhotoImage(app_image)

app_logo = Label(FrameCima, image=app_image, text="  Orçamento de Viagem", width=1000, compound=LEFT, relief=RAISED, anchor=NW,  padx=5, pady=5, font=("Verdana 20 bold"))
app_logo.place(x=0,y=0)




#Espaço para fazer as funções futuramente


#Convertendo data para aceitar no postgre
def formatar_data_global(data_str):
    try:
        #converter a data para o formato datetime
        data_formatada = datetime.strptime(data_str, "%m/%d/%y")
        #Retorna a data no formato ISO
        return data_formatada.strftime("%Y-%m-%d")
    except ValueError:
        return None  #Retorna None se a data for inválida
    
#Definindo tree como global
global tree

#Função inserir categorias
def inserir_categoria_main():
    nome_categoria = e_add_categorias.get()
    lista_inserir_main = [nome_categoria]
    for i in lista_inserir_main:
        if i == "":
            messagebox.showerror("Erro", "Preencha todos os campos")
            return 
        
    #passanddo a lista para a função inserir gastos do backend    
    inserir_categoria(nome_categoria)
    messagebox.showinfo("Sucesso", f"A categoria '{nome_categoria}' foi inserida com sucesso")

    #deletando o valor que ta na entry
    e_add_categorias.delete(0,'end')

    #Pegando os valores da categoria para atualizar
    categorias_funcao_main = ver_categoria()
    categoria = []

    for i in categorias_funcao_main:
        categoria.append(i[1])
    
    #Atualizando a combobox de categorias
    combo_categoria_despesa['values'] = tuple(categoria)


#Função para inserir nova receita
def inserir_receitas_main():
    nome_receitas = 'Receita'
    data_receitas = e_calendario_receitas.get()
    quantia_receitas = e_valor_receitas.get()

    lista_inserir_main = [nome_receitas,data_receitas,quantia_receitas]

    for i in lista_inserir_main:
        if i == "":
            messagebox.showerror("Erro", "Preencha todos os campos com valor válido")
            return

    try:
        quantia_receitas = float(quantia_receitas)  
        if quantia_receitas < 0: 
            messagebox.showerror("Erro", "O valor da receita não pode ser negativo")
            return
    except ValueError: 
        messagebox.showerror("Erro", "O valor da receita deve ser um número válido")
        return
    
    data_receitas = formatar_data_global(data_receitas)
    #chamando a funçaõ inserir receitas do backend
    inserir_receitas(nome_receitas,data_receitas,quantia_receitas)
    messagebox.showinfo("Sucesso","Os dados foram inseridos com sucesso")

    #limpando os dados
    e_calendario_receitas.delete(0,'end')
    e_valor_receitas.delete(0,'end')

    #Atualizando dados
    mostrar_renda()
    grafico_barra()
    resumo()
    grafico_pizza()


#Função para inserir nova despesa
def inserir_despesas_main():
    nome_despesas = combo_categoria_despesa.get()
    data_despesas = e_calendario_despesas.get()
    quantia_despesas = e_valor_despesas.get()

    lista_inserir_main = [nome_despesas,data_despesas,quantia_despesas]

    for i in lista_inserir_main:
        if i == "":
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
    try:
        quantia_despesas = float(quantia_despesas)  
        if quantia_despesas < 0: 
            messagebox.showerror("Erro", "O valor da despesa não pode ser negativo")
            return
    except ValueError: 
        messagebox.showerror("Erro", "O valor da despesa deve ser um número válido")
        return
    
    data_despesas = formatar_data_global(data_despesas)
    #chamando a funçaõ inserir despesas do backend
    inserir_gastos(nome_despesas,data_despesas,quantia_despesas)
    messagebox.showinfo("Sucesso","Os dados foram inseridos com sucesso")

    #limpando os dados
    combo_categoria_despesa.delete(0,'end')
    e_calendario_despesas.delete(0,'end')
    e_valor_despesas.delete(0,'end')

    #Atualizando dados
    mostrar_renda()
    grafico_barra()
    resumo()
    grafico_pizza()


#Função para deletar uma tabela
def deletar_main():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        nome = treev_lista[1]

        if nome=="Receita":
            deletar_receitas([valor])
            messagebox.showinfo("Sucesso", "Os dados foram deletados com sucesso")

            #Atualizando dados
            mostrar_renda()
            grafico_barra()
            resumo()
            grafico_pizza()

        else:
            deletar_gastos([valor])
            messagebox.showinfo("Sucesso", "Os dados foram deletados com sucesso")

            #Atualizando dados
            mostrar_renda()
            grafico_barra()
            resumo()
            grafico_pizza()

    except IndexError:
        messagebox.showerror("Erro", "Seleciona uma linha da tabela para exclusão")


#Função para o gráfico de barras
def grafico_barra():
    lista_categorias = ["Renda", "Despesas", "Saldo"]
    lista_valores = barra_valores()

    #Definindo cores específicas para cada barra
    cores_barras = ["#4fa882", "#ff0000", "#038cfc"]  #Verde para Renda, Vermelho para Despesas, Azul para Saldo

    #Criação da figura e atribuição dos objetos de eixo
    figura = plt.Figure(figsize=(4.9, 3.75), dpi=65)
    ax = figura.add_subplot(111)
    ax.autoscale(enable=True, axis='both', tight=None)
    bars = ax.bar(lista_categorias, lista_valores, color=cores_barras, width=1.0)

    #Definindo os ticks no eixo X
    ax.set_xticks(range(len(lista_categorias)))  

    c = 0
    for i in ax.patches:
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic', verticalalignment='bottom', color='dimgrey')
        c += 1

    #Configuração dos rótulos dos ticks
    ax.set_xticklabels(lista_categorias, fontsize=16)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    #Desativa a grid
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, FrameMeio)
    canva.get_tk_widget().place(x=15, y=15)


#Função de resumo total
def resumo():
    valor = barra_valores()

    l_linha = Label(FrameMeio, text="", width=240, anchor=NW, font=("Arial 1"), bg="#545454")
    l_linha.place(x=350, y=55)
    l_sumario = Label(FrameMeio, text="TOTAL RENDA MENSAL       ", anchor=NW, font=("Verdana 12 bold"), bg=cBranca, fg="#4fa882")
    l_sumario.place(x=350, y=32)
    l_sumario = Label(FrameMeio, text="R$ {:,.2f}".format(valor[0]), anchor=NW, font=("Arial 16"), bg=cVerde)
    l_sumario.place(x=350, y=70)


    l_linha = Label(FrameMeio, text="", width=240, anchor=NW, font=("Arial 1"), bg="#545454")
    l_linha.place(x=350, y=135)
    l_sumario = Label(FrameMeio, text="TOTAL DESPESAS MENSAIS       ", anchor=NW, font=("Verdana 12 bold"), bg=cBranca, fg=cVermelho)
    l_sumario.place(x=350, y=112)
    l_sumario = Label(FrameMeio, text="R$ {:,.2f}".format(valor[1]), anchor=NW, font=("Arial 16"), bg=cVermelho)
    l_sumario.place(x=350, y=150)


    l_linha = Label(FrameMeio, text="", width=240, anchor=NW, font=("Arial 1"), bg="#545454")
    l_linha.place(x=350, y=220)
    l_sumario = Label(FrameMeio, text="SALDO RESTANTE       ", anchor=NW, font=("Verdana 12 bold"), bg=cBranca, fg="#038cfc")
    l_sumario.place(x=350, y=192)
    l_sumario = Label(FrameMeio, text="R$ {:,.2f}".format(valor[2]), anchor=NW, font=("Arial 16"), bg=cAzul)
    l_sumario.place(x=350, y=233)


#Frame para a pizza
frame_gra_pizza = Frame(FrameMeio, width=640, height=300, bg=cBranca)
frame_gra_pizza.place(x=490, y=10)


#funcao grafico pizza
def grafico_pizza():
   
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pizza_valores()[1]
    lista_categorias = pizza_valores()[0]

    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.60, 0.8))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pizza)
    canva_categoria.get_tk_widget().grid(row=0, column=0)


#Criando frames dentro do frame baixo
Frame_renda = Frame(FrameBaixo, width=350, height=250, bg=cBranca, relief="flat")
Frame_renda.grid(row=0, column = 0)

Frame_operacoes = Frame(FrameBaixo, width=260, height=250, bg=cBranca, relief="flat")
Frame_operacoes.grid(row=0, column = 1, padx=40)

Frame_configuracao = Frame(FrameBaixo, width=260, height=250, bg=cBranca, relief="flat")
Frame_configuracao.grid(row=0, column = 2, padx = 5)


#Titulo do label da tabela mensal
app_tabela = Label(FrameMeio,text="Tabela de Receitas e Despesas",anchor=NW,  padx=5, pady=5, font=("Verdana 12 bold"), bg=cBranca)
app_tabela.place(x=40,y=305)


#funcao para mostrar_renda
def mostrar_renda():
    tabela_head = ['#Id','Categoria','Data','Quantia']
    lista_itens = tabela()
    global tree
    tree = ttk.Treeview(Frame_renda, selectmode="extended",columns=tabela_head, show="headings")
    #barra vertical
    vsb = ttk.Scrollbar(Frame_renda, orient="vertical", command=tree.yview)
    #barra horizontal
    hsb = ttk.Scrollbar(Frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)


#Configurações das despesas
l_info = Label(Frame_operacoes, text="Insira novas despesas", anchor=NW, font=("Verdana 10 bold"), bg=cBranca, fg=cPreta)
l_info.place(x=10,y=10)


#categoria
l_categoria= Label(Frame_operacoes, text="Categoria", anchor=NW, font=("Ivy 10"), bg=cBranca, fg=cPreta)
l_categoria.place(x=10,y=40)
#combobox da categoria de despesa
categoria_funcao = ver_categoria()
categoria = []
for i in categoria_funcao:
    categoria.append(i[1])

combo_categoria_despesa = ttk.Combobox(Frame_operacoes, width=10, font=("Ivy 10"))
combo_categoria_despesa["values"] = (categoria)
combo_categoria_despesa.place(x=80, y=40)


#data despesas
l_calendario_despesas= Label(Frame_operacoes, text="Data", anchor=NW, font=("Ivy 10"), bg=cBranca, fg=cPreta)
l_calendario_despesas.place(x=10,y=70)
e_calendario_despesas = DateEntry(Frame_operacoes, Width=12, background='darkblue', foreground='white', bordewidth=2, year=2025)
e_calendario_despesas.place(x=80,y=70)


#valor das despesas
l_valor_despesas= Label(Frame_operacoes, text="Valor R$", anchor=NW, font=("Ivy 10"), bg=cBranca, fg=cPreta)
l_valor_despesas.place(x=10,y=100)
e_valor_despesas = Entry(Frame_operacoes, width=14, justify='left', relief='solid')
e_valor_despesas.place(x=80,y=101)
#Botão inserir despesass
botao_inserir_despesas = Button(Frame_operacoes, text="  + ADICIONAR", width=12, compound=LEFT, anchor=NW, font=("Ivy 9 bold"), overrelief=RIDGE, fg=cVerde, command=inserir_despesas_main)
botao_inserir_despesas.place(x=78,y=130)


#botao excluir 
l_excluir= Label(Frame_operacoes, text="Excluir ação", anchor=NW, font=("Ivy 10 bold"), bg=cBranca, fg=cPreta)
l_excluir.place(x=10,y=200)
botao_excluir = Button(Frame_operacoes, text="    DELETAR", width=12, compound=LEFT, anchor=NW, font=("Ivy 9 bold"), overrelief=RIDGE, fg=cVermelho, command=deletar_main)
botao_excluir.place(x=95,y=198)



#Configurações das receitas
l_info = Label(Frame_configuracao, text="Insira novas receitas", anchor=NW, font=("Verdana 10 bold"), bg=cBranca, fg=cPreta)
l_info.place(x=10,y=10)

#data receeita
l_calendario_receitas= Label(Frame_configuracao, text="Data", anchor=NW, font=("Ivy 10"), bg=cBranca, fg=cPreta)
l_calendario_receitas.place(x=10,y=40)
e_calendario_receitas = DateEntry(Frame_configuracao, Width=12, background='darkblue', foreground='white', bordewidth=2, year=2025)
e_calendario_receitas.place(x=80,y=40)

#valor das receitas
l_valor_receitas= Label(Frame_configuracao, text="Valor R$", anchor=NW, font=("Ivy 10"), bg=cBranca, fg=cPreta)
l_valor_receitas.place(x=10,y=70)
e_valor_receitas = Entry(Frame_configuracao, width=14, justify='left', relief='solid')
e_valor_receitas.place(x=80,y=71)

#Botão inserir receitas
botao_inserir_receitas = Button(Frame_configuracao, text="  + ADICIONAR", width=12, compound=LEFT, anchor=NW, font=("Ivy 9 bold"), overrelief=RIDGE, fg=cVerde, command=inserir_receitas_main)
botao_inserir_receitas.place(x=78,y=101)



#Operação add categoria
l_add_categorias= Label(Frame_configuracao, text="Categoria", anchor=NW, font=("Ivy 10"), bg=cBranca, fg=cPreta)
l_add_categorias.place(x=10,y=180)
e_add_categorias = Entry(Frame_configuracao, width=14, justify='left', relief='solid')
e_add_categorias.place(x=80,y=181)
#Botao add categoria
botao_inserir_categoias = Button(Frame_configuracao, text="Add Categoria", width=12, compound=LEFT, anchor=NW, font=("Ivy 9 bold"), overrelief=RIDGE, fg=cAzulEscuro, command=inserir_categoria_main)
botao_inserir_categoias.place(x=77,y=208)



#chamando as funções
grafico_barra()
resumo()
grafico_pizza()
mostrar_renda()


#Para a janela abrir
janela.mainloop()