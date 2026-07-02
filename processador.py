import gerenciador_grafico as gg
class processador:
    def __init__(self,id,qt):
        self.id=id
        self.ociosidade=0
        self.status=0
        self.quantum=qt
        self.quantum_atual=0
        self.tarefa_rodando=None
        
    def executar(self,Ggrafico,tempo):

        if self.tarefa_rodando is None:
            self.ociosidade=1#caso processador esteja ocioso, marca como ocioso e retorna
            return
        self.ociosidade=0#marca o processador como ocupado
        Ggrafico.desenhar_retangulo(tempo,self.tarefa_rodando.id,self.tarefa_rodando.cor, self.id)
        if self.tarefa_rodando.mutex_atual is not None:
            Ggrafico.desenhar_tag_mutex(tempo, self.tarefa_rodando.id, self.tarefa_rodando.mutex_atual.id)
        self.tarefa_rodando.incrementa_passo()
        self.quantum_atual+=1
        if self.tarefa_rodando.verifica_quantum==1:
            self.quantum_atual=0
            self.tarefa_rodando==None
        if(self.tarefa_rodando.duracao==0):#finaliza a tarefa caso sua duração chegue a 0
            Ggrafico.desenhar_fim(tempo, self.tarefa_rodando.id)
            self.quantum_atual=0
            self.tarefa_rodando.status='finalizada'
            self.tarefa_rodando.cpu=None
            self.tarefa_rodando= None
            
