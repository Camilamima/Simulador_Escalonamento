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
            tarefa.mutex_atual=self
        else:
            tarefa.status='suspensa_mutex'
            self.fila_espera.append(tarefa)

    
    def libera_mutex(self):
        if self.dono:
            self.dono.mutex_atual = None
            print("liberou mutex")  
        if self.fila_espera:
            # pega próxima tarefa
            prox = self.fila_espera.pop(0)
            print(f"tarefa {prox.id} assumiu o mutex {self.id}")

            self.dono = prox
            prox.mutex_atual = self
            self.dono.status = 'pronta'
        else:
            self.dono = None
            self.livre = True

