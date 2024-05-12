from drawing_multiplePolicies import DrawingMultiplePolicies
from drawing_singlePolicy import DrawingSinglePolicy
from determine_figure import determine_figure

from utils import LoggerManager
logger = LoggerManager().getLogger()

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Parsing de los argumentos para decidir el modo de ejecución.
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--mode', help='Modo de ejecución del ambiente: single_policy o mutiple_policy. Default: mutiple_policy')
args = parser.parse_args()

print()
print(Colors.BOLD + "Bienvenid@ a Boosted Logo!" + Colors.ENDC)
print("Para empezar, debe configurar el agente. Responda a las siguientes preguntas:" + Colors.ENDC)
print()

print(Colors.OKBLUE + "(1) ¿Cuál algoritmo debo usara para encontrar la política óptima? (v) para 'value iteration, (p) para 'policy iteration''" + Colors.ENDC)
algoritmo = input()
print()

print(Colors.OKBLUE + "(2) ¿Cuál estrategia de dibujo debo ejecutar? (s) para 'single policy', (m) para 'miltiple policy''" + Colors.ENDC)
estrategia = input()
print()


# Ejecutando el algoritmo de acuerdo con la política seleccionada. Se usa la
# solución de múltiples políticas por defecto.
if estrategia == 's':
    logger.info('Ejecutando la versión de política simple')
    DrawingSinglePolicy().run()

else:
    logger.info('Ejecutando la versión de múltiples políticas')
    figure_sequence, dimensions = determine_figure("square 10x10 centered")
    DrawingMultiplePolicies(figure_sequence, dimensions).run()


