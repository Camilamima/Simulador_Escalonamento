from PIL import Image, ImageDraw, ImageGrab, ImageFont
import tkinter as tk
from tkinter import filedialog, messagebox
class gerenciador_grafico:
    def __init__(self):
        self.janela = tk.Tk()
        self.canvas = tk.Canvas(self.janela, width=1200, height=600)
        self.control_frame = tk.Frame(self.janela)
        self.control_frame.pack(side=tk.TOP, pady=10)
        self.canvas.config(scrollregion=(0, 0, 600, 1200))

        self.scroll_y = tk.Scrollbar(
            self.janela,
            orient="vertical",
            command=self.canvas.yview
        )

        #Scrollbar horizontal
        self.scroll_x = tk.Scrollbar(
            self.janela,
            orient="horizontal",
            command=self.canvas.xview
        )

        #Conecta canvas -> scrollbar
        self.canvas.config(
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set
        )

        #Posicionamento
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")

        self.canvas.pack(side="left", fill="both", expand=True)


        self.canvas.pack()
        self.xOrigem = 60
        self.yOrigem = 540
        self.alturaQuadrado = 25
        self.larguraQuadrado = 50

    #desenha um retângulo representando a execução de uma tarefa no processador
    def desenhar_retangulo(self,tempo,id,cor, cpu):
        tag = f"passo_{tempo}"
        x1=(tempo*self.larguraQuadrado)+self.xOrigem
        y1=self.yOrigem-((id-1)*self.alturaQuadrado)
        x2=(tempo*self.larguraQuadrado)+(self.larguraQuadrado+self.xOrigem)
        y2=(self.yOrigem-self.alturaQuadrado)-((id-1)*self.alturaQuadrado)
        self.id=self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, tags=(tag,))
        

    def desenhar_retangulo_envelhecimento(self,tempo,id,cor, cpu,prioridade):
        tag = f"passo_{tempo}"
        x1=(tempo*self.larguraQuadrado)+self.xOrigem
        y1=self.yOrigem-((id-1)*self.alturaQuadrado)
        x2=(tempo*self.larguraQuadrado)+(self.larguraQuadrado+self.xOrigem)
        y2=(self.yOrigem-self.alturaQuadrado)-((id-1)*self.alturaQuadrado)
        self.id=self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, tags=(tag,))
        xc = (x1 + x2) / 2
        yc = (y1 + y2) / 2

        self.canvas.create_text(
            xc,
            yc,
            text=str(prioridade),   # ou prioridade_v
            fill="black",
            tags=(tag,)
        )

    def desenhar_retangulo_mutex(self,tempo,id,cor):
        tag = f"passo_{tempo}"
        x1=(tempo*self.larguraQuadrado)+self.xOrigem
        y1=self.yOrigem-((id-1)*self.alturaQuadrado)
        x2=(tempo*self.larguraQuadrado)+(self.larguraQuadrado+self.xOrigem)
        y2=(self.yOrigem-self.alturaQuadrado)-((id-1)*self.alturaQuadrado)
        self.id=self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, tags=(tag,))
        xc = (x1 + x2) / 2
        yc = (y1 + y2) / 2

        self.canvas.create_text(
            xc,
            yc,
            text="MTX",   # ou prioridade_v
            fill="white",
            tags=(tag,)
        )
    
    def desenhar_retangulo_io(self,tempo,id,cor, cpu,prioridade):
        tag = f"passo_{tempo}"
        x1=(tempo*self.larguraQuadrado)+self.xOrigem
        y1=self.yOrigem-((id-1)*self.alturaQuadrado)
        x2=(tempo*self.larguraQuadrado)+(self.larguraQuadrado+self.xOrigem)
        y2=(self.yOrigem-self.alturaQuadrado)-((id-1)*self.alturaQuadrado)
        self.id=self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, tags=(tag,))
        
        # Desenha as linhas transversais (diagonais)
        left = min(x1, x2)
        right = max(x1, x2)
        top = min(y1, y2)
        bottom = max(y1, y2)
        h = bottom - top
        spacing = 8
        
        x_start = left - h
        while x_start < right:
            x1_line = x_start
            y1_line = top
            x2_line = x_start + h
            y2_line = bottom
            
            if x1_line < left:
                y1_line = top + (left - x1_line)
                x1_line = left
                
            if x2_line > right:
                y2_line = bottom - (x2_line - right)
                x2_line = right
                
            if x1_line < x2_line:
                self.canvas.create_line(x1_line, y1_line, x2_line, y2_line, fill="black", tags=(tag,))
            
            x_start += spacing

        xc = (x1 + x2) / 2
        yc = (y1 + y2) / 2

        self.canvas.create_text(
            xc,
            yc,
            text=str(prioridade),   # ou prioridade_v
            fill="black",
            tags=(tag,)
        )

    #desenha o estado atual dos processadores, tarefas prontas e quantum atual de cada processador
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

    def atualizar_scrollregion(self, tempo, altura=None):
        # Calcula a largura necessária para acomodar o passo atual
        # O x2 do passo atual é (tempo * self.larguraQuadrado) + self.larguraQuadrado + self.xOrigem
        largura_necessaria = (tempo + 1) * self.larguraQuadrado + self.xOrigem + 100
        
        # Garante que a largura seja pelo menos a largura atual visível do canvas ou um mínimo padrão (1200)
        largura_canvas = self.canvas.winfo_width()
        largura = max(largura_necessaria, largura_canvas, 1200)
        
        # Recupera a altura atual do scrollregion para preservar se não for passada
        if altura is None:
            scrollregion = self.canvas.cget("scrollregion")
            if scrollregion:
                parts = [int(float(x)) for x in scrollregion.split()]
                altura = parts[3]
            else:
                altura = self.canvas.winfo_height()
                if altura <= 0:
                    altura = 600
                    
        self.canvas.config(scrollregion=(0, 0, largura, altura))

    #desenha o gráfico vertical de tarefas, mostrando o id, prioridade e duração de cada tarefa
    def desenhar_grafico(self,lista):
        # Ajusta a origem Y e a altura do canvas com base no número de tarefas
        num_tarefas = len(lista)
        self.yOrigem = num_tarefas * self.alturaQuadrado + 40
        canvas_height = self.yOrigem + 80
        self.canvas.config(height=canvas_height)
        self.atualizar_scrollregion(0, altura=canvas_height)

        for i, iterador in enumerate(lista):
            strt = "T" + str(iterador.id) + " (p" + str(iterador.prioridade) + ", d" + str(iterador.duracao) + ")\n(i" + str(iterador.ingresso) + ")"
            y=self.yOrigem-(iterador.id*25)
            y1=(self.yOrigem-(self.alturaQuadrado/2))-((iterador.id-1)*self.alturaQuadrado)
            x=self.xOrigem-30
            self.canvas.create_text(x, y1, text=strt, font=("Arial", 8))

    #desenha as linhas verticais e horizontais do gráfico, além do tempo de execução
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
        self.atualizar_scrollregion(tempo)
        
    #limpa os elementos gráficos de um tempo específico
    def limpar_passo(self, tempo):
        tag = f"passo_{tempo}"
        self.canvas.delete(tag)
        self.atualizar_scrollregion(max(0, tempo - 1))

    # desenha o indicador de entrada na fila de prontas (flecha para cima em verde)
    def desenhar_ingresso(self, tempo, id_tarefa):
        tag = f"passo_{tempo}"
        x = (tempo * self.larguraQuadrado) + self.xOrigem
        y1 = self.yOrigem - ((id_tarefa-1) * self.alturaQuadrado)
        y2 = (self.yOrigem - self.alturaQuadrado) - ((id_tarefa-1) * self.alturaQuadrado)
        
        # Desenha a haste vertical (preta)
        self.canvas.create_line(x, y1, x, y2, fill="black", width=2, tags=(tag,))
        # Desenha a ponta da flecha para cima (y2 é o topo)
        self.canvas.create_line(x, y2, x - 6, y2 + 6, fill="black", width=2, tags=(tag,))
        #self.canvas.create_line(x, y2, x + 6, y2 + 6, fill="black", width=2, tags=(tag,))

    # desenha o indicador de fim de execução (flecha para baixo em preto)
    def desenhar_fim(self, tempo, id_tarefa):
        tag = f"passo_{tempo}"
        x = (tempo * self.larguraQuadrado) + self.larguraQuadrado + self.xOrigem
        y1 = self.yOrigem - ((id_tarefa -1 ) * self.alturaQuadrado)
        y2 = (self.yOrigem - self.alturaQuadrado) - ((id_tarefa-1) * self.alturaQuadrado)
        
        # Desenha a haste vertical (preta)
        self.canvas.create_line(x, y2, x, y1, fill="black", width=2, tags=(tag,))
        # Desenha a ponta da flecha para baixo (y1 é o fundo)
        #self.canvas.create_line(x, y1, x - 6, y1 - 6, fill="black", width=2, tags=(tag,))
        self.canvas.create_line(x, y1, x + 6, y1 - 6, fill="black", width=2, tags=(tag,))

    # Salva imagem do gráfico compreendendo todo o canvas, inclusive a área com scroll
    def salvar_canvas_jpg(self, nome="saida.jpg"):
        self.janela.update_idletasks()
        
        # Obtém o tamanho da área de scroll do canvas
        scrollregion = self.canvas.cget("scrollregion")
        if scrollregion:
            parts = [int(float(x)) for x in scrollregion.split()]
            width, height = parts[2], parts[3]
        else:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            
        # Fallbacks caso o canvas ainda não tenha dimensões definidas
        if width <= 0:
            width = 1200
        if height <= 0:
            height = 600
            
        # Obtém a cor de fundo do canvas e converte para RGB (0-255)
        bg_color = self.canvas.cget("bg")
        try:
            r, g, b = tuple(x // 256 for x in self.canvas.winfo_rgb(bg_color))
            bg_rgb = (r, g, b)
        except Exception:
            bg_rgb = (240, 240, 240) # Cinza claro padrão
            
        img = Image.new("RGB", (width, height), bg_rgb)
        draw = ImageDraw.Draw(img)
        
        def to_rgb(color_str):
            if not color_str or color_str == "SystemButtonFace":
                return bg_rgb
            try:
                return tuple(x // 256 for x in self.canvas.winfo_rgb(color_str))
            except Exception:
                return None

        # Redesenha todos os elementos do canvas na imagem do PIL
        for item in self.canvas.find_all():
            item_type = self.canvas.type(item)
            coords = self.canvas.coords(item)
            if not coords:
                continue
                
            if item_type == "rectangle":
                x1, y1, x2, y2 = coords
                fill_color = self.canvas.itemcget(item, "fill")
                outline_color = self.canvas.itemcget(item, "outline")
                
                fill_rgb = to_rgb(fill_color) if fill_color else None
                outline_rgb = to_rgb(outline_color) if outline_color else None
                
                if fill_color == "":
                    fill_rgb = None
                if outline_color == "":
                    outline_rgb = None
                    
                draw.rectangle([x1, y1, x2, y2], fill=fill_rgb, outline=outline_rgb)
                
            elif item_type == "line":
                fill_color = self.canvas.itemcget(item, "fill")
                fill_rgb = to_rgb(fill_color) if fill_color else (0, 0, 0)
                try:
                    line_width = int(float(self.canvas.itemcget(item, "width")))
                except Exception:
                    line_width = 1
                draw.line(coords, fill=fill_rgb, width=line_width)
                
            elif item_type == "text":
                if len(coords) >= 2:
                    x, y = coords[0], coords[1]
                    text_str = self.canvas.itemcget(item, "text")
                    fill_color = self.canvas.itemcget(item, "fill")
                    fill_rgb = to_rgb(fill_color) if fill_color else (0, 0, 0)
                    
                    font_str = self.canvas.itemcget(item, "font")
                    font_size = 10
                    if font_str:
                        parts = font_str.split()
                        if len(parts) >= 2 and parts[-1].isdigit():
                            font_size = int(parts[-1])
                            
                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except Exception:
                        font = ImageFont.load_default()
                        
                    draw.text((x, y), text_str, fill=fill_rgb, font=font, anchor="mm")
                    
        # Salva a imagem com a extensão apropriada
        ext = nome.split('.')[-1].lower()
        fmt = "PNG" if ext == "png" else "JPEG"
        img.save(nome, format=fmt)

    # Abre um diálogo para salvar a imagem manualmente
    def salvar_imagem_manual(self):
        caminho = filedialog.asksaveasfilename(
            initialdir=".",
            title="Salvar imagem do escalonamento",
            defaultextension=".png",
            filetypes=[("Imagem PNG", "*.png"), ("Imagem JPEG", "*.jpg"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            try:
                self.salvar_canvas_jpg(caminho)
                messagebox.showinfo("Sucesso", f"Imagem salva com sucesso em:\n{caminho}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar a imagem:\n{str(e)}")


    #abre janela mostrando o status de todas as tarefas
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

    #abre janela para modificar tarefas
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

        #Verifica se o ID da tarefa é válido
        def validar(*args):
            val = entry_id.get()

            if val.isdigit() and int(val) < len(fila):
                btn.config(state="normal")
            else:
                btn.config(state="disabled")

        entry_id.bind("<KeyRelease>", validar)

        #Aplica as modificações na tarefa selecionada
        def aplicar():
            id_tarefa = int(entry_id.get())

            tarefa = fila[id_tarefa] 
            x=tarefa.status
            if entry_prio.get().isdigit() and int(entry_prio.get()) >= 0:
                tarefa.prioridade = int(entry_prio.get())
            elif entry_status.get().lower() not in ("pronta","nova","rodando","finalizada"):
                tarefa.status = entry_status.get()
            tarefa.duracao = int(entry_dur.get())
            if x == "finalizada" and entry_status.get().lower() == "pronta":
                tarefa.status = "nova"
            janela.destroy()

        btn.config(command=aplicar)
