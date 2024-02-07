# LabMoodle-Attendance-List

# Instalar python, pip e git (se ainda não tiver instalado)

## 👇️ Debian / Ubuntu
```
sudo apt update
sudo apt install python3-venv python3-pip
python3 -m pip install --upgrade pip
sudo apt install git-all
```

# 👇️ Download LabMoodle-Attendance-List 
```
git clone git@github.com:fzampirolli/LabMoodle-Attendance-List.git
```

# 👇️ Configurar ambiente virtual 
```
python -m venv ../venvLabMoodle
source ../venvLabMoodle/bin/activate
# pip freeze > requirements.txt
pip install -r requirements.txt
```

# Preparar os dados

## Turmas do SIGAA

Criar uma pasta `turmas_sigaa_*`, por exemplo `turmas_sigaa_PI2024.1` e incluir os arquivos `*.xls` exportados do SIGAA e deixar na pasta deste projeto.

## Logs do Moodle

Crie uma pasta chamada `logs_*`, por exemplo, `logs_PI2024.1`, e inclua os arquivos `*.csv` exportados do Moodle e coloque-a na pasta deste projeto.

Para evitar a geração de um log para cada atividade, como ilustrado na pasta `logs_PI2024.1`, é possível solicitar um log geral da disciplina. Geralmente, não é possível gerar um CSV com todas as informações da disciplina. No entanto, é possível aplicar alguns filtros: na engrenagem na página da disciplina -> mais... -> Logs.

* Em `Todas as ações`, mude para `Todas as mudanças`.
* Em `Todas as origens`, mude para `web`.

## Configuração geral em `dados.py`

Configurar os dados gerais e das turmas no arquivo `dados.py`. Por exemplo, alterar:

```
# Definir o quadrimestre
SUFIXO = "PI2024.1"
MAX_FALTAS = 48

```

```
# Alterar: Definir período letivo, dias de aula e duração
periodo_letivo = ["2024/2/5", "2024/4/27"]
dias_aula = ["terça", "quinta"]
duracao_aula = ["2:00", "2:00"]
IPs = "177.104.50"

# Definição das turmas
turmas = [
    criar_turma(
        # Alterar: Turma (SIGAA), hora da aula e prefixo dos IPs dos laboratórios
        "TDA2BCM0505-22SA",
        ["08:00", "10:00"],
        [IPs, IPs],
        periodo_letivo,
        dias_aula,
        duracao_aula,
    ), ...
```



# 👇️ Executar main.py
```
python3 main.py
```

# Verificar arquivos gerados

Os dados deste GitHub são fake e foram gerados a partir do código `dados_fake.py`.

Na pasta `turmas_sigaa_PI2024.1_faltas` foram gerados arquivos `faltas_*`. 

Foi incluído o número de faltas, conforme condições definidas em `dados.py`, nas chaves:

```
"somente_F": True, # reprovação por falta somente para quem tirou F e tem mais que limite_faltas
"limite_faltas": 10,# math.ceil(0.25 * 48),
```

Se `"somente_F": False`, reprova todos com mais que `limite_faltas`, atribuindo o conceito "O".