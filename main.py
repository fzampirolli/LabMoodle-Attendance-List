"""'
python -m venv venv
source venv/bin/activate
# pip freeze > requirements.txt
pip install -r requirements.txt
python main.py
"""
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
import zipfile
import os
import pandas as pd
import shutil
import csv
from datetime import datetime, timedelta

########################################################################
# ler logs_vpl.zip e gera logs_combinado.csv
########################################################################

logs_combinado = "logs_combinado.csv"
nome_a_remover = "Francisco de Assis Zampirolli"

caminho_zip = "logs_vpl.zip"
diretorio_destino = "logs_vpl"

# Extrai os arquivos do ZIP para o diretório de destino
with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
    zip_ref.extractall(diretorio_destino)

# Define o caminho para a pasta "__MACOSX"
macosx_path = os.path.join(diretorio_destino, "__MACOSX")

# Verifica se a pasta "__MACOSX" existe e tenta removê-la
if os.path.exists(macosx_path):
    try:
        shutil.rmtree(macosx_path)  # Remove a pasta e seu conteúdo
    except OSError as e:
        print(f"Could not remove: {e}")
else:
    print('Folder "__MACOSX" not found.')

# Crie uma lista para armazenar todos os caminhos dos arquivos CSV
arquivos_csv = []

# Percorra todos os diretórios e subdiretórios em diretorio_destino
for diretorio_raiz, diretorios, arquivos in os.walk(diretorio_destino):
    for arquivo in arquivos:
        if arquivo.endswith(".csv"):
            caminho_completo = os.path.join(diretorio_raiz, arquivo)
            arquivos_csv.append(caminho_completo)

df_combinado = pd.DataFrame()
for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo)
    df_combinado = pd.concat([df_combinado, df], ignore_index=True)

df_combinado = df_combinado[df_combinado["Nome completo"] != nome_a_remover]
df_combinado.to_csv(logs_combinado, index=False)

# Leia o arquivo CSV
df_logs = pd.read_csv(logs_combinado)
df_logs["Nome completo"] = df_logs[
    "Nome completo"
].str.upper()  # deixar nomes em maúsculo
# Converter a coluna 'Hora' para o tipo DateTime
df_logs["Hora"] = pd.to_datetime(
    df_logs["Hora"], format="%d/%m/%Y %H:%M", dayfirst=True
)

# Remover uma pasta não vazia
shutil.rmtree(diretorio_destino)

print(df_logs.shape)


########################################################################
# Gera dias de aulas com IPs dos labs
########################################################################
diretorio_dias = 'dias'

if not os.path.exists(diretorio_dias):
    os.makedirs(diretorio_dias)

def geraDiaHoraAulas(
    periodo=["2023/5/29", "2023/8/31"],
    dias=["segunda", "quarta"],
    horas=["10:00", "08:00"],
    duracao=["2:00", "2:00"],
    IPs=["177.181.6", "177.181.7"],
    arquivo="dias.csv",):

    # Definir as datas de início (primeira segunda-feira de maio) e fim (última quarta-feira de agosto)
    aux = periodo[0].split("/")
    aux = list(map(int, aux))
    data_inicio = datetime(aux[0], aux[1], aux[2])

    aux = periodo[1].split("/")
    aux = list(map(int, aux))
    data_fim = datetime(aux[0], aux[1], aux[2])

    # Definir os horários para os dias de aula
    dias_semana = ["segunda", "terça", "quarta", "quinta", "sexta"]
    horarios = [datetime.strptime(hora, "%H:%M").time() for hora in horas]
    duracoes = [datetime.strptime(dur, "%H:%M").time() for dur in duracao]

    # Abrir o arquivo CSV para escrita
    with open(arquivo, "w", newline="") as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["Inicio", "Fim", "IP"])  # Escrever o cabeçalho das colunas

        # Iterar pelas datas de maio a agosto
        data_atual = data_inicio
        while data_atual <= data_fim:
            if data_atual.weekday() in [
                dias_semana.index(dia) for dia in dias
            ]:  # Verificar se é um dos dias de aula
                for i, dia in enumerate(dias):
                    if data_atual.weekday() == dias_semana.index(dia):
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


# DA4BCM0505-22SA; segundas das 10:00 às 12:00;  quartas das 08:00 às 10:00 - L506
geraDiaHoraAulas(
    periodo=["2023/5/29", "2023/8/31"],
    dias=["segunda", "quarta"],
    horas=["10:00", "08:00"],
    duracao=["2:00", "2:00"],
    IPs=["172.17.11", "172.17.11"],
    arquivo=os.path.join(diretorio_dias, "dias_DA4.csv"),
)

# DB4BCM0505-22SA; segundas das 08:00 às 10:00;  quartas das 10:00 às 10200 - L506
geraDiaHoraAulas(
    periodo=["2023/5/29", "2023/8/31"],
    dias=["segunda", "quarta"],
    horas=["08:00", "10:00"],
    duracao=["2:00", "2:00"],
    IPs=["172.17.11", "172.17.11"],
    arquivo=os.path.join(diretorio_dias, "dias_DB4.csv"),
)

########################################################################
# ler turmas do SIGAA em turmas_sigaa/notas_*.xls
########################################################################

# Prepara arquivos exportados do SIGAA, convertido para CSV

# número de faltas totais da turma
numero_faltas = 48

# Diretório onde estão os arquivos "notas_*.xls"
diretorio_turmas = "turmas_sigaa"
caminho_zip = "turmas_sigaa.zip"

# Extrai os arquivos do ZIP para o diretório de destino
with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
    zip_ref.extractall("./")

# Lista para armazenar DataFrames de cada arquivo
dataframes = []

# Lista para armazenar nomes de arquivos processados
arquivos_processados = []

# Iterar por todos os arquivos no diretório
for nome_arquivo in os.listdir(diretorio_turmas):
    if nome_arquivo.startswith("notas_") and nome_arquivo.endswith(".xls"):
        caminho_arquivo = os.path.join(diretorio_turmas, nome_arquivo)

        #print(caminho_arquivo)
        # Ler o arquivo CSV
        # df = pd.read_csv(caminho_arquivo, sep=";", encoding='UTF-16')

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
            "Situação",
        ]
        df.columns = novo_cabecalho
        df.loc[:, "Faltas"] = numero_faltas

        # Salvar o DataFrame final em um arquivo CSV
        df.to_csv(
            os.path.join(diretorio_turmas, "faltas_" + nome_arquivo + ".csv"), index=False
        )

lista_dias = []
# Iterar por todos os arquivos no diretório
for nome_arquivo in os.listdir(diretorio_dias):
    if nome_arquivo.startswith("dias_") and nome_arquivo.endswith(".csv"):
        caminho_dias = os.path.join(diretorio_dias, nome_arquivo)
        lista_dias.append(nome_arquivo[5:8])

for nome_arquivo in os.listdir(diretorio_turmas): # para cada turma
    if nome_arquivo.startswith("faltas_") and nome_arquivo.endswith(".csv"):
        for dia in lista_dias:
            if dia in nome_arquivo:
                caminho_dias = os.path.join(diretorio_dias, "dias_"+dia+".csv")
                caminho_turma = os.path.join(diretorio_turmas, nome_arquivo)
                #print(caminho_dias)
                #print(caminho_turma)
                #print()
                df_dias = pd.read_csv(caminho_dias)
                df_faltas = pd.read_csv(caminho_turma)

                for _, linha in df_faltas.iterrows(): # para cada aluno da turma
                    #print(linha[1])
                    df_filtro = df_logs.query("`Nome completo` == '"+linha[1]+ "'")
                    if len(df_filtro): # aluno está no log
                        for _, lin in df_dias.iterrows(): # para cada aula, verifica se o aluno esteve no lab
                            dia_aula = lin[0]  # Primeiro elemento da linha é o dia e hora de início
                            dia_aula_fim = lin[1]  # Segundo elemento da linha é o dia e hora de fim
                            inicio = pd.to_datetime(dia_aula, format='%d/%m/%Y %H:%M')
                            fim = pd.to_datetime(dia_aula_fim, format='%d/%m/%Y %H:%M')
                            linhas_filtradas = df_filtro[(df_filtro['Hora'] >= inicio) & (df_filtro['Hora'] <= fim)]
                            presente = False
                            if len(linhas_filtradas):
                                filtro = linhas_filtradas[linhas_filtradas['endereço IP'].str.contains(lin[2])]
                                if len(filtro): # verifica IP do lab
                                    print(linha[1])
                                    print(f"{dia_aula} - {dia_aula_fim} - {lin[2]} - {len(filtro)}")
                                    presente = True 
                            if presente:
                                # Decrementar a coluna "Faltas" em 2 para o aluno presente
                                df_faltas.loc[df_faltas['Nome'] == linha[1], 'Faltas'] -= 2

                # Salvar o arquivo CSV modificado
                df_faltas.to_csv(caminho_turma, index=False) 

'''
limpar
rm -rf *.csv turmas_sigaa dias
'''