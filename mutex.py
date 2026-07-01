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
        if self.fila_espera:
            print(f"tarefa {self.dono.id} liberou o mutex {self.id}")
            # libera o dono atual

            # pega próxima tarefa
            prox = self.fila_espera.pop(0)
            print(f"tarefa {self.id} assumiu {self.mutex_atual.id}")

            self.dono = prox
            prox.mutex_atual = self
            self.dono.status = 'pronta'  # ou 'pronta' dependendo da sua lógica
            
        else:
            if self.dono:
                self.dono.mutex_atual = None

            self.dono = None
            self.livre = True

