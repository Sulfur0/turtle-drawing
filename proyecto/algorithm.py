class AlgorithmImpl:

    def __init__(self):
        self.canvas = None

    def run(self):
        pass


from enum import Enum

class Algorithm(Enum):
    VALUE_ITERATION = 1
    POLICY_ITERATION = 2
    MONTE_CARLO = 3
    TEMPORAL_DIFFERENCE = 4