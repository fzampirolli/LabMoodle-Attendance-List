import os
import pandas as pd
from faker import Faker
import random

fake = Faker()

# Crie um DataFrame para os dados falsos
dados_fake = pd.DataFrame(columns=['Matrícula', 'Nome', 'E-mail', 'Resultado', 'Faltas', 'Situação'])

# Preencha o DataFrame com dados falsos
for _ in range(50):
    matricula = random.randint(11202000000, 11202999999)
    nome = fake.name().upper()
    email = fake.email()
    resultado = random.choice(['A', 'B', 'C', 'D', 'F', 'F', 'F'])
    faltas = random.randint(10, 40)
    situacao = 0

    nova_linha = {'Matrícula': matricula, 'Nome': nome, 'E-mail': email, 'Resultado': resultado, 'Faltas': faltas, 'Situação': situacao}
    dados_fake = pd.concat([dados_fake, pd.DataFrame([nova_linha])], ignore_index=True)

# Salve os dados falsos em um arquivo CSV
dados_fake.to_csv('dados_fake.csv', index=False)

# Ler o arquivo CSV com nomes
arquivo_nomes = 'dados_fake.csv'
df_nomes = pd.read_csv(arquivo_nomes)
nomes = df_nomes['Nome'].tolist()

# Listar todos os arquivos CSV na pasta "logs_vpl_PI"
pasta_logs = 'logs_vpl_PI'
arquivos_logs = [arq for arq in os.listdir(pasta_logs) if arq.endswith('.csv')]

# Para cada arquivo CSV na pasta "logs_vpl_PI"
for arquivo_csv in arquivos_logs:
    caminho_arquivo_csv = os.path.join(pasta_logs, arquivo_csv)

    # Ler o arquivo CSV original
    df_original = pd.read_csv(caminho_arquivo_csv)

    print(caminho_arquivo_csv, len(df_original))

    # Substituir os valores da coluna "Nome completo" aleatoriamente
    df_original['Nome completo'] = [random.choice(nomes) for _ in range(len(df_original))]
    df_original['Usuário afetado'] = '-'
    df_original['Descrição'] = '-'

    # Gere endereços IP aleatórios entre ["172.17.11", "172.17.15"]
    enderecos_ip_aleatorios = [random.choice(["172.17.11.234", "172.17.12.12"]) for _ in range(len(df_original))]

    # Atribua os valores gerados à coluna "endereço IP" no DataFrame
    df_original['endereço IP'] = enderecos_ip_aleatorios

    # Salvar o arquivo CSV com os novos valores
    df_original.to_csv(caminho_arquivo_csv, index=False)

print("Substituição concluída.")
