import gerenciador_grafico as gg
import tarefa as tf
import copy 

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
        esc='SRTF'
        cpu=1
        tf.queue = copy.deepcopy(self.tarefas)
        while True:
            tarefas_faltantes=0
            self.Ggrafico.desenhar_palavra(str(tempo),(tempo*50)+50,550,10)
            if esc == 'SRTF':
                tf.queue.sort(key=lambda t: t.duracao)
            for i, interator in enumerate(tf.queue):
                if interator.status == "Não iniciado" and interator.ingresso >= tempo:
                    interator.status = "Ocioso"
                if interator.duracao==0:
                    interator.status = "Finalizada"
                if(i<cpu and interator.status in ["Ocioso","Rodando"]):
                    interator.status="Rodando"
                if (i>= cpu and interator.status in ["Ocioso","Rodando"]):
                    interator.status="Ocioso"
                print("tempo:",tempo)
                print("Tarefa:",interator.id)
                print("Status:",interator.status)
                print("Duracao:",interator.duracao)
                if interator.status=="Rodando":
                    self.Ggrafico.desenhar_retangulo((tempo*50)+50,550-(interator.id*50)
                                                     ,(tempo*50)+100,500-(interator.id*50),'blue')
                    tarefas_faltantes+=1
                    interator.duracao-=1
                if interator.status=="Ocioso":
                    self.Ggrafico.desenhar_retangulo((tempo*50)+50,550-(interator.id*50)
                                                     ,(tempo*50)+100,500-(interator.id*50),'white')
                    tarefas_faltantes+=1
            tf.queue[:] = [t for t in tf.queue if t.status != "Finalizada"]
            tempo+=1
            if not tf.queue:
                break



    def cria_tarefas(self):
        i=1
        while True:
            #cor = input(f"coloque a cor da tarefa {i}: ")
            ingresso=input(f'coloque o ingresso da tarefa {i}: ')
            duracao=input(f'coloque a duracao da tarefa {i}: ')
            #prioridade=input('prioridade')
            tarefa = tf.tarefa(i,'red', ingresso, 0,duracao)
            self.tarefas.append(tarefa)
            i+=1
            x=input('Digite 3 para sair').strip()
            if x=='3':
                break

