import gerenciador_grafico as gg
class processador:
    def __init__(self,id,qt):
        self.id=id
        self.status=0 #0 para para ocioso 1 para ocupado
        self.quantum=qt
        self.quantum_atual=0
        self.flag_q=0
        self.tarefa_rodando=None

    def reseta_quantum_atual(self):
        self.quantum_atual=0
        self.flag_q=0

    def incrementa_quantum(self):
        if self.flag_q==1:
            self.flag_q=0
        else:
            self.quantum_atual+=0

    def executar(self,Ggrafico,tempo):
        if self.tarefa_rodando is None:
            return
        Ggrafico.desenhar_retangulo(tempo,self.tarefa_rodando.id,self.tarefa_rodando.cor)
        self.tarefa_rodando.duracao-=1
        self.quantum_atual+=1
        if(self.tarefa_rodando.duracao==0):
            self.tarefa_rodando.status='Finalizado'
            self.tarefa_rodando= None
            self.reseta_quantum_atual()
