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
python -m venv venv
source venv/bin/activate
# pip freeze > requirements.txt
pip install -r requirements.txt
```

# Preparar os dados

## Turmas do SIGAA

Criar uma pasta `turmas_sigaa_*`, por exemplo `turmas_sigaa_PI` e incluir os arquivos `*.xls` exportados do SIGAA. Compactar essa pasta com o nome `turmas_sigaa_*.zip` e deixar na pasta deste projeto.

## Logs do Moodle

Criar uma pasta `logs_*`, por exemplo `logs_PI` e incluir os arquivos `*.csv` exportados do Moodle. Compactar essa pasta com o nome `logs_*.zip` e deixar na pasta deste projeto.

## Configuração geral em `dados.py`

Configurar os dados gerais e das turmas no arquivo `dados.py`.

# 👇️ Executar main.py
```
python main.py
```

# Verificar arquivos gerados

Os dados deste GitHub são fake e foram gerados a partir do código `dados_fake.py`.

Na pasta `turmas_sigaa_PI_faltas` foram gerados arquivos `faltas_*`. 

Foi incluído o número de faltas, conforme condições definidas em `dados.py`, nas chaves:

```
"somente_F": True, # reprovação por falta somente para quem tirou F e tem mais que limite_faltas
"limite_faltas": 10,# math.ceil(0.25 * 48),
```

Se `"somente_F": False`, reprova todos com mais que `limite_faltas`, atribuindo o conceito "O".