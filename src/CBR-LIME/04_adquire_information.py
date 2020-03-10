import os
import random
import sys
import tkinter as tk
from tkinter import constants as cs
import tkinter.font as font
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import Tk
from tkinter import ttk

import utils.gui
import utils.system


class LimeExperiment():
    '''
    Application for adquire the users explication preferences.

    Shows a windows with nine options, the user must choose based on her best
    human perception explication.
    '''

    _exp_folder = ''
    _img_folder = ''
    _res_folder = ''
    _res_file = ''
    _img_list = list()
    _img_dict = dict()
    _index = 0

    def __init__(self, explicationsImagesFolder: str, imagesFolder: str, resFolder: str, resFile: str):
        '''
        Constructor. Create a windows for choose the best Lime configuration for explain the image.

        Parameters:
            explicationsImagesFolder,   folder with the explications images.
            imagesFolder,               folder with the master images.
        '''

        # Parameters
        self._exp_folder = explicationsImagesFolder
        self._img_folder = imagesFolder
        self._res_folder = resFolder
        self._res_file = resFile

        # Window
        root = Tk()
        root.title('')
        if 'nt' == os.name:
            root.iconbitmap(r'img/icon.ico')
        else:
            root.iconphoto(True, PhotoImage(
                file=os.path.join('img', "icon.png")))

        # WindowsControls
        self._create_controls(root)

        # Show images in yhe window
        self._show_images()

        # Start the window
        root.mainloop()

    def _create_controls(self, root):
        '''Create the windows controls.'''

        # Frames
        fr_header = ttk.Frame(root)
        fr_body = ttk.Frame(root)

        fr_header.pack(side=cs.LEFT, expand=True)
        fr_body.pack(side=cs.RIGHT, expand=True)

        fr_top_images = ttk.Frame(fr_body)
        fr_mid_images = ttk.Frame(fr_body)
        fr_bot_images = ttk.Frame(fr_body)

        fr_top_images.pack(side=cs.TOP, expand=True)
        fr_mid_images.pack(side=cs.TOP, expand=True)
        fr_bot_images.pack(side=cs.BOTTOM, expand=True)

        # Header
        canvas00 = tk.Canvas(fr_header, width=224, height=224, bg="yellow")
        lab_info = ttk.Label(
            fr_header, text='Choose the best explication for', font=tk.font.Font(size=12))
        fontStyle = tk.font.Font(size=20, weight="bold")
        lab_text = ttk.Label(fr_header, font=fontStyle)

        canvas00.pack(side=cs.TOP, expand=True, padx=5, pady=5)
        lab_text.pack(side=cs.BOTTOM, padx=5, pady=5)
        lab_info.pack(side=cs.BOTTOM, padx=15, pady=5)

        # Body
        canvas11 = tk.Canvas(fr_top_images, width=224, height=224, bg="yellow")
        canvas12 = tk.Canvas(fr_top_images, width=224, height=224, bg="blue")
        canvas13 = tk.Canvas(fr_top_images, width=224, height=224, bg="green")

        canvas11.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        canvas12.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        canvas13.pack(side=cs.LEFT, expand=True, padx=5, pady=5)

        canvas21 = tk.Canvas(fr_mid_images, width=224, height=224, bg="yellow")
        canvas22 = tk.Canvas(fr_mid_images, width=224, height=224, bg="blue")
        canvas23 = tk.Canvas(fr_mid_images, width=224, height=224, bg="green")

        canvas21.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        canvas22.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        canvas23.pack(side=cs.LEFT, expand=True, padx=5, pady=5)

        canvas31 = tk.Canvas(fr_bot_images, width=224, height=224, bg="yellow")
        canvas32 = tk.Canvas(fr_bot_images, width=224, height=224, bg="blue")
        canvas33 = tk.Canvas(fr_bot_images, width=224, height=224, bg="green")

        canvas31.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        canvas32.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        canvas33.pack(side=cs.LEFT, expand=True, padx=5, pady=5)

        # Object list
        self.__objects_list = [canvas00, lab_text,
                               [canvas11, canvas12, canvas13, canvas21, canvas22, canvas23, canvas31, canvas32, canvas33]]

    def _load_images(self):
        '''Load images in the application.'''

        original_img = utils.system.ls(self._img_folder)
        explication_img = utils.system.ls(self._exp_folder)

        for data in original_img:
            related = [i for i in explication_img if os.path.basename(
                os.path.splitext(data)[0]) in i]
            random.shuffle(related)
            self._img_dict[data] = related

        self._img_list = list(self._img_dict.keys())
        random.shuffle(self._img_list)
        self._index = 0
        pass

    def _show_images(self):
        '''Show images in window.'''

        if self._index == 0:
            # Check output
            self._check_output()
            # Load tha images
            self._load_images()

        self.masterName = self._img_list[self._index]
        utils.gui.load_path_image_canvas(
            path=self.masterName, canvas=self.__objects_list[0])

        self.__loaded_images = self._img_dict[self.masterName]
        num_items = len(self.__loaded_images)

        for item in range(num_items):
            utils.gui.load_path_image_canvas(
                path=self.__loaded_images[item], canvas=self.__objects_list[2][item], event=self._on_object_click)

        text = os.path.splitext(os.path.basename(self.masterName))[
            0].split('__')[1]
        text = '{photoName}'.format(
            photoName=text)
        self.__objects_list[1].config(text=text)

        if self._index == len(self._img_list)-1:
            messagebox.showinfo(
                "Information", "Congratulations, you reached the end of the dataset\neven so you can start again")

        self._index = (self._index+1) % len(self._img_list)

    def _on_object_click(self, event):
        '''
        Event to manage the click event in a explication image.

        Parameters:
            event,  Event object.
        '''

        selected_index = self.__objects_list[2].index(event.widget)
        selected_name = os.path.basename(self.__loaded_images[selected_index])
        self._write_result(selected_name)
        self._show_images()

    def _write_result(self, text):
        '''
        Persist text in output file.

        Parameters:
            text,   Text to persist
        '''

        line = os.path.splitext(text)[0].split('__')
        line.append(os.path.splitext(text)[0])
        line.append(text)
        line.append(utils.system._clean_filename(self.masterName))
        line.append('\n')
        text = ';'.join(line)

        with open(os.path.join(self._res_folder, self._res_file), 'a') as the_file:
            the_file.write(text)

    def _check_output(self):
        '''
        Create the output directory and the experiment results file
        '''
        utils.system.create_folder(self._res_folder)
        list_items = utils.system.ls(self._res_folder)

        list_items = list(
            filter(lambda x: x.find(self._res_file), list_items))

        if len(list_items) > 0:
            self._res_file = self._res_file.split(
                '_')[0]+'.'+self._res_file.split('.')[1]
            self._res_file = self._res_file.split(
                '.')[0]+'_'+str(len(list_items))+'.'+self._res_file.split('.')[1]

        if not os.path.isfile(os.path.join(self._res_folder, self._res_file)):
            with open(os.path.join(self._res_folder, self._res_file), 'w') as the_file:
                the_file.write(
                    'Id;Prediction;Acuracity;KernelSize;Disturbances;KernelWidth;Features;FullName;FileName;Original;\n')


def main(argv):
    """
    Main function.
    """

    efolder = 'explications/'
    ifolder = 'topImg/'
    rfolder = 'experiments/'
    rfile = 'result.csv'

    LimeExperiment(efolder, ifolder, rfolder, rfile)
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
