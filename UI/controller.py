import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleCreaGrafo(self, e):
        data1 = self._view._dpFrom.value
        data2 = self._view._dpTo .value

        if not data1 or not  data2:
            self._view.create_alert("Selezionare le DATE prima di creare il grafo.", color="red")
            return

        try:
            self._model.creaGrafo(data1, data2)
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()

            # Stampa immediata numero di vertici e archi (Punto 1.c)
            self._view._txt_result.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}",
                        color="green"))

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red")
            )
            # return
        self._view.update_page()



    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()
        # Verifica preventiva che il grafo sia stato creato
        if self._model.get_num_nodes() == 0 or self._model.get_num_edges() is None:
            self._view.create_alert("Creare prima il grafo!", color="red")
            return

        # A) Il regista con grado maggiore (numero di archi);
        reg_degree = self._model.getRegistaMaxDegree()
        self._view._txt_result.controls.append(
            ft.Text(f"Regista con grado maggiore: {reg_degree.name} "
              f"(grado: {self._model._grafo.degree(reg_degree)})", color="orange"))

        #B)  # Attore con somma dei pesi maggiore
        actor_weight, peso = self._model.getSumPesiArchiMax()
        self._view._txt_result.controls.append(
            ft.Text( f"Regista con somma pesi maggiore: {actor_weight.name} "
                f"(somma pesi: {peso})", color="orange") )

        #C) 5 ARCHI CON PESO MAGGIORE
        top5 = self._model.getTop5Archi()
        #self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f" 5 Archi di peso maggiore",color="green"))
        for arco in top5:
            self._view._txt_result.controls.append(ft.Text(f"{arco[0]}-->{arco[1]} (peso: {arco[2]["weight"]})"))
        self._view.update_page()


    def handleTrovaGruppo(self, e):
        pass

