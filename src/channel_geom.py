import numpy as np
from matplotlib.widgets import AxesWidget

def format_polyvects(x1, x2, y1, y2):
    x = np.hstack((x1, np.flipud(x2)))
    y = np.hstack((y1, np.flipud(y2)))
    xy = np.column_stack((x, y))
    return xy

def get_flowdepth(Q, B, Cfc, Cff, S0, g, Qbf):
    if Q > Qbf:
        Qob = Q - Qbf
        Hob = get_Hn(Qob, B, Cff, S0, g)
    else:
        Hob = 0
    Hc = get_Hn(Q, B, Cfc, S0, g)
    return Hc + Hob

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
    y = np.hstack((0 - Hnmax + np.array([Hn]),
                   np.zeros(len(x)-2)-Hnmax,
                   0 - Hnmax + np.array([Hn])))
    return y

def channel_bed(x, xmin, xmax):
    cbed = 0.85 * np.sin(-0.5 - 0.01*(x + np.sin(x))) - 0.852
    bed_poly = np.vstack((np.array([xmin*2, -10]),
                          np.array([xmin*2, 0]),
                          np.column_stack((x, cbed)),
                          np.array([xmax*2, 0]),
                          np.array([xmax*2, -10])))    
    print(np.shape(bed_poly))
    return bed_poly
