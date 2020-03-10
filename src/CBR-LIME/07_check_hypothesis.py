import os
import random
import tkinter as tk
import tkinter.font as font
from tkinter import Tk
from tkinter import ttk
from tkinter import constants as cs
from tkinter import PhotoImage
from tkinter import messagebox
import sys

import utils.gui
import utils.system


class LimeExperiment():
    '''
    Application for choose the best Lime configuration between the default configuration and the process configuration.
    '''

    _img_list = list()
    _img_dict = dict()
    _index = 0

    def __init__(self, experimentPath: str, originalPath: str, similDict: str, res_folder: str, res_file: str):
        '''
        Constructor. Create a windows for choose the best Lime configuration for explain the image.

        Parameters:
            experimentPath, file with similarity matrix between images and neighborhood.
            originalPath,   folder with the master images.
            similDict,      similitude dictionary
            res_folder,     path of the result file
            res_file,       name of the result file
        '''

        # Parameters
        self._img_dict = utils.system.read_dict_csv(
            experimentPath, header=False)

        self._simil_data, _ = utils.system.load_simil_dict_file_data(
            similDict)

        for _, v in self._img_dict.items():
            for i in range(len(v), 0, -1):
                if i-1 != 3 and i-1 != 9:
                    v.pop(i-1)

        self._original_images = list(map(
            lambda x: utils.system._clean_filename(x), utils.system.ls(originalPath)))

        self._original_path = originalPath

        self._res_folder = res_folder
        self._res_file = res_file

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
        fr_bot_images = ttk.Frame(fr_body)

        fr_top_images.pack(side=cs.TOP, expand=True)

        fr_header_controls = ttk.Frame(fr_header)
        fr_header_images = ttk.Frame(fr_header)

        fr_header_controls.pack(side=cs.BOTTOM, expand=True)
        fr_header_images.pack(side=cs.BOTTOM, expand=True)

        # Header
        canvas00 = tk.Canvas(fr_header, width=224, height=224)
        lab_info = ttk.Label(
            fr_header, text='Choose the best explication for', font=tk.font.Font(size=12))
        fontStyle = tk.font.Font(size=20, weight="bold")
        lab_text = ttk.Label(fr_header, font=fontStyle)

        canvas00.pack(side=cs.BOTTOM, expand=True, padx=5, pady=5)
        lab_text.pack(side=cs.BOTTOM, padx=5, pady=5)
        lab_info.pack(side=cs.BOTTOM, padx=15, pady=5)

        canvas31 = tk.Canvas(fr_header_images, width=60, height=60)
        canvas32 = tk.Canvas(fr_header_images, width=60, height=60)
        canvas33 = tk.Canvas(fr_header_images, width=60, height=60)

        canvas31.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        canvas32.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        canvas33.pack(side=cs.LEFT, expand=True, padx=5, pady=5)

        # Body
        canvas11 = tk.Canvas(fr_top_images, width=224, height=224)
        lab11 = ttk.Label(fr_top_images)
        canvas12 = tk.Canvas(fr_top_images, width=224, height=224)
        lab12 = ttk.Label(fr_top_images)

        canvas11.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        lab11.pack(side=cs.LEFT, padx=5, pady=5)
        canvas12.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        lab12.pack(side=cs.LEFT, padx=5, pady=5)

        canvas21 = tk.Canvas(fr_bot_images, width=224, height=224)
        lab21 = ttk.Label(fr_bot_images)
        canvas22 = tk.Canvas(fr_bot_images, width=224, height=224)
        lab22 = ttk.Label(fr_bot_images)

        canvas21.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        lab21.pack(side=cs.LEFT, padx=5, pady=5)
        canvas22.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        lab22.pack(side=cs.LEFT, padx=5, pady=5)

        # Object list
        self._objects_list = [canvas00, lab_text,
                              [canvas11, canvas12,  canvas21, canvas22],
                              [lab11, lab12,  lab21, lab22],
                              [canvas31, canvas32, canvas33]]

    def _load_images(self):
        '''Load images in the application.'''

        self._img_list = list(self._original_images)
        random.shuffle(self._img_list)
        self._index = 0
        pass

    def _show_images(self):
        '''Show imagess in th window.'''

        if self._index == 0:
            # Check output
            self._check_output()
            # Load tha images
            self._load_images()

        # Load master image
        self.master_name = self._img_list[self._index]
        self.master_index = self.master_name.split('__')[0]
        utils.gui.load_path_image_canvas(
            path=os.path.join(self._original_path, self.master_name), canvas=self._objects_list[0])

        # Load experiment images
        self._loaded_images = self._img_dict[self.master_index]
        num_items = len(self._loaded_images)

        for item in range(num_items):
            utils.gui.load_path_image_canvas(
                path=self._loaded_images[item], canvas=self._objects_list[2][item], event=self._on_object_click)
        # Load related images
        self._load_simil_images()

        # Show text
        text = os.path.splitext(os.path.basename(self.master_name))[
            0].split('__')[1].replace('_', ' ')
        text = '{photoName}'.format(
            photoName=text)
        self._objects_list[1].config(text=text)

        if self._index == len(self._img_list)-1:
            messagebox.showinfo(
                "Information", "Congratulations, you reached the end of the dataset\n take a reward or even you can start again")

        self._index = (self._index+1) % len(self._img_list)

    def _load_simil_images(self):
        related = self._simil_data[self.master_name]

        for i, element in enumerate(related):
            utils.gui.load_path_image_canvas(
                path=os.path.join('topImg', element),
                canvas=self._objects_list[4][i],
                size=(60, 60))

    def _on_object_click(self, event):
        '''
        Event to manage the click event in a explication image.

        Parameters:
            event,  Event object.
        '''

        selected_index = self._objects_list[2].index(event.widget)
        selected_name = os.path.basename(self._loaded_images[selected_index])
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
        line.append(utils.system._clean_filename(self.master_name))
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

    experimentPath = r'output/experimentComparationResults.csv'
    originalPath: str = r'topImg'
    similDict: str = r'output/similDict.csv'
    res_folder = r'experiments2'
    res_file = r'result.csv'

    LimeExperiment(experimentPath, originalPath,
                   similDict, res_folder, res_file)
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
