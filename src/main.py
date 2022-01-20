import algo as d # algorithmes basés sur Dijkstra
import recherches_BFS as b # algorithmes basés sur BFS
import gurobi as g # algorithmes basés sur Gurobi
from interp import interp_file, interp_input

graph_name = 'diff.txt'
start = 'A'
end = 'C'
ts = 0
te = 20

G = interp_file('../graphs/' + graph_name)

dt1,dt2,dt3,dt4 = d.algo(start,end,G,ts,te)
print("Dijkstra type1 :", dt1)
print("Dijkstra type2 :", dt2)
print("Dijkstra type3 :", dt3)
print("Dijkstra type4 :", dt4)

gt4 = g.type4(start,end,G,ts,te)
print("Gurobi type4 :", gt4)

bt1 = b.type1(start,end,G,ts,te)
bt2 = b.type2(start,end,G,ts,te)
print("BFS type1 :", bt1)
print("BFS type2 :", bt2)
