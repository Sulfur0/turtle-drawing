from drawing_multiplePolicies import DrawingMultiplePolicies
from drawing_singlePolicy import DrawingSinglePolicy
from determine_figure import determine_figure

from utils import LoggerManager
logger = LoggerManager().getLogger()

# Parsing de los argumentos para decidir el modo de ejecución.
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--mode', help='Modo de ejecución del ambiente: single_policy o mutiple_policy')
args = parser.parse_args()

# Ejecutando el algoritmo de acuerdo con la política seleccionada. Se usa la
# solución de múltiples políticas por defecto.
if args.mode == 'single_policy':
    logger.info('Ejecutando la versión de política simple')
    DrawingSinglePolicy().run()

else:
    logger.info('Ejecutando la versión de múltiples políticas')
    figure_sequence, dimensions = determine_figure("square 10x10 centered")
    DrawingMultiplePolicies(figure_sequence, dimensions).run()