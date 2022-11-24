import logging

from config import Config


def create_file_logger(player_id, module_name = ''):
    logger = logging.getLogger("{}:{}".format(player_id[:8], module_name))
    logger.setLevel(Config.logging_level)

    sh = logging.StreamHandler()
    sh.setLevel(Config.logging_stream_level)
    formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s'.format(module_name))
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    fh = logging.FileHandler(Config.logging_file_path + player_id[:8] + '.log')
    fh.setLevel(Config.logging_file_level)
    formatter = logging.Formatter('[%(asctime)s] {}:%(levelname)s: %(message)s'.format(module_name))
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
