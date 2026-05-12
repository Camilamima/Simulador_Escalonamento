import gerenciador_grafico as gg
import tarefa as tf
import copy 

class simulador:
    ##inicialização de variaveis
    def __init__(self):
        self.tarefas = []
        self.cpu=2
        self.escalonador=''
        self.quantum=2
        self.cria_tarefas()
        self.Ggrafico = gg.gerenciador_grafico()
    #inicializador
    def iniciar(self):
        #self.cria_tarefas()
        #self.Ggrafico.atualizar()
        self.simulador_grafico()
        self.Ggrafico.janela.mainloop()

    def simulador_grafico(self):
        tempo=0
        #Fila local independente para manipulação
        fila = copy.deepcopy(self.tarefas)
        
        #Roda a simulação enquanto ainda houver tarefas a processar
        while fila:
            self.Ggrafico.desenhar_palavra(tempo,10)#desenha os números
            
            #Identifica tarefas que já chegaram no tempo atual
            #tarefas_prontas = [t for t in fila if t.ingresso <= tempo]
            tarefas_prontas = []
            for tarefa in fila:
                if tarefa.ingresso <= tempo:
                    tarefas_prontas.append(tarefa)
                    quantum_Atual=self.quantum
            if tarefas_prontas:
                if quantum_Atual == self.quantum and self.escalonador == "priop":##Organiza lista por prioridade (PRIOP)
                    tarefas_prontas.sort(key=lambda t: (-t.prioridade, t.status=="Rodando", t.ingresso, t.duracao))
                    quantum_Atual=0
                elif quantum_Atual == self.quantum and self.escalonador == "srtf":##Organiza lista por duracao (SRTF)
                    tarefas_prontas.sort(key=lambda t: (t.status=="Rodando",t.duracao,t.ingresso))
                    quantum_Atual=0
                #Percorre o vetor de tarefas prontas
                for i, iterador in enumerate(tarefas_prontas):
                    #Tarefa de maior prioridade assume a CPU caso haja uma disponível.
                    #Maior prioridade é definida pela ordem da tarefa na lista de prontas,
                    #ou seja, se houver 4 cpus disponíveis, as 4 primeiras tarefas da 
                    #lista de prontas serão executadas nesse mesmo ciclo
                    if i < self.cpu: 
                        iterador.status="Rodando"
                        self.Ggrafico.desenhar_retangulo(tempo,iterador.id,iterador.cor)
                        iterador.duracao-=1
                        if iterador.duracao == 0:
                            quantum_Atual=self.quantum-1
                    else:
                        iterador.status="Ocioso"
                        self.Ggrafico.desenhar_retangulo(tempo,iterador.id,'white')            
            fila = [t for t in fila if t.duracao > 0]##Refaz a fila baseado nas tarefas que ainda tem duração restante
            tempo+=1
            quantum_Atual+=1

    def cria_tarefas(self):
        try:
            with open('srtf.txt', 'r') as f:
                linhas = f.readlines()
                for i, linha in enumerate(linhas):
                    linha = linha.strip().lower()
                    if not linha:  # Pula linhas em branco
                        continue 
                    if i == 0: # se for a primeira linha,preenche os parâmetros do simulador
                        cabecalho = linha.split(';')
                        if len(cabecalho) >= 3:
                            self.escalonador = cabecalho[0]
                            self.quantum = int(cabecalho[1])
                            self.cpu = int(cabecalho[2])
                        continue 
                    valores = linha.split(';')
                    if len(valores) >= 5:
                        id_tarefa = int(valores[0])
                        cor = valores[1]
                        ingresso = int(valores[2])
                        duracao = int(valores[3]) 
                        prioridade = int(valores[4])
                        
                        # Construtor de tarefa: id, cor, ingresso, prioridade, duracao
                        nova_tarefa = tf.tarefa(id_tarefa, cor, ingresso, prioridade, duracao)
                        self.tarefas.append(nova_tarefa)
        except FileNotFoundError:
            print("Arquivo não encontrado.")
