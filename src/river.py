import numpy as np

class River(object):
    def __init__(self, Bc, Bf, S0, Cfc, Cff, Qbf):

        self.channel = Channel(Bc, S0, Cfc, Qbf, parent=self)
        print(self.channel)


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




class Channel(object):
    def __init__(self, B, S0, Cf, Qbf, parent=None):
        self.B = B
        self.S0 = S0
        self.Cf = Cf
        self.Qbf = Qbf

        self.bed = self.make_bed(self.B)


    def make_bed(self, B):
        x = np.hstack((np.array([-B*1/3]),
                       np.linspace(-B*1/3, B*2/3),
                       np.array([B*2/3])))
        return x




class Floodplain(object):
    def __init__(self, B, S0, Cf, parent=None):
        a=1


class Flow(object):
    def __init__(self, parent):
        a=1


    

