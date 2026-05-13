from PIL import Image, ImageDraw, ImageGrab

import tkinter as tk
## gerencia  interface grafica
class gerenciador_grafico:
    def __init__(self):
        self.janela = tk.Tk()
        self.canvas = tk.Canvas(self.janela, width=1200, height=600)
        self.canvas.pack()

    def desenhar_retangulo(self,tempo,id,cor):
        tag = f"passo_{tempo}"
        x1=(tempo*50)+55
        y1=550-(id*25)
        x2=(tempo*50)+105
        y2=525-(id*25)
        self.id=self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, tags=(tag,))
    
    def desenhar_processador(self,proc, tempo):
        strt="Processadores inativos: " + str(proc)
        x=600
        y=593
        tag = f"passo_{tempo}"
        # Deleta o texto anterior para evitar sobreposição
        self.canvas.delete("proc_text")
        self.canvas.create_text(x, y, text=strt, font=("Arial", 10), tags=("proc_text", tag))


    def desenhar_legenda(self,lista):
        for i, iterador in enumerate(lista):
            strt="T" + str(i) + " (p" + str(iterador.prioridade) + ",d" + str(iterador.duracao)+")"
            y=550-(iterador.id*25)
            y1=537-(iterador.id*25)
            self.canvas.create_text(23, y1, text=strt, font=("Arial", 8))
            self.canvas.create_line(15, y, 1200, y, fill="gray", dash=(2, 4))

    def desenhar_palavra(self,tempo):
        tag = f"passo_{tempo}"
        strt=str(tempo)
        x=(tempo*50)+55
        y=575
        self.canvas.create_text(x, y, text=strt, font=("Arial", 10), tags=(tag,))
        self.canvas.create_line(x, 0, x, 570, fill="gray", dash=(2, 4), tags=(tag,))
        
    def limpar_passo(self, tempo):
        """Deleta todos os elementos gráficos associados a um passo de tempo específico."""
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