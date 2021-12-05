import logging


def getLogger(module,name=None):
    if name is None:
        logging.basicConfig(format='[%(asctime)s] "%(message)s"', datefmt='%d/%b/%Y %H:%M:%S')
    else:
        logging.basicConfig(format=f'[%(asctime)s] ({name}) "%(message)s"', datefmt='%d/%b/%Y %H:%M:%S')   
    log = logging.getLogger(module)
   
    return log
