import tkinter

размер_доски = 400

окно = None
холст = None

def init_gui():
    global окно, холст

    окно = tkinter.Tk()
    # окно.config(width = 600, height = 600, background = "brown")
    окно.title("Chess")

    # l = окно.winfo_rootx()
    # t = окно.winfo_rooty()

    mw = окно.winfo_screenwidth()
    mh = окно.winfo_screenheight()
    w = h = размер_доски

    окно.geometry("{}x{}+{}+{}".format(w + 20, h + 20, (mw - w) // 2, (mh - h) // 2))
    окно.resizable(0, 0)

    холст = tkinter.Canvas(background = "lightyellow")
    холст.pack(fill = tkinter.BOTH, expand = True)


def draw_board():
    сторона_квадрата = размер_доски // 8

    номер_квадратика = 0
    for iy in range(8):
        номер_квадратика += 1

        for ix in range(8):
            номер_квадратика += 1
            if номер_квадратика % 2 == 1:
                цвет_клетки = "black"
            else:
                цвет_клетки = None

            холст.create_rectangle(ix*сторона_квадрата+5, iy*сторона_квадрата+5,
                                   (ix+1)*сторона_квадрата+5, (iy+1)*сторона_квадрата+5,
                                   fill = цвет_клетки, width = 1,
                                   tags = "rect{}{}".format(iy+1, ix+1))

    буквы = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for ix in range(8):
        холст.create_text(сторона_квадрата*(ix + 0.5), размер_доски + 10, text = буквы[ix])

    for iy in range(8):
        холст.create_text(размер_доски + 10, размер_доски - сторона_квадрата*(iy + 0.5), text = iy+1)


def highlight_cell(ix, iy, color):
    tag = "rect{}{}".format(iy, ix)

    try:
        холст.itemconfig(tag, fill = color)

        холст.update_idletasks()
        холст.update()
    except:
        pass


def draw_arrow(ix_from, iy_from, ix_to, iy_to, color):
    tag_from = "rect{}{}".format(iy_from, ix_from)
    tag_to = "rect{}{}".format(iy_to, ix_to)

    сторона_квадрата = размер_доски // 8

    try:
        rect_from = холст.coords(tag_from)
        rect_to = холст.coords(tag_to)

        from_x = rect_from[0] + сторона_квадрата // 2
        from_y = rect_from[1] + сторона_квадрата // 2
        to_x = rect_to[0] + сторона_квадрата // 2
        to_y = rect_to[1] + сторона_квадрата // 2

        print(from_x, from_y, to_x, to_y)
        холст.create_line(from_x, from_y, to_x, to_y, fill = color, arrow = tkinter.LAST)

        холст.update_idletasks()
        холст.update()
    except:
        pass


init_gui()
draw_board()


# tkinter.mainloop()

