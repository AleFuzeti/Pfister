import tkinter as tk

class PyramidApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pyramid with Color Palette")
        
        # Configura a janela em modo de janela e centraliza
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 800
        window_height = 600
        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # Cores iniciais da paleta e contagem de cada cor
        self.colors = [
            "#FF0000", "#00FF00", "#0000FF", "#FFFF00",
            "#FF00FF", "#00FFFF", "#800000", "#808000",
            "#008000", "#800080", "#008080", "#000080",
            "#FFA500", "#A52A2A", "#8A2BE2", "#5F9EA0",
            "#D2691E", "#FF7F50", "#6495ED", "#DC143C",
            "#B0E0E6", "#FFD700", "#ADFF2F", "#FF69B4"
        ]
        self.color_counts = {color: 50 for color in self.colors}
        self.color_count_texts = {}
        self.selected_color = None
        self.dragging_item = None
        self.item_positions = {}

        self.create_pyramid()
        self.create_palette()

    def create_pyramid(self):
        size = 40
        # Cria a pirâmide de quadrados brancos
        for i in range(5):
            for j in range(i + 1):
                x = 200 - (i * size / 2) + (j * size)
                y = 50 + (i * size)
                rect = self.canvas.create_rectangle(
                    x, y, x + size, y + size, fill="white", tags="square"
                )
                self.item_positions[rect] = (x, y)
                self.canvas.tag_bind(rect, "<Button-1>", self.select_square)
                

    def create_palette(self):
        # Cria a paleta de cores com a quantidade abaixo
        for i, color in enumerate(self.colors):
            row = i // 6
            col = i % 6
            x0 = 350 + col * 50
            y0 = 50 + row * 70
            x1 = x0 + 40
            y1 = y0 + 40
            palette_rect = self.canvas.create_rectangle(
                x0, y0, x1, y1, fill=color, tags=("palette", color)
            )
            self.canvas.tag_bind(palette_rect, "<Button-1>", self.start_drag)
            count_text = self.canvas.create_text(
                (x0 + x1) / 2, y1 + 10, text=str(self.color_counts[color]), tags=("count", color)
            )
            self.color_count_texts[color] = count_text

    def select_square(self, event):
        # Seleciona um quadrado colorido para arrastar
        item = self.canvas.find_withtag("current")[0]
        color = self.canvas.itemcget(item, "fill")
        if color != "white":
            self.dragging_item = item
            self.selected_color = color
            self.canvas.tag_raise(self.dragging_item)
            self.canvas.bind("<Motion>", self.drag_motion)
            self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        else:
            self.dragging_item = None

    def start_drag(self, event):
        # Inicia o arrasto se houver unidades disponíveis
        item = self.canvas.find_withtag("current")[0]
        color = self.canvas.itemcget(item, "fill")
        if self.color_counts[color] > 0:
            self.dragging_item = item
            self.selected_color = color
            self.canvas.tag_raise(self.dragging_item)
            self.canvas.bind("<Motion>", self.drag_motion)
            self.canvas.bind("<ButtonRelease-1>", self.end_drag)

    def drag_motion(self, event):
        # Move o item com o cursor
        if self.dragging_item:
            self.canvas.coords(
                self.dragging_item,
                event.x - 20,
                event.y - 20,
                event.x + 20,
                event.y + 20,
            )

    def end_drag(self, event):
        # Solta a cor e verifica se está sobre um quadrado
        if self.dragging_item:
            overlapping_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
            placed = False
            for item in overlapping_items:
                if "square" in self.canvas.gettags(item):
                    if self.canvas.itemcget(item, "fill") == "white":
                        # Preenche o quadrado de destino com a cor
                        self.canvas.itemconfig(item, fill=self.selected_color)
                        placed = True
                    else:
                        # Destino já pintado, retorna à posição original
                        placed = False
                    break
            if placed:
                # Torna o quadrado original branco
                if "square" in self.canvas.gettags(self.dragging_item):
                    self.canvas.itemconfig(self.dragging_item, fill="white")
                    # Retorna o quadrado original para a posição inicial
                    x, y = self.item_positions[self.dragging_item]
                    self.canvas.coords(self.dragging_item, x, y, x + 40, y + 40)
                elif "palette" in self.canvas.gettags(self.dragging_item):
                    # Decrementa a contagem
                    self.color_counts[self.selected_color] -= 1
                    self.update_color_count(self.selected_color)
            else:
                # arraste não foi colocado, retorna à posição original
                if "square" in self.canvas.gettags(self.dragging_item):
                    # se o quadrado for arrastado para fora da piramide, torna branco e volta pra paleta
                    self.canvas.itemconfig(self.dragging_item, fill="white")
                    # incrementa a contagem
                    self.color_counts[self.selected_color] += 1
                    self.update_color_count(self.selected_color)
                    # Retorna o quadrado original para a posição inicial
                    x, y = self.item_positions[self.dragging_item]
                    self.canvas.coords(self.dragging_item, x, y, x + 40, y + 40)
                    
            if "palette" in self.canvas.gettags(self.dragging_item):
                # Desabilita a cor se a contagem chegar a zero
                if self.color_counts[self.selected_color] == 0:
                    self.disable_color(self.selected_color)
                else:
                    # Devolve a cor para a paleta
                    idx = self.colors.index(self.selected_color)
                    row = idx // 6
                    col = idx % 6
                    x0 = 350 + col * 50
                    y0 = 50 + row * 70
                    x1 = x0 + 40
                    y1 = y0 + 40
                    self.canvas.coords(self.dragging_item, x0, y0, x1, y1)
            
            self.dragging_item = None
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def update_color_count(self, color):
        # Atualiza o texto da contagem
        text_item = self.color_count_texts[color]
        self.canvas.itemconfig(text_item, text=str(self.color_counts[color]))

    def disable_color(self, color):
        # Desabilita a cor quando a contagem chega a zero
        items = self.canvas.find_withtag(color)
        for item in items:
            self.canvas.itemconfig(item, state="disabled", stipple="gray50")

    def enable_color(self, color):
        # Reabilita a cor na paleta
        items = self.canvas.find_withtag(color)
        for item in items:
            self.canvas.itemconfig(item, state="normal", stipple="")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyramidApp(root)
    root.mainloop()
