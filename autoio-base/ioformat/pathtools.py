"""
  Handle the generation of paths as well, moving between them
  and interacting with files that may exist at the paths.
"""

import os
from io import StringIO as _StringIO
import json
import numpy
from ioformat._format import remove_comment_lines
from ioformat._format import (
    remove_whitespace_from_string as remove_whitespace_)


# Handles construction and movement between different paths
def current_path():
    """ Obtain the path of the current working path.
    """
    return os.getcwd()


def go_to(path):
    """ Move to the directory that exists at a specified path.

        :param path: path of directory to move to
        :type path: str
    """
    os.chdir(path)


def prepare_path(path_lst, make=False):
    """ Build a full path from a list of strings that define parts of the
        path, and if requested, make a directory at the path.

        :param path_lst: list of strings which, when combined, define path
        :type path_lst: tuple(str)
        :param make: paramter to control making a directory at the path
        :type make: bool
        :rtype: str
    """

    path_lst = [path.lstrip('/') for path in path_lst]

    path = os.path.join('/', *path_lst)
    if make:
        os.makedirs(path)

    return path


# Handles writing and reading different file types
def write_file(string, path, file_name):
    """ Write a given string in a file with specified prefix path
        and name.

        :param string: string to write to file
        :type string: str
        :param path: path of directory where file will be written
        :type path: str
        :param file_name: name of file to be written
        :type file_name: str
    """

    fname = os.path.join(path, file_name)
    with open(fname, 'w', errors='ignore') as file_obj:
        file_obj.write(string)


def read_file(path, file_name, remove_comments=None, remove_whitespace=False):
    """ Read a file with specified prefix path
        and name into a string.

        :param path: path of directory where file will be read
        :type path: str
        :param file_name: name of file to be read
        :type file_name: str
        :rtype: str
    """

    fname = os.path.join(path, file_name)
    if os.path.exists(fname):
        with open(fname, 'r', errors='ignore') as file_obj:
            file_str = file_obj.read()
            if remove_comments is not None:
                file_str = remove_comment_lines(file_str, remove_comments)
            if remove_whitespace:
                file_str = remove_whitespace_(file_str)
    else:
        file_str = None

    return file_str


def write_numpy_file(np_arr, path, file_name):
    """ Save some numpy array to a file using the numpy interface.

        :param np_arr: array to write to file
        :type np_arr: numpy.ndarray
        :param path: path of directory where file will be written
        :type path: str
        :param file_name: name of file to be written
        :type file_name: str
    """

    np_str_io = _StringIO()
    numpy.savetxt(np_str_io, np_arr)
    np_str = np_str_io.getvalue()
    np_str_io.close()

    write_file(np_str, path, file_name)


def read_numpy_file(path, file_name):
    """ Read a file containing some array of data that is formatted by
        numpy and return the data as the appropriate numpy object.

        :param path: path of directory where file will be read
        :type path: str
        :param file_name: name of file to be read
        :type file_name: str
        :rtype: str
    """

    if os.path.exists(os.path.join(path, file_name)):
        file_str = read_file(path, file_name)
        file_str_io = _StringIO(file_str)
        np_arr = numpy.loadtxt(file_str_io)
    else:
        np_arr = None

    return np_arr


def write_json_file(dct, path, file_name):
    """ Write a JSON file which contains all of the information as
        the input Python-formatted dictionary.

        :param dct: Python dictionary to write to file
        :type dct: dict[str:vdict]
        :param path: path of directory where file will be written
        :type path: str
        :param file_name: name of file to be written
        :type file_name: str
    """

    fname = os.path.join(path, file_name)
    with open(fname, 'w') as fobj:
        json.dump(dct, fobj, indent=2, sort_keys=True)


def read_json_file(path, file_name):
    """ read a json file, send to pathtools/mechanalyzer parser
    """

    json_path = os.path.join(path, file_name)
    if os.path.exists(json_path):
        with open(json_path, 'r') as fobj:
            json_dct = json.load(fobj)
    else:
        json_dct = None

    return json_dct
