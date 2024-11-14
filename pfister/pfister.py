import tkinter as tk

class PyramidApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pyramid with Color Palette")
        self.canvas = tk.Canvas(root, width=500, height=400)
        self.canvas.pack()

        # Cores iniciais da paleta e variável para a cor selecionada
        self.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF"]
        self.selected_color = None
        self.dragging_item = None  # Item em movimento durante o arrasto
        self.item_positions = {}  # Dicionário para armazenar a posição inicial dos quadrados

        self.create_pyramid()
        self.create_palette()
        self.create_trash_bin()

    def create_pyramid(self):
        size = 40
        # Cria a pirâmide invertida de quadrados brancos
        for i in range(5):
            for j in range(i + 1):
                x = 200 - (i * size / 2) + (j * size)
                y = 50 + (i * size)
                rect = self.canvas.create_rectangle(x, y, x + size, y + size, fill="white", tags="square")
                self.canvas.tag_bind(rect, "<Enter>", self.highlight_square)
                self.canvas.tag_bind(rect, "<Leave>", self.unhighlight_square)
                self.item_positions[rect] = (x, y)  # Armazena a posição inicial do quadrado

                # Não adicionamos a opção de arrastar os quadrados brancos
                self.canvas.tag_bind(rect, "<Button-1>", self.select_square)

    def create_palette(self):
        # Cria a paleta de cores na lateral
        for i, color in enumerate(self.colors):
            palette_rect = self.canvas.create_rectangle(350, 50 + i * 50, 390, 90 + i * 50, fill=color, tags="palette")
            self.canvas.tag_bind(palette_rect, "<Button-1>", self.start_drag)

    def create_trash_bin(self):
        # Cria a lixeira para remover cores
        self.trash_bin = self.canvas.create_rectangle(450, 50, 490, 90, fill="gray", outline="black", tags="trash")
        self.canvas.create_text(470, 70, text="Lixeira", font=("Arial", 10))

    def select_square(self, event):
        # Seleciona um quadrado para permitir que ele seja pintado
        self.dragging_item = self.canvas.find_withtag("current")[0]
        self.selected_color = self.canvas.itemcget(self.dragging_item, "fill")
        if self.selected_color != "white":  # Só podemos arrastar se não for branco
            self.canvas.tag_raise(self.dragging_item)  # Traz o item para frente durante o arrasto
            self.canvas.bind("<Motion>", self.drag_motion)
            self.canvas.bind("<ButtonRelease-1>", self.end_drag)

    def start_drag(self, event):
        # Inicia o arrasto de uma cor da paleta
        self.dragging_item = self.canvas.find_withtag("current")[0]
        self.selected_color = self.canvas.itemcget(self.dragging_item, "fill")
        self.canvas.tag_raise(self.dragging_item)  # Traz o item para frente durante o arrasto
        self.canvas.bind("<Motion>", self.drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)

    def drag_motion(self, event):
        # Move a cor selecionada com o cursor
        if self.dragging_item:
            self.canvas.coords(self.dragging_item, event.x - 20, event.y - 20, event.x + 20, event.y + 20)

    def end_drag(self, event):
        # Solta a cor e verifica se está sobre um quadrado ou sobre a lixeira
        if self.dragging_item:
            overlapping_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
            for item in overlapping_items:
                if "square" in self.canvas.gettags(item) and self.canvas.itemcget(item, "fill") == "white":
                    # Preenche o quadrado com a cor
                    self.canvas.itemconfig(item, fill=self.selected_color)
                    break
                elif "trash" in self.canvas.gettags(item):
                    # Apaga a cor do quadrado se a lixeira for acionada
                    if "square" in self.canvas.gettags(self.dragging_item):
                        # Retorna o quadrado para a posição inicial e torna branco
                        x, y = self.item_positions[self.dragging_item]
                        self.canvas.coords(self.dragging_item, x, y, x + 40, y + 40)
                        self.canvas.itemconfig(self.dragging_item, fill="white")
                    break

            # Retorna a cor para a paleta caso não tenha sido solta em nenhum quadrado
            if "palette" in self.canvas.gettags(self.dragging_item):
                idx = self.colors.index(self.selected_color)
                self.canvas.coords(self.dragging_item, 350, 50 + idx * 50, 390, 90 + idx * 50)

            self.dragging_item = None
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def highlight_square(self, event):
        # Destaca o quadrado sob o cursor
        item = self.canvas.find_withtag("current")[0]
        self.canvas.itemconfig(item, outline="black", width=2)

    def unhighlight_square(self, event):
        # Remove o destaque quando o cursor sai do quadrado
        item = self.canvas.find_withtag("current")[0]
        self.canvas.itemconfig(item, outline="white", width=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = PyramidApp(root)
    root.mainloop()
