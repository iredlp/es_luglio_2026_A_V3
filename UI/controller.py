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

            self.fillDDRegisti()

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


    def fillDDRegisti(self):
        try:

            registi= self._model.getRegistiGrafo()
            for y in registi:
                self._view._ddDirector.options.append(ft.dropdown.Option(
                    key=y.id,
                    text=y.name))

            self._view.update_page()

        except Exception as ex:
            self._view._txt_result.controls.append(ft.Text(f"Errore nel recupero dei registi: {ex}", color="red") )
            self._view.update_page()

    def handleTrovaGruppo(self, e):
        self._view._txt_result.controls.clear()
        k = self._view._txtInN.value
        # qui dovremmo fare i solti controlli sulla validità

        try:
            kInt = int(k)
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire un intero per procedere: {ex}", color="red")
            )
            self._view.update_page()
            return
        if kInt <= 0:
            self._view.create_alert(
                "N deve essere un intero positivo.", color="red")
            return

        # recupero il regista selezionato dal Dropdown
        start_node = self._model._idMapR[self._view._ddDirector.value]

        if self._view._ddDirector.value is None:
            self._view.create_alert("Selezionare prima un REGISTA di partenza.", color="red")
            return

        listRegisti, bestScore = self._model.getGruppoRegisti(start_node, kInt)

        if  listRegisti is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(
                f"Non ci sono abbastanza comoonenti connesse per trovare N registi", color="red"))
            return

        # Ordino i registi in ordine alfabetico
        listRegisti.sort(key=lambda r: r.name)

        self._view._txt_result.controls.clear()
        # Stampo le informazioni complessive del gruppo
        self._view._txt_result.controls.append(
            ft.Text(f"Numero totale di registi: {len(listRegisti)}", color="orange")
        )

        self._view._txt_result.controls.append(
            ft.Text(f"Incasso complessivo del gruppo: {bestScore:,.2f}", color="orange")
        )

        self._view._txt_result.controls.append(ft.Text(
            f" Di seguito il Gruppo di N registi ADIACENTI, massimizzando il numero di incassi:", color="green"))
        # Stampo le informazioni di ogni regista
        for regista in listRegisti:
            numeroFilm = len(regista.film)
            incasso = self._model._scoreRegista(regista)

            self._view._txt_result.controls.append(
                ft.Text( f"{regista.name} - Film diretti: {numeroFilm} - "
                    f"Incasso totale: {incasso:,.2f}"
                )
            )

        self._view.update_page()


