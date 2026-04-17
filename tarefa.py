
class tarefa:
    def __init__(self,id,cor,ingresso,prioridade,duracao):
        self.id=id
        self.cor=cor
        self.ingresso=int(ingresso)
        self.prioridade=prioridade
        self.duracao=int(duracao)
        self.status="Não iniciado" #1 para não iniciado, 2 para ociosos 3 para rodando

    def set_status(self,j):
        self.status=j