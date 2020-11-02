#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from math_helpers import matrices as mat
from math_helpers import vectors as vec
from numpy.linalg import norm
import numpy as np


def T_inertiaframe(Imatrix, Tmatrix):
    """similarity transformation for an inertia matrix
    written in one frame into another frame
    """
    rightmult = mat.mxm(m2=Imatrix, m1=mat.mT(Tmatrix))
    Imatrix_new = mat.mxm(m2=Tmatrix, m1=rightmult)
    return np.array(Imatrix_new)


def cg_tensor(rvec):
    """computes the center of gravity matrix for inertia calculations
    """
    r_skew = mat.skew_tilde(v1=rvec)
    r_skew_t = mat.mT(m1=r_skew)
    cg_tensor = mat.mxm(m2=r_skew, m1=r_skew_t)
    return np.array(cg_tensor)


def rotational_kenergy(I_cg, w):
    return np.array(0.5* vec.vTxv(w, v2=mat.mxv(I_cg, w)))


if __name__ == "__main__":
    pass