import pandas as pd
import PySimpleGUI as sg
import os
import csv
cwd = os.getcwd()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PERSISTENCIA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def grava_dados(viagens):
    arquivo = open('viagens.csv', 'a+')
    codigo = viagens['codigo']
    municipio = viagens['municipio']
    estado = viagens['estado']
    atividades = viagens['atividades']
    arquivo.write(codigo + ", " + municipio + ", " + estado + ", " + atividades + "\n")
    print('GRAVOU O ARQUIVO')
    arquivo.close()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TELA INICIAL ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def tela_inicial():
    sg.theme('DarkTeal3')
    layout = [
              [sg.Text("Cadastro de viagens", font="Arial 16 bold", pad=(25, 30))],
              [sg.Button("Cadastro", key="cadastro", size=(40, 2))],
              [sg.Button("Consulta", key="consulta", size=(40, 2))]
             ]

    janela = sg.Window("Tela inicial", layout, text_justification="center") # Cria uma janela com o PySimpleGUI
    botao, valores = janela.read()
    janela.close()
    return botao

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CADASTRO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cadastra():
    sg.theme('DarkTeal3')
    layout = [
              [sg.Text("Cadastre sua viagem!", font=("Arial 16 bold"), pad=(20, 30))],
              [sg.Text("Código", size=(10, 1)), sg.Input(key="codigo", size=(40, 1))],
              [sg.Text("Município", size=(10,1)), sg.Input(key="municipio", size =(40, 1))],
              [sg.Text("Estado", size=(10,1)), sg.Input(key="estado", size =(40, 1))],
              [sg.Text("Atividades", size=(10,1)), sg.Input(key="atividades", size =(40, 1))],
              [sg.Button("Cadastrar", key = "cadastrar", size=(23, 2)), sg.Button("Voltar", key = "voltar", size=(24,2))]
              ]

    janela = sg.Window("Cadastro", layout)
    botao, valores = janela.read()
    janela.close()
    if botao == 'cadastrar':
        grava_dados(valores)
        sg.popup("Viagem salva com sucesso!")
    elif botao == 'voltar':
        tela_inicial()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TABELA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def listar():
    with open('viagens.csv', 'r') as arquivo_referencia:
        # ler a tabela
        tabela = csv.reader(arquivo_referencia, delimiter=',')
        matriz = []
        #navegar pela tabela
        for l in tabela:
            print(l)
            codigo = l[0]
            municipio = l[1]
            estado = l[2]
            ativ = l[3]
            matriz.append([codigo, municipio, estado, ativ])
            
        return matriz


def lista_viagens():
    dados = listar()
    headings = ['Código', 'Município', 'Estado', 'Atividades']
    sg.theme('DarkTeal3')
    layout = [
        [sg.Text("Lista de viagens", font=("Arial 16 bold"), pad=(5, 10))],
        [sg.Table(values=dados, headings=headings, num_rows=10)],
        [sg.Button("Voltar", key="voltar", size=(11, 1)), sg.Button("Excluir", key="excluir", size=(11,1)), sg.Button("Alterar", key="alterar", size=(11,1))]
            ]
    janela = sg.Window("Lista de viagens", layout)
    botao, valores = janela.read()
    janela.close()
    if botao == 'voltar':
        tela_inicial()
    elif botao == 'excluir':
        excluir()
    elif botao == 'alterar':
        seleciona_viagem()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ALTERAR VIAGEM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def seleciona_viagem():

    layout = [
        [sg.Text("Lista de viagens", font=("Arial 16 bold"), pad=(5, 10))],
        [sg.Text("Código", size=(10, 1)), sg.Input(key="codigo", size=(40, 1))],
        [sg.Button("Voltar", key="voltar", size=(11, 1)), sg.Button("Ok", key="ok", size=(11, 1))]
        ]
    janela = sg.Window("Encontre sua viagem", layout)
    botao, valores = janela.read()
    janela.close()
    if botao == 'ok':
        alterar_viagem(valores["codigo"])
    if botao == 'voltar':
        lista_viagens()

def alterar_viagem(codigo):
    with open('viagens.csv', 'r') as arquivo_referencia:
        tabela = csv.reader(arquivo_referencia, delimiter=',')
        for l in tabela:
            if l[0] == codigo:
                codigo = l[0]
                municipio = l[1]
                estado = l[2]
                ativ = l[3]



    layout = [
        [sg.Text("Codigo:", size=(18, 1)), sg.Text(codigo, size=(28, 1))],
        # O código não pode ser modificado, sendo um Texto e não uma Entrada (Input)
        [sg.Text("Municipio:", size=(18, 1)), sg.Input(default_text=municipio, key="municipio", size=(28, 1))],
        [sg.Text("Estado:", size=(18, 1)), sg.Input(default_text=estado, key="estado", size=(28, 1))],
        [sg.Text("Atividade", size=(18, 1)), sg.Input(default_text=ativ, key="atividades", size=(28, 1))],
        [sg.Button("Ok", key="ok", size=(11, 1))]

    ]
    janela = sg.Window("Alterar viagem", layout)
    botao, valores = janela.read()
    janela.close()

    if botao == 'ok':
        municipio = valores["municipio"]
        estado = valores["estado"]
        ativ = valores["atividades"]
        with open('viagens.csv', 'r') as arquivo_referencia:
           tabela = csv.reader(arquivo_referencia, delimiter=',')

           linhas = []
           for l in tabela:
                if l[0] == codigo:
                    l[1] = municipio
                    l[2] = estado
                    l[3] = ativ
                linhas.append(l)
        with open('viagens.csv', 'w', newline='') as arquivo_referencia:
           tabela = csv.writer(arquivo_referencia, delimiter=',')
           tabela.writerows(linhas)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Excluindo do CSV~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def excluir():
    arquivo_referencia = open('viagens.csv', 'w+')
    arquivo_referencia.close()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Buttons come to life~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    sg.theme('DarkTeal3')
    while True:
        opcao = tela_inicial()
        try:
            match opcao:
                case 'cadastro':  # Inclui
                    cadastra()
                case 'consulta':
                    lista_viagens()
                case _:
                    grava_dados()
                    break
        except SystemExit:
            exit()

main()
