from drawing_multiplePolicies import DrawingMultiplePolicies
from drawing_singlePolicy import DrawingSinglePolicy
from determine_figure import determine_figure
from algorithm import Algorithm

from utils import LoggerManager
logger = LoggerManager().getLogger()

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    CLOSE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print()
print(Colors.BOLD + "————————————————————————————————————————————————————————————————————————————————————————————" + Colors.CLOSE)
print(Colors.BOLD + "¡Bienvenid@ a Reinforced Logo!" + Colors.CLOSE)
print(Colors.BOLD + "————————————————————————————————————————————————————————————————————————————————————————————" + Colors.CLOSE)
print()
print("Para empezar, debe configurar el agente. Responda a las siguientes preguntas:" + Colors.CLOSE)
print()

# Identificando el algoritmo que se debe ejecutar. Posibles opciones: value iteration, policy iteration, ...

print(Colors.OKBLUE + "(1) ¿Cuál algoritmo debo usara para encontrar la política óptima?" + Colors.CLOSE)
print(Colors.OKBLUE + "    — 'v'  para Value Iteration" + Colors.CLOSE)
print(Colors.OKBLUE + "    — 'p'  para Policy Iteration" + Colors.CLOSE)
print(Colors.OKBLUE + "    — 'mc' para Monte Carlo" + Colors.CLOSE)

algoritmo = input()
print()

algorithm_kind = None
if algoritmo == 'v':
    algorithm_kind = Algorithm.VALUE_ITERATION
elif algoritmo == 'p':
    algorithm_kind = Algorithm.POLICY_ITERATION
elif algoritmo == 'mc':
    algorithm_kind = Algorithm.MONTE_CARLO

# Identificando la estrategia de dibujo que se debe usar. Posibles opciones: 'single policy' y 'multiple policy'.

estrategia = None

# El método de Monte Carlo no soporta la estrategia de política única.
if algorithm_kind == Algorithm.MONTE_CARLO:
    estrategia = 'm'
else:
    print(Colors.OKBLUE + "(2) ¿Cuál estrategia de dibujo debo ejecutar?" + Colors.CLOSE)
    print(Colors.OKBLUE + "    — 'm' para Multiple Policy" + Colors.CLOSE)
    print(Colors.OKBLUE + "    — 's' para Single Policy" + Colors.CLOSE)
    estrategia = input()
    print()


# Ejecutando el algoritmo seleccionado de acuerdo con la estrategia de dibujo seleccionada. 
if estrategia == 's':
    logger.info('Ejecutando la versión de política simple')
    DrawingSinglePolicy(algorithm_kind=algorithm_kind).run()
else:
    logger.info('Ejecutando la versión de múltiples políticas')
    #figure_sequence, dimensions = determine_figure("square 20x20 centered")
    #DrawingMultiplePolicies(figure_sequence, dimensions, algorithm_kind=algorithm_kind).run()
    DrawingMultiplePolicies(algorithm_kind=algorithm_kind).run()


