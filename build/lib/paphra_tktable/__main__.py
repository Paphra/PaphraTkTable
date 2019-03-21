""" Just in case the package is run as a module """

import tkinter as tk
from table import Table

root = tk.Tk()
table = Table(root)
table.add_rows()

root.mainloop()
