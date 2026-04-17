import gerenciador_grafico as gg
import tarefa as tf

class simulador:
    def __init__(self):
        self.tarefas = []
        self.cria_tarefas()
        self.Ggrafico = gg.gerenciador_grafico()

    def iniciar(self):
        #self.cria_tarefas()
        #self.Ggrafico.atualizar()
        self.simulador_grafico()
        self.Ggrafico.janela.mainloop()
    
    def simulador_grafico(self):
        tempo=0
        tarefa_rodando=1
        while True:
            self.Ggrafico.desenhar_palavra(str(tempo),(tempo*100)+50,550,10)
            for id in self.tarefas:
                #dá pra virar um case when facil
                if(tempo==id.ingresso and id.ingresso=='Não iniciado'):
                    id.status='Ocioso'
                if(id.duracao==0 and tarefa_rodando== id.id):
                    id.status='Terminada'
                    tarefa_rodando+=1
                if(id.id==tarefa_rodando):
                    id.status='Rodando'
                    print(f"o id é {id.id}")
                if(id.status=='Rodando'):
                    self.Ggrafico.desenhar_retangulo((tempo*100)+50,550-(id.id*100)
                                                     ,(tempo*100)+150,450-(id.id*100),'blue')
                    id.duracao=id.duracao-1
                if(id.status=='Ocioso'):
                    self.Ggrafico.desenhar_retangulo((tempo*100)+50,550-(id.id*100)
                                                     ,(tempo*100)+150,450-(id.id*100),'white')
            if tarefa_rodando>len(self.tarefas):
                break
            tempo+=1



    def cria_tarefas(self):
        i=1
        while True:
            #cor = input(f"coloque a cor da tarefa {i}: ")
            ingresso=input(f'coloque o ingresso da tarefa {i}:')
            duracao=input(f'coloque a duracao da tarefa {i}')
            #prioridade=input('prioridade')
            tarefa = tf.tarefa(i,'red', ingresso, 0,duracao)
            self.tarefas.append(tarefa)
            i+=1
            x=input('Digite 3 para sair').strip()
            if x=='3':
                break

