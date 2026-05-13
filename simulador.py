import gerenciador_grafico as gg
import tarefa as tf
import copy
import tkinter as tk
 
class simulador:
    ##inicialização de variaveis
    def __init__(self):
        self.tarefas = []
        self.cpu=2
        self.escalonador=''
        self.quantum=2
        self.Ggrafico = gg.gerenciador_grafico()
        # Variáveis de estado da simulação para o modo passo a passo
        self.tempo = 0
        self.quantum_Atual = self.quantum
        self.fila = [] # Fila de execução principal
        
        self.botao_passo = None
        self.botao_executar_tudo = None
        self.botao_retroceder = None
        self.historico_estados = []

    #inicializador
    def iniciar(self):
        self.cria_tarefas()
        self.fila = copy.deepcopy(self.tarefas)
        self.Ggrafico.desenhar_legenda(self.fila)
        self.salvar_estado_atual()

        # --- Interface de Controle ---
        control_frame = tk.Frame(self.Ggrafico.janela)
        control_frame.pack(side=tk.BOTTOM, pady=10)

        # Botão para retroceder um passo
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
        
        if self.fila:
            self.passo_escalonamento()
            # Agenda a próxima execução se a simulação não tiver terminado
            if self.fila:
                self.Ggrafico.janela.after(50, self.executar_tudo)

    def passo_escalonamento(self):
  
        if not self.fila:
            self.finalizar_simulacao()
            return
        self.Ggrafico.desenhar_palavra(self.tempo)
        #prontas = [t for t in self.fila if t.ingresso <= self.tempo]
        self.prontas = []
        for fila in self.fila:
            if fila.ingresso <= self.tempo:
                self.prontas.append(fila)
                #self.quantum_Atual = self.quantum # Reseta o quantum para tarefas que acabaram de chegar
        #Se houver tarefas prontas, executa a lógica de escalonamento.
        if self.prontas:

            if self.quantum_Atual >= self.quantum and self.escalonador == "priop":##Organiza lista por prioridade (PRIOP)
                   self.prontas.sort(key=lambda t: (-t.prioridade, not t.status=="Rodando", t.ingresso, t.duracao))
                   self.quantum_Atual=0
            elif self.escalonador == "srtf":##Organiza lista por duracao (SRTF)
                    self.prontas.sort(key=lambda t: (t.duracao, not t.status=="Rodando",t.ingresso))
                    self.quantum_Atual=0
            # Executa as tarefas para o tempo atual e atualiza o quantum se uma tarefa terminou.
            for i, iterador in enumerate(self.prontas):  
                print(i)
                if i < self.cpu: 
                    iterador.status="Rodando"
                    self.Ggrafico.desenhar_retangulo(self.tempo,iterador.id,iterador.cor)
                    iterador.duracao-=1
                    #print("tarefa: " + str(iterador.id) + " duracao: " + str(iterador.duracao))
                    if iterador.duracao == 0:
                        self.quantum_Atual=self.quantum-1       
                else:
                    iterador.status="Ocioso"
                    iterador.ociosidade+=1
                    #print("tarefa: " + str(iterador.id) + " duracao: " + str(iterador.duracao))
                    self.Ggrafico.desenhar_retangulo(self.tempo,iterador.id,'white')   
        self.fila = [t for t in self.fila if t.duracao > 0]
        self.tempo += 1
        self.quantum_Atual += 1

        # Salva o estado após o passo ser concluído
        self.salvar_estado_atual()
        self.botao_retroceder.config(state="normal")
        #Se a fila ficou vazia, atualiza o botão.
        if not self.fila:
            self.finalizar_simulacao()

    def salvar_estado_atual(self):
        """Salva o estado atual da simulação (tempo, quantum, fila) no histórico."""
        estado = {
            'tempo': self.tempo,
            'quantum_Atual': self.quantum_Atual,
            'fila': copy.deepcopy(self.fila)
        }
        self.historico_estados.append(estado)

    def retroceder_passo(self):
        """Restaura a simulação para o estado do passo anterior."""
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
        self.quantum_Atual = estado_anterior['quantum_Atual']
        self.fila = copy.deepcopy(estado_anterior['fila'])

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

    #Tarefa de maior prioridade assume a CPU caso haja uma disponível.
    #Maior prioridade é definida pela ordem da tarefa na lista de prontas,
    #ou seja, se houver 4 cpus disponíveis, as 4 primeiras tarefas da 
    #lista de prontas serão executadas nesse mesmo ciclo
   ## def executar(self, tempo, prontas):

        
                

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
                        ingresso = int(valores[2]) # Corrigido para pegar o índice correto
                        duracao = int(valores[3]) 
                        prioridade = int(valores[4])
                        
                        # Construtor de tarefa: id, cor, ingresso, prioridade, duracao
                        nova_tarefa = tf.tarefa(id_tarefa, cor, ingresso, prioridade, duracao)
                        self.tarefas.append(nova_tarefa)
        except FileNotFoundError:
            print("Arquivo não encontrado.")
