from datetime import datetime

import logging as log
import os


class SimpleLogger():
    def __init__(self):
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        log_file = datetime.now().strftime("%Y.%m.%d_%H-%M-%S") + ".log"
        log_path = os.path.join(logs_dir, log_file)
        log.basicConfig(filename=log_path, level=log.INFO, format='%(asctime)s | %(filename)s:%(lineno)d | [%(levelname)s]: %(message)s', encoding='utf-8')
