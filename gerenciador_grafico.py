
import tkinter as tk
## gerencia  interface grafica
class gerenciador_grafico:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Retângulo")
        self.canvas = tk.Canvas(self.janela, width=1200, height=600)
        self.canvas.pack()

    def desenhar_retangulo(self, x1, y1, x2, y2,i):
        self.id=self.canvas.create_rectangle(x1, y1, x2, y2, fill=i)
    
    def move_retangulo(self,x):
        self.canvas.move(self.id,x,0)

    def aumentar_retangulo(self, dx, dy):
        x1, y1, x2, y2 = self.canvas.coords(self.id)

        x2 += dx  
        y2 += dy  
        self.canvas.coords(self.id, x1, y1, x2, y2)

    def desenhar_palavra(self,strt,x,y,fonte):
        self.canvas.create_text(x, y, text=strt, font=("Arial", fonte))

    def atualizar(self):
        self.move_retanculo(1)
        self.janela.after(33,self.atualizar)