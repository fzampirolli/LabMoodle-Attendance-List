import json, os, math

sufixo = "PI"

# DA2BCM0505-22SA; terça das 08:00 às 10:00, semanal; quinta das 10:00 às 12:00, semanal - Lab. 405-2
# DB2BCM0505-22SA; terça das 10:00 às 12:00, semanal; quinta das 08:00 às 10:00, semanal - Lab. 405-2

# Seu dicionário de dados
dados = {
    "nome_a_remover": "Francisco de Assis Zampirolli",
    "somente_F": True, # reprovação por falta somente para quem tirou F e tem mais que limite_faltas
    "limite_faltas": 10,# math.ceil(0.25 * 48),
    "logs": f"logs_{sufixo}",
    "turmas_dias": f"turmas_dias_{sufixo}",
    "turmas_sigaa": f"turmas_sigaa_{sufixo}",
    "turmas": [
        {
            "periodo": ["2023/2/5", "2023/3/27"],
            "dias": ["terca", "quinta"],
            "horas": ["08:00", "10:00"],
            "duracao": ["2:00", "2:00"],
            "IPs": ["172.17.11", "172.17.11"], # VALIDAR OS PREFIXOS DO IP'S NO LAB!!!
            "arquivo": os.path.join(f"turmas_dias_{sufixo}", "dias_TDA2BCM0505-22SA.csv"),
        },
        {
            "periodo": ["2023/2/5", "2023/3/27"],
            "dias": ["terca", "quinta"],
            "horas": ["10:00", "08:00"],
            "duracao": ["2:00", "2:00"],
            "IPs": ["172.17.11", "172.17.11"], # VALIDAR OS PREFIXOS DO IP'S NO LAB!!!
            "arquivo": os.path.join(f"turmas_dias_{sufixo}", "dias_TDB2BCM0505-22SA.csv"),
        },
    ],
}

# Nome do arquivo JSON
nome_arquivo_json = "dados.json"

# Salvar o dicionário em um arquivo JSON
with open(nome_arquivo_json, "w") as json_file:
    json.dump(dados, json_file, indent=4)

print(f"Dados salvos no arquivo JSON: {nome_arquivo_json}")
