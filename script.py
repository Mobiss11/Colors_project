import sys
from pathlib import Path
from tkinter import *
import tkinter as tk
import re
import os

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import gspread
from PIL import Image

from config import *

credentials = gspread.service_account(filename=FILE_NAME)
sheet = credentials.open_by_url(PATH_TABLE)
connectors_sheet = sheet.worksheet(WORKSHEET)

directory = 'logo/'

files = Path(directory).glob('*')
files_1 = []

gr = []
gr_two = []
gr_third = []
gr_fourth = []


class Gui(object):

    def __init__(self):
        self.build_gui()

    def build_gui(self):

        for file in files:
            files_1.append(str(file))

            im = Image.open(file)
            obj = im.load()
            height = im.size[1]

            plt.imshow(mpimg.imread(file))
            plt.ion()
            plt.show()

            colors = []
            for i in range(1, height):
                color = str(obj[i, i])
                colors.append(color)

            colors2 = []

            for l in colors:
                if l not in colors2:
                    colors2.append(l)

            colors = colors2

            root = Tk()
            global root2
            root2 = Tk()

            w = 900  # width for the Tk root
            h = 950  # height for the Tk root

            # get screen width and height
            ws = root.winfo_screenwidth()  # width of the screen
            hs = root.winfo_screenheight()  # height of the screen

            # calculate x and y coordinates for the Tk root window
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)

            root.geometry('%dx%d+%d+%d' % (w, h, x, y))

            def exit():

                sys.exit()

            def google_table():
                print(gr)
                print(gr_two)
                print(gr_third)
                print(gr_fourth)

                logos_col = connectors_sheet.col_values(8)
                name = str(files_1[0])
                name1 = name[5:]


                if name1 in logos_col:

                    index = logos_col.index(name1)
                    row = index + 1

                    connectors_sheet.update(f'I{row}', gr[0])
                    connectors_sheet.update(f'J{row}', gr[1])
                    connectors_sheet.update(f'K{row}', gr_two[0])
                    connectors_sheet.update(f'L{row}', gr_third[0])
                    connectors_sheet.update(f'M{row}', gr_fourth[0])

                    files_1.pop(0)
                    os.remove(file)

                    print(row)

                gr.clear()
                root.destroy()
                root2.destroy()
                plt.close()

            tk.Button(root, text="Отправить в таблицу", command=google_table).grid(row=1, column=6, padx=3)
            tk.Button(root, text="Остановить", command=exit).grid(row=3, column=6, padx=3)

            tk.Label(root, text=f"Логотип:\n{file}").grid(row=2,column=6, padx=3)

            for color_gr in colors:

                index = colors.index(color_gr)
                re_digits = re.compile(r"\b\d+\b")
                ls = re_digits.findall(colors[index])

                hex_color = '#%02x%02x%02x' % (int(ls[0]), int(ls[1]), int(ls[2]))

                color_gr = hex_color

                button = Button(root, text=f'цвет - {hex_color}', fg='black', bg=hex_color, command=lambda color_gr=color_gr: self.table_gradient(color_gr))

                button.grid(row=index, column=1)

            for color_3 in colors:

                index = colors.index(color_3)

                re_digits = re.compile(r"\b\d+\b")
                ls = re_digits.findall(colors[index])

                hex_color = '#%02x%02x%02x' % (int(ls[0]), int(ls[1]), int(ls[2]))

                color_3 = hex_color

                button = Button(root, text=f'цвет - {hex_color}', fg='black', bg=hex_color, command=lambda color_3=color_3: self.table_two(color_3))

                button.grid(row=index,column=2)

            for color_4 in colors:

                index = colors.index(color_4)

                re_digits = re.compile(r"\b\d+\b")
                ls = re_digits.findall(colors[index])

                hex_color = '#%02x%02x%02x' % (int(ls[0]), int(ls[1]), int(ls[2]))

                color_4 = hex_color

                button = Button(root, text=f'цвет - {hex_color}', fg='black', bg=hex_color, command=lambda color_4=color_4: self.table_third(color_4))

                button.grid(row=index, column=4)

            for color_5 in colors:

                index = colors.index(color_5)

                re_digits = re.compile(r"\b\d+\b")
                ls = re_digits.findall(colors[index])

                hex_color = '#%02x%02x%02x' % (int(ls[0]), int(ls[1]), int(ls[2]))

                color_5 = hex_color

                button = Button(root, text=f'цвет - {hex_color}', fg='black', bg=hex_color, command=lambda color_5=color_5: self.table_fourth(color_5))

                button.grid(row=index, column=5)

            root.mainloop()

    def table_gradient(self, color_gr):

        gr.append(color_gr)

        if len(gr) > 2:
            gr.clear()

        if len(gr) == 2:
            class GradientFrame(tk.Canvas):
                '''A gradient frame which uses a canvas to draw the background'''

                def __init__(self, parent, color3=gr[0], color4=gr[1], **kwargs):
                    tk.Canvas.__init__(self, parent, **kwargs)
                    self._color3 = color3
                    self._color4 = color4
                    self.bind("<Configure>", self._draw_gradient)

                def _draw_gradient(self, event=None):
                    '''Draw the gradient'''
                    self.delete("gradient")
                    width = self.winfo_width()
                    height = self.winfo_height()
                    limit = 800
                    (r1, g1, b1) = self.winfo_rgb(self._color3)
                    (r2, g2, b2) = self.winfo_rgb(self._color4)
                    r_ratio = float(r2 - r1) / limit
                    g_ratio = float(g2 - g1) / limit
                    b_ratio = float(b2 - b1) / limit

                    for i in range(limit):
                        nr = int(r1 + (r_ratio * i))
                        ng = int(g1 + (g_ratio * i))
                        nb = int(b1 + (b_ratio * i))
                        color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
                        self.create_line(i, 0, i, 300, tags=("gradient",), fill=color)
                    self.lower("gradient")

            tk.Label(root2, text=f"Для сайта Цвет 1: {gr[0]}, Цвет 2: {gr[1]}").grid(row=1, column=1, padx=3)
            GradientFrame(root2).grid(row=2, column=1)

        root2.mainloop()

    def table_two(self, color_3):

        try:
            gr_two.clear()
            gr_two.append(color_3)
        except:
            gr_two.append(color_3)

        class GradientFrame2(tk.Canvas):

            def __init__(self, parent, color1=color_3, color2=color_3, **kwargs):
                tk.Canvas.__init__(self, parent, **kwargs)
                self._color1 = color1
                self._color2 = color2
                self.bind("<Configure>", self._draw_gradient)

            def _draw_gradient(self, event=None):

                self.delete("gradient")
                width = self.winfo_width()
                height = self.winfo_height()
                limit = width
                (r1, g1, b1) = self.winfo_rgb(self._color1)
                (r2, g2, b2) = self.winfo_rgb(self._color2)
                r_ratio = float(r2 - r1) / limit
                g_ratio = float(g2 - g1) / limit
                b_ratio = float(b2 - b1) / limit

                for i in range(limit):
                    nr = int(r1 + (r_ratio * i))
                    ng = int(g1 + (g_ratio * i))
                    nb = int(b1 + (b_ratio * i))
                    color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
                    self.create_line(i, 0, i, 80, tags=("gradient",), fill=color)
                self.lower("gradient")

        tk.Label(root2, text=f"Ainsys Цвет 1 : {gr_two}").grid(row=1, column=2, padx=3)
        GradientFrame2(root2).grid(row=2, column=2)

        root2.mainloop()

    def table_third(self, color_4):

        try:
            gr_third.clear()
            gr_third.append(color_4)
        except:
            gr_third.append(color_4)

        class GradientFrame3(tk.Canvas):

            def __init__(self, parent, color1=color_4, color2=color_4, **kwargs):
                tk.Canvas.__init__(self, parent, **kwargs)
                self._color1 = color1
                self._color2 = color2
                self.bind("<Configure>", self._draw_gradient)

            def _draw_gradient(self, event=None):

                self.delete("gradient")
                width = self.winfo_width()
                height = self.winfo_height()
                limit = width
                (r1, g1, b1) = self.winfo_rgb(self._color1)
                (r2, g2, b2) = self.winfo_rgb(self._color2)
                r_ratio = float(r2 - r1) / limit
                g_ratio = float(g2 - g1) / limit
                b_ratio = float(b2 - b1) / limit

                for i in range(limit):
                    nr = int(r1 + (r_ratio * i))
                    ng = int(g1 + (g_ratio * i))
                    nb = int(b1 + (b_ratio * i))
                    color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
                    self.create_line(i, 0, i, 80, tags=("gradient",), fill=color)
                self.lower("gradient")

        tk.Label(root2, text=f"Ainsys Цвет 2 : {gr_third}").grid(row=1, column=3, padx=3)
        GradientFrame3(root2).grid(row=2, column=3)

        root2.mainloop()

    def table_fourth(self, color_5):

        try:
            gr_fourth.clear()
            gr_fourth.append(color_5)
        except:
            gr_third.append(color_5)

        class GradientFrame4(tk.Canvas):

            def __init__(self, parent, color1=color_5, color2=color_5, **kwargs):
                tk.Canvas.__init__(self, parent, **kwargs)
                self._color1 = color1
                self._color2 = color2
                self.bind("<Configure>", self._draw_gradient)

            def _draw_gradient(self, event=None):

                self.delete("gradient")
                width = self.winfo_width()
                #height = self.winfo_height()
                limit = width
                (r1, g1, b1) = self.winfo_rgb(self._color1)
                (r2, g2, b2) = self.winfo_rgb(self._color2)
                r_ratio = float(r2 - r1) / limit
                g_ratio = float(g2 - g1) / limit
                b_ratio = float(b2 - b1) / limit

                for i in range(limit):
                    nr = int(r1 + (r_ratio * i))
                    ng = int(g1 + (g_ratio * i))
                    nb = int(b1 + (b_ratio * i))
                    color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
                    self.create_line(i, 0, i, 80, tags=("gradient",), fill=color)
                self.lower("gradient")

        tk.Label(root2, text=f"Ainsys Цвет 3 : {gr_fourth}").grid(row=3, column=2, padx=3)
        GradientFrame4(root2).grid(row=4, column=2)

        root2.mainloop()

        root2.mainloop()


app = Gui()
