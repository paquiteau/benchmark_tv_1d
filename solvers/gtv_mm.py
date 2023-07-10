from benchopt import BaseSolver
from benchopt import safe_import_context

with safe_import_context() as import_ctx:
    from benchmark_utils.tv_numba import gtv_mm_tol2, jit_module

class Solver(BaseSolver):
    """Group TV Denoising with Majoration-Minimisation.

    I. W. Selesnick and P.-Y. Chen, “Total variation denoising with overlapping
    group sparsity”, 2013
    doi:10.1109/ICASSP.2013.6638755.
    """

    name = "Group TV MM"
    stopping_strategy = "iteration"
    parameters = {"group_size": [1, 2, 3, 4, 5]}

    requirements = ["pip:numba"]

    def set_objective(self, A, reg, y, c, delta, data_fit):
        self.reg = reg
        self.A, self.y = A, y
        self.c = c
        self.tol = 1e-8
        self.data_fit = data_fit
        # Delta is ignored, only used for huber function.
        jit_module()

    def skip(self, **objective_dict):
        if objective_dict["data_fit"] != "quad":
            return True, "TVMM solver only useable for quadratic data_fit"
        return False, None

    def run(self, n_iter):
        self.u = gtv_mm_tol2(self.y, self.reg, self.group_size, n_iter, self.tol)

    def get_result(self):
        return self.u
