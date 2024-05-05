from drawing import Drawing

from utils import Logger
logger = Logger().get_logger()

def main():
    logger.info('hello')
    Drawing().run()

if __name__ == '__main__':
    main()

main()

