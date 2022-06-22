import sys
from pathlib import Path
from tkinter import *
import tkinter as tk
from tkinter import colorchooser
import re
import os

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import gspread
from PIL import Image

from config import *
from consts import *

credentials = gspread.service_account(filename=FILE_NAME)
sheet = credentials.open_by_url(PATH_TABLE)
connectors_sheet = sheet.worksheet(WORKSHEET)

directory = DIR

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

            width = 900
            height = 950

            width_screen = root.winfo_screenwidth()
            height_screen = root.winfo_screenheight()

            cor_x = (width_screen / 2) - (width / 2)
            cor_y = (height_screen / 2) - (height / 2)

            root.geometry(ROOT_CONSTANT % (width, height, cor_x, cor_y))

            def reset_gradient():
                gr.clear()

            def next_logo():

                gr.clear()
                root.destroy()
                root2.destroy()
                plt.close()

            def exit_window():
                sys.exit()

            def google_table():

                logos_col = connectors_sheet.col_values(8)
                name_logo_file = str(file)
                name_logo_file_table = name_logo_file[5:]

                if name_logo_file_table in logos_col:

                    index_logo = logos_col.index(name_logo_file_table)
                    row = index_logo + 1

                    connectors_sheet.update(f'I{row}', gr[0])
                    connectors_sheet.update(f'J{row}', gr[1])
                    connectors_sheet.update(f'K{row}', gr_two[0])
                    connectors_sheet.update(f'L{row}', gr_third[0])
                    connectors_sheet.update(f'M{row}', gr_fourth[0])

                    files_1.pop(0)
                    os.remove(file)

                gr.clear()
                root.destroy()
                root2.destroy()
                plt.close()

            tk.Button(root,
                      text=BUTTON_SEND,
                      command=google_table).grid(row=1,
                                                 column=6,
                                                 padx=3)
            tk.Button(root,
                      text=BUTTON_CLOSE,
                      command=exit_window).grid(row=1,
                                                column=8,
                                                padx=3)

            tk.Button(root,
                      text=BUTTON_MISS,
                      command=next_logo).grid(row=1,
                                              column=7,
                                              padx=3)
            tk.Button(root,
                      text=BUTTON_RESET,
                      command=reset_gradient).grid(row=2,
                                                   column=7,
                                                   padx=3)

            tk.Label(root,
                     text=f"{LABEL_LOGO}\n{file}").grid(row=2,
                                                        column=6,
                                                        padx=3)

            for color_gr in colors:

                index = colors.index(color_gr)
                re_digits = re.compile(r"\b\d+\b")
                ls = re_digits.findall(colors[index])

                hex_color = HEX_CONSTANT % (int(ls[0]), int(ls[1]), int(ls[2]))

                color_gr = hex_color

                tk.Button(root,
                          text=f'{hex_color}',
                          fg=FONT_COLOR, bg=hex_color,
                          command=lambda color_gr=color_gr: self.table_gradient(color_gr)).grid(row=index,
                                                                                                column=1)

            for color_3 in colors:

                index = colors.index(color_3)

                re_digits = re.compile(r"\b\d+\b")
                ls = re_digits.findall(colors[index])

                hex_color = HEX_CONSTANT % (int(ls[0]), int(ls[1]), int(ls[2]))

                color_3 = hex_color

                tk.Button(root,
                          text=f'{hex_color}',
                          fg=FONT_COLOR,
                          bg=hex_color,
                          command=lambda color_3=color_3: self.table_two(color_3)).grid(row=index,
                                                                                        column=2)

            for color_4 in colors:

                index = colors.index(color_4)

                re_digits = re.compile(r"\b\d+\b")
                ls = re_digits.findall(colors[index])

                hex_color = HEX_CONSTANT % (int(ls[0]), int(ls[1]), int(ls[2]))

                color_4 = hex_color

                tk.Button(root,
                          text=f'{hex_color}',
                          fg=FONT_COLOR, bg=hex_color,
                          command=lambda color_4=color_4: self.table_third(color_4)).grid(row=index,
                                                                                          column=4)

            for color_5 in colors:

                index = colors.index(color_5)

                re_digits = re.compile(r"\b\d+\b")
                ls = re_digits.findall(colors[index])

                hex_color = HEX_CONSTANT % (int(ls[0]), int(ls[1]), int(ls[2]))

                color_5 = hex_color

                tk.Button(root,
                          text=f'{hex_color}',
                          fg=FONT_COLOR, bg=hex_color,
                          command=lambda color_5=color_5: self.table_fourth(color_5)).grid(row=index,
                                                                                           column=5)

            root.mainloop()

    def table_gradient(self, color_gr):

        def pick_color():

            color = colorchooser.askcolor(color_gr,
                                          title=BUTTON_COLOR)

            gr.append(color[1])

            if len(gr) == 2:

                class GradientFrame(tk.Canvas):

                    def __init__(self, parent, color3=gr[0], color4=gr[1], **kwargs):
                        tk.Canvas.__init__(self, parent, **kwargs)
                        self._color3 = color3
                        self._color4 = color4
                        self.bind(CONFIG, self._draw_gradient)

                    def _draw_gradient(self, event=None):

                        self.delete(TAG_COLOR_TABLE)
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
                            color = COLOR_TABLE_CONSTANT % (nr, ng, nb)
                            self.create_line(i, 0, i, 300, tags=(TAG_COLOR_TABLE,),fill=color)
                        self.lower(TAG_COLOR_TABLE)

                tk.Label(root2,
                         text=f"{AINSYS_GR_1} {gr[0]}, {AINSYS_GR_2} {gr[1]}").grid(row=1,
                                                                                    column=1,
                                                                                    padx=3)
                GradientFrame(root2).grid(row=3,
                                          column=1)

        tk.Button(root2,
                  text=BUTTON_COLOR,
                  command=pick_color,
                  bg=BG_COLOR,
                  fg=FONT_COLOR_W2).grid(row=2,
                                         column=1)

        gr.append(color_gr)

        if len(gr) == 2:
            class GradientFrame(tk.Canvas):

                def __init__(self, parent, color3=gr[0], color4=gr[1], **kwargs):

                    tk.Canvas.__init__(self, parent, **kwargs)
                    self._color3 = color3
                    self._color4 = color4
                    self.bind(CONFIG, self._draw_gradient)

                def _draw_gradient(self, event=None):

                    self.delete(TAG_COLOR_TABLE)
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
                        color = COLOR_TABLE_CONSTANT % (nr, ng, nb)
                        self.create_line(i, 0, i, 300, tags=(TAG_COLOR_TABLE,), fill=color)
                    self.lower(TAG_COLOR_TABLE)

            tk.Label(root2,
                     text=f"{AINSYS_GR_1} {gr[0]}, {AINSYS_GR_2} {gr[1]}").grid(row=1,
                                                                                column=1,
                                                                                padx=3)
            GradientFrame(root2).grid(row=3,
                                      column=1)

        root2.mainloop()

    def table_two(self, color_3):

        def pick_color():

            color = colorchooser.askcolor(color_3,
                                          title=BUTTON_COLOR)

            try:
                gr_two.clear()
                gr_two.append(color[1])

            except:
                gr_two.append(color[1])

            class GradientFrame2(tk.Canvas):

                def __init__(self, parent, color1=gr_two[0], color2=gr_two[0], **kwargs):
                    tk.Canvas.__init__(self, parent, **kwargs)
                    self._color1 = color1
                    self._color2 = color2
                    self.bind(CONFIG, self._draw_gradient)

                def _draw_gradient(self, event=None):
                    self.delete(TAG_COLOR_TABLE)
                    width = self.winfo_width()
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
                        color = COLOR_TABLE_CONSTANT % (nr, ng, nb)
                        self.create_line(i, 0, i, 80, tags=(TAG_COLOR_TABLE,), fill=color)
                    self.lower(TAG_COLOR_TABLE)

            tk.Label(root2,
                     text=f"{AINSYS_TABLE1}{gr_two[0]}").grid(row=1,
                                                              column=2)
            GradientFrame2(root2).grid(row=3,
                                       column=2)

        tk.Button(root2,
                  text=BUTTON_COLOR,
                  command=pick_color,
                  bg=BG_COLOR,
                  fg=FONT_COLOR_W2).grid(row=2,
                                         column=2)

        try:
            gr_two.clear()
            gr_two.append(color_3)

        except:
            gr_two.append(color_3)

        class GradientFrame2(tk.Canvas):

            def __init__(self, parent, color1=gr_two[0], color2=gr_two[0], **kwargs):
                tk.Canvas.__init__(self, parent, **kwargs)
                self._color1 = color1
                self._color2 = color2
                self.bind(CONFIG, self._draw_gradient)

            def _draw_gradient(self, event=None):

                self.delete(TAG_COLOR_TABLE)
                width = self.winfo_width()
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
                    color = COLOR_TABLE_CONSTANT % (nr, ng, nb)
                    self.create_line(i, 0, i, 80, tags=(TAG_COLOR_TABLE,), fill=color)
                self.lower(TAG_COLOR_TABLE)

        tk.Label(root2,
                 text=f"{AINSYS_TABLE1}{gr_two[0]}").grid(row=1,
                                                          column=2)
        GradientFrame2(root2).grid(row=3,
                                   column=2)

        root2.mainloop()

    def table_third(self, color_4):

        def pick_color():

            color = colorchooser.askcolor(color_4,
                                          title=BUTTON_COLOR)

            try:
                gr_third.clear()
                gr_third.append(color[1])

            except:
                gr_third.append(color[1])

            class GradientFrame2(tk.Canvas):

                def __init__(self, parent, color1=gr_third[0], color2=gr_third[0], **kwargs):
                    tk.Canvas.__init__(self, parent, **kwargs)
                    self._color1 = color1
                    self._color2 = color2
                    self.bind(CONFIG, self._draw_gradient)

                def _draw_gradient(self, event=None):
                    self.delete(TAG_COLOR_TABLE)
                    width = self.winfo_width()
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
                        color = COLOR_TABLE_CONSTANT % (nr, ng, nb)
                        self.create_line(i, 0, i, 80, tags=(TAG_COLOR_TABLE,), fill=color)
                    self.lower(TAG_COLOR_TABLE)

            tk.Label(root2,
                     text=f"{AINSYS_TABLE2}{gr_third[0]}").grid(row=1,
                                                                column=3)
            GradientFrame2(root2).grid(row=3,
                                       column=3)

        tk.Button(root2,
                  text=BUTTON_COLOR,
                  command=pick_color,
                  bg=BG_COLOR,
                  fg=FONT_COLOR_W2).grid(row=2,
                                         column=3)

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
                self.bind(CONFIG, self._draw_gradient)

            def _draw_gradient(self, event=None):

                self.delete(TAG_COLOR_TABLE)
                width = self.winfo_width()
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
                    color = COLOR_TABLE_CONSTANT % (nr, ng, nb)
                    self.create_line(i, 0, i, 80, tags=(TAG_COLOR_TABLE,), fill=color)
                self.lower(TAG_COLOR_TABLE)

        tk.Label(root2,
                 text=f"{AINSYS_TABLE2}{gr_third[0]}").grid(row=1,
                                                            column=3,
                                                            padx=3)
        GradientFrame3(root2).grid(row=3,
                                   column=3)

        root2.mainloop()

    def table_fourth(self, color_5):

        def pick_color():

            color = colorchooser.askcolor(color_5,
                                          title=BUTTON_COLOR)

            try:
                gr_fourth.clear()
                gr_fourth.append(color[1])

            except:
                gr_fourth.append(color[1])

            class GradientFrame2(tk.Canvas):

                def __init__(self, parent, color1=gr_fourth[0], color2=gr_fourth[0], **kwargs):
                    tk.Canvas.__init__(self, parent, **kwargs)
                    self._color1 = color1
                    self._color2 = color2
                    self.bind(CONFIG, self._draw_gradient)

                def _draw_gradient(self, event=None):
                    self.delete(TAG_COLOR_TABLE)
                    width = self.winfo_width()
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
                        color = COLOR_TABLE_CONSTANT % (nr, ng, nb)
                        self.create_line(i, 0, i, 80, tags=(TAG_COLOR_TABLE,), fill=color)
                    self.lower(TAG_COLOR_TABLE)

            tk.Label(root2,
                     text=f"{AINSYS_TABLE3}{gr_fourth[0]}").grid(row=1,
                                                                 column=4)
            GradientFrame2(root2).grid(row=3,
                                       column=4)

        tk.Button(root2,
                  text=BUTTON_COLOR,
                  command=pick_color,
                  bg=BG_COLOR,
                  fg=FONT_COLOR_W2).grid(row=2,
                                         column=4)

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
                self.bind(CONFIG, self._draw_gradient)

            def _draw_gradient(self, event=None):

                self.delete(TAG_COLOR_TABLE)
                width = self.winfo_width()
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
                    color = COLOR_TABLE_CONSTANT % (nr, ng, nb)
                    self.create_line(i, 0, i, 80, tags=(TAG_COLOR_TABLE,), fill=color)
                self.lower(TAG_COLOR_TABLE)

        tk.Label(root2,
                 text=f"{AINSYS_TABLE3}{gr_fourth[0]}").grid(row=1,
                                                             column=4,
                                                             padx=3)
        GradientFrame4(root2).grid(row=3,
                                   column=4)

        root2.mainloop()


app = Gui()
