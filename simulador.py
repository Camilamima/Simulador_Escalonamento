import gerenciador_grafico as gg
import tarefa as tf
import copy
import tkinter as tk
import processador as pr
 
class simulador:
    def __init__(self): #inicialização de variáveis
        self.tarefas = []
        self.cpu=[]
        self.escalonador=''
        self.prontas=[]
        self.Ggrafico = gg.gerenciador_grafico()
        self.tempo = 0
        self.fila = [] 
        self.botao_passo = None
        self.botao_executar_tudo = None
        self.botao_retroceder = None
        self.botao_status = None
        self.historico_estados = []
        self.botao_modificar = []

    def iniciar(self):
        #Cria as tarefas a partir do arquivo de parâmetros
        self.cria_tarefas()
        #Faz uma cópia da fila original para manipulação durante a simulação, preservando os dados originais
        self.fila = copy.deepcopy(self.tarefas)

        #Desenha o gráfico inicial com as tarefas a serem simuladas
        self.Ggrafico.desenhar_grafico(self.fila)

        #Salva o estado inicial para permitir retroceder ao início
        self.salvar_estado_atual()

        #Botão para retroceder passo
        self.botao_retroceder = tk.Button(self.Ggrafico.control_frame, text="Retroceder Passo", command=self.retroceder_passo, state="disabled")
        self.botao_retroceder.pack(side=tk.RIGHT, padx=10)

        #Botão para próximo passo
        self.botao_passo = tk.Button(self.Ggrafico.control_frame, text="Próximo Passo", command=self.passo_escalonamento)
        self.botao_passo.pack(side=tk.RIGHT, padx=10)

        #Botão para executar tudo
        self.botao_executar_tudo = tk.Button(self.Ggrafico.control_frame, text="Executar Tudo", command=self.executar_tudo)
        self.botao_executar_tudo.pack(side=tk.RIGHT, padx=10)

        #Botão para mostrar status simulação
        self.botao_status=tk.Button(self.Ggrafico.control_frame,text= "Status tarefa", command=lambda: self.Ggrafico.abrir_janela_status(self.fila))
        self.botao_status.pack(side=tk.RIGHT, padx=10)
        
        #Botão para modificar tarefas
        self.botao_modificar=tk.Button(self.Ggrafico.control_frame,text='Modificar tarefa', command=lambda: self.Ggrafico.modificar(self.fila))
        self.botao_modificar.pack(side=tk.RIGHT,padx=10)

        self.Ggrafico.janela.mainloop()

    #Função recursiva para execução continuada da simulação
    def executar_tudo(self):
        #configura os estados dos botões para evitar interações durante a execução automática
        self.botao_passo.config(state="disabled")
        self.botao_executar_tudo.config(state="disabled")
        self.botao_retroceder.config(state="disabled")

        if self.prontas or self.tempo==0:
            self.passo_escalonamento()
            if self.prontas or self.tempo==0:
                self.Ggrafico.janela.after(50, self.executar_tudo)

    #Função para execução de um Tick de tempo do sistema
    def passo_escalonamento(self):
        
        #Caso não haja mais tarefas para processar, finaliza a simulação
        if not self.fila:
            self.finalizar_simulacao()
            return
        #Desenha informações do sistemas no gráfico como tempo atual, numero de tarefas prontas, etc
        self.Ggrafico.desenhar_palavra(self.tempo, len(self.tarefas))

        #Adiciona e ordena as tarefas que estão prontas pra execução na fila de prontas
        for t in self.fila:
            if t.ingresso <= self.tempo and t.status=='nova':
                t.status='pronta'
                self.prontas.append(t)
                #Define a ordem de execução das tarefas na fila de prontas de acordo com o escalonador
                if self.escalonador == "priop":
                    self.prontas.sort(key=lambda t: (-t.prioridade,  not t.status == 'rodando', t.ingresso, t.duracao))
                elif self.escalonador == "srtf":
                    self.prontas.sort(key=lambda t: (t.duracao, not t.status == 'rodando', t.ingresso))

        #Executa as tarefas nos processadores disponíveis, verificando se é necessário trocar de tarefa ou se o quantum acabou                
        if self.prontas:
            for cpu in self.cpu:
                if cpu.quantum_atual % cpu.quantum == 0 or cpu.tarefa_rodando==None:#verifica se o quantum acabou ou se o processador está ocioso
                    if cpu.tarefa_rodando is not None:
                        cpu.tarefa_rodando.status='pronta'#Marca como pronta tarefa preemptada anteriormente
                    for tarefa in self.prontas:#percorre fila de prontas
                        if tarefa.status == "pronta": #Encontra a primeira tarefa pronta para execução
                            tarefa.status = "rodando"
                            cpu.tarefa_rodando = tarefa #atribui tarefa para o processador
                            break
                cpu.executar(self.Ggrafico,self.tempo) #Executa a tarefa no processador e atualiza o gráfico 
            i = 0
            for cpu in self.cpu:#verifica quantos processadores estão ociosos
                if cpu.ociosidade==1:
                    i += 1
            #desenha a quantidade de processadores ociosos no gráfico
            self.Ggrafico.desenhar_processador(i,self.tempo, len(self.prontas), self.cpu) 

            for x in self.prontas: #Desenha as tarefas que estão esperando processador
                if(x.status=='pronta'):
                    self.Ggrafico.desenhar_retangulo(self.tempo,x.id,'white', 0)
        #Reoganiza a fila de prontas para remover as tarefas finalizadas e manter a ordem correta
        self.prontas = [t for t in self.prontas if t.duracao > 0 and (t.status=="pronta" or t.status=="rodando")]
        #avança o tempo do sistema
        self.tempo += 1
        
        #Salva os parametros atuais da simulação para permitir retroceder a este ponto posteriormente
        self.salvar_estado_atual()

        #habilita o botão de retroceder passo somente depois do primeiro avanço de tempo
        self.botao_retroceder.config(state="normal")
        #Caso fila de prontas esteja vazia, finaliza a simulação
        if not self.prontas:
            self.finalizar_simulacao()


    #Cria uma pilha de estados para cada tempo de relógio do sistema
    def salvar_estado_atual(self):
        estado = {
            'tempo': self.tempo,
            'fila_prontas': copy.deepcopy(self.prontas),
            'fila_original': copy.deepcopy(self.fila),
            'cpus': copy.deepcopy(self.cpu),
        }
        self.historico_estados.append(estado)


    #Função para retroceder um passo na simulação
    def retroceder_passo(self):
        if len(self.historico_estados) <= 1:
            return
        tempo_a_limpar = self.tempo - 1 #Passo_escalonamento termina com tempo incrementado
        self.Ggrafico.limpar_passo(tempo_a_limpar)#Apaga elemntos gráficos daquele tick de relogio
        self.historico_estados.pop()#Remove topo da pilha de estados
        estado_anterior = self.historico_estados[-1]
        #restaura os parametros anteriores da simulação
        self.tempo = estado_anterior['tempo']
        self.prontas = copy.deepcopy(estado_anterior['fila_prontas'])
        self.fila=copy.deepcopy(estado_anterior['fila_original'])
        self.cpu = copy.deepcopy(estado_anterior['cpus'])
        self.botao_passo.config(state="normal", text="Próximo Passo")
        self.botao_executar_tudo.config(state="normal", text="Executar Tudo")
        #Se não houver mais estados para retroceder, desabilita o botão de retroceder passo
        if len(self.historico_estados) <= 1:
            self.botao_retroceder.config(state="disabled")

    #Função para finalizar a simulação
    def finalizar_simulacao(self):
        #desenha o estado final da simulação no gráfico
        self.Ggrafico.desenhar_palavra(self.tempo, len(self.tarefas))
        self.Ggrafico.desenhar_processador(len(self.cpu),self.tempo, len(self.prontas), self.cpu)
        #desativa os botões de interação
        if self.botao_passo:
            self.botao_passo.config(state="disabled", text="Finalizado")
        if self.botao_executar_tudo:
            self.botao_executar_tudo.config(state="disabled", text="Finalizado")
        #Salva a imagem final do gráfico
        self.Ggrafico.salvar_canvas_jpg()

    #Carrega as tarefas e processadores a partir do arquivo de parametros
    def cria_tarefas(self):
        try:
            with open('parametros.txt', 'r') as f:
                linhas = f.readlines()
                for i, linha in enumerate(linhas):
                    linha = linha.strip().lower()#Converte tudo para lower case
                    if not linha:#caso haja linhas em branco, ignora
                        continue 
                    if i == 0:#trata o cabeçalho de maneira diferente
                        cabecalho = linha.split(';')
                        if len(cabecalho) >= 3:#Garante que o cabeçalho tem os parametros necessários
                            self.escalonador = cabecalho[0]
                            for i in range(int(cabecalho[2])):
                                print("Numero processadores:",i)
                                if self.escalonador == "priop":
                                    self.cpu.append(pr.processador(i,int(cabecalho[1])))
                                elif self.escalonador == "srtf":
                                    self.cpu.append(pr.processador(i,1))
                        continue 
                    valores = linha.split(';')
                    if len(valores) >= 5:
                        id_tarefa = int(valores[0])
                        cor = valores[1]
                        ingresso = int(valores[2])
                        duracao = int(valores[3]) 
                        prioridade = int(valores[4])
                        
                        nova_tarefa = tf.tarefa(id_tarefa, cor, ingresso, prioridade, duracao)
                        self.tarefas.append(nova_tarefa)
        except FileNotFoundError:
            print("Arquivo não encontrado.")
