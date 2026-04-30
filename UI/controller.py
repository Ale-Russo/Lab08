import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        self._view._txtOut.controls.clear()
        nerc_v = self._view._ddNerc.value
        nerc = self._idMap[nerc_v]
        maxY = int(self._view._txtYears.value)
        maxH = int(self._view._txtHours.value)
        (migliore, colpite, durata) = self._model.worstCase(nerc, maxY, maxH)
        self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {colpite}"))
        self._view._txtOut.controls.append(ft.Text(f"Tot hours of outage: {durata}"))
        for p in migliore:
            self._view._txtOut.controls.append(ft.Text(f"{p}"))

        self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
