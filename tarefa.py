
class tarefa: #Simula a TCB do sistema operacional
    def __init__(self,id,cor,ingresso,prioridade,duracao,quantum,alfa,io):
        self.id=id
        self.cor=cor
        self.ingresso=int(ingresso)
        self.prioridade=prioridade
        self.duracao=int(duracao)
        self.ociosidade=0
        self.status="nova"
        self.quantum=quantum
        self.quantum_atual=0
        self.prioridade_v=prioridade
        self.cpu=None
        self.alfa=int(alfa)
        self.mutex_info=[]
        self.rodado=0
        self.mutex_atual=None
        self.io=io
        self.tempoexec=0

    def reseta_quantum(self):
        self.quantum_atual=0
        if(self.cpu is not None):
            self.cpu.tarefa_atual=None
            self.cpu=None
        self.status='pronta'

    def incrementa_passo(self):
        self.duracao -= 1
        self.quantum_atual += 1
        self.rodado += 1
        self.tempoexec += 1
        if self.mutex_atual is not None:
            print(self.mutex_atual.id)
            for i in self.mutex_info:
                if i["id"] == self.mutex_atual.id:

                    i["fim"] -= 1  # tempo restante no mutex
                    print(f"{i['fim']} para o fim do mutex atual({self.mutex_atual.id}) da tarefa {self.id}: {i['fim']}")
                    print('AOOO POTENCIA')
                    if i["fim"] == 0:
                        print(f"tarefa {self.id} liberou o mutex {self.mutex_atual.id}")
                        self.mutex_atual.libera_mutex()
                        self.mutex_atual = None

                    break


    def verifica_quantum(self):
        if self.quantum_atual==self.quantum:
            self.reseta_quantum
            return 1
        else:
            return 0
        
    def incrementa_prioridade(self):
        self.prioridade_v = self.prioridade + (self.ociosidade * self.alfa)


    def reseta_prioridade(self):
        self.prioridade_v=self.prioridade