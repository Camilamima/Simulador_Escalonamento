from PIL import Image, ImageDraw, ImageGrab

import tkinter as tk
class gerenciador_grafico:
    def __init__(self):
        self.janela = tk.Tk()
        self.canvas = tk.Canvas(self.janela, width=1200, height=600)
        self.control_frame = tk.Frame(self.janela)
        self.control_frame.pack(side=tk.TOP, pady=10)
        self.canvas.config(scrollregion=(0, 0, 4000, 4000))

        self.scroll_y = tk.Scrollbar(
            self.janela,
            orient="vertical",
            command=self.canvas.yview
        )

        # Scrollbar horizontal
        self.scroll_x = tk.Scrollbar(
            self.janela,
            orient="horizontal",
            command=self.canvas.xview
        )

        # Conecta canvas -> scrollbar
        self.canvas.config(
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set
        )

        # Posicionamento
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")

        self.canvas.pack(side="left", fill="both", expand=True)


        self.canvas.pack()
        self.xOrigem = 60
        self.yOrigem = 540
        self.alturaQuadrado = 25
        self.larguraQuadrado = 50


    def desenhar_retangulo(self,tempo,id,cor, cpu):
        tag = f"passo_{tempo}"
        x1=(tempo*self.larguraQuadrado)+self.xOrigem
        y1=self.yOrigem-(id*self.alturaQuadrado)
        x2=(tempo*self.larguraQuadrado)+(self.larguraQuadrado+self.xOrigem)
        y2=(self.yOrigem-self.alturaQuadrado)-(id*self.alturaQuadrado)
        self.id=self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, tags=(tag,))
       
    
    def desenhar_processador(self,proc, tempo, tarefas, cpu):
        strt="Processadores inativos: " + str(proc)
        strt1="Tarefas prontas: " + str(tarefas) 
        
        x=300
        y=self.yOrigem + 40
        tag = f"passo_{tempo}"
        self.canvas.delete("proc_text")
        self.canvas.delete("task_text")
        self.canvas.delete("quantum_text")
        self.canvas.create_text(x, y, text=strt, font=("Arial", 10), tags=("proc_text", tag))
        self.canvas.create_text(x+200, y, text=strt1, font=("Arial", 10), tags=("task_text",tag,))
        for i in range(len(cpu)):
            strt2="Quantum cpu "+ str(cpu[i].id) + ": " + str(cpu[i].quantum_atual) 
            self.canvas.create_text(x+350+(i*110), y, text=strt2, font=("Arial", 10), tags=("quantum_text", tag))

    def desenhar_grafico(self,lista):
        for i, iterador in enumerate(lista):
            strt="T" + str(i) + " (p" + str(iterador.prioridade) + ",d" + str(iterador.duracao)+")"
            y=self.yOrigem-(iterador.id*25)
            y1=(self.yOrigem-(self.alturaQuadrado/2))-(iterador.id*self.alturaQuadrado)
            x=self.xOrigem-30
            self.canvas.create_text(x, y1, text=strt, font=("Arial", 8))
            #self.canvas.create_line(x, y, 1200, y, fill="black", dash=(2, 4))

    def desenhar_palavra(self,tempo, iterador):
        tag = f"passo_{tempo}"
        strt=str(tempo)
        x=(tempo*self.larguraQuadrado)+self.xOrigem
        y=self.yOrigem + 15
        y1=self.yOrigem + 5
        self.canvas.create_text(x, y, text=strt, font=("Arial", 10), tags=(tag,))
        y=self.yOrigem-(self.alturaQuadrado*iterador)
        self.canvas.create_line(x, y, x, y1, fill="black", dash=(2, 4), tags=(tag,))
        for i in range(iterador):
             x1=(tempo*self.larguraQuadrado)+self.xOrigem
             y1=self.yOrigem-(i*self.alturaQuadrado)
             x2=(tempo*self.larguraQuadrado)+(self.larguraQuadrado+self.xOrigem)
             self.canvas.create_line(x1, y1, x2, y1, fill="black", dash=(2, 4), tags=(tag,))
        
        
    def limpar_passo(self, tempo):
        tag = f"passo_{tempo}"
        self.canvas.delete(tag)

    def salvar_canvas_jpg(self, nome="saida.jpg"):
            # Garante que a geometria da janela está atualizada antes de capturar
            self.janela.update_idletasks()

            # Pega as coordenadas e dimensões da janela principal
            x = self.janela.winfo_rootx()
            y = self.janela.winfo_rooty()
            largura = self.janela.winfo_width()
            altura = self.janela.winfo_height()
            # Define a área de captura (bounding box)
            bbox = (x, y, x + largura, y + altura)
            img = ImageGrab.grab(bbox=bbox)
            img.save(nome, "jpeg")

    def abrir_janela_status(self,fila):
        janela = tk.Toplevel()
        janela.title("Status das tarfefas")
        janela.geometry("300x200")
        lista=[]
        for t in fila:
            lista.append(
                "Tarefa: " + str(t.id) +
                " Prioridade: " + str(t.prioridade) +
                " Duracao: " + str(t.duracao) +
                " Status: " + str(t.status)
            )
        texto = "\n".join(lista)
        label = tk.Label(janela, text=texto)
        label.pack(pady=20)

    def modificar(self,fila):
        janela = tk.Toplevel()
        janela.title("Editar tarefa")

        tk.Label(janela, text="ID da tarefa").pack()
        entry_id = tk.Entry(janela)
        entry_id.pack()

        tk.Label(janela, text="Nova prioridade").pack()
        entry_prio = tk.Entry(janela)
        entry_prio.pack()

        tk.Label(janela, text="Novo status").pack()
        entry_status = tk.Entry(janela)
        entry_status.pack()

        tk.Label(janela, text="Nova duração").pack()
        entry_dur = tk.Entry(janela)
        entry_dur.pack()

        btn = tk.Button(janela, text="Aplicar", state="disabled")
        btn.pack(pady=10)

        def validar(*args):
            val = entry_id.get()

            if val.isdigit() and int(val) < len(fila):
                btn.config(state="normal")
            else:
                btn.config(state="disabled")

        entry_id.bind("<KeyRelease>", validar)

        def aplicar():
            id_tarefa = int(entry_id.get())

            tarefa = fila[id_tarefa] 

            tarefa.prioridade = int(entry_prio.get())
            tarefa.status = entry_status.get()
            tarefa.duracao = int(entry_dur.get())

            janela.destroy()

        btn.config(command=aplicar)
