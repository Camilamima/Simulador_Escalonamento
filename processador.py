class processador:
    def __init__(self,id):
        self.id=id
        self.ociosidade=0
        self.status=0 #0 para para ocioso 1 para ocupado

    def set_status(self,j):
        self.status=j