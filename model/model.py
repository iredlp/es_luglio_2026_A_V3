
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMapR = {}

    def creaGrafo(self, data1, data2):
        self._grafo.clear()
        self._idMapR.clear()

        registi = DAO.getAllNodes(data1, data2)
        for a in registi:
            self._idMapR[a.id] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")
    # self._grafo.add_nodes_from(movie)

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

