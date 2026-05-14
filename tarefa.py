
class tarefa: #Simula a TCB do sistema operacional
    def __init__(self,id,cor,ingresso,prioridade,duracao):
        self.id=id
        self.cor=cor
        self.ingresso=int(ingresso)
        self.prioridade=prioridade
        self.duracao=int(duracao)
        self.ociosidade=0
        self.status="nova"

    def set_status(self,j):
        self.status=j