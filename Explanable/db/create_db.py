import psycopg2
import os
import sys
from pathlib import Path
current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())
sys.path.append(os.path.join(current_dir, 'log_app'))
from log import log

# instance de log
file = "log_app/base_de_donnée.log"
logfile = os.path.join(current_dir, file)
logger = log()
log = logger.log(logfile)

# connection à la base de donnée
try:
    log.info('connection avec le serveur postgres')
    conn = psycopg2.connect(
        database="postgres",
        user='citus',
        password='FRAst@201',
        host='database',
        port='5432'
    )
except Exception as e:
    log.error(e)

try:
    conn.autocommit = True

    # Création du cursor
    log.info('creation du curseur de la base de donnée')
    cursor = conn.cursor()

    # query pour crée la base de donnée
    log.info('creation de la base donnée ')
    sql = ''' CREATE database app_metadata ''';

    # execution du query
    cursor.execute(sql)
    log.info("la base de donnée crée avec succès !!")

    # ferméture connection
    log.info('ferméture de la base de donnée')
    conn.close()
except Exception as e:
    log.error(e)

