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
log.info('connection à la base de donnée')
try:
    conn = psycopg2.connect(
        database="postgres",
        user='postgres',
        password='0000',
        host='database',
        port='5432'
    )
except Exception as e:
    log.error(e)

# crée la table pour les metadata des fichiers donnée chargée
command1 = '''
        CREATE TABLE IF NOT EXISTS metadata_donnée_v2  (
            date VARCHAR(255),
            fichier  VARCHAR(255),
            contenu text
        );
        '''

# crée la table pour les metadata des fichiers modèle chargée
command2 = '''
        CREATE TABLE IF NOT EXISTS metadata_modèle  (
            date VARCHAR(255),
            fichier  VARCHAR(255),
            model VARCHAR(255),
            hyperparametre text,
            contenu text
        );
        '''

try:
    # connect to the PostgreSQL server
    cur = conn.cursor()
    # create table one by one
    log.info('création de la table metadata_file')
    cur.execute(command1)
    cur.execute(command2)
    # close communication with the PostgreSQL database server
    log.info('Arret du curseur de la base de donnée')
    cur.close()
    # commit the changes
    log.info('éxecution de la commande')
    conn.commit()
except Exception as e:
    log.error(e)
finally:
    if conn is not None:
        log.info('ferméture de la base de donnée')
        # ferméture de la connection à la base de donnée
        conn.close()