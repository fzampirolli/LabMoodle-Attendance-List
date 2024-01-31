import json

# Importar o módulo JSON

# Definir o quadrimestre
SUFIXO = "PI2024.1"

# Definir outras constantes
LOGS_DIR = f"logs_{SUFIXO}"
TURMAS_DIAS_DIR = f"turmas_dias_{SUFIXO}"
TURMAS_SIGAA_DIR = f"turmas_sigaa_{SUFIXO}"

# Função auxiliar para criar turmas
def criar_turma(nome, horas, IPs, periodo, dias, duracao):
    return {
        "nome": nome,
        "periodo": periodo,
        "dias": dias,
        "horas": horas,
        "duracao": duracao,
        "IPs": IPs,
        "arquivo": f"{TURMAS_DIAS_DIR}/dias_{nome}.csv",
    }

# Alterar: Definir período letivo, dias de aula e duração
periodo_letivo = ["2023/2/5", "2023/3/27"]
dias_aula = ["terça", "quinta"]
duracao_aula = ["2:00", "2:00"]

# Definição das turmas
turmas = [
    criar_turma(
        # Alterar: Turma (SIGAA), hora da aula e prefixo dos IPs dos laboratórios
        "TDA2BCM0505-22SA",
        ["08:00", "10:00"],
        ["172.17.11", "172.17.11"],
        periodo_letivo,
        dias_aula,
        duracao_aula,
    ),
    criar_turma(
        # Alterar: Turma (SIGAA), hora da aula e prefixo dos IPs dos laboratórios
        "TDB2BCM0505-22SA",
        ["10:00", "08:00"],
        ["172.17.11", "172.17.11"],
        periodo_letivo,
        dias_aula,
        duracao_aula,
    )
]

# Dicionário de dados
dados = {
    "nome_a_remover": "", # Francisco de Assis Zampirolli
    "somente_F": False,  # se True, reprovação por falta somente para quem tirou F e tem mais que limite_faltas
    "limite_faltas": 10, # math.ceil(0.25 * 48),
    "logs": LOGS_DIR,
    "turmas_dias": TURMAS_DIAS_DIR,
    "turmas_sigaa": TURMAS_SIGAA_DIR,
    "turmas": turmas,
}

# Nome do arquivo JSON
nome_arquivo_json = "dados.json"

# Salvar o dicionário em um arquivo JSON
with open(nome_arquivo_json, "w") as json_file:
    json.dump(dados, json_file, indent=4)

print(f"Dados salvos no arquivo JSON: {nome_arquivo_json}")