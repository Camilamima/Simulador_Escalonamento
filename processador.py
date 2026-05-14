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
            self.ociosidade=1#caso processador esteja ocioso, marca como ocioso e retorna
            return
        self.ociosidade=0#marca o processador como ocupado
        Ggrafico.desenhar_retangulo(tempo,self.tarefa_rodando.id,self.tarefa_rodando.cor, self.id)
        self.tarefa_rodando.duracao-=1#decrementa a duração da tarefa atual
        self.quantum_atual+=1#incrementa o quantum atual do processador
        if self.quantum_atual % self.quantum == 0:
            self.reseta_quantum_atual()
        if(self.tarefa_rodando.duracao==0):#finaliza a tarefa caso sua duração chegue a 0
            self.tarefa_rodando.status='finalizada'
            self.tarefa_rodando= None
            self.reseta_quantum_atual()
            
