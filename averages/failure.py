"""
Failure criteria for unconventional materials.

Author: Dmytro Kuksenko
Date: Sept 14, 2022
"""
import numpy as np

def tsai_wu():
    pass

def max_stress():
    pass

def max_strain():
    pass

def mises_stress(t):
    mises = np.sqrt(
        0.5
        * (
            (t[:, 0] - t[:, 1]) ** 2
            + (t[:, 1] - t[:, 2]) ** 2
            + (t[:, 2] - t[:, 0]) ** 2
        )
        + 3 * (t[:, 3] ** 2 + t[:, 4] ** 2 + t[:, 5] ** 2)
    )
    return mises
