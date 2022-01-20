from Arc import Arc

def str_to_arc(arc_str):
    '''
    Retourne l'arc associé à la chaine de caractère donnée en argument
    '''
    u,v,t,l = "","","",""
    i = 1
    while arc_str[i] != ',':
        u += arc_str[i]
        i += 1
    i += 1
    while arc_str[i] != ',':
        v += arc_str[i]
        i += 1
    i += 1
    while arc_str[i] != ',':
        t += arc_str[i]
        i += 1
    i += 1
    while arc_str[i] != ')':
        l += arc_str[i]
        i += 1
    return Arc(u,v,int(t),int(l))

def interp_file(path):
    '''
    Interprete le fichier passé en argument en renvoyant le graphe associé
    '''
    f = open(path,'r')
    n = int(f.readline())
    m = int(f.readline())
    sommets = []
    arcs = []
    # Pour les sommets
    for i in range(n):
        sommets += [f.readline()[:-1]]
    # Pour les arcs
    for i in range(m):
        arcs += [str_to_arc(f.readline())]
    f.close()
    return sommets, arcs

def interp_input():
    '''
    Construction du graphe depuis le terminal en demandant à l'utilisateur. Renvoie le graphe construit
    '''
    sommets = []
    arcs = []
    n = int(input("Nombre de sommets (int) : "))
    m = int(input("Nombre d'arcs (int) : "))
    # Récupération des sommets
    for i in range(n):
        s = input("Nom du sommet " + str(i) + " : ")
        sommets += [s]
    # Récupération des arcs
    for i in range(m):
        a = input("Arc " + str(i) + " (u,v,t,lambda) : ")
        arcs += [str_to_arc(a)]
    return sommets, arcs
