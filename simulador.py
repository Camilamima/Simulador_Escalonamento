import gerenciador_grafico as gg
import tarefa as tf
import processador as pr
import copy
import tkinter as tk
import io
from PIL import ImageGrab
 
class simulador:
    ##inicialização de variaveis
    def __init__(self):
        self.flag=0
        self.tarefas = []
        self.cpu=[]
        self.escalonador=''
        self.prontas=[]
        self.Ggrafico = gg.gerenciador_grafico()
        self.tempo = 0
        self.fila = [] # Fila de execução principal
        self.botao_passo = None
        self.botao_executar_tudo = None
        self.botao_retroceder = None
        self.botao_modificar = None
        self.historico_estados = []

    #inicializador
    def iniciar(self):
        self.cria_tarefas()
        self.fila = copy.deepcopy(self.tarefas)
        self.Ggrafico.desenhar_legenda(self.fila)
        self.salvar_estado_atual(None,None)

        # --- Interface de Controle ---
        control_frame = tk.Frame(self.Ggrafico.janela)
        control_frame.pack(side=tk.BOTTOM, pady=10)

        #Botão para retroceder um passo
        self.botao_retroceder = tk.Button(control_frame, text="Retroceder Passo", command=self.retroceder_passo, state="disabled")
        self.botao_retroceder.pack(side=tk.LEFT, padx=10)

        # Botão para executar a simulação passo a passo
        self.botao_passo = tk.Button(control_frame, text="Próximo Passo", command=self.passo_escalonamento)
        self.botao_passo.pack(side=tk.LEFT, padx=10)

        # Botão para executar a simulação inteira de uma vez
        self.botao_executar_tudo = tk.Button(control_frame, text="Executar Tudo", command=self.executar_tudo)
        self.botao_executar_tudo.pack(side=tk.LEFT, padx=10)

        # O estado inicial (tempo 0) é desenhado no primeiro clique de "Próximo Passo"

        self.Ggrafico.janela.mainloop()

    def executar_tudo(self):
        """Executa a simulação automaticamente até o fim com uma animação rápida."""
        self.botao_passo.config(state="disabled")
        self.botao_executar_tudo.config(state="disabled")
        self.botao_retroceder.config(state="disabled")

        if self.prontas or self.tempo==0:
            self.passo_escalonamento()
            # Agenda a próxima execução se a simulação não tiver terminado
            ##Continua rodando se não estiver vazio
            if self.prontas or self.tempo==0:
                self.Ggrafico.janela.after(50, self.executar_tudo)

    def passo_escalonamento(self):
        quantum_cpu=[]#guarda quantum dos processadores para retorno
        tarefas_cpu=[]
        #guarda tarefas rodando
        ##Se fila for vazia, para a simulação
        if not self.fila:
            self.finalizar_simulacao()
            return
        ##Desenha o tempo
        self.Ggrafico.desenhar_palavra(self.tempo)
        ##Inclui tarefas na fila de prontas

        for t in self.fila:
            if t.ingresso <= self.tempo and t.status=='Não iniciado':
                t.status='Pronta'
                self.prontas.append(t)
                #REORDENA TODA VEZ QUE ADICIONA UMA NOVA TAREFA
                if self.escalonador == "priop":
                      self.prontas.sort(key=lambda t: (-t.prioridade, t.id))
                elif self.escalonador == "srtf":
                        self.prontas.sort(key=lambda t: (t.duracao,t.prioridade))


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
                quantum_cpu.append(cpu.quantum_atual)
                tarefas_cpu.append(cpu.tarefa_rodando)
            for x in self.prontas:
                if(x.status=='Pronta'):
                    self.Ggrafico.desenhar_retangulo(self.tempo,x.id,'white')

        self.prontas = [t for t in self.prontas if t.duracao > 0]
        

        self.tempo += 1
        # Salva o estado após o passo ser concluído
        self.salvar_estado_atual(quantum_cpu,tarefas_cpu)
        self.botao_retroceder.config(state="normal")
        #Se a fila ficou vazia, finaliza a simulação
        if not self.prontas:
            self.finalizar_simulacao()

    def salvar_estado_atual(self,q,t):
        ##Salva dicionario por tempo
        estado = {
            'tempo': self.tempo,
            'fila_prontas': copy.deepcopy(self.prontas),
            'fila_original': copy.deepcopy(self.fila),
            'prontas': copy.deepcopy(self.prontas),
            'cpus': copy.deepcopy(self.cpu),
        }
        #A cada tempo passado, salva numa fila o tempo, quantum e como está a fila(via dicionario)
        self.historico_estados.append(estado)

    def retroceder_passo(self):
        """Restaura a simulação para o estado do passo anterior."""
        ##Impede retornar se 
        if len(self.historico_estados) <= 1:
            return
        # 1. Limpa os desenhos do passo de tempo que será "desfeito"
        tempo_a_limpar = self.tempo - 1
        self.Ggrafico.limpar_passo(tempo_a_limpar)

        # 2. Remove o estado atual (o mais recente) do histórico
        self.historico_estados.pop()

        # 3. Carrega o estado anterior, que agora é o último da lista
        estado_anterior = self.historico_estados[-1]
        self.tempo = estado_anterior['tempo']
        self.prontas = copy.deepcopy(estado_anterior['fila_prontas'])
        self.fila=copy.deepcopy(estado_anterior['fila_original'])
        self.cpu = copy.deepcopy(estado_anterior['cpus'])

        # 4. Reabilita os botões de avançar e atualiza o de retroceder
        self.botao_passo.config(state="normal", text="Próximo Passo")
        self.botao_executar_tudo.config(state="normal")
        if len(self.historico_estados) <= 1:
            self.botao_retroceder.config(state="disabled")

    def finalizar_simulacao(self):
        """Ações a serem tomadas quando a simulação termina."""
        self.Ggrafico.desenhar_palavra(self.tempo) # Desenha a marca de tempo final
        if self.botao_passo:
            self.botao_passo.config(state="disabled", text="Finalizado")
        if self.botao_executar_tudo:
            self.botao_executar_tudo.config(state="disabled", text="Finalizado")
        if self.botao_retroceder:
            self.botao_retroceder.config(state="disabled")
        self.Ggrafico.salvar_canvas_jpg()


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
                            for i in range(int(cabecalho[2])):
                                print("Numero id",i)
                                self.cpu.append(pr.processador(i,self.quantum))
                        continue 
                    valores = linha.split(';')
                    if len(valores) >= 5:
                        id_tarefa = int(valores[0])
                        cor = valores[1]
                        ingresso = int(valores[2]) # Corrigido para pegar o índice correto
                        duracao = int(valores[3]) 
                        prioridade = int(valores[4])
                        
                        # Construtor de tarefa: id, cor, ingresso, prioridade, duracao
                        nova_tarefa = tf.tarefa(id_tarefa, cor, ingresso, prioridade, duracao)
                        self.tarefas.append(nova_tarefa)
        except FileNotFoundError:
            print("Arquivo 'parametros.txt' não encontrado.")
