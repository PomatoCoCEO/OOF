# OOF: The Output Organizing Framework

For research projects where it is easy to become overwhelmed with the disorganization of the output files.

Supports the following features:
- logging text into a log
- saving matplotlib figures
- saving numpy arrays, compressed or uncompressed
- saving any other data structure you like, as long as you define a function to save it
- producing a report of all the files saved throughout one run of your program

The various files generated throughout program execution are then adequately organized into a directory structure of the kind ``(year)/(month)/(day)/(hour)-(minute)/(run number)``; and are separated by format (text, figures, numpy arrays, etc).

To use it, simply import the module and create an instance of the class OOF:

```python

from oof import OOF
oof = OOF()

```

Then, you can use the methods of the class to save your files:

```python
# logged text is saved in the log file
oof.log("This is a log message")

# figures are saved as png files; and non-blocking plots are shown with plot()
oof.plot(x,y)
oof.plot_3d(x,y,z)

# numpy arrays are saved as npy or npz files
oof.save_array(my_array,'my_array')
oof.save_array(my_array,'my_array',compressed=True)

# user-defined data structures are saved with a user-defined function
oof.save_data(my_data,'my_data',my_save_function)

```

Finally, you can produce a report of all the files saved throughout the program execution:

```python
oof.report()

```
If your goal is just to analyse directory structure, you can initialize the class with analyse=True and with the directory to analyse:

```python

oof = OOF(analyse=True,dir='path/to/directory')
oof.report()

```

