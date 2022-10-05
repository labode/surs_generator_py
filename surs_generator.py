import random
import argparse
import os
import shutil
import sys
if os.name == 'nt':
    import win32api, win32con


def check_positive(number):
    if number <= 0:
        sys.exit('ERROR! The supplied number is 0 or negative. Only numbers greater than 0 are allowed.')


def is_hidden(file):
    if os.name == 'nt':
        if win32api.GetFileAttributes(file) & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM):
            return True
    else:
        if file.startswith('.'):
            return True

    return False


# Generate random number between 0 and step size
def random_start(limit):
    start = random.SystemRandom().randint(0, limit - 1)  # Limit -1 as we start at 0
    print('Randomly starting at file no. ' + str(start + 1))
    return start


# Get a list of the files
def list_dir(path, file_extension=None):
    try:
        files = os.listdir(path)
    except PermissionError:
        sys.exit('ERROR! Could not read directory ' + path + '. No permission.')
    except FileNotFoundError:
        sys.exit('ERROR! Could not read directory ' + path + '. Invalid path.')

    files.sort()

    data = []
    if file_extension is not None:
        for file in files:
            if file.endswith(file_extension):
                if not is_hidden(path + '/' + file):
                    data.append(path + '/' + file)
        return data
    else:
        for file in files:
            if not is_hidden(path + '/' + file):
                data.append(path + '/' + file)
        return data


# Generate list of files to copy
def draw_sample(files, start, step):
    size = len(files)
    if size < start or size < step:
        sys.exit('ERROR! Step size is larger than number of files! '
                 'Choose a smaller step size and check that you are working on the correct directory.')

    sample_set = []
    i = start
    while i < size:  # This is important! The index of the last file is len - 1, as the index starts at 0!
        sample_set.append(files[i])
        i = i + step

    return sample_set


# Perform copying action
def write_sample(sample_set, destination=None):
    if destination is not None:
        path = destination
    else:
        path = 'sample'
        print('No directory specified, writing output to folder ' + path + '/')

    # Check if path exists
    if os.path.exists(path):
        # If it exists it should be empty
        if len(os.listdir(path)) != 0:
            sys.exit('ERROR! The directory ' + path + ' is not empty. '
                                                      'Please specify another directory using the -o option.')
    # If not, try to create it
    else:
        try:
            os.mkdir(path)
        except PermissionError:
            sys.exit('ERROR! Could not create directory ' + path + '. No permission.')
        except FileNotFoundError:
            sys.exit('ERROR! Could not create directory ' + path + '. Invalid path.')

    for entry in sample_set:
        shutil.copy2(entry, path)  # TODO: Should we follow symlinks?


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Draw a uniform random sample from a folder containing an image stack')
    parser.add_argument('step', action='store', type=int, help='Step size')
    parser.add_argument('directory', action='store', type=str, help='Directory containing the image stack')
    parser.add_argument('-o', '--output', action='store', type=str, required=False,
                        help='Directory to write the sample to. '
                             'If not supplied, a folder with the name sample is created in the current directory')
    parser.add_argument('-f', '--filetype', action='store', type=str, required=False,
                        help='Type of the files to draw a sample from '
                             '(e.g. if non images are present in the directory)')
    # TODO: Option to link files?
    #  This would safe space if the user works on the same machine the image stack is located on

    # TODO: Option to supply random value to recreate a specific run?
    #  Then we would have to check, if it is consistent with the step size...

    # TODO: Option to specify a file pattern? => Would extend the file type filter

    # TODO: Status output for bored users?

    args = parser.parse_args()

    step_size = args.step
    directory = args.directory
    output = args.output
    filetype = args.filetype

    check_positive(step_size)

    print('Generating list of files')
    file_list = list_dir(directory, filetype)

    print('Creating a random number')
    start_point = random_start(step_size)

    print('Creating list of samples')
    sample = draw_sample(file_list, start_point, step_size)

    print('Writing samples to output directory')
    write_sample(sample, output)

    print('Done!')
