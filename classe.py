

import tkinter as tk

janela = tk.Tk()
janela.title("Retângulo")

canvas = tk.Canvas(janela, width=400, height=300)
canvas.pack()

# cria um retângulo
canvas.create_rectangle(50, 50, 200, 150, fill="blue")

janela.mainloop()

