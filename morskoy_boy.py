from tkinter import *
from tkinter import messagebox
import time

tk = Tk()
app_running = True

size_canvas_x = 500
size_canvas_y = 500

ship_image = PhotoImage(file='images/animation.gif')
bullet_image = PhotoImage(file='images/img_1.png').subsample(3, 3)

counter_ships = 10
counter_dead_ships = 0
counter_bullets = 10


def on_closing():
    global app_running
    app_running = False
    tk.destroy()


def generate_enemy_ships(ship_image):
    global counter_ships
    counter_ships -= 1
    check_game_status()
    ship = canvas.create_image(0, 0, image=ship_image, anchor=NW, tags="ship")
    move_ship(ship)
    update_info_labels()


def move_ship(ship):
    x, y = canvas.coords(ship)
    x += 1
    canvas.coords(ship, x, y)
    if x >= size_canvas_x:
        canvas.delete(ship)
        respawn_ship()
    else:
        tk.after(10, move_ship, ship)


def respawn_ship():
    global counter_ships
    counter_ships -= 1
    check_game_status()
    ship = canvas.create_image(0, 0, image=ship_image, anchor=NW, tags="ship")
    move_ship(ship)
    update_info_labels()


def generate_gun():
    canvas.create_rectangle(190, 480, 310, 500, fill="black")
    canvas.create_rectangle(240, 460, 260, 480, fill="black")


def create_bullet(event):
    global bullet_image
    global counter_bullets
    counter_bullets -= 1
    check_game_status()
    bullet = canvas.create_image(230, 380, image=bullet_image, anchor=NW)
    fly_bullet(bullet)
    update_info_labels()


def fly_bullet(bullet):
    x, y = canvas.coords(bullet)
    y -= 1
    canvas.coords(bullet, x, y)
    if y <= 0:
        canvas.delete(bullet)
        update_info_labels()
        check_game_status()
    else:
        if y > 0:
            tk.after(5, fly_bullet, bullet)
        check_collision(bullet)


def check_collision(bullet):
    global counter_dead_ships
    x_bullet, y_bullet = canvas.coords(bullet)
    ship_objects = canvas.find_withtag("ship")
    for ship in ship_objects:
        x_ship, y_ship, width_ship, height_ship = canvas.bbox(ship)
        if (x_ship < x_bullet < x_ship + width_ship) and (y_ship < y_bullet < y_ship + height_ship):
            canvas.delete(ship)
            canvas.delete(bullet)
            counter_dead_ships += 1
            update_info_labels()
            respawn_ship()
            break
    check_game_status()


def check_game_status():
    global counter_dead_ships, counter_bullets
    if counter_dead_ships == 10:
        messagebox.showinfo("Результат игры", "Победа!")
        on_closing()
    elif counter_ships <= 0 and counter_bullets < 0:
        messagebox.showinfo("Результат игры", "Поражение!")
        on_closing()
    elif counter_ships < 0 or counter_bullets < 0:
        messagebox.showinfo("Результат игры", "Поражение!")
        on_closing()


def update_info_labels():
    bullets_label.config(text=f"Оставшиеся пули: {counter_bullets}")
    dead_ships_label.config(text=f"Подбитые корабли: {counter_dead_ships}")
    ships_left_label.config(text=f"Оставшиеся корабли: {counter_ships}")


tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Игра Морской Бой")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=size_canvas_x, height=size_canvas_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
canvas.pack()

bullets_label = Label(tk, text=f"Оставшиеся пули: {counter_bullets}")
bullets_label.pack()

dead_ships_label = Label(tk, text=f"Подбитые корабли: {counter_dead_ships}")
dead_ships_label.pack()

ships_left_label = Label(tk, text=f"Оставшиеся корабли: {counter_ships}")
ships_left_label.pack()

tk.update()

generate_gun()
generate_enemy_ships(ship_image)
tk.bind("<space>", create_bullet)

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
