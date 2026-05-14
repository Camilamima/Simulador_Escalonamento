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
        self.cria_tarefas()
        self.fila = copy.deepcopy(self.tarefas)
        self.Ggrafico.desenhar_grafico(self.fila)
        self.salvar_estado_atual()
        #cria um frame para os botões de controle
        control_frame = tk.Frame(self.Ggrafico.janela)
        control_frame.pack(side=tk.BOTTOM, pady=10)
        #inicialização dos botões
        self.botao_retroceder = tk.Button(control_frame, text="Retroceder Passo", command=self.retroceder_passo, state="disabled")
        self.botao_retroceder.pack(side=tk.LEFT, padx=10)

        self.botao_passo = tk.Button(control_frame, text="Próximo Passo", command=self.passo_escalonamento)
        self.botao_passo.pack(side=tk.LEFT, padx=10)

        self.botao_executar_tudo = tk.Button(control_frame, text="Executar Tudo", command=self.executar_tudo)
        self.botao_executar_tudo.pack(side=tk.LEFT, padx=10)

        # Botão para mostrar status simulação
        self.botao_status=tk.Button(control_frame,text= "Status tarefa", command=lambda: self.Ggrafico.abrir_janela_status(self.fila))
        self.botao_status.pack(side=tk.LEFT, padx=10)
        
        #Botão para modificar tarefas
        self.botao_modificar=tk.Button(control_frame,text='Modificar tarefa', command=lambda: self.Ggrafico.modificar(self.fila))
        self.botao_modificar.pack(side=tk.LEFT,padx=10)

        self.Ggrafico.janela.mainloop()

    def executar_tudo(self):
        self.botao_passo.config(state="disabled")
        self.botao_executar_tudo.config(state="disabled")
        self.botao_retroceder.config(state="disabled")

        if self.prontas or self.tempo==0:
            self.passo_escalonamento()
            if self.prontas or self.tempo==0:
                self.Ggrafico.janela.after(50, self.executar_tudo)

    def passo_escalonamento(self):
        if not self.fila:
            self.finalizar_simulacao()
            return
        self.Ggrafico.desenhar_palavra(self.tempo, len(self.tarefas))

        for t in self.fila:
            if t.ingresso <= self.tempo and t.status=='Não iniciado':
                t.status='Pronta'
                self.prontas.append(t)
                if self.escalonador == "priop":
                    self.prontas.sort(key=lambda t: (-t.prioridade,  not t.status == 'Rodando', t.ingresso, t.duracao))
                elif self.escalonador == "srtf":
                    self.prontas.sort(key=lambda t: (t.duracao, not t.status == 'Rodando', t.ingresso))
                        
        if self.prontas:
            for cpu in self.cpu:
                if cpu.quantum_atual % cpu.quantum == 0 or cpu.tarefa_rodando==None:
                    if cpu.tarefa_rodando is not None:
                        cpu.tarefa_rodando.status='Pronta'
                    for tarefa in self.prontas:
                        if tarefa.status == "Pronta":
                            tarefa.status = "Rodando"
                            cpu.tarefa_rodando = tarefa
                            break
                cpu.executar(self.Ggrafico,self.tempo)
            i = 0
            for cpu in self.cpu:
                if cpu.ociosidade==1:
                    i += 1
            self.Ggrafico.desenhar_processador(i,self.tempo, len(self.prontas), self.cpu)
            for x in self.prontas:
                if(x.status=='Pronta'):
                    self.Ggrafico.desenhar_retangulo(self.tempo,x.id,'white', 0)
        self.prontas = [t for t in self.prontas if t.duracao > 0 and (t.status=="Pronta" or t.status=="Rodando")]
        self.tempo += 1
        
        self.salvar_estado_atual()
        self.botao_retroceder.config(state="normal")
        if not self.prontas:
            self.finalizar_simulacao()

    def salvar_estado_atual(self):
        estado = {
            'tempo': self.tempo,
            'fila_prontas': copy.deepcopy(self.prontas),
            'fila_original': copy.deepcopy(self.fila),
            'cpus': copy.deepcopy(self.cpu),
        }
        self.historico_estados.append(estado)

    def retroceder_passo(self):
        if len(self.historico_estados) <= 1:
            return
        tempo_a_limpar = self.tempo - 1
        self.Ggrafico.limpar_passo(tempo_a_limpar)
        self.historico_estados.pop()
        estado_anterior = self.historico_estados[-1]
        self.tempo = estado_anterior['tempo']
        self.prontas = copy.deepcopy(estado_anterior['fila_prontas'])
        self.fila=copy.deepcopy(estado_anterior['fila_original'])
        self.cpu = copy.deepcopy(estado_anterior['cpus'])
        self.botao_passo.config(state="normal", text="Próximo Passo")
        self.botao_executar_tudo.config(state="normal", text="Executar Tudo")
        if len(self.historico_estados) <= 1:
            self.botao_retroceder.config(state="disabled")

    def finalizar_simulacao(self):
        self.Ggrafico.desenhar_palavra(self.tempo, len(self.tarefas))
        self.Ggrafico.desenhar_processador(len(self.cpu),self.tempo, len(self.prontas), self.cpu)
        if self.botao_passo:
            self.botao_passo.config(state="disabled", text="Finalizado")
        if self.botao_executar_tudo:
            self.botao_executar_tudo.config(state="disabled", text="Finalizado")
        self.Ggrafico.salvar_canvas_jpg()

    def cria_tarefas(self):
        try:
            with open('parametros.txt', 'r') as f:
                linhas = f.readlines()
                for i, linha in enumerate(linhas):
                    linha = linha.strip().lower()
                    if not linha:
                        continue 
                    if i == 0:
                        cabecalho = linha.split(';')
                        if len(cabecalho) >= 3:
                            self.escalonador = cabecalho[0]
                            for i in range(int(cabecalho[2])):
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
