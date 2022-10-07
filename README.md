# Systematic uniform random sample generator
This program draws a systematic uniform random sample from an image series (e.g. a CT image stack). That sample can then be used with other analysis tools, e.g. the Stepanizer (https://www.stepanizer.com/) for stereological assessment.

It was written to have a method of sample generation that employs a robust random number generation system and is user-friendly.

## What is systematic uniform random sampling?
"Systematic uniformly random sampling (SURS) of 1/m, where m is the sampling period, of the slices is performed with a systematic and a random component. The systematic component is the decision to choose a sampling period of m. The random sampling component is to look up a random number between 1 and m. The first slice is decided by the random number, and from then on every mth slice is chosen from the ordered set of slices, arranged in a smooth order." [1]

## How ist the random start determined?
The random starting value is taken from the host OS random number generator [2].
On Unix-like system this is /dev/urandom, on Windows CryptGenRandom() is used [3]. 

## Requirements
Required packages are listed in requirements.txt and can be installed using pip as follows:\
`pip3 install -r requirements.txt`

## How to use this program?
Only two parameters are required to run this program.
A user must specify the step size, as well as the directory containing the image stack. Example:

`python3 surs_generator.py 50 my_filedir/`

Tip: If you are running this program from within your image stack folder, use e.g. `python3 surs_generator.py 50 ./` to choose the current directory.

Optional parameters are the path of an output directory (-o option). E.g. `python3 surs_generator.py 50 my_filedir/ -o path/to/my_output_dir` 

You can also limit the program to a certain file type. If e.g. your stack of .png images is in a directory also containing .log files, the option `-f .png` allows you to exclude every non-png file from the sampling procedure.

## Sources
[1] J. R. Nyengaard, H. J. G. Gundersen, European Respiratory Review 2006 15: 107-114; DOI: 10.1183/09059180.00010101

[2] https://docs.python.org/3.8/library/random.html#random.SystemRandom

[3] https://docs.python.org/3.8/library/os.html#os.urandom