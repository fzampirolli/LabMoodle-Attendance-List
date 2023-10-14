# LabVPL-Attendance-Checker

# Preparar os dados

## Turmas do SIGAA

Criar uma pasta `turmas_sigaa_*`, por exemplo `turmas_sigaa_PI` e incluir os arquivos `*.xls` exportados do SIGAA. Compactar essa pasta com o nome `turmas_sigaa_*.zip`.

## Logs do VPL

Criar uma pasta `logs_vpl_*`, por exemplo `logs_vpl_PI` e incluir os arquivos `*.csv` exportados do Moodle. Compactar essa pasta com o nome `logs_vpl_*.zip`.

## Configuração geral em `dados.py`

Configurar os dados gerais e das turmas no arquivo `dados.py`.

# Instalar python, pip e git (se ainda não tiver instalado)

## 👇️ Debian / Ubuntu
```
sudo apt update
sudo apt install python3-venv python3-pip
python3 -m pip install --upgrade pip
sudo apt install git-all
```

# 👇️ Download LabVPL-Attendance-Checker 
```
git clone git@github.com:fzampirolli/LabVPL-Attendance-Checker.git
```

# 👇️ Configurar ambiente virtual 
```
python -m venv venv
source venv/bin/activate
# pip freeze > requirements.txt
pip install -r requirements.txt
```

# 👇️ Executar main.py
```
python main.py
```