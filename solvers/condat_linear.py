from benchopt import BaseSolver
from benchopt import safe_import_context
from benchopt.stopping_criterion import SingleRunCriterion

with safe_import_context() as import_ctx:
    from benchmark_utils.tv_numba import prox_condat, jit_module


class Solver(BaseSolver):
    """Direct algorithm for 1D TV denoising.

    Condat, L. (2013). A direct algorithm for 1D total variation denoising.
    https://github.com/albarji/proxTV/blob/master/src/TVL1opt.cpp
    """

    name = "Linearized Taut String"
    stopping_criterion = SingleRunCriterion()
    requirements = ["pip:numba"]

    def set_objective(self, A, reg, y, c, delta, data_fit):
        self.reg = reg
        self.A, self.y = A, y
        self.c = c
        self.data_fit = data_fit
        # Delta is ignored, only used for huber function.
        jit_module()

    def skip(self, **objective_dict):
        if objective_dict["data_fit"] != "quad":
            return True, "TVMM solver only useable for quadratic data_fit"
        return False, None

    def run(self, n_iter):
        self.u = prox_condat(self.y, self.reg)

    def get_result(self):
        return self.u
