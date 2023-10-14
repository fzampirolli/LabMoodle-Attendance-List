import json, os, math

sufixo = "PI"

# TDA4BCM0505-22SA; segundas das 10:00 às 12:00;  quartas das 08:00 às 10:00 - L506
# TDB4BCM0505-22SA; segundas das 08:00 às 10:00;  quartas das 10:00 às 10200 - L506

# Seu dicionário de dados
dados = {
    "nome_a_remover": "Francisco de Assis Zampirolli",
    "somente_F": True, # reprovação por falta somente para quem tirou F e tem mais que limite_faltas
    "limite_faltas": 10,# math.ceil(0.25 * 48),
    "logs_zip": f"logs_{sufixo}.zip",
    "turmas_dias": f"turmas_dias_{sufixo}",
    "turmas_sigaa_zip": f"turmas_sigaa_{sufixo}.zip",
    "turmas": [
        {
            "periodo": ["2023/5/29", "2023/8/12"],
            "dias": ["segunda", "quarta"],
            "horas": ["10:00", "08:00"],
            "duracao": ["2:00", "2:00"],
            "IPs": ["172.17.11", "172.17.11"],
            "arquivo": os.path.join(f"turmas_dias_{sufixo}", "dias_TDA4BCM0505-22SA.csv"),
        },
        {
            "periodo": ["2023/5/29", "2023/8/12"],
            "dias": ["segunda", "quarta"],
            "horas": ["08:00", "10:00"],
            "duracao": ["2:00", "2:00"],
            "IPs": ["172.17.11", "172.17.11"],
            "arquivo": os.path.join(f"turmas_dias_{sufixo}", "dias_TDB4BCM0505-22SA.csv"),
        },
    ],
}

# Nome do arquivo JSON
nome_arquivo_json = "dados.json"

# Salvar o dicionário em um arquivo JSON
with open(nome_arquivo_json, "w") as json_file:
    json.dump(dados, json_file, indent=4)

print(f"Dados salvos no arquivo JSON: {nome_arquivo_json}")
