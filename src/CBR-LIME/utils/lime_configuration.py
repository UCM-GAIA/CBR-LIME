import os
from random import randint


class lime_configuration():
    '''
    Class to structure the Lime configuration parameters.
    '''

    __kernel_size = 0
    __disturbances = 0
    __kernel_width = 0
    __top_features = 0
    __file_name = 0

    def __init__(self, fname: str, ksize: int = 0, disturb: int = 0, kwidth: float = 0.0):
        '''Constructor.

        Generate the LimeConfiguration class with the parameters value
            ksize,      kernel size value
            disturb,    number of disturbances value
            kwidth,     kernel width value

        Also calculates the top features value using the formula:
            top features = (11 - ksize) * 5
        '''
        self.__file_name = fname
        self.__kernel_size = ksize
        self.__disturbances = disturb
        self.__kernel_width = kwidth
        self.__top_features = (11-self.__kernel_size)*2
        # self.__top_features = (11-self.__kernel_size)*5

    def get_file_path(self):
        '''Return the file name path.'''
        return str(self.__file_name)

    def get_file_name(self):
        '''Return the file name with extension'''
        return str(os.path.basename(self.__file_name))

    def get_kernel_size(self):
        '''Return the kernel size value.'''
        return self.__kernel_size

    def get_disturbances(self):
        '''Return the disturbance value..'''
        return self.__disturbances

    def get_kernel_width(self):
        '''Return the kernel width value.'''
        return self.__kernel_width

    def get_top_features(self):
        '''Return the top features value.'''
        return self.__top_features

    @staticmethod
    def get_default():
        '''
        Return the default configuration for Lime algorithm.

        Return
            LimeConfiguration object loaded with the default values.
        '''

        config = lime_configuration('default', 4, 150, 0.25)
        config.__top_features = 4
        return config

    @staticmethod
    def get_random():
        '''
        Return a random configuration for Lime algorithm.

        Return
            lime_algorithm object loaded with random values.
        '''

        config = lime_configuration('random', randint(2, 10), [100, 200][randint(0, 1)], [
            0.25, 0.75][randint(0, 1)])
        config.__top_features = randint(2, 18)
        return config

    def set_file_name(self, name: str):
        self.__file_name = name

    def __str__(self):
        '''
        Transform the class in a string.

        Returns:
            A concatenated string using the attributes. 
        '''

        return self.__file_name+' '+str(self.__kernel_size)+' '+str(self.__disturbances)+' '+str(self.__kernel_width)+' '+str(self.__top_features)
