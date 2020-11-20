# -*- coding: iso-8859-1 -*-

import sqlite3
from tkinter import *
from datetime import datetime
from tkinter import messagebox as tkMessageBox


data_atual = datetime.today().strftime('%Y-%m-%d')

#Criar conexão e cursor
con = sqlite3.connect('banco_produtos7.db')
cur = con.cursor()

#Criar tabela clientes
cur.execute("""CREATE TABLE IF NOT EXISTS produtos (
            cod_produto VARCHAR PRIMARY KEY,
            nome_produto VARCHAR,
            data_vencimento_produto TEXT)""")

class main:
    def __init__(self,master):
#--------------------------------------TKINTER INTERFACE------------------------------------------------#
        self.frame1 = Frame(master,bg='sky blue')
        self.frame1.configure(relief=GROOVE)
        self.frame1.configure(borderwidth="2")
        self.frame1.place(relx=0.0,rely=0.0,relheight=1.0,relwidth=0.51)
        Label(self.frame1,text='CADASTRO DE PRODUTOS',font=('Ariel','20'),bg='sky blue').place(relx=0.30,rely=0.01)
        Label(self.frame1,text='Código do Produto',font=('Ariel','15'),bg='sky blue').place(relx=0.02,rely=0.12)
        self.cod_produto=Entry(self.frame1,font=('Ariel','20'))
        self.cod_produto.place(relx=0.02,rely=0.16)
        Label(self.frame1,text='Nome do Produto',font=('Ariel','15'),bg='sky blue').place(relx=0.02,rely=0.21)
        self.nome_produto = Entry(self.frame1,font=('Ariel','20'))
        self.nome_produto.place(relx=0.02,rely=0.25,relwidth=0.94)
        Label(self.frame1,text='Data de Vencimento',font=('Ariel','15'),bg='sky blue').place(relx=0.02,rely=0.31)
        self.data_vencimento_produto = Entry(self.frame1,font=('Ariel','20'))
        self.data_vencimento_produto.place(relx=0.02,rely=0.36,width=200)

        self.botaocadastra = Button(self.frame1,text='Cadastrar',font=('Ariel','20'),
                                    fg='green',command=self.cadastraproduto)
        self.botaocadastra.place(relx=0.62,rely=0.33,relwidth=0.31)
        self.botaocancela = Button(self.frame1,text='Novo/Cancelar',font=('Ariel','20'),
                                   fg='red',command=self.limpaproduto)
        self.botaocancela.place(relx=0.62,rely=0.44,relwidth=0.31)


        self.frame2 = Frame(master,bg='sky blue')
        self.frame2.configure(relief=GROOVE)
        self.frame2.configure(borderwidth="2")
        self.frame2.place(relx=0.51,rely=0.0,relheight=0.31,relwidth=0.49)
        Label(self.frame2,text='CONSULTAR',font=('Ariel','20'),bg='sky blue').place(relx=0.35,rely=0.05)
        self.botaook = Button(self.frame2, text='TODOS PRODUTOS',font=('Ariel','15'),
                              fg='green',command=self.mostraprodutos)
        self.botaook.place(relx=0.00,rely=0.65)
        self.botaovencidos = Button(self.frame2, text='PRODUTOS VENCIDOS',font=('Ariel','15'),
                              fg='green',command=self.mostraprodutosvencidos)
        self.botaovencidos.place(relx=0.62,rely=0.65)


        self.frame3 = Frame(master)
        self.frame3.configure(relief=GROOVE)
        self.frame3.configure(borderwidth="2")
        self.frame3.place(relx=0.51,rely=0.31,relheight=0.69,relwidth=0.49)
        self.mostra1 = Text(self.frame3,bg='azure',font=('Courier','20','bold'),fg='blue')
        self.mostra1.place(relx=0.00,rely=0.0,relheight=1.0,relwidth=1.0)


#-----------------------------------------FUNÇÕES-----------------------------------------------------------#
    def cadastraproduto(self):
        cod_produto=self.cod_produto.get()
        nome_produto=self.nome_produto.get()
        data_vencimento_produto=self.data_vencimento_produto.get().split("/")[2]+'-'+self.data_vencimento_produto.get().split("/")[1]+'-'+self.data_vencimento_produto.get().split("/")[0]
        try:
            cur.execute("INSERT INTO produtos VALUES(?,?,?)",
                    (cod_produto,nome_produto,data_vencimento_produto))
            tkMessageBox.showinfo('Aviso!', 'Produto cadastrado com sucesso!')
        except:
            tkMessageBox.showinfo('Aviso!','Produto já cadastrado')
        con.commit()
        self.cod_produto.delete(0,END)
        self.nome_produto.delete(0, END)
        self.data_vencimento_produto.delete(0, END)


    def limpaproduto(self):
        self.cod_produto.delete(0,END)
        self.nome_produto.delete(0,END)
        self.data_vencimento_produto.delete(0,END)


    def mostraprodutos(self):
        self.mostra1.delete(0.0,END)
        cur.execute("SELECT * FROM produtos")
        consulta = cur.fetchall()
        for i in consulta:
            produtos = i[2].split("-")[2] + '/' + i[2].split("-")[1] + '/' + i[2].split("-")[0]
            self.mostra1.insert(END,'''CODIGO DO PRODUTO:{}
PRODUTO:{}
DATA DE VENCIMENTO:{} \n \n'''.format(i[0],i[1],produtos))

    def mostraprodutosvencidos(self):
        self.mostra1.delete(0.0, END)
        cur.execute("SELECT * FROM produtos WHERE data_vencimento_produto <= '%s'" % data_atual)
        consulta = cur.fetchall()
        for i in consulta:
            venc_prod = i[2].split("-")[2]+'/'+i[2].split("-")[1]+'/'+i[2].split("-")[0]
            self.mostra1.insert(END, '''CODIGO DO PRODUTO:{}
PRODUTO:{}
DATA DE VENCIMENTO:{} \n \n'''.format(i[0], i[1], venc_prod ))


root = Tk()
root.title("Cadastro e Consulta de Validade de Produtos")
root.geometry("1366x768")
main(root)
root.mainloop()