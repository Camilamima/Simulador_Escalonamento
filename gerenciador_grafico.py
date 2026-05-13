from PIL import Image, ImageDraw, ImageGrab
import io
import tkinter as tk
## gerencia  interface grafica
class gerenciador_grafico:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Retângulo")
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

    def move_retangulo(self,x):
        self.canvas.move(self.id,x,0)

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

    def atualizar(self):
        self.move_retanculo(1)
        self.janela.after(33,self.atualizar)

    def salvar_canvas_jpg(self, nome="saida.jpg"):
            img = ImageGrab.grab()
            img.save(nome, "jpeg")