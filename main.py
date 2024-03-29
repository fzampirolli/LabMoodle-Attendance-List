import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import zipfile
import os
import shutil
import csv
import time
from datetime import datetime, timedelta
import json

import subprocess

# script a ser executado
script_name = 'dados.py'
MAX_FALTAS = 48

# Execute o script
try:
    result = subprocess.run(['python', script_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
except subprocess.CalledProcessError as e:
    print(f"Erro ao executar o script: {e}")

# Nome do arquivo JSON que você deseja ler
nome_arquivo_json = "dados.json"  # Substitua pelo nome do seu arquivo JSON

# Abra o arquivo JSON para leitura
with open(nome_arquivo_json, "r") as json_file:
    dados = json.load(json_file)

########################################################################
# Gerar dias de aulas com IPs dos labs
########################################################################

if not os.path.exists(dados["turmas_dias"]):
    os.makedirs(dados["turmas_dias"])

def geraDiaHoraAulas(
    periodo,
    dias,
    horas,
    duracao,
    IPs,
    arquivo):

    # Definir as datas de início e fim 
    aux = periodo[0].split("/")
    aux = list(map(int, aux))
    data_inicio = datetime(aux[0], aux[1], aux[2])

    aux = periodo[1].split("/")
    aux = list(map(int, aux))
    data_fim = datetime(aux[0], aux[1], aux[2])

    # Definir os horários para os dias de aula
    dias_semana = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado"]
    horarios = [datetime.strptime(hora, "%H:%M").time() for hora in horas]
    duracoes = [datetime.strptime(dur, "%H:%M").time() for dur in duracao]

    # Abrir o arquivo CSV para escrita
    with open(arquivo, "w", newline="") as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["Inicio", "Fim", "IP"])  # Escrever o cabeçalho das colunas

        # Iterar pelas datas 
        data_atual = data_inicio
        while data_atual <= data_fim:
            dia_da_semana_ajustado = data_atual.weekday()
            if dia_da_semana_ajustado in [
                dias_semana.index(dia) for dia in dias]:  # Verificar se é um dos dias de aula
                for i, dia in enumerate(dias):
                    if dia_da_semana_ajustado == dias_semana.index(dia):
                        data_hora1 = datetime.combine(data_atual, horarios[i])
                        data_hora2 = data_hora1 + timedelta(
                            hours=duracoes[i].hour, minutes=duracoes[i].minute
                        )  # Adicionar a duração correta
                        writer.writerow(
                            [
                                data_hora1.strftime("%d/%m/%Y %H:%M"),
                                data_hora2.strftime("%d/%m/%Y %H:%M"),
                                IPs[i],
                            ]
                        )

            data_atual += timedelta(days=1)  # Avançar para o próximo dia

for t in dados["turmas"]:
    geraDiaHoraAulas(
        t["periodo"],
        t["dias"],
        t["horas"],
        t["duracao"],
        t["IPs"],
        t["arquivo"])


########################################################################
# ler logs_PI.zip e gera logs_PI_combinado.csv
########################################################################

# Extrai os arquivos do ZIP para o diretório de destino
#with zipfile.ZipFile(dados["logs"], "r") as zip_ref:
#    zip_ref.extractall("./")

# Crie uma lista para armazenar todos os caminhos dos arquivos CSV
arquivos_csv = []

# Percorra todos os diretórios e subdiretórios em logs
for diretorio_raiz, diretorios, arquivos in os.walk(dados["logs"]):
    for arquivo in arquivos:
        if arquivo.endswith(".csv"):
            caminho_completo = os.path.join(diretorio_raiz, arquivo)
            arquivos_csv.append(caminho_completo)

df_combinado = pd.DataFrame()
for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo)
    df_combinado = pd.concat([df_combinado, df], ignore_index=True)

df_combinado = df_combinado[df_combinado["Nome completo"] != dados["nome_a_remover"]]

# Deixar nomes em maúsculo
df_combinado["Nome completo"] = df_combinado["Nome completo"].str.upper()  
# Converter a coluna 'Hora' para o tipo DateTime
# df_combinado["Hora"] = pd.to_datetime(
#     df_combinado["Hora"], format="%d/%m/%Y %H:%M", dayfirst=True
# )
df_combinado["Hora"] = pd.to_datetime(df_combinado["Hora"], format="%d/%m/%y, %H:%M:%S")


# Remover uma pasta não vazia
#shutil.rmtree(dados["logs"])

#df_combinado = df_combinado.sort_values(by='Hora')

df_combinado.to_csv(dados["logs"]+"_combinado.csv", index=False)

print(df_combinado.shape)


########################################################################
# ler turmas do SIGAA em turmas_sigaa_PI/notas_*.xls
########################################################################

# Prepara arquivos exportados do SIGAA, convertido para CSV

# número de faltas iniciais
numero_faltas = 0

# Extrai os arquivos do ZIP para o diretório de destino
# with zipfile.ZipFile(dados["turmas_sigaa"], "r") as zip_ref:
#     zip_ref.extractall("./")

# Lista para armazenar DataFrames de cada arquivo
dataframes = []

# Lista para armazenar nomes de arquivos processados
arquivos_processados = []

if not os.path.exists(dados["turmas_sigaa"]+"_faltas"):
    os.makedirs(dados["turmas_sigaa"]+"_faltas")

# Iterar por todos os arquivos no diretório
for nome_arquivo in os.listdir(dados["turmas_sigaa"]):
    if nome_arquivo.startswith("notas_") and nome_arquivo.endswith(".xls"):
        caminho_arquivo = os.path.join(dados["turmas_sigaa"], nome_arquivo)

        # Ler o arquivo Excel
        df = pd.read_excel(caminho_arquivo, sheet_name="Sheet0")

        # Realizar as operações especificadas
        df = df.iloc[11:, 1:]
        novo_cabecalho = [
            "Matrícula",
            "Nome",
            "E-mail",
            "Resultado",
            "Faltas",
            "Sit.",
        ]

        df = df.drop(df.columns[-1], axis=1) # remove a última coluna
        df = df.dropna()

        df.columns = novo_cabecalho
        df.loc[:, "Faltas"] = numero_faltas

        # Salvar o DataFrame final em um arquivo CSV
        df.to_csv(
            os.path.join(dados["turmas_sigaa"]+"_faltas", "faltas_" + nome_arquivo + ".csv"), index=False
        )

lista_dias = []
# Iterar por todos os arquivos no diretório
for nome_arquivo in os.listdir(dados["turmas_dias"]):
    if nome_arquivo.startswith("dias_") and nome_arquivo.endswith(".csv"):
        lista_dias.append(nome_arquivo.split("_")[1])
print(lista_dias)
time.sleep(3)

for nome_arquivo in os.listdir(dados["turmas_sigaa"]+"_faltas"): # para cada turma
    if nome_arquivo.startswith("faltas_") and nome_arquivo.endswith(".csv"):
        for dia in lista_dias: # para cada dia de aula
            if dia[:-4] in nome_arquivo:
                #print("\n\n"+dia)
                caminho_dias = os.path.join(dados["turmas_dias"], "dias_"+dia)
                caminho_turma = os.path.join(dados["turmas_sigaa"]+"_faltas", nome_arquivo)
                df_dias = pd.read_csv(caminho_dias)
                df_faltas = pd.read_csv(caminho_turma)
                for z, linha in df_faltas.iterrows(): # para cada aluno da turma
                    #print(z+1,linha[1],linha[3])
                    if not dados["somente_F"] or linha[3] == "F":
                    
                        df_filtro = df_combinado.query("`Nome completo` == '"+linha[1]+ "'")

                        if len(df_filtro): # aluno está no log
                            for _, lin in df_dias.iterrows(): # para cada aula, verifica se o aluno esteve no lab
                                #print(">>>>",lin, "<<<<")
                                dia_aula = lin[0]  # Primeiro elemento da linha é o dia e hora de início
                                dia_aula_fim = lin[1]  # Segundo elemento da linha é o dia e hora de fim
                                inicio = pd.to_datetime(dia_aula, format='%d/%m/%Y %H:%M')
                                fim = pd.to_datetime(dia_aula_fim, format='%d/%m/%Y %H:%M')                                
                                linhas_filtradas = df_filtro[(df_filtro['Hora'] >= inicio) & (df_filtro['Hora'] <= fim)]
                                # print(f"dia_aula        {dia_aula}")
                                # print(f"dia_aula_fim    {dia_aula_fim}")                                
                                # print(f"inicio {inicio}")
                                # print(f"fim    {fim}")
                                # print(linhas_filtradas)
                                # print(df_filtro)
                                # exit(0)
                                presente = False
                                if len(linhas_filtradas):
                                    #print("linhas_filtradas",len(linhas_filtradas))
                                    filtro = linhas_filtradas[linhas_filtradas['endereço IP'].str.contains(lin[2])]
                                    if len(filtro): # verifica IP do lab
                                        #print(f"{dia_aula} - {dia_aula_fim} {lin[2]} {len(filtro):3d} ações {dia} {linha[1]}")
                                        presente = True 
                                if not presente:
                                    # Decrementar a coluna "Faltas" em 2 para o aluno presente
                                    df_faltas.loc[df_faltas['Nome'] == linha[1], 'Faltas'] += 2
                        
                        else: # aluno não entrou no moodle
                            df_faltas.loc[df_faltas['Nome'] == linha[1], 'Faltas'] = MAX_FALTAS

                # Salvar o arquivo CSV modificado
                df_faltas.to_csv(caminho_turma, index=False) 

# atribui "O" para os reprovados por falta
for nome_arquivo in os.listdir(dados["turmas_sigaa"]+"_faltas"): # para cada turma
    if nome_arquivo.startswith("faltas_") and nome_arquivo.endswith(".csv"):

        caminho_turma = os.path.join(dados["turmas_sigaa"]+"_faltas", nome_arquivo)

        df_faltas = pd.read_csv(caminho_turma)

        print(f"\n\n{caminho_turma}")
        for z, linha in df_faltas.iterrows(): # para cada aluno da turma
            if not dados["somente_F"] or linha[3] == "F" or linha[3] == "-":
                if linha[4] > dados["limite_faltas"]:
                    df_faltas.loc[df_faltas['Nome'] == linha[1], 'Resultado'] = 'O'
                    linha[3] = 'O'
            print(f"{z+1:2d} {linha[1]:45s} {linha[3]}  {linha[4]:2d}")

        df_faltas.to_csv(caminho_turma, index=False) 
