import algo as d # algorithmes basés sur Dijkstra
import recherches_BFS as b # algorithmes basés sur BFS
import gurobi as g # algorithmes basés sur Gurobi
from interp import interp_file
from os import listdir
import matplotlib.pyplot as plt
from time import time

################################################################################

def measure(fun,test):
    '''
    Renvoie le temps d'execution de la fonction fun
    '''
    start,end,ts,te,name = test
    G = interp_file(name)
    print(name)
    t = time()
    fun(start,end,G,ts,te)
    return time() - t

def performance(fun,list_test):
    '''
    Calcul l'efficacite de la fonction fun sur une liste de tests
    Renvoie une liste des temps chronométrés
    '''
    perf = []
    for test in list_test:
        perf += [measure(fun,test)]
    return perf

def list_test(start,end,ts,te,path):
    names = listdir(path)
    names.sort(key=int)
    tests = []
    ord = []
    for n in names:
        ord += [int(n)]
        tests += [(start,end,ts,te,path+n)]
    return ord,tests

################################################################################

path_to_graphs = "../graphs_arcs/" # Ne pas oublier le / à la fin
symb = "--"

start = '0'
end = '2'
ts = -1
te = 1000
ord,tests = list_test(start,end,ts,te,path_to_graphs)

perfDA = performance(d.algo,tests)
# perfDT1 = performance(d.type1,tests)
# perfDT2 = performance(d.type2,tests)
# perfDT3 = performance(d.type3,tests)
# perfDT4 = performance(d.type4,tests[:15])
#
# perfGT4 = performance(g.type4,tests[:15])
#
# perfBT1 = performance(b.type1,tests[:13])
# perfBT2 = performance(b.type2,tests)

plt.plot(ord,perfDA,symb)

# plt.legend(["DT1", "BT1"])
plt.xlabel("Nombre d'arcs pour 25 sommets")
plt.ylabel("Temps (s)")
plt.set_yscale('log')
plt.title("Algorithme des 4 chemins")

plt.show()
