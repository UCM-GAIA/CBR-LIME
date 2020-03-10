import os
import errno


def read_csv(file_path: str, split_line: bool = True, split_char: str = ';', header=True) -> list:
    '''
    Read a csv file format and return a list

    Read a file in csv format and return a list with the information
    one element per row.

    Parameters
        file_path,  path of the file
        split_line, if the line has been splitted
        split_char, character for split the line
        header,     if the file have header line
    '''
    if os.path.isfile(file_path):
        result = list()

        with open(file_path, 'r') as the_file:
            if header:
                the_file.readline()

            for line in the_file:
                if split_line:
                    line = line.split(split_char)
                    line.pop()
                result.append(line)

        return result


def read_dict_csv(file_path: str, split_char: str = ';', header=True) -> dict():
    '''
    Read a csv file and return a dictionary

    Read a file in csv format and return a dictionary with
    the first item in the row as key and the oters in a list
    as value

    Parameters
        file_path,  path of the file
        split_line, if the line has been splitted
        split_char, character for split the line
        header,     if the file have header line
    '''

    if os.path.isfile(file_path):
        result = dict()

        with open(file_path, 'r') as the_file:
            if header:
                the_file.readline()

            for line in the_file:
                line = line.split(split_char)
                line.pop()
                key = line.pop(0)
                result[key] = line

        return result


def write_csv(data: list, out_file: str, separator: str = ';', header: bool = False, header_data: list = list()) -> str:
    '''
    Write a csv file format and return a the file path

    Write a file in csv format write one line per element in the parameter data
    and return the destination file path.

    Parameters
        data,           data to save
        out_file,       path of the file
        separator,      character for split the data
        header,         must write a header
        header_data,    header text
    '''

    with open(out_file, 'w') as the_file:
        if header:
            header_data.append('\n')
            header_text = separator.join(header_data)
            the_file.write(header_text)

        for line in data:
            line.append('\n')
            line = list(map(lambda x: str(x), line))
            text = separator.join(line)
            the_file.write(text)

    return the_file.name


def ls(path: str) -> list:
    '''
    Obtain the file list found in the parameter folder path.

    Parameters:
        path,   Folder path to find the files.
    '''
    return [obj.path for obj in os.scandir(path) if obj.is_file()]


def load_simil_matrix_file_data(path: str) -> (dict, list):
    '''
    Load the similitude matrix in the sistem.

    Parameters
        path,    path to the similitude matrix file.

    Return
        dictionary with the similitude data
        list with the images names
    '''

    similData = dict()

    with open(path, 'r') as the_file:
        header = the_file.readline()
        header = header.split(';')
        header.pop(0)
        header.pop()

        for line in the_file:
            line = line.split(';')
            item = _clean_filename(line.pop(0))
            line.pop()
            localData = dict()

            for index in range(len(line)):
                localData[_clean_filename(header[index])] = line[index]

            similData[item] = localData
    return similData, list(map(_clean_filename, header))


def load_simil_dict_file_data(path: str) -> (dict, list):
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
            index = _clean_filename(line.pop(0))

            localData = dict()
            for item in range(0, len(line), 2):
                localData[_clean_filename(line[item])] = line[item+1]

            result[index] = localData

    return result, list(map(_clean_filename, result.keys()))


def _clean_filename(filename: str) -> str:
    '''
    Return the filename and extension from a path

    Parameters
        filename,   path to the file

    Return
        filename and extension
    '''

    return os.path.basename(filename)


def create_folder(path: str):
    '''
    Create folder.

    Create folder recived, if obtains a relative path, try to create 
    it in the current directory if not exists, if the folder already
    exists do nothing.

    Parameters
        path,   path of the objetive folder
    '''

    try:
        os.mkdir(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
