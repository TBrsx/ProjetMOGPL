from math import inf
from annexe import transform, dijkstra, dijk_to_path

# Algorithme principal
def algo(start,end,G,ts,te):
    '''
    Renvoie les 4 plus courts chemins du graphe G de start à end dans l'intervalle [ts,te]
    '''
    G_1,G_2,G_3,G_4 = transform(start,end,G,ts,te)

    p1 = sub_type1(start,end,G_1)
    p2 = sub_type2(start,end,G_2)
    p3 = sub_type3(start,end,G_3)
    p4 = sub_type4(start,end,G_4)

    return (p1,p2,p3,p4)

# Sous algorithmes pour l'algorithme principal
def sub_type1(start,end,G_):
    '''
    Renvoie le chemin d'arrivée au plus tôt de start à end dans le graphe transformé G_
    '''
    ### Initialisation
    # s_dep correspond au couple (sommet,t) où t a la plus petite valeur possible
    # Il correspond au sommet à partir lequel on va chercher les PCC
    s_dep = (start,inf)
    for k in G_.keys():
        if k[0] == start and k[1] < s_dep[1]:
            s_dep = k

    if s_dep[1] == inf:
        return []

    ### Shortest path algorithm
    # Dijkstra calcule les PCC
    paths = dijkstra(s_dep,G_)

    ### Explicit the shortest path
    # On récupère le chemin qui arrive au plus tot au sommet end
    path = []
    val = inf
    for s_arr,ch in paths.items():
        if s_arr[0] == end and s_arr[1] < val:
            path = ch[1]
            val = s_arr[1]

    # Renvoie le chemin sous forme plus lisible en supprimant les sommets inutiles
    return dijk_to_path(path)

def sub_type2(start,end,G_):
    '''
    Renvoie le chemin de départ au plus tard de start à end dans le graphe transformé G_
    '''
    ### Initialisation
    # s_dep correspond au couple (sommet,t) où t a la plus grande valeur possible
    s_dep = (start,-1)
    for k in G_.keys():
        if k[0] == start and k[1] > s_dep[1]:
            s_dep = k

    if s_dep[1] == -1:
        return []

    ### Shortest path algorithm
    # Dijkstra calcule les PCC
    paths = dijkstra(s_dep,G_)

    ### Explicit the shortest path
    # On récupère le chemin qui arrive au plus tard au sommet end
    path = []
    val = -1
    for s_arr,ch in paths.items():
        if s_arr[0] == end and s_arr[1] > val:
            path = ch[1]
            val = s_arr[1]

    # Lors de la conversion du chemin, c'est le sommet sommet de départ au plus tard réalisable qui est conservé
    return dijk_to_path(path)

def sub_type3(start,end,G_):
    '''
    Renvoie le chemin le plus rapide de start à end dans le graphe transformé G_
    '''
    ### Initialisation
    # s_dep correspond au couple (sommet,t) où t a la plus petite valeur possible
    s_dep = (start,inf)
    for k in G_.keys():
        if k[0] == start and k[1] < s_dep[1]:
            s_dep = k

    if s_dep[1] == inf:
        return []

    ### Shortest path algorithm
    # Dijkstra calcule les PCC
    paths = dijkstra(s_dep,G_)

    ### Excplicit the shortest path
    # On récupère le chemin qui a le plut petit coût total et qui arrive au sommet end
    path = []
    val = inf
    for s_arr,ch in paths.items():
        if s_arr[0] == end and ch[0] < val:
            path = ch[1]
            val = ch[0]

    # Renvoie le chemin sous forme plus lisible en supprimant les sommets inutiles
    return dijk_to_path(path)

def sub_type4(start,end,G_):
    '''
    Renvoie le plus court chemin de start à end dans le graphe transformé G_
    '''
    ### Initialisation
    # s_dep correspond au couple (sommet,t) où t a la plus petite valeur possible
    # Il correspond au sommet à partir du quel on va chercher les PCC
    s_dep = (start,inf)
    for k in G_.keys():
        if k[0] == start and k[1] < s_dep[1]:
            s_dep = k

    if s_dep[1] == inf:
        return []

    ### Shortest path algorithm
    # Dijkstra calcule les PCC
    paths = dijkstra(s_dep,G_)

    ### Explicit the shortest path
    # On récupère le chemin qui a le plut petit coût total et qui arrive au sommet end
    path = []
    val = inf
    for s_arr,ch in paths.items():
        if s_arr[0] == end and ch[0] < val:
            path = ch[1]
            val = ch[0]

    # Renvoie le chemin sous forme plus lisible en supprimant les sommets inutiles
    return dijk_to_path(path)

# Algorithmes secondaires
def type1(start,end,G,ts,te):
    G_ = transform(start,end,G,ts,te)[0]
    path = sub_type1(start,end,G_)
    return path

def type2(start,end,G,ts,te):
    G_ = transform(start,end,G,ts,te)[1]
    path = sub_type2(start,end,G_)
    return path

def type3(start,end,G,ts,te):
    G_ = transform(start,end,G,ts,te)[2]
    path = sub_type3(start,end,G_)
    return path

def type4(start,end,G,ts,te):
    G_ = transform(start,end,G,ts,te)[3]
    path = sub_type4(start,end,G_)
    return path
