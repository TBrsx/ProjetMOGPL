from annexe import transform
from math import inf

#===== Les fonctions qui suivent n'ont pas été testées de manière exhaustives.
#===== Elles correspondent à la résolution des chemins type 1 et 2 en utilisant BFS
#===== On les donne ici comme bonus et traces de nos recherches

# Retrouve le noeud objectif étant donné le pseudo-arbre de BFS_Like()
def remonter_Rec(chemin,peres,depart,objectif):
    '''
    Retourne une liste de chemins inversés vers le noeud d'étiquette objectif, ou vide si pas de chemin
    '''
    listeChemins = []
    #Pour chaque ancetre du noeud donné en entrée, on crée n nouveau chemin avec le père comme suivant
    for r in peres[depart]:
        #Si on a atteint un noeud de départ
        if r[0]==objectif[0]:
            #Et qu'on ne l'avait pas déjà atteint
            if r[0] not in [c[0] for c in chemin]:
                #On l'ajoute au chemin
                chemin.append(r)
            #Le chemin est terminé on peut l'ajouter à la liste
            listeChemins.append(chemin)
        #On va continuer à construire le chemin à partir du chemin qu'on a crée + le père considéré
        else:
            if r[0] not in [c[0] for c in chemin]:
                newChemin = chemin+[r]
            else:
                newChemin = chemin
            res = remonter_Rec(newChemin,peres,r,objectif)
            #Si un chemin jusqu'au noeud de départ a été trouvé, on l'ajoute à la liste
            if res:
                listeChemins += res
    return listeChemins
#Le fonction est quasi identique à la fonction précédente,
#si ce n'est qu'au lieu de remonter de fils en père on descend de père en fils
def redescendre_Rec(chemin,fils,depart,objectif):
    '''
    Retourne un chemin vers le noeud d'étiquette objectif, ou vide si pas de chemin
    '''
    listeChemins = []
    for r in fils[depart]:
        if r[0]==objectif and r not in chemin:
            chemin.append(r)
            listeChemins.append(chemin)
        else:
            if r[0] not in [c[0] for c in chemin]:
                newChemin = chemin+[r]
            else:
                newChemin = chemin
                newChemin = [r if c[0]==r[0] else c for c in chemin]
            res = redescendre_Rec(newChemin,fils,r,objectif)
            if res:
                listeChemins += res
    return listeChemins


def BFS_Like(s_dep,index_end,graph,inverseMode=False):
    '''
    Finds the earliest s_end node and return a path to it
    (inverseMode = partir de la fin du trajet)
    '''
    #BFS où l'on sauvegarde les pères OU les fils de chaque noeud

    #Sens "normal", on descend et on sauvegarde les pères car on veut l'arrivée au plus tôt
    #Sens "inverse", on descend et on sauvegarde les fils car on veut le départ au plus tard
    peresOuFils,ouverts,interets = {s_dep:[]},[s_dep],[]
    index_dep = s_dep[0]
    if inverseMode:
        interets.append(s_dep)
    while ouverts:
        pere = ouverts.pop()
        fils = [f for f in graph[pere]]
        if fils :
            for f in fils :
                if inverseMode :
                    if pere in peresOuFils :
                        peresOuFils[pere].append(f)
                    else :
                        peresOuFils[pere] = [f]
                else :
                    if f in peresOuFils :
                        peresOuFils[f].append(pere)
                    else:
                        peresOuFils[f] = [pere]
                ouverts.append(f)
                if inverseMode :
                    if f[0] == index_dep and f not in interets :
                        interets.append(f)
                else :
                    if f[0] == index_end and f not in interets:
                        interets.append(f)
        if not fils and inverseMode :
            peresOuFils[f] = []

    # "Remonte" l'arbre à partir des objectifs à l'aide la fonction auxiliaire remonter_rec
    # Dans le cas inverse_mode, "redescend" à l'aide de la fonction auxilaire redescendre_rec

    while interets:
        chemin = []
        #Récupérer le noeud qui nous intéresse
        if inverseMode :
            #Le départ au plus tard
            chemin.append(max(interets,key= lambda t: t[1]))
            interets.remove(chemin[-1])
            #Construire la liste des chemins possibles
            res = redescendre_Rec(chemin,peresOuFils,chemin[-1],index_end)
        else :
            #L'arrivée au plus tôt
            chemin.append(min(interets,key= lambda t: t[1]))
            interets.remove(chemin[-1])
            #Construire la liste des chemins possibles
            res = remonter_Rec(chemin,peresOuFils,chemin[-1],s_dep)
        #Traiter la liste pour obtenir le chemin ayant le moins d'étapes + la mettre en ordre
        if res :
            minres = min(res,key=len)
            if not inverseMode : #On a construit à l'envers, il faut donc inverser le résultat
                minres.reverse()
            return minres
    print("Aucun chemin trouvé !")
    return []

def type1(start,end,G,ts,te):
    '''
    Returns the shortest path (type1) from start to end
    '''
    #Transforme G en G_ selon la méthode de tranformation dans l'énoncé
    G_ = transform(start,end,G,ts,te)[0]
    #Récupération du noeud de départ
    s_dep = (start,inf)
    for k in G_.keys():
        if k[0] == start and k[1] < s_dep[1]:
            s_dep = k
    #Calcul du chemin
    return BFS_Like(s_dep, end, G_,False)

def type2(start,end,G,ts,te):
    '''
    Returns the shortest path (type2) from start to end
    '''
    #Transforme G en G_ selon la méthode de transformation dans l'énoncé
    G_ = transform(start,end,G,ts,te)[0]
    #Récupération du noeud de départ
    s_dep = (start,inf)
    for k in G_.keys():
        if k[0] == start and k[1] < s_dep[1]:
            s_dep = k
    #Calcul du chemin
    return BFS_Like(s_dep, end, G_,True)
