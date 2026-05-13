from PIL import Image, ImageDraw, ImageGrab
import tkinter as tk
class gerenciador_grafico:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Retângulo")
        self.canvas = tk.Canvas(self.janela, width=1200, height=600)
        self.canvas.pack()
        self.xOrigem = 60
        self.yOrigem = 540
        self.alturaQuadrado = 25
        self.larguraQuadrado = 50


    def desenhar_retangulo(self,tempo,id,cor):
        tag = f"passo_{tempo}"
        x1=(tempo*self.larguraQuadrado)+self.xOrigem
        y1=self.yOrigem-(id*self.alturaQuadrado)
        x2=(tempo*self.larguraQuadrado)+(self.larguraQuadrado+self.xOrigem)
        y2=(self.yOrigem-self.alturaQuadrado)-(id*self.alturaQuadrado)
        self.id=self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, tags=(tag,))
    
    def desenhar_processador(self,proc, tempo, tarefas):
        strt="Processadores inativos: " + str(proc)
        strt1="Tarefas prontas: " + str(tarefas) 
        x=400
        y=self.yOrigem + 40
        tag = f"passo_{tempo}"
        self.canvas.delete("proc_text")
        self.canvas.delete("task_text")
        self.canvas.create_text(x, y, text=strt, font=("Arial", 10), tags=("proc_text", tag))
        self.canvas.create_text(x+200, y, text=strt1, font=("Arial", 10), tags=("task_text",tag,))

    def move_retangulo(self,x):
        self.canvas.move(self.id,x,0)

    def desenhar_legenda(self,lista):
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

    def atualizar(self):
        self.move_retanculo(1)
        self.janela.after(33,self.atualizar)

    def salvar_canvas_jpg(self, nome="saida.jpg"):
            
            self.janela.update_idletasks()
            x = self.janela.winfo_rootx()
            y = self.janela.winfo_rooty()
            largura = self.janela.winfo_width()
            altura = self.janela.winfo_height()

            bbox = (x, y, x + largura, y + altura)
            img = ImageGrab.grab(bbox=bbox)
            img.save(nome, "jpeg")