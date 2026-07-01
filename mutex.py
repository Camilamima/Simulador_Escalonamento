class Mutex:
    def __init__(self,id):
        self.id=id
        self.livre = True
        self.dono = None
        self.fila_espera = []

    def solicita_mutex(self,tarefa):
        if self.livre == True:
            self.livre=False
            self.dono=tarefa
        else:
            tarefa.status='suspensa'
            self.fila_espera.append(tarefa)

    def libera_mutex(self,tarefa):
        if self.fila_espera:
            prox=self.fila_espera.pop(0)
            self.dono=prox
            self.dono.status='pronta'
        else:
            self.dono=None
            self.livre=True

