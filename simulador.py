import gerenciador_grafico as gg
import tarefa as tf
import copy 

class simulador:
    ##iniciação de variaveis
    def __init__(self):
        self.tarefas = []
        self.cria_tarefas()
        self.Ggrafico = gg.gerenciador_grafico()
    #inicializador
    def iniciar(self):
        #self.cria_tarefas()
        #self.Ggrafico.atualizar()
        self.simulador_grafico()
        self.Ggrafico.janela.mainloop()
    ##Aqui que a mágica acontece
    def simulador_grafico(self):
        tempo=0
        esc='SRTF'
        cpu=2
        cores_terefas = ['blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'pink']
        # Fila local independente para não corromper self.tarefas
        fila = copy.deepcopy(self.tarefas)
        
        # Roda a simulação enquanto ainda houver tarefas a processar
        while fila:
            self.Ggrafico.desenhar_palavra(str(tempo),(tempo*50)+50,550,10)#desenha os números
            
            # Identifica tarefas que já chegaram no tempo atual
            tarefas_prontas = [t for t in fila if t.ingresso <= tempo]
            
            if tarefas_prontas:
                tarefas_prontas.sort(key=lambda t: t.duracao)##Organiza lista por duracao (SRTF)
                
                # Percorre o vetor de tarefas prontas
                for i, iterador in enumerate(tarefas_prontas):
                    #Tarefa de maior prioridade assume a CPU caso haja uma disponível.
                    #Maior prioridade é definida pela ordem da tarefa na lista de prontas,
                    #ou seja, se houver 4 cpus disponíveis, as 4 primeiras tarefas da 
                    # lista de prontas serão executadas nesse mesmo ciclo
                    if i < cpu: 
                        iterador.status="Rodando"
                        iterador.cor=cores_terefas[iterador.id % len(cores_terefas)]
                        self.Ggrafico.desenhar_retangulo((tempo*50)+50,550-(iterador.id*50),(tempo*50)+100,500-(iterador.id*50), iterador.cor)
                        iterador.duracao-=1
                    else:
                        iterador.status="Ocioso"
                        self.Ggrafico.desenhar_retangulo((tempo*50)+50,550-(iterador.id*50),(tempo*50)+100,500-(iterador.id*50),'white')
                    print(f"Tempo: {tempo} | Tarefa: {iterador.id} | Status: {iterador.status} | Duracao Restante: {iterador.duracao}")
            
            fila = [t for t in fila if t.duracao > 0]##Refaz a fila baseado nas tarefas que ainda tem duração restante
            tempo+=1



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
