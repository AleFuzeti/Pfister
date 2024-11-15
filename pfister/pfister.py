import tkinter as tk
import random

BACKGROUND_COLOR = "#F9E9B6"

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

        self.canvas = tk.Canvas(root, width=800, height=600, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        # Cores iniciais da paleta e contagem de cada cor
        self.colors = {
            "blue1": "#A7E8FC",
            "blue2": "#3E999A",
            "blue3": "#3D87A0",
            "blue4": "#2D2C65",
            "red1": "#FF7E91",
            "red2": "#C72E26",
            "red3": "#A22418",
            "red4": "#88352F",
            "green1": "#D4E80B",
            "green2": "#94DD1C",
            "green3": "#128125",
            "green4": "#2C3E24",
            "violet1": "#ACA3D8",
            "violet2": "#77314D",
            "violet3": "#63476F",
            "yellow1": "#FFFF07",
            "yellow2": "#FEB81A",
            "orange1": "#FF7729",
            "orange2": "#FF4625",
            "brown1": "#79412A",
            "brown2": "#583426",
            "black": "#000000",
            "white": "#FFFFFF",
            "gray": "#7F8F8F"
        }
        self.colors = dict(random.sample(self.colors.items(), len(self.colors)))
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
                    x, y, x + size, y + size, fill=BACKGROUND_COLOR, tags=("square",)  
                )
                self.item_positions[rect] = (x, y)
                self.canvas.tag_bind(rect, "<Button-1>", self.select_square)
                

    def create_palette(self):
        # Cria a paleta de cores com a quantidade abaixo
        for i, color in enumerate(self.colors.values()):
            x0, y0, x1, y1 = self.get_palette_coords(i)
            palette_rect = self.canvas.create_rectangle(
                x0, y0, x1, y1, fill=color, outline="", tags=("palette",)
            )
            self.canvas.tag_bind(palette_rect, "<Button-1>", self.start_drag)

    def select_square(self, event):
        # Seleciona um quadrado colorido para arrastar
        item = self.canvas.find_withtag("current")[0]
        color = self.canvas.itemcget(item, "fill")
        if color != BACKGROUND_COLOR:
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
                    if self.canvas.itemcget(item, "fill") == BACKGROUND_COLOR:
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
                    self.canvas.itemconfig(self.dragging_item, fill=BACKGROUND_COLOR)
                    # Retorna o quadrado original para a posição inicial
                    x, y = self.item_positions[self.dragging_item]
                    self.canvas.coords(self.dragging_item, x, y, x + 40, y + 40)
            else:
                # arraste não foi colocado, retorna à posição original
                if "square" in self.canvas.gettags(self.dragging_item):
                    # se o quadrado for arrastado para fora da piramide, torna branco e volta pra paleta
                    self.canvas.itemconfig(self.dragging_item, fill=BACKGROUND_COLOR)
                    # Retorna o quadrado original para a posição inicial
                    x, y = self.item_positions[self.dragging_item]
                    self.canvas.coords(self.dragging_item, x, y, x + 40, y + 40)
                    
            if "palette" in self.canvas.gettags(self.dragging_item):
                # Devolve a cor para a paleta
                idx = list(self.colors.values()).index(self.selected_color)
                x0, y0, x1, y1 = self.get_palette_coords(idx)
                self.canvas.coords(self.dragging_item, x0, y0, x1, y1)
        
            self.dragging_item = None
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
    
    def get_palette_coords(self, idx):
        row = idx // 6
        col = idx % 6
        x0 = 380 + col * 50
        y0 = 50 + row * 50
        x1 = x0 + 40
        y1 = y0 + 40
        return x0, y0, x1, y1
    
if __name__ == "__main__":
    root = tk.Tk()
    app = PyramidApp(root)
    root.mainloop()
