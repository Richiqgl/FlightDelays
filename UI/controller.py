import flet as ft
from UI.view import View
from modello.model import Model
class Controller:
    def __init__(self, view:View, model:Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAeroportoP = None
        self._choiceAeroportoA = None

    def handelAnalizza(self, e):
        nMinStr = self._view._txtInNumC.value
        try:
            nMin = int(nMinStr)
        except ValueError:
            self._view._txt_result.controls.append(
                ft.Text("Il valore inserito nel campo nMin non è un intero."))
            self._view.update_page()
            return

        self._model.buildGraph(nMin)

        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato. "))
        self._view._txt_result.controls.append(
            ft.Text(f"Num nodi:{self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Num archi:{self._model.getNumArchi()}"))
        self._view._ddAeroportoP.disabled = False
        self._view._ddAeroportoA.disabled = False
        self._view._btnConnessi.disabled = False
        self._view._btnPercorso.disabled = False
        self.fillDD()
        self._view.update_page()


    def handleConnessi(self, e):
        if self._choiceAeroportoP is None:
            self._view._txt_result.controls.append(ft.Text(f"Selezionare un aeroporto di partenza"))
            return
        v0 = self._choiceAeroportoP
        vicini =  self._model.getSortedVicini(v0)

        self._view._txt_result.controls.append(ft.Text(f"Ecco i vicini di {v0}"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))

        self._view.update_page()

    def handleTestConnessione(self, e):
        v0=self._choiceAeroportoP
        v1=self._choiceAeroportoA
        self._view._txt_result.controls.clear()

        #verificare che ci sia un percorso
        if not self._model.esistePercorso(v0,v1):
            self._view._txt_result.controls.append(ft.Text(f"Non esiste un percorso tra {v0} e {v1}"))
            self._view.update_page()
            return
        else:
            self._view._txt_result.controls.append(ft.Text(f"Trovato un percorso tra {v0} e {v1}"))
        #trovare un percorso possibile
        path=self._model.trovaCamminov2(v0,v1)
        self._view._txt_result.controls.append(ft.Text(f"Il cammino con il minor numero di nodi tra {v0} e {v1}"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(p))
        self._view.update_page()
        self._view._txtInNumTratte.disabled=False
        self._view._btnCercaItinerario.disabled=False
        print(f"handleTestConnessione called")

    def handleCercaItinerario(self,e):
        v0 = self._choiceAeroportoP
        v1 = self._choiceAeroportoA
        t=self._view._txtInNumTratte.value
        try:
            tInt=int(t)
        except ValueError:
            self._view.create_alert("Valore inerito non è un numero")
            self._view.update_page()
            return
        path=self._model.getCamminoOttimo(v0,v1,tInt)
        self._view._txt_result.controls.append(f"il percorso ottimo tra {v0} e {v1} è")
        for p in path:
            self._view._txt_result.controls.append(ft.Text(p))
        self._view._txt_result.controls.append(ft.Text(f"Numero voli {len(path)-1}"))
        self._view.update_page()
        #print(f"handleCercaItinerario called")

    def fillDD(self):
        allNodes = self._model.getAllNodes()
        for n in allNodes:
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(
                    data= n,
                    on_click=self.readDDAeroportoP,
                    text=n.AIRPORT
                ))
            self._view._ddAeroportoA.options.append(
                ft.dropdown.Option(
                    data=n,
                    on_click=self.readDDAeroportoA,
                    text=n.AIRPORT
                ))

    def readDDAeroportoP(self, e):
        if e.control.data is None:
            self._choiceAeroportoP = None
        else:
            self._choiceAeroportoP = e.control.data
        print(f"readDDAeroportoP called -- {self._choiceAeroportoP}")

    def readDDAeroportoA(self, e):
        if e.control.data is None:
            self._choiceAeroportoA = None
        else:
            self._choiceAeroportoA = e.control.data
        print(f"readDDAeroportoA called -- {self._choiceAeroportoA}")