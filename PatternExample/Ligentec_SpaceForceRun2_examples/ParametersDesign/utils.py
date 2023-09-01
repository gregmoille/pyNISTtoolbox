import numpy as np
from copy import copy


def gregArange(start, step, stop, microns=False):
    if microns:
        scale = 1
    else:
        scale = 1e-3
    return [
        float("{:.4f}".format(ii * scale))
        for ii in np.arange(start, stop + step / 2, step)
    ]
