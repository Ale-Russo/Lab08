from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()



    def worstCase(self, nerc, maxY, maxH):
        self._solBest = []
        self.loadEvents(nerc)
        self.ricorsione([], maxY, maxH,0)
        colpite = self.nPersone_colpite(self._solBest)
        durata = self.durataEventi(self._solBest)
        return self._solBest, colpite, durata

    def ricorsione(self, parziale, maxY, maxH, pos):
        if (pos == len(self._listEvents)):
            persone_correnti = self.nPersone_colpite(parziale)
            record_persone = self.nPersone_colpite(self._solBest)
            if (persone_correnti > record_persone):
                self._solBest = list(parziale)
            return
        else:
            self.ricorsione(parziale, maxY, maxH, pos + 1)

            evento_corrente = self._listEvents[pos]

            diff = evento_corrente.date_event_finished - evento_corrente.date_event_began
            durata_nuovo = diff.total_seconds() / 3600

            sfora_anni = False
            if len(parziale) > 0:
                anni = [p.date_event_began.year for p in parziale]
                anni.append(evento_corrente.date_event_began.year)

                if (max(anni) - min(anni)) > maxY:
                    sfora_anni = True

            if (self.durataEventi(parziale) + durata_nuovo) <= maxH and not sfora_anni:
                parziale.append(evento_corrente)
                self.ricorsione(parziale, maxY, maxH, pos + 1)
                parziale.pop()


    def nPersone_colpite(self,parziale):
        count=0
        for p in parziale:
            count+=p._customers_affected
        return count

    def durataEventi(self,parziale):
        count=0
        for p in parziale:
            diff = p._date_event_finished - p._date_event_began
            count += diff.total_seconds() / 3600
        return count

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc