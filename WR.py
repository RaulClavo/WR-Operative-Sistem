import tkinter as tk
from tkinter import simpledialog, colorchooser, Toplevel, Label, Scale, HORIZONTAL, Canvas, messagebox
import pygame
import os
from datetime import datetime
import time
import calendar
import random

# Inicializar Pygame y la ventana de Tkinter
pygame.init()

# Configuración de la ventana de Tkinter
root = tk.Tk()
root.title("WR Operative Sistem")
root.geometry("1366x768")
width = 1366
height = 768

# Superficie de Pygame dentro de Tkinter
embed = tk.Frame(root, width=width, height=height - 50)  # Ajustar la altura para la barra de tareas
embed.pack()
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
pygame.display.init()
screen = pygame.display.set_mode((width, height))

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW1 = (245, 210, 60)
YELLOW2 = (255, 225, 75)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 115, 255)
BLUE3 = (140, 190, 250)
GREEN = (35, 175, 70)

# Lista para almacenar los objetos del escritorio
objects = []
current_folder = None
mouse_pos = (400, 400)
dragging_obj = None
volume_value = 0


# Redibujar el escritorio
def redraw():
    screen.fill(BLUE3)
    rect1 = pygame.Rect(0, 450, 1366, 768)
    pygame.draw.rect(screen, GREEN, rect1)
    pygame.draw.polygon(screen, GREEN, [(0, 375), (250, 350), (375, 343), (500, 350), (1366, 450), (0, 450)])
    if current_folder:
        for obj in current_folder.contents:
            obj.draw(screen)
    else:
        for obj in objects:
            obj.draw(screen)
    pygame.display.update()
    update_close_button()


class DesktopObject:
    def __init__(self, x, y, text, color):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.text = text
        self.color = color
        self.dragging = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.SysFont("lucindaconsole", 20)
        img = font.render(self.text, True, (0, 0, 0))
        surface.blit(img, (self.rect.x, self.rect.y + 65))


class Folder(DesktopObject):
    def __init__(self, x, y, text, parent=None):
        super().__init__(x, y, text, BLUE1)
        self.contents = []
        self.parent = parent

    def draw(self, surface):
        rect1 = pygame.Rect(self.rect.x, self.rect.y, 48, 60)
        rect2 = pygame.Rect(self.rect.x, self.rect.y, 32, 60)
        pygame.draw.rect(surface, YELLOW1, rect1)
        pygame.draw.rect(surface, YELLOW2, rect2)
        font = pygame.font.SysFont("lucindaconsole", 20)
        img = font.render(self.text, True, (0, 0, 0))
        surface.blit(img, (self.rect.x, self.rect.y + 65))

    def open(self):
        global current_folder
        current_folder = self


class TextFile(DesktopObject):
    def __init__(self, x, y, text, parent=None):
        super().__init__(x, y, text, BLUE1)
        self.content = ""
        self.parent = parent

    def draw(self, surface):
        rect9 = pygame.Rect(self.rect.x, self.rect.y, 48, 60)
        rect1 = pygame.Rect(self.rect.x, self.rect.y, 48, 60)
        rect2 = pygame.Rect(self.rect.x + 5, self.rect.y + 7, 38, 3)
        rect3 = pygame.Rect(self.rect.x + 5, self.rect.y + 14, 38, 3)
        rect4 = pygame.Rect(self.rect.x + 5, self.rect.y + 21, 38, 3)
        rect5 = pygame.Rect(self.rect.x + 5, self.rect.y + 28, 38, 3)
        rect6 = pygame.Rect(self.rect.x + 5, self.rect.y + 35, 38, 3)
        rect7 = pygame.Rect(self.rect.x + 5, self.rect.y + 42, 38, 3)
        rect8 = pygame.Rect(self.rect.x + 5, self.rect.y + 49, 38, 3)
        pygame.draw.rect(surface, WHITE, rect9)
        pygame.draw.rect(surface, BLACK, rect1, 3)
        pygame.draw.rect(surface, BLACK, rect2, 3)
        pygame.draw.rect(surface, BLACK, rect3, 3)
        pygame.draw.rect(surface, BLACK, rect4, 3)
        pygame.draw.rect(surface, BLACK, rect5, 3)
        pygame.draw.rect(surface, BLACK, rect6, 3)
        pygame.draw.rect(surface, BLACK, rect7, 3)
        pygame.draw.rect(surface, BLACK, rect8, 3)
        font = pygame.font.SysFont("lucindaconsole", 20)
        img = font.render(self.text, True, (0, 0, 0))
        surface.blit(img, (self.rect.x, self.rect.y + 65))

    def open(self):
        text_editor = tk.Toplevel(root)
        text_editor.title(self.text)
        text_editor.geometry("400x500")

        text_widget = tk.Text(text_editor)
        text_widget.pack(expand=True, fill='both')
        text_widget.insert('1.0', self.content)

        def save_and_close():
            self.content = text_widget.get('1.0', 'end-1c')
            text_editor.destroy()

        save_button = tk.Button(text_editor, text="Cerrar y Guardar", command=save_and_close)
        save_button.pack()


class ImageFile(DesktopObject):
    def __init__(self, x, y, text, pixel_data=None):
        super().__init__(x, y, text, BLUE1)
        self.canvas = None
        self.current_color = (0, 0, 0)  # Negro como color predeterminado
        self.brush_size = 5
        if pixel_data is None:
            self.pixel_data = [[(255, 255, 255) for _ in range(300)] for _ in range(300)]  # Inicializa con blanco
        else:
            self.pixel_data = pixel_data

    def draw(self, surface):
        rect1 = pygame.Rect(self.rect.x, self.rect.y, 60, 60)
        pygame.draw.rect(surface, BLUE1, rect1)
        pygame.draw.polygon(surface, BLUE2, [(self.rect.x, self.rect.y + 60), (self.rect.x, self.rect.y + 45),
                                             (self.rect.x + 30, self.rect.y + 30), (self.rect.x + 59, self.rect.y + 45),
                                             (self.rect.x + 59, self.rect.y + 60)])
        pygame.draw.circle(surface, BLUE2, (self.rect.x + 45, self.rect.y + 20), 6)
        font = pygame.font.SysFont("lucindaconsole", 20)
        img = font.render(self.text, True, (0, 0, 0))
        surface.blit(img, (self.rect.x, self.rect.y + 65))

    def open(self):
        image_editor = tk.Toplevel(root)
        image_editor.title(self.text)
        image_editor.geometry("300x340")  # Ajusta la altura para dejar espacio para los botones

        self.canvas = tk.Canvas(image_editor, bg='white', width=300, height=300)  # Reducido el tamaño del lienzo
        self.canvas.pack(expand=True, fill='both')

        def change_color():
            color = colorchooser.askcolor(color=self.rgb_to_hex(self.current_color))[1]
            if color:
                self.current_color = self.hex_to_rgb(color)

        def change_brush_size(sizes):
            self.brush_size = sizes

        def paint(event):
            x, y = event.x, event.y
            r = self.brush_size // 2
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.rgb_to_hex(self.current_color), outline="")
            # Guarda el color en la lista de píxeles
            for i in range(max(0, x - r), min(300, x + r)):
                for j in range(max(0, y - r), min(300, y + r)):
                    self.pixel_data[j][i] = self.current_color

        self.canvas.bind('<B1-Motion>', paint)

        color_button = tk.Button(image_editor, text="Seleccionar Color", command=change_color)
        color_button.pack(side=tk.LEFT)

        brush_size_frame = tk.Frame(image_editor)
        brush_size_frame.pack(side=tk.LEFT)
        for size in [2, 5, 10, 20]:
            brush_button = tk.Button(brush_size_frame, text=str(size), command=lambda s=size: change_brush_size(s))
            brush_button.pack(side=tk.LEFT)

        def save_and_close():
            # Guarda los cambios si es necesario
            image_editor.destroy()

        save_button = tk.Button(image_editor, text="Cerrar y Guardar", command=save_and_close)
        save_button.pack(side=tk.RIGHT)

        # Dibujar la imagen inicial
        self.draw_initial_image()

    def draw_initial_image(self):
        for y, row in enumerate(self.pixel_data):
            for x, color in enumerate(row):
                self.canvas.create_rectangle(x, y, x + 1, y + 1, fill=self.rgb_to_hex(color), outline="")

    @staticmethod
    def rgb_to_hex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    @staticmethod
    def hex_to_rgb(hex_string):
        return tuple(int(hex_string[i:i + 2], 16) for i in (1, 3, 5))

    @staticmethod
    def rgb_to_int(rgb):
        return tuple(int(x) for x in rgb)


def new_folder():
    folder = Folder(mouse_pos[0], mouse_pos[1], "Carpeta", current_folder)
    if current_folder:
        current_folder.contents.append(folder)
    else:
        objects.append(folder)


def new_text_file():
    text_file = TextFile(mouse_pos[0], mouse_pos[1], "Texto", current_folder)
    if current_folder:
        current_folder.contents.append(text_file)
    else:
        objects.append(text_file)


def new_image_file():
    image_file = ImageFile(mouse_pos[0], mouse_pos[1], "Imagen", current_folder)
    if current_folder:
        current_folder.contents.append(image_file)
    else:
        objects.append(image_file)


def rename_object(obj):
    new_name = simpledialog.askstring("Renombrar", "Nuevo nombre:")
    if new_name:
        obj.text = new_name


def delete_object(obj):
    if current_folder:
        current_folder.contents.remove(obj)
    else:
        objects.remove(obj)


def show_context_menu(event):
    global mouse_pos
    mouse_pos = (event.x, event.y)
    clicked_obj = None
    if current_folder:
        for obj in current_folder.contents:
            if obj.rect.collidepoint(mouse_pos):
                clicked_obj = obj
                break
    else:
        for obj in objects:
            if obj.rect.collidepoint(mouse_pos):
                clicked_obj = obj
                break
    if clicked_obj:
        if isinstance(clicked_obj, Folder) or isinstance(clicked_obj, TextFile) or isinstance(clicked_obj, ImageFile):
            obj_context_menu.entryconfig("Abrir", command=clicked_obj.open)
        else:
            obj_context_menu.entryconfig("Abrir", state=tk.DISABLED)
        obj_context_menu.entryconfig("Renombrar", command=lambda: rename_object(clicked_obj))
        obj_context_menu.entryconfig("Eliminar", command=lambda: delete_object(clicked_obj))
        obj_context_menu.tk_popup(event.x_root, event.y_root)
    else:
        desktop_context_menu.tk_popup(event.x_root, event.y_root)


def close_folder():
    global current_folder
    if current_folder:
        current_folder = current_folder.parent
    redraw()


def update_close_button():
    if current_folder:
        close_button.place(x=10, y=10)
    else:
        close_button.place_forget()


def new_calculator():
    calculator_window = tk.Toplevel(root)
    calculator_window.title("Calculadora")
    calculator_window.geometry("300x400")

    def add_to_display(char):
        display_var.set(display_var.get() + char)

    def clear_display():
        display_var.set("")

    def calculate():
        try:
            result = eval(display_var.get())
            display_var.set(str(result))
        except:
            messagebox.showerror("Error", "Expresión inválida")

    display_var = tk.StringVar()
    display = tk.Entry(calculator_window, textvariable=display_var, font=("Helvetica", 20), justify="right")
    display.pack(expand=True, fill="x")

    button_frame = tk.Frame(calculator_window)
    button_frame.pack(expand=True, fill="both")

    for row in range(4):
        button_frame.grid_rowconfigure(row, weight=1)
        for col in range(3):
            button_frame.grid_columnconfigure(col, weight=1)
            button_text = str(9 - (3 * row + col))
            if button_text == "0":
                button_text = "0"
            button = tk.Button(button_frame, text=button_text, font=("Helvetica", 16),
                               command=lambda char=button_text: add_to_display(char))
            button.grid(row=row, column=col, sticky="nsew")

    operator_buttons = ["+", "-", "*", "/"]
    for index, operator in enumerate(operator_buttons):
        button_frame.grid_rowconfigure(index, weight=1)
        button_frame.grid_columnconfigure(3, weight=1)
        button = tk.Button(button_frame, text=operator, font=("Helvetica", 16),
                           command=lambda char=operator: add_to_display(char))
        button.grid(row=index, column=3, sticky="nsew")

    button_frame.grid_rowconfigure(3, weight=1)
    for col in range(2):
        button_frame.grid_columnconfigure(col, weight=1)
        clear_button = tk.Button(button_frame, text="C", font=("Helvetica", 16), command=clear_display)
        clear_button.grid(row=3, column=col, sticky="nsew")

    button_frame.grid_columnconfigure(2, weight=1)
    equal_button = tk.Button(button_frame, text="=", font=("Helvetica", 16), command=calculate)
    equal_button.grid(row=3, column=2, columnspan=2, sticky="nsew")


def new_tictactoe():
    def check_winner():
        # Verificar filas y columnas
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != "":
                return True
            if board[0][i] == board[1][i] == board[2][i] != "":
                return True
        # Verificar diagonales
        if board[0][0] == board[1][1] == board[2][2] != "":
            return True
        if board[0][2] == board[1][1] == board[2][0] != "":
            return True
        return False

    def on_click(fila, columna):
        nonlocal current_player
        nonlocal game_over
        if not game_over and board[fila][columna] == "":
            board[fila][columna] = current_player
            buttons[fila][columna].config(text=current_player)
            if check_winner():
                messagebox.showinfo("¡Felicidades!", f"¡El jugador {current_player} ha ganado!")
                game_over = True
            elif all(cell != "" for filas in board for cell in filas):
                messagebox.showinfo("¡Empate!", "¡El juego ha terminado en empate!")
                game_over = True
            else:
                current_player = "O" if current_player == "X" else "X"
        if game_over:
            tictactoe_window.destroy()

    tictactoe_window = tk.Toplevel(root)
    tictactoe_window.title("Tres en Raya")

    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False

    buttons = []
    for row in range(3):
        button_row = []
        for col in range(3):
            button = tk.Button(tictactoe_window, text="", width=6, height=3, font=("Helvetica", 16),
                               command=lambda r=row, c=col: on_click(r, c))
            button.grid(row=row, column=col, padx=5, pady=5)
            button_row.append(button)
        buttons.append(button_row)


def show_widgets_menu():
    global mouse_pos
    widgets_menu.tk_popup(mouse_pos[0], mouse_pos[1])


# Menú contextual para el escritorio
desktop_context_menu = tk.Menu(root, tearoff=0)
desktop_context_menu.add_command(label="Nueva Carpeta", command=new_folder)
desktop_context_menu.add_command(label="Nuevo Fichero de Texto", command=new_text_file)
desktop_context_menu.add_command(label="Nuevo Fichero de Imagen", command=new_image_file)
desktop_context_menu.add_separator()  # Separador
desktop_context_menu.add_command(label="Widgets")
desktop_context_menu.entryconfig("Widgets", command=show_widgets_menu)

# Menú de Widgets
widgets_menu = tk.Menu(root, tearoff=0)
widgets_menu.add_command(label="Calculadora", command=new_calculator)
widgets_menu.add_command(label="Tic Tac Toe", command=new_tictactoe)

# Menú contextual para los objetos
obj_context_menu = tk.Menu(root, tearoff=0)
obj_context_menu.add_command(label="Abrir")
obj_context_menu.add_command(label="Renombrar")
obj_context_menu.add_command(label="Eliminar")

# Botón para cerrar la carpeta
close_button = tk.Button(root, text="Cerrar Carpeta", command=close_folder)

# Asignar el evento del clic derecho al escritorio
root.bind("<Button-3>", show_context_menu)


def handle_mouse_event(event):
    global dragging_obj
    if event.type == pygame.MOUSEBUTTONDOWN:
        if current_folder:
            for obj in current_folder.contents:
                if obj.rect.collidepoint(event.pos):
                    if event.button == 1:
                        obj.dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = obj.rect.x - mouse_x
                        offset_y = obj.rect.y - mouse_y
                        dragging_obj = (obj, offset_x, offset_y)
                        break
        else:
            for obj in objects:
                if obj.rect.collidepoint(event.pos):
                    if event.button == 1:
                        obj.dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = obj.rect.x - mouse_x
                        offset_y = obj.rect.y - mouse_y
                        dragging_obj = (obj, offset_x, offset_y)
                        break
    elif event.type == pygame.MOUSEBUTTONUP:
        if dragging_obj:
            dragging_obj[0].dragging = False
            dragging_obj = None
    elif event.type == pygame.MOUSEMOTION:
        if dragging_obj:
            mouse_x, mouse_y = event.pos
            dragging_obj[0].rect.x = mouse_x + dragging_obj[1]
            dragging_obj[0].rect.y = mouse_y + dragging_obj[2]


# Crear la barra de tareas
taskbar = tk.Frame(root, bg="blue", height=60, bd=0)  # Hacer la barra más alta y azul
taskbar.pack(side=tk.BOTTOM, fill=tk.X)


# Función para mostrar el control deslizante de volumen
def show_volume_slider(event):
    global volume_value
    volume_slider_window = tk.Toplevel(root)
    volume_slider_window.title("Volumen")
    volume_slider_window.geometry("300x100")  # Más alargado hacia los lados y más corto hacia arriba y abajo
    volume_slider = Scale(volume_slider_window, from_=0, to=100, orient=HORIZONTAL, label="Volumen")
    volume_slider.set(volume_value)  # Establecer el valor guardado
    volume_slider.pack(expand=True, fill='both')
    volume_close_button = tk.Button(volume_slider_window, text="Cerrar",
                                    command=lambda: close_volume_slider(volume_slider_window, volume_slider))
    volume_close_button.pack()


def close_volume_slider(window, slider):
    global volume_value
    volume_value = slider.get()  # Guardar el valor del slider al cerrar la ventana
    window.destroy()


# Reloj digital
clock_label = tk.Label(taskbar, text="", fg="white", bg="blue", font=("Helvetica", 16))
clock_label.pack(side=tk.RIGHT, padx=(0, 10))  # Colocar a la derecha


# Función para apagar la aplicación
def shutdown_app():
    root.destroy()  # Cierra la aplicación


# Botón de apagado
shutdown_button = tk.Canvas(taskbar, width=1200, height=30, bg="blue", highlightthickness=0)
shutdown_button.pack(side=tk.LEFT, padx=(10, 0))  # Ajuste de coordenadas para colocar en la esquina izquierda
shutdown_button.create_oval(5, 5, 25, 25, outline="white", width=2)
shutdown_button.create_line(8, 15, 22, 15, fill="white", width=2)
shutdown_button.create_line(10, 20, 20, 20, fill="white", width=2)

# Asocia la función de apagado al botón
shutdown_button.bind("<Button-1>", lambda event: shutdown_app())

# Botón de volumen (triángulo de Pygame)
volume_button = tk.Canvas(taskbar, width=30, height=30, bg="blue", highlightthickness=0)
volume_button.pack(side=tk.LEFT, padx=(10, 0))  # Colocar a la izquierda
volume_button.create_polygon(5, 15, 15, 5, 15, 25, 5, 15, fill="white")  # Pico apuntando hacia la izquierda

# Triángulo con un pico hacia la izquierda
volume_button.create_polygon(5, 15, 15, 5, 15, 25, 5, 15, fill="white")

# Barra en paralelo con el triángulo
volume_button.create_rectangle(17, 10, 20, 20, fill="white")

# Barra a la derecha del triángulo
volume_button.create_rectangle(20, 7, 24, 23, fill="white")

volume_button.bind("<Button-1>", show_volume_slider)


def update_clock():
    now = datetime.now()
    clock_label.config(text=now.strftime("%H:%M:%S"))
    root.after(1000, update_clock)


update_clock()


# Función para mostrar un reloj grande y un calendario
def show_large_clock(event):
    now = datetime.now()
    clock_window = tk.Toplevel(root)
    clock_window.title("Reloj y Calendario")
    clock_window.geometry("400x400")

    time_label = tk.Label(clock_window, text=now.strftime("%H:%M:%S"), font=("Helvetica", 48))
    time_label.pack(pady=20)

    def update_large_clock():
        rnow = datetime.now()
        time_label.config(text=rnow.strftime("%H:%M:%S"))
        clock_window.after(1000, update_large_clock)

    update_large_clock()

    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(now.year, now.month)

    cal_frame = tk.Frame(clock_window)
    cal_frame.pack()

    for week in month_days:
        week_frame = tk.Frame(cal_frame)
        week_frame.pack()
        for day in week:
            day_label = tk.Label(week_frame, text=str(day) if day != 0 else "", width=4, height=2,
                                 bg="yellow" if day == now.day else "white")
            day_label.pack(side=tk.LEFT)

    clock_close_button = tk.Button(clock_window, text="Cerrar", command=clock_window.destroy)
    clock_close_button.pack(pady=10)  # Añadir espacio alrededor del botón de cerrar


clock_label.bind("<Button-1>", show_large_clock)


def check_password():
    # Solicitar la contraseña al usuario
    password = simpledialog.askstring("Pantalla de bloqueo", "Ingresa la contraseña:", show="*")
    # Verificar si la contraseña es correcta
    if password == "1234":
        # Si es correcta, continuar con el programa principal
        pass
    else:
        messagebox.showerror("Error", "Contraseña incorrecta. La aplicación se cerrará.")
        root.destroy()

# Bucle principal
def mainloop():
    while True:
        for event in pygame.event.get():
            handle_mouse_event(event)
        root.update()
        redraw()

check_password()
mainloop()
