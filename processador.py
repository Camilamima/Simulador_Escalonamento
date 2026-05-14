import gerenciador_grafico as gg
class processador:
    def __init__(self,id,qt):
        self.id=id
        self.ociosidade=0
        self.status=0
        self.quantum=qt
        self.quantum_atual=0
        self.tarefa_rodando=None

    def reseta_quantum_atual(self):
        self.quantum_atual=0
        
    def executar(self,Ggrafico,tempo):
        if self.tarefa_rodando is None:
            self.ociosidade=1
            return
        self.ociosidade=0
        Ggrafico.desenhar_retangulo(tempo,self.tarefa_rodando.id,self.tarefa_rodando.cor, self.id)
        self.tarefa_rodando.duracao-=1
        self.quantum_atual+=1
        if self.quantum_atual % self.quantum == 0:
            self.reseta_quantum_atual()
        if(self.tarefa_rodando.duracao==0):
            self.tarefa_rodando.status='Finalizado'
            self.tarefa_rodando= None
            self.reseta_quantum_atual()
            
