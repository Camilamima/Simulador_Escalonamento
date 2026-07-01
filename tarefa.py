
class tarefa: #Simula a TCB do sistema operacional
    def __init__(self,id,cor,ingresso,prioridade,duracao,quantum,alfa):
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

    def reseta_quantum(self):
        self.quantum_atual=0
        if(self.cpu is not None):
            self.cpu.tarefa_atual=None
            self.cpu=None
        self.status='pronta'

    def incrementa_passo(self):
        self.duracao-=1
        self.quantum_atual+=1

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