import tkinter

#глобальные переменные - виджеты
окно = None
холст = None
поле_величина_задержки = None
кнопка_расчитать = None

#другие глобальные переменные
размер_доски = 400
ширина_информационной_панели = 150

цвет_фона_доски = '#F5F5E5'
цвет_фона_информационной_панели = None

цвет_белой_клетки = None
цвет_черной_клетки = None

выбранная_фигура = None

отладка = None
анимация = None


def init_gui(info_panel = False):
    global окно, холст, поле_величина_задержки, кнопка_расчитать,\
           ширина_информационной_панели, выбранная_фигура, \
           отладка, анимация

    if not info_panel:
        ширина_информационной_панели = 0

    w = h = размер_доски

    окно = tkinter.Tk()
    окно.title("Chess")

    mw = окно.winfo_screenwidth()
    mh = окно.winfo_screenheight()

    окно.geometry("{}x{}+{}+{}".format(w + ширина_информационной_панели + 20, h + 20, (mw - w) // 2, (mh - h) // 2))
    окно.resizable(0, 0)

    контейнер1 = tkinter.Frame(master = окно)
    контейнер1.place(x = 0, y = 0, width = w + 20, height = h + 20)

    холст = tkinter.Canvas(master = контейнер1, background = цвет_фона_доски)
    холст.pack(fill = tkinter.BOTH, expand=True)

    if info_panel:
        контейнер2 = tkinter.Frame(master = окно, background = цвет_фона_информационной_панели)
        контейнер2.place(x = w + 20, y = 0, width = ширина_информационной_панели - 20, height = h + 20)

        отладка = tkinter.BooleanVar()
        отладка.set(1)
        флажок_отладка = tkinter.Checkbutton(master = контейнер2, text = 'Отладка', variable = отладка, background = цвет_фона_информационной_панели)
        флажок_отладка.place(x = 20, y = 0)

        анимация = tkinter.BooleanVar()
        анимация.set(1)
        флажок_анимация = tkinter.Checkbutton(master = контейнер2, text = 'Анимация', variable = анимация, background = цвет_фона_информационной_панели)
        флажок_анимация.place(x = 20, y = 30)

        метка_величина_задержки = tkinter.Label(master = контейнер2, text = 'Задержка, с:', background = цвет_фона_информационной_панели)
        метка_величина_задержки.place(x = 20, y = 50)

        поле_величина_задержки = tkinter.Spinbox(master = контейнер2, from_ = 0, to = 1, increment = 0.1)
        поле_величина_задержки.place(x = 20, y = 70, width = 100)

        кнопка_расчитать = tkinter.Button(master = контейнер2, text = 'Рассчитать', foreground = 'red')
        кнопка_расчитать.place(x = 20, y = 110, width = 100)

        метка_выбранная_фигура = tkinter.Label(master = контейнер2, text = 'Фигура:', background = цвет_фона_информационной_панели)
        метка_выбранная_фигура.place(x = 20, y = 150)

        ФИГУРЫ = [
                'конь',
                'ладья',
                'король',
                'ферзь'
        ]

        выбранная_фигура = tkinter.StringVar()
        выбранная_фигура.set('король')

        for i, фигура in enumerate(ФИГУРЫ):
            b = tkinter.Radiobutton(master = контейнер2, text = фигура, variable = выбранная_фигура, value = фигура, indicatoron = 0)
            b.place(x = 20, y = 170 + i*20, width = 100)


def get_delay():
    try:
        задержка = поле_величина_задержки.get()
    except:
        задержка = 0

    return float(задержка)


def get_debug():
    return отладка.get()


def get_animate():
    return анимация.get()


def get_selected_figure():
    return выбранная_фигура.get()


def draw_board(whitecolor = None, blackcolor = None):
    global цвет_белой_клетки, цвет_черной_клетки

    #запомним расцветку клеток. пригодится при очистке доски
    цвет_белой_клетки = whitecolor
    цвет_черной_клетки = blackcolor

    сторона_квадрата = размер_доски // 8

    номер_квадратика = 0
    for iy in range(8):
        номер_квадратика += 1

        for ix in range(8):
            номер_квадратика += 1
            if номер_квадратика % 2 == 1:
                цвет_клетки = blackcolor
            else:
                цвет_клетки = whitecolor

            холст.create_rectangle(ix*сторона_квадрата+5, iy*сторона_квадрата+5,
                                   (ix+1)*сторона_квадрата+5, (iy+1)*сторона_квадрата+5,
                                   fill = цвет_клетки, width = 1,
                                   tags = "rect{}{}".format(iy+1, ix+1))

    буквы = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for ix in range(8):
        холст.create_text(сторона_квадрата*(ix + 0.5), размер_доски + 10, text = буквы[ix])

    for iy in range(8):
        холст.create_text(размер_доски + 12, размер_доски - сторона_квадрата*(iy + 0.5), text = iy+1)


def highlight_cell(ix, iy, color, kind = 'dot'):
    tag = None
    rect_tag = 'rect{}{}'.format(iy, ix)

    #пользователь захотел подсветить всю клетку
    if kind == 'rect':
        tag = rect_tag

    # пользователь захотел подсветить кружок в центре клетки
    if kind == 'dot':
        dot_tag = 'dot {}{}'.format(iy, ix)

        try:
            rect = холст.coords(rect_tag)

            tag = холст.find_withtag(dot_tag)

            if tag == ():
                сторона_квадрата = размер_доски // 8

                rect_center_x = rect[0] + сторона_квадрата // 2
                rect_center_y = rect[1] + сторона_квадрата // 2

                холст.create_oval(rect_center_x - 5, rect_center_y - 5, rect_center_x + 5, rect_center_y + 5, tags = dot_tag)

            tag = dot_tag
        except:
            pass

    #меняем цвет подсвечиваемого элемента (того, на который указывает tag)
    try:
        холст.itemconfig(tag, fill = color)

        окно.update_idletasks()
        окно.update()
    except:
        pass


def draw_arrow(ix_from, iy_from, ix_to, iy_to, color = "black", width = 1):
    tag_from = 'rect{}{}'.format(iy_from, ix_from)
    tag_to = 'rect{}{}'.format(iy_to, ix_to)

    сторона_квадрата = размер_доски // 8

    try:
        rect_from = холст.coords(tag_from)
        rect_to = холст.coords(tag_to)

        from_x = rect_from[0] + сторона_квадрата // 2
        from_y = rect_from[1] + сторона_квадрата // 2
        to_x = rect_to[0] + сторона_квадрата // 2
        to_y = rect_to[1] + сторона_квадрата // 2

        tag = 'line{}{}{}{}'.format(iy_from, ix_from, iy_to, ix_to)
        холст.create_line(from_x, from_y, to_x, to_y, fill = color, arrow = tkinter.LAST, width = width, tags = tag)

        окно.update_idletasks()
        окно.update()
    except:
        pass


def draw_text(ix, iy, text, color = None):
    tag = 'rect{}{}'.format(iy, ix)

    сторона_квадрата = размер_доски // 8

    try:
        rect = холст.coords(tag)

        x = rect[0] + сторона_квадрата // 2
        y = rect[1] + сторона_квадрата // 2

        холст.create_text(x, y, fill = color, text = text, tags = 'text{}{}'.format(iy, ix))

        окно.update_idletasks()
        окно.update()
    except:
        pass


def remove_text(ix, iy):
    tag = 'text{}{}'.format(iy, ix)
    холст.delete(tag)


def remove_arrow(ix_from, iy_from, ix_to, iy_to):
    tag = 'line{}{}{}{}'.format(iy_from, ix_from, iy_to, ix_to)
    холст.delete(tag)


def clear_board():
    try:
        for элемент in холст.find_all():
            холст.delete(элемент)

        draw_board(whitecolor = цвет_белой_клетки, blackcolor = цвет_черной_клетки)
    except:
        pass


if __name__ == '__main__':
    init_gui(info_panel = True)

    draw_board()

    окно.mainloop()


