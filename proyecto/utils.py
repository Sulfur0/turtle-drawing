import logging

class Logger:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        fomatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(fomatter)
        
        self.logger.addHandler(consoleHandler)
        logging.basicConfig(filename='drawing.log', level=logging.INFO)
        
        
    def get_logger(self):
        return self.logger

    