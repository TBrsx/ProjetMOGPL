from gurobipy import *

def type4(start,end,G,ts,te):
    '''
    Renvoie le plus court chemin de start à end en fonction du graphe G dans l'intervalle [ts,te]
    '''
    # avoid gurobi output messages
    env = Env(empty=True)
    env.setParam('OutputFlag', 0)
    env.start()

    sommets,arcs = G
    if start not in sommets or end not in sommets:
        return []

    a,b,c = pl(start,end,G,ts,te)

    lignes = range(len(a))
    colonnes = range(len(a[0]))

    m = Model("mogplex",env=env)

    x = []
    for i in colonnes:
        x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%d" % (i+1)))

    m.update()

    obj = LinExpr();
    obj = 0
    for j in colonnes:
        obj += c[j] * x[j]

    m.setObjective(obj,GRB.MINIMIZE)

    for i in lignes:
        m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)

    m.optimize()

    # Renvoie le chemin vide si il n'y a pas de solution
    try:
        m.objVal
    except:
        return []

    # Reconstruction du chemin
    sommets,arcs = G
    res = []
    for i in colonnes:
        if(x[i].x == 1):
            res += [arcs[i]]

    # Renvoie le chemin trié
    return sort(start, res)

def pl(start,end,G,ts,te):
    '''
    Renvoie le problème linéaire modélisé sur les 3 variables a,b et c
    où a représente la matrice des contraintes, b le second membre
    et c la fonction objectif
    '''
    a = matrice_contraite(start,end,G,ts,te)
    nbcont = len(a)
    b = [-1,-1] + [0]*(nbcont-2)
    sommets,arcs = G
    c = []
    for arc in G[1]:
        c += [arc.l]
    return a,b,c

def matrice_contraite(start,end,G,ts,te):
    '''
    Renvoie la matrice des contrainte construite à partir de start, end, G, ts et te
    '''
    sommets,arcs = G
    nbvar = len(arcs)
    a = [[0]*nbvar, [0]*nbvar]

    # On force au moins l'un des arcs sortant du sommet de départ
    # et au moins l'un des arcs entrant dans le sommet d'arrivée
    # à être emprunté (variable mise à 1)
    for i in range(nbvar):
        ar = arcs[i]
        if ar.u == start:
            if ar.t >= ts:
                a[0][i] = -1
            else:
                # Si la variable ne respecte pas l'intervalle on la force à être nulle
                line = [0]*nbvar
                line[i] = 1
                a += [line]
        if ar.v == end:
            if ar.t+ar.l <= te:
                a[1][i] = -1
            else:
                # Si la variable ne respecte pas l'intervalle on la force à être nulle
                line = [0]*nbvar
                line[i] = 1
                a += [line]

    # On ajoute les contraintes basiques sur tous les particuliers
    # Un arc ne peut être emprunté que si au moins un de ses arcs
    # parent l'a été sauf pour un arc d'origine le sommet de départ
    for i in range(nbvar):
        if(arcs[i].u != start):
            a += [contrainte(i,arcs)]

    return a

def contrainte(n,arcs):
    '''
    Crée la contrainte de la n-ième variable vis-à-vis des arcs parents empruntés
    '''
    nbvar = len(arcs)
    ar = arcs[n]
    cont = [0]*nbvar
    nb_pred = 0
    for i in range(nbvar):
        ar2 = arcs[i]
        if (ar2.v == ar.u):
            nb_pred += 1
            if(ar2.t + ar2.l <= ar.t): # Vérifie qu'il est possible de passer de l'arc parent à l'arc étudié
                cont[i] = -1
    if(nb_pred != 0):
        cont[n] = 1
    return cont

def sort(start,path):
    '''
    Trie un chemin d'arcs qui commence par le sommet start
    '''
    sorted_path = []
    for e in path:
        if e.u == start:
            sorted_path += [e]
            path.remove(e)
            break
    while path != []:
        v = sorted_path[-1].v
        for e in path:
            if e.u == v:
                sorted_path += [e]
                path.remove(e)
                break
    return sorted_path
