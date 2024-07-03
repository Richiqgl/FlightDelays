from modello.model import Model
import networkx as nx
myModel=Model()
myModel.buildGraph(5)
myModel.printGraphDetails()
v0=myModel.getAllNodes()[0]
connessa=list(nx.node_connected_component(myModel._grafo,v0))
v1=connessa[10]
pathD=myModel.trovoCamminov1(v0,v1)
pathBFS=myModel.trovaCamminov2(v0,v1)
pathDFS=myModel.trovaCamminov3(v0,v1)
print("---------------")
print("Metodo dijstra")
print(*pathD, sep="\n")
print("----------------")
print(*pathBFS,sep="\n")
#cammino con il numero minore
print("----------------")
print(*pathDFS,sep="\n")
#cammino con il numero maggiore
print("************************************")
print("************************************")
bestPath,bestScore=myModel.getCamminoOttimo(v0,v1,3)
print(f"Cammino ottimo ha peso={bestScore}")
print(*bestPath,sep="\n")