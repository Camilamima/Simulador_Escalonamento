
import tkinter as tk
## gerencia  interface grafica
class gerenciador_grafico:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Retângulo")
        self.canvas = tk.Canvas(self.janela, width=1200, height=600)
        self.canvas.pack()

    def desenhar_retangulo(self, tempo,id,cor):

        x1=(tempo*50)+50
        y1=550-(id*25)
        x2=(tempo*50)+100
        y2=525-(id*25)
        self.id=self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor)
    
    def move_retangulo(self,x):
        self.canvas.move(self.id,x,0)

    def desenhar_palavra(self,tempo,fonte):
        strt=str(tempo)
        x=(tempo*50)+50
        y=575
        self.canvas.create_text(x, y, text=strt, font=("Arial", fonte))

    def atualizar(self):
        self.move_retanculo(1)
        self.janela.after(33,self.atualizar)