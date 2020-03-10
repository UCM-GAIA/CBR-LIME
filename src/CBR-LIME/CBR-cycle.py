import os
from PIL import Image, ImageTk
from shutil import copyfile
import subprocess
import tkinter as tk
from tkinter import Tk
from tkinter import IntVar
from tkinter import DoubleVar
from tkinter import ttk
from tkinter import Scale
from tkinter import constants as cs
from tkinter import PhotoImage
from tkinter import filedialog
import uuid

import utils.images
import utils.brainy


class Aplicacion():

    def __init__(self,simil_dict:str):
        '''
        Constructor.
        '''
        # set the brainy model
        self.modelo = utils.brainy.getPredictionModel(utils.brainy.Model.MobileNet)

        # Window
        self.raiz = Tk()
        self.raiz.title("Colibri Lime")
        if 'nt'==os.name:
            self.raiz.iconbitmap(r'img/icon.ico')
        else:
            self.raiz.iconphoto(True, PhotoImage(file=os.path.join('img', "icon.png")))

        # Interface control variables
        self.__kernel_size = IntVar(value=4)
        self.__max_dist = IntVar(value=200)
        self.__ratio = DoubleVar(value=0.2)
        self.__num_perturb = IntVar(value=150)
        self.__kernel_width = DoubleVar(value=0.25)
        self.__num_top_features = IntVar(value=4)

        # Windows controls
        self.createControls()

        # Simil data
        self._simil_data, _ = self._load_simil_dict_file_data(simil_dict)

        # Show controls
        self.showControl()

        # start the main window loop
        self.raiz.mainloop()

    def showControl(self):
        """
        Show controls in UI.
        """
        # Frames
        self.fr_Images.pack(side=cs.LEFT, expand=True, anchor='w')
        self.fr_Labels.pack(side=cs.BOTTOM, expand=True, anchor="w", padx=15)
        self.fr_Menu.pack(side=cs.RIGHT, expand=True)

        # Input image
        self.fr_header_images.pack(side=cs.LEFT, padx=5, pady=5)
        self.lab_prediction.pack(side=cs.RIGHT, padx=5, pady=5)

        self.canvas3.pack(side=cs.RIGHT, expand=True, padx=20, pady=20)
        self.canvas2.pack(side=cs.RIGHT, expand=True, padx=20, pady=20)
        self.canvas.pack(side=cs.RIGHT, expand=True, padx=20, pady=20)

        # Options menu
        self.btnLoadImage.pack(side=cs.TOP, padx=5, pady=5)
        self.kernel_size.pack(side=cs.TOP, fill=cs.X,
                              expand=True, padx=5, pady=5)
        self.num_perturb.pack(side=cs.TOP, fill=cs.X,
                              expand=True, padx=5, pady=5)
        self.kernel_width.pack(side=cs.TOP, fill=cs.X,
                               expand=True, padx=5, pady=5)
        self.num_top_features.pack(
            side=cs.TOP, fill=cs.X, expand=True, padx=5, pady=5)

        # self.btnShowImages.pack(side=cs.BOTTOM, padx=20, pady=5)
        self.btnExportImages.pack(side=cs.BOTTOM, padx=20, pady=5)
        self.btnPrediction.pack(side=cs.BOTTOM, padx=20, pady=5)
        self.btnCalcular.pack(side=cs.BOTTOM, padx=20, pady=5)

    def createControls(self):
        """
        Create controls.
        """
        # Frames
        self.fr_Images = ttk.Frame(self.raiz)
        self.fr_Labels = ttk.Frame(self.fr_Images)
        self.fr_Menu = ttk.Frame(self.raiz)

        # Options menu
        self.kernel_size = Scale(self.fr_Menu, variable=self.__kernel_size, from_=1,
                                 to=10, orient=cs.HORIZONTAL, resolution=1, label="Cluster size (C):")
        self.num_perturb = Scale(self.fr_Menu, variable=self.__num_perturb, from_=50,
                                 to=450, orient=cs.HORIZONTAL, resolution=50, label="Perturbations (P):")
        self.kernel_width = Scale(self.fr_Menu, variable=self.__kernel_width, from_=0.25,
                                  to=1.0, orient=cs.HORIZONTAL, digits=3,  resolution=0.25, label="Proximity measure (Π):")
        self.num_top_features = Scale(self.fr_Menu, variable=self.__num_top_features,
                                      from_=1, to=50, orient=cs.HORIZONTAL, resolution=1, label="# top features:")

        self.lab_kernel_size = ttk.Label(self.fr_Menu, text="Kernel size:")
        self.lab_max_dist = ttk.Label(self.fr_Menu, text="Max distance:")
        self.lab_ratio = ttk.Label(self.fr_Menu, text="Ratio:")
        self.lab_num_per = ttk.Label(
            self.fr_Menu, text="Number of disturbances:")
        self.lab_ker_wid = ttk.Label(self.fr_Menu, text="Kernel width:")
        self.lab_num_top = ttk.Label(self.fr_Menu, text="Number top features:")

        self.lab_prediction = ttk.Label(
            self.fr_Labels, text="Predicted class:")

        # Buttons
        self.btnCalcular = ttk.Button(
            self.fr_Menu, text='Calculate perturbation', command=self.doPerturbation)
        self.btnPrediction = ttk.Button(
            self.fr_Menu, text='Explication', command=self.doPredictions)
        self.btnExportImages = ttk.Button(
            self.fr_Menu, text='Store as new case', command=self.doExportImages)

        self.btnLoadImage = ttk.Button(
            self.fr_Menu, text='Load image', command=self.eventLoadImage)

        self.btnShowImages = ttk.Button(
            self.fr_Menu, text='Show images', command=self.eventShowImages)

        # Canvas for images
        self.canvas = tk.Canvas(
            self.fr_Images, width=300, height=300, bg="blue")
        self.canvas2 = tk.Canvas(
            self.fr_Images, width=300, height=300, bg="yellow")
        self.canvas3 = tk.Canvas(
            self.fr_Images, width=300, height=300, bg="green")

        # Canvas for related
        self.fr_header_images = ttk.Frame(self.fr_Labels)
        canvas31 = tk.Canvas(self.fr_header_images,
                             width=60, height=60,  bg="blue")
        canvas32 = tk.Canvas(self.fr_header_images,
                             width=60, height=60, bg="blue")
        canvas33 = tk.Canvas(self.fr_header_images,
                             width=60, height=60, bg="blue")

        canvas31.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        canvas32.pack(side=cs.LEFT, expand=True, padx=5, pady=5)
        canvas33.pack(side=cs.LEFT, expand=True, padx=5, pady=5)

        # Object list
        self._objects_list = [canvas31, canvas32, canvas33]

    def doPerturbation(self):
        '''
        Function for perturbing the image.
        '''
        segmented, self.superpixels, self.num_superpixels = utils.images.segmentImage(
            self.Xi, self.__kernel_size.get(), self.__max_dist.get(), self.__ratio.get())

        extension = '.jpg'
        filename = 'segmentation'
        segmentedPath, self.numFiles = self.calculate_file_name(
            filename, extension)

        utils.images.saveImage(segmentedPath, segmented)

        self.loadImage(segmentedPath, self.canvas2)

        self.perturbations = utils.images.calculatePerturbations(
            self.__num_perturb.get(), self.num_superpixels)

    def _load_simil_dict_file_data(self, path: str):
        '''
        Load the similitude dictionary in the sistem.

        Parameters
            path,    path to the similitude dictionary file.

        Return
            dictionary with the similitude data
            list with the images names
        '''

        result = dict()
        with open(path, 'r') as the_file:

            for line in the_file:
                line = line.split(';')
                line.pop()
                index = os.path.basename(line.pop(0))

                localData = dict()
                for item in range(0, len(line), 2):
                    localData[os.path.basename(line[item])] = line[item+1]

                result[index] = localData

        return result, list(map(os.path.basename, result.keys()))

    def _load_simil_images(self):
        '''
        Load the simil images canvas.
        '''
        related = self._simil_data[os.path.basename(self.file_path)]

        for i, element in enumerate(related):
            # Data
            path = os.path.join('topImg', element)
            canvas = self._objects_list[i]
            size = (60, 60)
            # Open image
            img = Image.open(path)
            # Resize image to 224x224
            img = img.resize(size, Image.ANTIALIAS)
            # Convert to PhotoImage for load in the canvas
            img = ImageTk.PhotoImage(img)
            # Prevent garbage collector
            canvas.image = img
            # Show in canvas
            canvas.create_image(size[0]/2, size[1]/2, image=img)

    def doExportImages(self):
        '''
        Export the images.
        '''
        extension = '.jpg'
        filename = 'segmentation'
        for i in range(self.__num_perturb.get()):
            perturbedPath, _ = self.calculate_file_name(
                filename+str(self.numFiles), extension, 'Perturbations')

            utils.images.saveImage(perturbedPath, utils.images.perturb_image(
                self.Xi/2+0.5, self.perturbations[i], self.superpixels))

    def doPredictions(self):
        '''
        Obtain the image classification.
        '''
        mask = utils.brainy.doWork(self.modelo, self.perturbations, self.Xi, self.superpixels,
                             self.num_superpixels, self.__kernel_width.get(), self.__num_top_features.get())

        extension = '.jpg'
        filename = 'relevantPixels'
        relevantPath, _ = self.calculate_file_name(filename, extension)

        utils.images.saveImage(relevantPath, utils.images.perturb_image(
            self.Xi/2+0.5, mask, self.superpixels))

        self.loadImage(relevantPath, self.canvas3)

    def calculate_file_name(self, filename, extension, folder=None):
        '''
        Calculate filename for data.

        Calculate the filename, given the number of files that have the same name
        and concatenating a correlative number to avoid repeated names.

        Returns the os.path of the file and the number of repeated filenames.

        Parameters:
            filename,   Name desired name for the file
            extension,  File extension
            folder,     (Optional) Name added to the current directory path
        '''
        number_repeated_name = 0
        _exit = False
        _folder = os.path.join(os.getcwd(), 'output', self.identificator)

        filename = str(filename)
        extension = str(extension)
        if extension[0:1] != '.':
            extension = '.'+extension

        if not os.path.isdir(_folder):
            os.makedirs(_folder)

        if folder != None:
            _folder = os.path.join(_folder, folder)
            if not os.path.isdir(_folder):
                os.makedirs(_folder)

        while _exit == False:
            if number_repeated_name == 0:
                if os.path.isfile(os.path.join(_folder, str(filename) + str(extension))):
                    number_repeated_name += 1
                else:
                    path = os.path.join(_folder, str(filename)+str(extension))
                    _exit = True
            else:
                if os.path.isfile(os.path.join(_folder, str(filename)+'_'+str(number_repeated_name)+str(extension))):
                    number_repeated_name += 1
                else:
                    path = os.path.join(_folder, str(
                        filename)+'_' + str(number_repeated_name)+str(extension))
                    _exit = True
        return path, number_repeated_name

    def eventLoadImage(self):
        '''
        Handle the load image event.
        '''
        tk.Tk().withdraw()
        self.file_path = filedialog.askopenfilename(
            initialdir=os.path.join(os.getcwd(), 'topimg'), title="Select photo",
            filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        if self.file_path != '':
            self.identificator = str(uuid.uuid4())

            self.path = self.copyOriginal(self.file_path)

            self.loadImage(self.path, self.canvas)
            self.canvas2.delete("all")
            self.canvas3.delete("all")
            self.Xi = utils.images.loadImage(self.path)
            decode = utils.brainy.getDecodePrediction(self.modelo, self.Xi)

            texto = ""
            for linea in decode:
                texto += linea[1]+' '+str('%.6f' % (linea[2]*100))+'%'+'\n'

            self.lab_prediction.config(text=texto)
            self._load_simil_images()

    def loadImage(self, path, canvas):
        """
        Load image in canvas.

        Load image, resize and show image in the canvas
        """
        img = Image.open(path)
        # Resize image to 300x300
        img = img.resize((300, 300), Image.ANTIALIAS)
        # Convert to PhotoImage for load in the canvas
        img = ImageTk.PhotoImage(img)
        # Prevent garbage collector
        canvas.image = img
        # Show in canvas
        canvas.create_image(150, 150, image=img)

    def eventShowImages(self):
        '''
        Handle the show images event.
        '''
        folder = os.path.join(os.getcwd(), 'output')
        if not os.path.isdir(folder):
            os.makedirs(folder)
        subprocess.Popen('explorer "'+folder+'"')

    def getImagePrediction(self):
        '''
        Decode the image classification.
        '''
        predictions = utils.brainy.getDecodePrediction(self.modelo, self.Xi)
        return predictions

    def copyOriginal(self, original_path):
        '''
        Deep copy of image.
        '''
        destination_path, _ = self.calculate_file_name("original", "jpg")
        copyfile(original_path, destination_path)
        return destination_path


def main():
    simil_dict=r'output/similDict.csv'
    Aplicacion(simil_dict)
    return 0


if __name__ == '__main__':
    main()
