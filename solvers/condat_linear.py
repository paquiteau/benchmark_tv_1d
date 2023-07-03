from benchopt import BaseSolver
from benchopt import safe_import_context
from benchopt.stopping_criterion import SingleRunCriterion
with safe_import_context() as import_ctx:
    import numpy as np
    import numba as nb
    from benchmark_utils.tv_numba import linearizedTautString

class Solver(BaseSolver):
    """Solve the TV minimization problem using a majorization-minimization algorithm."""

    name = 'tv_mm'
    stopping_strategy = SingleRunCriterion()

    def set_objective(self, A, reg, y, c , delta, data_fit):
        self.reg = reg
        self.A, self.y = A, y
        self.c = c
        self.data_fit = data_fit
        # Delta is ignored, only used for huber function.
        self.run(5)

    def skip(self, **objective_dict):
        if objective_dict['data_fit'] != 'quad':
            return True, "TVMM solver only useable for quadratic data_fit"
        return False, None

    def run(self, n_iter):
        self.u = linearizedTautString(self.y, self.reg)

    def get_result(self):
        return self.u
