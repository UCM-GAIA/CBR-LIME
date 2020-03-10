from PIL import Image, ImageTk
import numpy as np


def load_array_image_canvas(image, canvas, size=(224, 224), event=None):
    """
    Load image in canvas.

    Load image array in the canvas and resize.

    Parameters
        image,  image in array
        canvas, tkinter canvas to show the image
        size,   size dimensions
        event,  event to asing in the mouse button 1 click
    """

    image = Image.fromarray((image).astype(np.uint8))
    image = image.resize(size, Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    obj = canvas.create_image(size[0]/2, size[1]/2,  image=image)

    if event != None:
        # Click event
        canvas.tag_bind(obj, '<ButtonPress-1>', event)


def load_path_image_canvas(path, canvas, size=(224, 224), event=None):
    """
    Load image in canvas.

    Load image, resize and show image in the canvas.

    Parameters
        path,   path to the image file
        canvas, tkinter canvas to show the image
        size,   resize dimensions
        event,  event to asing in the mouse button 1 click
    """

    # Open image
    img = Image.open(path)
    # Resize image to 224x224
    img = img.resize(size, Image.ANTIALIAS)
    # Convert to PhotoImage for load in the canvas
    img = ImageTk.PhotoImage(img)
    # Prevent garbage collector
    canvas.image = img
    # Show in canvas
    obj = canvas.create_image(size[0]/2, size[1]/2, image=img)

    if event != None:
        # Click event
        canvas.tag_bind(obj, '<ButtonPress-1>', event)


def clean_image_canvas(canvas_list: list):
    '''
    Clean the images in the canvas list.

    For each canvas recived in the parameter erase the image loaded.

    Parameters
        canvas_list,    list of canvas
    '''
    for item in canvas_list:
        item.delete('all')
