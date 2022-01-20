class Arc():

    '''
    Cette classe permet de représenter les arcs des graphes pré-transformation
    '''

    def __init__(self, u=None, v=None, t=None, l=None):
        self.u = u # Sommet de départ
        self.v = v # Sommet d'arrivée
        self.t = t # Temps de départ
        self.l = l # Temps de traversée

    def __repr__(self):
        return str((self.u, self.v, self.t, self.l))
