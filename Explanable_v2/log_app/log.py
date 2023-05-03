import logging
import os
from pathlib import Path


class log:
    def __init__(self):
        current_dir = os.getcwd()
        self.current_dir = Path(Path(current_dir).parent.absolute())

    # management des logs erreur
    def log(self, file, log_type='info'):
        logfile = os.path.join(self.current_dir, file)
        logger = logging.getLogger(log_type)
        logger.setLevel(logging.INFO)
        filehandler = logging.FileHandler(logfile, mode='a')
        formatter = logging.Formatter('%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s: %(message)s', datefmt='%m/%d/%Y/ %I:%M:%S %p')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        return logger