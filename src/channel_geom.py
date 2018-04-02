import numpy as np
from matplotlib.widgets import AxesWidget

def format_polyvects(x1, x2, y1, y2):
    x = np.hstack((x1, np.flipud(x2)))
    y = np.hstack((y1, np.flipud(y2)))
    xy = np.column_stack((x, y))
    return xy

def get_Hn(Q, B, Cf, S0, g):
    # generalized Darcy Weisbach, from Ganti et al., 2014 supp info
    HnDW =  (Q/B)**(2/3) * (Cf / (g*S0))**(1/3)
    return HnDW


def make_xcoords(B):
    x = np.hstack((np.array([-B*1/3]),
                   np.linspace(-B*1/3, B*2/3),
                   np.array([B*2/3])))
    return x

def make_ycoords(x, Hn, Hnmax):
    y = np.hstack((0 - np.array([Hn]),
                   np.zeros(len(x)-2)-Hnmax,
                   0 - np.array([Hn])))
    return y