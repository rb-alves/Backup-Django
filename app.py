from decouple import config
from pathlib import Path
from datetime import datetime
import subprocess
import os
import gzip

DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_NAME = config("DB_NAME")


def backup_mdfmoveis():
    # Caminho onde o backup será armazenado
    backup_dir = Path(__file__).resolve().parent
    
    # Nome do arquivo com data, hora, minuto e segundo para torna-lo unico
    file_name = f'{DB_NAME}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'

    # Concatena o caminho e o nome do arquivo
    backup_path = f'{backup_dir}\\{file_name}.sql'

    # Comando para gerar o dump
    pg_dump_command = f'pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -f "{backup_path}"'

    # Variavel que armazena a senha para executar o comando
    env = {'PGPASSWORD': DB_PASSWORD, **os.environ}

    # Execução do comando do dump
    subprocess.run(pg_dump_command, shell=True, check=True, env=env)

    compress_backup_path = f'{backup_dir}\\{file_name}.sql.gz'
    with open(backup_path, 'rb') as original_file:
        with gzip.open(compress_backup_path, 'wb') as compress_file:
            compress_file.write(original_file.read())
    
    os.remove(backup_path)


backup_mdfmoveis()