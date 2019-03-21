# Python Tkinter Table by Paphra
------------------------

: This module creates a tkinter table according to the specifications.
The table is entirely scrollable and allows selection of a row
and visibly seeing the selected row using the highlight of grey
color, but the color can be changed easily.
Deleting of a row is supported by this table using the appropriate
functions and methods and once a row is deleted, another is
automatically selected in the place of the deleted row
Scrolling can be done by the mouse wheel or the Scrollbar for both
the vertical and the horizontal

--------

## Note:
--------
: Python Dictionaries are used for the rows. Each row must be
a python dictionary for this table to work well. Uniform or
constant keys for these dictionaries must be used

-------------

## Imports:
-------------
1. tk - The main tkinter module
2. messagebox - For the confirmation of the deletion of a row
3. ttk - The themed tkinter
4. Thread - For background tasks
-------------

## Procedure of How to use the Python Table
-------------------------------------------
1. Make a list of all the keys for the python dictionaries. The
keys which represent the individual columns in the row

2. Make a list of dictionaries for the titles. Each title
dictionary is a single column and this dictionary represents
the column header. The dictionary must contain the following
keys:
    - text:     this is text for the column header
    - width:    the integer for the width of the column
    - type:     the type of the widget to use for holding the
        data in the column. The type is represented by a single
        letter in the string data type
        * 'l' - for the Label widget
        * 'c' - for the Combobox widget

3. Make a list of dictionaries, each dictionary representing the
row. Each row must be having all the keys specified in the list
of keys.

4. Initialize the class called 'Table' passing the neccessary arguments
5. Call 'add_rows()' passing the neccessary arguments

6. For deleting, select a row and call 'delete_row()'
7. You can also get the currently selected row by calling the
method 'get_selected()'

# installing
~~~~
pip install paphra-tktable
from paphra_tktable import table

tb = table.Table(master)
~~~~
----------------------
