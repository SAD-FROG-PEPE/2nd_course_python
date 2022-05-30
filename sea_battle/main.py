from tkinter import *
from tkinter import messagebox
import time
import random

tk = Tk()
app_running = True

canvas_x = canvas_y = 500  # размер окна
s_x = s_y = 10  # размер игрового поля
step_x = canvas_x // s_x  # шаг по горизонтали
step_y = canvas_y // s_y  # шаг по вертикали
canvas_x = step_x * s_x
canvas_y = step_y * s_y

txt_len_middle = "* Human vs Computer"
size_font_x = 10
len_txt_x = len(txt_len_middle) * size_font_x
delta_menu_x = len_txt_x // step_x + 1
menu_x = step_x * delta_menu_x

menu_y = 50
ships_kolvo = s_x // 2  # максимальное кол-во кораблей
ship_len1 = s_x // 5  # длина первого типа корабля
ship_len2 = s_x // 4  # длина второго типа корабля
ship_len3 = s_x // 2  # длина третьего типа корабля
enemy_ships1 = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)]
enemy_ships2 = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)]
list_ids = []  # список объектов canvas

# points1 - список куда мы кликнули мышкой
points1 = [[-1 for i in range(s_x)] for i in range(s_y)]
points2 = [[-1 for i in range(s_x)] for i in range(s_y)]

# ships_list - список кораблей игрока 1 и игрока 2
ships_list = []

# hod_polu_1 - если Истина, то ходит игрок №2, иначе ходит игрок №1
hod_polu_1 = False

# computer_vs_human - если Истина, то играем против компьютера
computer_vs_human = False
if computer_vs_human:
    add_to_label = " (Компьютер)"
    add_to_label2 = " (прицеливается)"
    hod_polu_1 = False
else:
    add_to_label = ""
    add_to_label2 = ""
    hod_polu_1 = False


def on_closing():  # выход из игры
    global app_running
    if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
        app_running = False
        tk.destroy()


# настройка окна
tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Игра Морской Бой")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=canvas_x + menu_x + canvas_x, height=canvas_y + menu_y, bd=0,
                highlightthickness=1, highlightbackground="black")
canvas.create_rectangle(0, 0, canvas_x, canvas_y, fill="misty rose")
canvas.create_rectangle(canvas_x + menu_x, 0, canvas_x + menu_x + canvas_x, canvas_y,
                        fill="lightyellow")
canvas.pack()
tk.update()


# отображение таблиц
def draw_table(offset_x=0):
    for i in range(0, s_x + 1):
        canvas.create_line(offset_x + step_x * i, 0, offset_x + step_x * i, canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(offset_x, step_y * i, offset_x + canvas_x, step_y * i)


draw_table()
draw_table(canvas_x + menu_x)
# отображение текста
t0 = Label(tk, text="Игрок №1", font=("Times", 16))
t0.place(x=canvas_x // 2 - t0.winfo_reqwidth() // 2, y=canvas_y + 3)
t1 = Label(tk, text="Игрок №2" + add_to_label, font=("Times", 16))
t1.place(x=canvas_x + menu_x + canvas_x // 2 - t1.winfo_reqwidth() // 2, y=canvas_y + 3)
t3 = Label(tk, text="@@@@@@@", font=("Times", 16))
t3.place(x=canvas_x + menu_x // 2 - t3.winfo_reqwidth() // 2, y=canvas_y)


# добавление текста если играешь с компьютером
def change_rb():
    global computer_vs_human, add_to_label, add_to_label2
    print(rb_var.get())
    if rb_var.get():
        computer_vs_human = True
        add_to_label = " (Компьютер)"
        add_to_label2 = " (целится...)"
    else:
        computer_vs_human = False
        add_to_label = ""
        add_to_label2 = ""


# радио
rb_var = BooleanVar()
rb1 = Radiobutton(tk, text="Human vs Computer", variable=rb_var, value=1, command=change_rb)
rb2 = Radiobutton(tk, text="Human vs Human", variable=rb_var, value=0, command=change_rb)
rb1.place(x=canvas_x + menu_x // 2 - rb1.winfo_reqwidth() // 2, y=120)
rb2.place(x=canvas_x + menu_x // 2 - rb2.winfo_reqwidth() // 2, y=140)
if computer_vs_human:
    rb1.select()


# маркировка ходов
def mark_igrok(igrok_mark_1):
    if igrok_mark_1:
        t0.configure(bg="palegreen")
        t0.configure(text="Игрок №1" + add_to_label2)
        t0.place(x=canvas_x // 2 - t0.winfo_reqwidth() // 2, y=canvas_y + 3)
        t1.configure(text="Игрок №2" + add_to_label)
        t1.place(x=canvas_x + menu_x + canvas_x // 2 - t1.winfo_reqwidth() // 2, y=canvas_y + 3)
        t1.configure(bg="#f0f0f0")
        t3.configure(text="Ход Игрока №2" + add_to_label)
    else:
        t1.configure(bg="palegreen")
        t0.configure(bg="#f0f0f0")
        t0.configure(text="Игрок №1")
        t0.place(x=canvas_x // 2 - t0.winfo_reqwidth() // 2, y=canvas_y + 3)
        t1.configure(text="Игрок №2" + add_to_label)
        t1.place(x=canvas_x + menu_x + canvas_x // 2 - t1.winfo_reqwidth() // 2, y=canvas_y + 3)
        t3.configure(text="Ход Игрока №1")


mark_igrok(hod_polu_1)


# методы для читерства(для отладки)
def button_show_enemy1():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                color = "red"
                if points1[j][i] != -1:
                    color = "green"
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


def button_show_enemy2():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                color = "red"
                if points2[j][i] != -1:
                    color = "green"
                _id = canvas.create_rectangle(canvas_x + menu_x + i * step_x, j * step_y,
                                              canvas_x + menu_x + i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


# очищение поля и генерация кораблей
def button_begin_again():
    global list_ids
    global points1, points2
    global enemy_ships1, enemy_ships2
    for element in list_ids:
        canvas.delete(element)
    list_ids = []
    generate_ships_list()
    enemy_ships1 = generate_enemy_ships()
    enemy_ships2 = generate_enemy_ships()
    points1 = [[-1 for i in range(s_x)] for i in range(s_y)]
    points2 = [[-1 for i in range(s_x)] for i in range(s_y)]


# кнопки
b0 = Button(tk, text="Показать корабли \n Игрока №1", command=button_show_enemy1)
b0.place(x=canvas_x + menu_x // 2 - b0.winfo_reqwidth() // 2, y=20)
b1 = Button(tk, text="Показать корабли \n Игрока №2", command=button_show_enemy2)
b1.place(x=canvas_x + menu_x // 2 - b1.winfo_reqwidth() // 2, y=70)
b2 = Button(tk, text="Начать заново!", command=button_begin_again)
b2.place(x=canvas_x + menu_x // 2 - b2.winfo_reqwidth() // 2, y=200)


# отметки на поле(+-попал, о-нет)
def draw_point(x, y):
    if enemy_ships1[y][x] == 0:
        color = "brown1"
        id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
        id2 = canvas.create_oval(x * step_x + step_x // 4, y * step_y + step_y // 4, x * step_x + step_x - step_x // 4,
                                 y * step_y + step_y - step_y // 4, fill="misty rose")
        list_ids.append(id1)
        list_ids.append(id2)
    if enemy_ships1[y][x] > 0:
        color = "green2"
        id1 = canvas.create_rectangle(x * step_x, y * step_y + step_y // 2 - step_y // 10, x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        list_ids.append(id2)


def draw_point2(x, y, offset_x=canvas_x + menu_x):
    # print(enemy_ships1[y][x])
    if enemy_ships2[y][x] == 0:
        color = "brown1"
        id1 = canvas.create_oval(offset_x + x * step_x, y * step_y, offset_x + x * step_x + step_x, y * step_y + step_y,
                                 fill=color)
        id2 = canvas.create_oval(offset_x + x * step_x + step_x // 4, y * step_y + step_y // 4,
                                 offset_x + x * step_x + step_x - step_x // 4,
                                 y * step_y + step_y - step_y // 4, fill="lightyellow")
        list_ids.append(id1)
        list_ids.append(id2)
    if enemy_ships2[y][x] > 0:
        color = "green2"
        id1 = canvas.create_rectangle(offset_x + x * step_x, y * step_y + step_y // 2 - step_y // 10,
                                      offset_x + x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(offset_x + x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      offset_x + x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y,
                                      fill=color)
        list_ids.append(id1)
        list_ids.append(id2)


# проверка победителя
def check_winner1():
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                if points1[j][i] == -1:
                    win = False
    return win


def check_winner2():
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                if points2[j][i] == -1:
                    win = False
    return win


# игра компьютера
def hod_computer():
    global points1, points2, hod_polu_1
    tk.update()
    time.sleep(1)
    hod_polu_1 = False
    ip_x = random.randint(0, s_x - 1)
    ip_y = random.randint(0, s_y - 1)
    points1[ip_y][ip_x] = 7
    draw_point(ip_x, ip_y)
    if check_winner1():
        winner = "Победа Игрока №2" + add_to_label
        points1 = [[10 for i in range(s_x)] for i in range(s_y)]
        points2 = [[10 for i in range(s_x)] for i in range(s_y)]
        id3 = canvas.create_text(canvas_x + menu_x // 2, 300, text=winner, font=("Times", 10), justify=CENTER)
        list_ids.append(id3)


# нажатие на поля и вывод победителя
def add_to_all(event):
    global points1, points2, hod_polu_1
    _type = 0  # ЛКМ
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    ip_x = mouse_x // step_x
    ip_y = mouse_y // step_y
    # первое игровое поле
    if ip_x < s_x and ip_y < s_y and hod_polu_1:
        if points1[ip_y][ip_x] == -1:
            points1[ip_y][ip_x] = _type
            hod_polu_1 = False
            draw_point(ip_x, ip_y)
            if check_winner1():
                hod_polu_1 = True
                winner = "Победа Игрока №2"
                points1 = [[10 for i in range(s_x)] for i in range(s_y)]
                points2 = [[10 for i in range(s_x)] for i in range(s_y)]
                id3 = canvas.create_text(canvas_x + menu_x // 2, 300,
                                         text=winner, font=("Times", 10), justify=CENTER)
                list_ids.append(id3)

    # второе игровое поле
    if s_x + delta_menu_x <= ip_x <= s_x + s_x + delta_menu_x and ip_y < s_y and not hod_polu_1:
        if points2[ip_y][ip_x - s_x - delta_menu_x] == -1:
            points2[ip_y][ip_x - s_x - delta_menu_x] = _type
            hod_polu_1 = True
            draw_point2(ip_x - s_x - delta_menu_x, ip_y)
            if check_winner2():
                hod_polu_1 = False
                winner = "Победа Игрока №1"
                points1 = [[10 for i in range(s_x)] for i in range(s_y)]
                points2 = [[10 for i in range(s_x)] for i in range(s_y)]
                id3 = canvas.create_text(canvas_x + menu_x // 2, 300,
                                         text=winner, font=("Times", 10), justify=CENTER)
                list_ids.append(id3)
            elif computer_vs_human:
                mark_igrok(hod_polu_1)
                hod_computer()
    mark_igrok(hod_polu_1)


canvas.bind_all("<Button-1>", add_to_all)  # ЛКМ


# генерируем список случайных длин кораблей
def generate_ships_list():
    global ships_list
    ships_list = []
    for i in range(0, ships_kolvo):
        ships_list.append(random.choice([ship_len1, ship_len2, ship_len3]))


# генерация коробалей противника на основе наших
def generate_enemy_ships():
    global ships_list
    enemy_ships = []
    # подсчет суммарной длины кораблей
    sum_1_all_ships = sum(ships_list)
    sum_1_enemy = 0
    while sum_1_enemy != sum_1_all_ships:
        # обнуляем массив кораблей врага
        enemy_ships = [[0 for i in range(s_x + 1)] for i in
                       range(s_y + 1)]  # +1 для доп. линии справа и снизу, для успешных проверок генерации противника
        for i in range(0, ships_kolvo):
            len = ships_list[i]
            horizont_vertikal = random.randrange(1, 3)  # 1- горизонтальное 2 - вертикальное расположение

            primerno_x = random.randrange(0, s_x)
            if primerno_x + len > s_x:
                primerno_x = primerno_x - len

            primerno_y = random.randrange(0, s_y)
            if primerno_y + len > s_y:
                primerno_y = primerno_y - len

            if horizont_vertikal == 1:
                if primerno_x + len <= s_x:
                    for j in range(0, len):
                        try:
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + enemy_ships[primerno_y][
                                primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j]
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y][primerno_x + j] = i + 1  # записываем номер корабля
                        except Exception:
                            pass
            else:
                if primerno_y + len <= s_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j][primerno_x - 1]
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y + j][primerno_x] = i + 1  # записываем номер корабля
                        except Exception:
                            pass

        # делаем подсчет 1ц
        sum_1_enemy = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1
    return enemy_ships


# генерация короблей и их длин
generate_ships_list()
enemy_ships1 = generate_enemy_ships()
enemy_ships2 = generate_enemy_ships()

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
