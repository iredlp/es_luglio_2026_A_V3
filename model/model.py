
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
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

        for a in registi:
            a.film.clear()
            film = DAO.getFilmPerRegista(a.id, data1, data2)
        #print("3 - Cast caricato:", len(film))

            for row in film:
                a.film.append((row[0], row[1], row[2]))
        print("4 - Film aggiunti ai registi")

        # SE NON AVESSI USATO LE TUPLE, MA SOLO ROW NEL DAO
        # actor = self._idMapA[row["name_id"]] #recupero dall'idMap
        # actor.movies.append(
        #   (row["title"], row["year"], row["avg_rating"]))

        for i in  range(len(registi)): #NON POSSO ACCEDERE DIRETTAMENTE, perchè movie è una lista!
            r1 = registi[i]
            generi1 = {film[1] for film in r1.film}
            for j in range(i + 1,len(registi )):
                r2 = registi[j]


                generi2 = {film[1] for film in r2.film}

                generi_comuni = generi1 & generi2
                peso = len(generi_comuni)

                if peso > 0:
                    self._grafo.add_edge(r1, r2, weight=peso)

       # print("5 - Archi creati:", self._grafo.number_of_edges())


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    # GRADO MAX
    def getRegistaMaxDegree(self):
        return max(self._grafo.nodes, key=lambda a: (self._grafo.degree(a), a.name))

    def getSumPesiArchiMax(self):
        # Lista di tuple: (Prodotto, score)
        classifica = []

        for nodo in self._grafo.nodes:
            # Somma dei pesi degli archi
            peso = sum(d["weight"] for u, v, d in self._grafo.edges(nodo, data=True))

          #  peso += sum(d["weight"]
              #  for u, v, d in self._grafo.out_edges(nodo, data=True))
            classifica.append((nodo, peso))

        # Ordiniamo in ordine decrescente di score
        classifica.sort(key=lambda x: x[1], reverse=True)
        return classifica[0]

    def getTop5Archi(self):
        return sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:5]


