import os
import tkinter as tk
from tkinter import Tk
from tkinter import ttk
import tkinter.constants as cs
from tkinter import PhotoImage
from PIL import Image

import utils.system
import utils.gui
import utils.images
import utils.brainy


class SimilImages():

    _images_list = None
    _simil_data = None
    _index = 0
    _path = ''

    def __init__(self, similPath, imagesPath):

        # Window
        root = Tk()
        root.title('')
        if 'nt'==os.name:
            root.iconbitmap(r'img/icon.ico')
        else:
            root.iconphoto(True, PhotoImage(file=os.path.join('img', "icon.png")))

        # WindowsControls
        self._create_window(root)

        # Data
        self._simil_data, self._images_list = utils.system.load_simil_dict_file_data(
            similPath)
        self._path = imagesPath
        self._load_image()

        # Start the window
        root.mainloop()

    def _create_window(self, root):
        # Frames
        fr_header = ttk.Frame(root)
        fr_img = ttk.Frame(fr_header)
        fr_buttons = ttk.Frame(fr_header)
        fr_body = ttk.Frame(root)

        fr_left = ttk.Frame(fr_body)
        fr_center = ttk.Frame(fr_body)
        fr_rigth = ttk.Frame(fr_body)

        fr_header.pack(side=cs.LEFT, expand=True)
        fr_img.pack(side=cs.TOP, expand=True)
        fr_buttons.pack(side=cs.BOTTOM, expand=True)
        fr_body.pack(side=cs.RIGHT, expand=True)

        fr_left.pack(side=cs.LEFT, expand=True)
        fr_center.pack(side=cs.LEFT, expand=True)
        fr_rigth.pack(side=cs.LEFT, expand=True)

        # Header
        canvas00 = tk.Canvas(fr_img, width=224, height=224, bg="blue")

        btnNext = ttk.Button(fr_buttons, text='Next', command=self._next_pic)
        btnPrev = ttk.Button(fr_buttons, text='Prev', command=self._prev_pic)

        canvas00.pack(side=cs.TOP, expand=True, padx=5, pady=5)
        btnNext.pack(side=cs.RIGHT, padx=5, pady=5)
        btnPrev.pack(side=cs.LEFT, padx=5, pady=5)

        # Body
        canvas11 = tk.Canvas(fr_left, width=224, height=224, bg="yellow")
        lab11 = ttk.Label(fr_left)
        lab21 = ttk.Label(fr_left)
        canvas12 = tk.Canvas(fr_center, width=224, height=224, bg="yellow")
        lab12 = ttk.Label(fr_center)
        lab22 = ttk.Label(fr_center)
        canvas13 = tk.Canvas(fr_rigth, width=224, height=224, bg="yellow")
        lab13 = ttk.Label(fr_rigth)
        lab23 = ttk.Label(fr_rigth)

        canvas11.pack(side=cs.TOP, expand=True, padx=5, pady=5)
        lab21.pack(side=cs.BOTTOM, expand=True, padx=5, pady=5)
        lab11.pack(side=cs.BOTTOM, expand=True, padx=5, pady=5)
        canvas12.pack(side=cs.TOP, expand=True, padx=5, pady=5)
        lab22.pack(side=cs.BOTTOM, expand=True, padx=5, pady=5)
        lab12.pack(side=cs.BOTTOM, expand=True, padx=5, pady=5)
        canvas13.pack(side=cs.TOP, expand=True, padx=5, pady=5)
        lab23.pack(side=cs.BOTTOM, expand=True, padx=5, pady=5)
        lab13.pack(side=cs.BOTTOM, expand=True, padx=5, pady=5)

        # Object list
        self.__objects_list = [canvas00, btnPrev, btnNext,
                               [canvas11, canvas12, canvas13],
                               [lab11, lab12, lab13],
                               [lab21, lab22, lab23]]

    def _next_pic(self):
        self._index += 1
        self._load_image()

    def _prev_pic(self):
        self._index -= 1
        self._load_image()

    def _load_image(self):
        self._index = self._index % len(self._images_list)

        utils.gui.load_path_image_canvas(
            os.path.join(self._path, self._images_list[self._index]), self.__objects_list[0])

        data = list(self._simil_data[self._images_list[self._index]].items())

        modelo = utils.brainy.getPredictionModel(utils.brainy.Model.MobileNet)

        for i in range(len(data)):
            path = os.path.join(self._path, data[i][0])
            utils.gui.load_path_image_canvas(path, self.__objects_list[3][i])

            self.__objects_list[4][i].config(
                text='Similitude: %.4f' % float(data[i][1]))

            clasiff = ''
            Xi = utils.images.loadImage(path)
            clasiff = utils.brainy.getDecodePrediction(modelo, Xi)
            text = ''
            for line in clasiff:
                text += line[1] + ' ' + str(line[2]) + '%' + '\n'
                # text += line[1] + ' ' + str('%.4f' % line[2]) + '%' + '\n'

            self.__objects_list[5][i].config(text=text)


def main():
    similPath = r'output/similDict.csv'
    imagesPath = r'topImg/'
    SimilImages(similPath, imagesPath)


if __name__ == "__main__":
    main()
