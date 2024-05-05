import logging

class LoggerMeta(type):
    '''
    Clase que implementa el singleton del Logger. Esto garantiza que tengo solamente una
    instancia del logger a lo largo de toda la ejecución del programa. 
    '''
    instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            instance = super().__call__(*args, **kwargs)
            cls.instances[cls] = instance
        return cls.instances[cls]


class LoggerManager(metaclass=LoggerMeta):
    
    def __init__(self):
        '''
        Inicializa la herramienta de logging que se usará en la aplicación.
        '''
        self.logger = logging.getLogger(__name__)
        fomatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(fomatter)
        self.logger.addHandler(consoleHandler)
        logging.basicConfig(filename='drawing.log', level=logging.INFO)

    def getLogger(self):
        return self.logger