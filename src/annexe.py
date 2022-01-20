from math import inf

def transform(start,end,G,ts,te):
    '''
    Cette fonction transforme le graphe G en 4 graphes particuliers
    adaptés à la recherche de chemins de type 1, 2, 3 et 4.
    '''
    ### Initialisation
    sommets,arcs = G
    G_,G_2,G_3 = {},{},{}

    sup_t = 1 # Va permettre de stocker la valeur de la somme des t + 1

    Vin = {}
    Vout = {}
    for s in sommets:
        Vin[s] = []
        Vout[s] = []

    ### Create V
    for a in arcs:
        sup_t += a.t
        Vout[a.u] += [(a.u,a.t)]
        Vin[a.v] += [(a.v,a.t+a.l)]
    for s in sommets:
        Vout[s] = list(set(Vout[s]))
        Vin[s] = list(set(Vin[s]))
    V = {k: Vin.get(k, 0) + Vout.get(k, 0) for k in set(Vin)}

    ### Create G_,G_2 and G_3
    for k,v in V.items():
        v.sort()
        length = len(v)
        if(length > 0):
            if(k == start): # Uniquement pour le sommet de départ
                v_ = v.copy()
                v_.reverse() # On crée cette liste uniquement pour le graphe de type 2
                for i in range(length):
                    if(v[i][1] >= ts): # On vérifie que l'arc sortant du sommet de départ est bien dans l'intervalle
                        if(i+1 < length and v[i+1][1] >= ts):
                            G_[v[i]] = {v[i+1] : 0} # Les sommets d'une même classe sont liés par un arc de poids 0
                            G_2[v[i]] = {v[i+1] : sup_t} # On met un poids très grand pour imposer l'exploration (par Dijkstra) de cet arc en dernier
                            G_3[v[i]] = {v[i+1] : 0}
                        else: # Le dernier sommet d'une même classe de sommets ne pointe vers personne dans sa classe
                            # Pour le graphe de type2 c'est le sommet dont la valeur de l'arc sortant
                            # est la plus petite à l'inverse des deux autres graphes
                            G_[v[i]] = {}
                            G_2[v[i]] = {}
                            G_3[v[i]] = {}
                            break
            elif(k == end): # Uniquement pour le sommet d'arrivée
                for i in range(length):
                    if(v[i][1] <= te): # On vérifie que l'arc entrant du sommet d'arrivée est bien dans l'intervalle
                        if(i+1 < length and v[i+1][1] <= te):
                            G_[v[i]] = {v[i+1] : 0}
                            G_2[v[i]] = {v[i+1] : 0}
                            G_3[v[i]] = {v[i+1] : 0}
                        else:
                            G_[v[i]] = {}
                            G_2[v[i]] = {}
                            G_3[v[i]] = {}
                            break
            else: # Cas général
                for i in range(length-1):
                    # Les sommets d'une même classe sont liés par un arc de poids 0 sauf pour le type 3
                    G_[v[i]] = {v[i+1] : 0}
                    G_2[v[i]] = {v[i+1] : 0}
                    G_3[v[i]] = {v[i+1] : v[i+1][1]-v[i][1]} # Expliquer
                # Le dernier sommet d'une même classe de sommets ne pointe vers personne dans sa classe
                G_[v[length-1]] = {}
                G_2[v[length-1]] = {}
                G_3[v[length-1]] = {}

    for a in arcs:  # On lie les sommets de classes différentes entre eux en tenant compte de l'intervalle imposé
                    # uniquement pour les arcs impliquant le sommet de départ ou le sommet d'arrivée
        condition = (a.u == start and a.t >= ts) or (a.v == end and a.t+a.l <= te) or (a.u != start and a.v != end)
        if condition:
            if (a.u,a.t) in G_.keys(): # Si (a.u,a.t) est bien une clé de G_ alors c'en est aussi une de G_2 et G_3
                # A chaque arc on associe son lambda a.l
                G_[(a.u,a.t)][(a.v,a.t+a.l)] = a.l
                G_2[(a.u,a.t)][(a.v,a.t+a.l)] = a.l
                G_3[(a.u,a.t)][(a.v,a.t+a.l)] = a.l
            else:
                G_[(a.u,a.t)] = {(a.v,a.t+a.l) : a.l}
                G_2[(a.u,a.t)] = {(a.v,a.t+a.l) : a.l}
                G_3[(a.u,a.t)] = {(a.v,a.t+a.l) : a.l}

    # Les graphes de type 1 et 4 etant les mêmes, on peut renvoyer directement ce qui suit.
    return (G_,G_2,G_3,G_)

def dijkstra(s_dep,graph):
    '''
    Application de l'algorithme de dijkstra sur le graphe graph à partir du sommet s_dep
    Renvoie les plus courts chemins à partir du sommet s_dep
    '''
    s_kw = { s_dep : [0,[s_dep]] } # Sommets décourverts
    s_unkw = { s : [inf,None] for s in graph if s != s_dep } # Sommets encore inconnus

    for s in graph[s_dep]:
        s_unkw[s] = [graph[s_dep][s],s_dep]

    while s_unkw and any(s_unkw[s][0] < inf for s in s_unkw):
        s = min(s_unkw,key=s_unkw.get) # On s'intéresse au sommet dont la valeur est la plus petite
        val_s, prev_s = s_unkw[s]
        for t in graph[s]:
            if t in s_unkw:
                new_val = val_s + graph[s][t]
                if new_val < s_unkw[t][0]:
                    s_unkw[t] = [new_val,s]
        # On est sur qu'on a découvert le plus court chemin jusqu'à s, on l'ajoute à la liste des sommets connus
        s_kw[s] = [val_s,s_kw[prev_s][1] + [s]]
        del s_unkw[s]

    return s_kw

def dijk_to_path(dijk_path):
    '''
    Convertit un chemin renvoyé par l'algorithme de Dijkstra à un chemin dans lequel
    chaque sous-sommet d'une même classe est unique. Pour des sommets d'une même classe,
    la priorité de conservation se fait de la droite vers la gauche.
    '''
    dijk_path.reverse()
    path = [(None,None)]
    for c in dijk_path:
        if c[0] != path[-1][0]:
            path += [c]
    path.reverse()
    return path[:-1]
