""" This module creates a table according to the specifications
The table is entirely scrollable and allows selection of a row
and visibly seeing the selected row using the highlight of grey
color, but the color can be changed easily.
Deleting of a row is supported by this table using the appropriate
functions and methods and once a row is deleted, another is
automatically selected in the place of the deleted row
Scrolling can be done by the mouse wheel or the Scrollbar for both
the vertical and the horizontal

Note:
-----
Python Dictionaries are used for the rows. Each row must be
a python dictionary for this table to work well. Uniform or
constant keys for these dictionaries must be used

Imports:
--------
:tk - The main tkinter module
:Thread - For loading and working in background
:messagebox - For the confirmation of the deletion of a row
:ttk - The themed tkinter

Procedure of How to use the Python Table
----------------------------------------
:- Make a list of all the keys for the python dictionaries. The
keys which represent the individual columns in the row

:- Make a list of dictionaries for the titles. Each title
dictionary is a single column and this dictionary represents
the column header. The dictionary must contain the following
keys:
    :- text:     this is text for the column header
    :- width:    the integer for the width of the column
    :- type:     the type of the widget to use for holding the
        data in the column. The type is represented by a single
        letter in the string data type
        :'l' - for the Label widget
        :'c' - for the Combobox widget

:- Make a list of dictionaries, each dictionary representing the
row. Each row must be having all the keys specified in the list
of keys.

:- Initialize the class called 'Table' passing the neccessary arguments
:- Call 'add_rows()' passing the neccessary arguments

:- For deleting, select a row and call 'delete_row()'
:- You can also get the currently selected row by calling the
method 'get_selected()'
"""

import tkinter as tk
from threading import Thread
from tkinter import messagebox as msg, ttk


def _shade(wl_, color=None):
    """ Shading a given row when selection occurs with the
    given color.
    :type wl_: list
    :param wl_: list of widgets on the row
    :type color: str
    :param color: color to be used. If it is None, then,
        shading occurs.
    :return: None
    """
    if color is None:
        color = ''
    for _w in wl_:
        if isinstance(_w, type(ttk.Label())):
            _w['background'] = color


def _sep_work(cont, lb_list):
    """ Create and Situate separators on a given container between
    widgets
    :type lb_list: list
    :param lb_list: list of widgets to be separated using the
        separators
    :type cont: any container; e.g Frame, LabelFrame, etc
    :param cont: container widget
    :return: None
    """
    _col = 0                            # First column is 0
    # For situating the separators on the container
    for _c in range(len(lb_list) + 1):
        if _c > 0:
            _col = _col + 2
        sep = ttk.Separator(cont, orient='vertical')
        sep.grid(column=_col, row=1, sticky='NS')

        if _c < len(lb_list):
            lb_list[_c].grid(column=(_col + 1), row=1, sticky='WE',
                             padx=2, pady=2)


def check_rows(rows_list, titles, _keys_):
    """ Checking the list of rows to see if they contain any rows.
    If the list is empty, then a row is created to show that
    nothing is found in the list of rows.
    :type rows_list: list
    :param rows_list: list of rows in the dictionary form to
        be put in the table
    :type titles: list
    :param titles: list of dictionaries for the titles which
        represent the column headers.
    :type _keys_: list
    :param _keys_: list of strings for the keys of the titles.
    :return: list - of dictionaries for the rows
    """
    if len(rows_list) == 0:
        no_rows = {}
        for _t in titles:
            if titles.index(_t) == 0:
                no_rows[_keys_[0]] = 'Nothing is Found!'
            else:
                no_rows[_keys_[titles.index(_t)]] = ''
        return [no_rows]
    return rows_list


class Table:
    """ Creates the table form as specified. A container e.g Frame,
    is passed at initialization. Then a method is called to create
    the table.
    """

    def __init__(self, container, _keys_=None, titles=None, width=None,
                 height=None):
        """ Initializes the Table creation
        :type container: any, e.g ttk.Frame(), ttk.LabelFrame(), etc
        :param container: the container to hold the table structure
        :type _keys_: list
        :param _keys_: list of strings for the keys of the titles
        :type titles: list
        :param titles: list of dictionaries for the column headers.
            The headers with their widths and the types of the data
            for the columns, e.g c for the Combobox, l for the Label
        :type width: int
        :param width: integer for the width of the table
        :type height: int
        :param height: integer for the height of the Table
        :return: None
        """
        self.host = ttk.Frame(master=container)
        self.title_pane = ttk.Frame(self.host)

        # the main canvas that is scrollable
        self.list_canvas = tk.Canvas(self.host)
        self._keys_ = _keys_

        # if the keys list id None, then a mock is created
        if self._keys_ is None:
            self._keys_ = ['col1', 'col2', 'col3', 'col4']
        self._width = width
        if self._width is None:
            self._width = 200
        self._height = height
        if self._height is None:
            self._height = 300

        self.titles = titles
        # if the titles list is None, then a mock is created
        if self.titles is None:
            self.titles = [{'text': 'Column 1', 'width': 15, 'type': 'l'},
                           {'text': 'Column 2', 'width': 15, 'type': 'l'},
                           {'text': 'Column 3', 'width': 15, 'type': 'l'},
                           {'text': 'Column 4', 'width': 15, 'type': 'l'}]

        # instance variables
        self.sel_ind = None
        self.col_span = None
        self.rows_list = None
        self.selected_w = None
        self.selected_row = None
        self.mock_rows = []

        # set up mock data in case the table is being run in the
        # stand alone mode
        self.work_on_mock()
        self.rows = []

        # create the main table which involves making the
        # column headers, fixing the width of the columns and the
        # height of the table
        self._create()

    def work_on_mock(self):
        """
        Filling the mock rows with mock data
        :return: None
        """
        for i in range(30):
            self.mock_rows.append({
                    'col1': 'value of col 1 row ' + str(i + 1),
                    'col2': 'value of col 2 row ' + str(i + 1),
                    'col3': 'value of col 3 row ' + str(i + 1),
                    'col4': 'value of col 4 row ' + str(i + 1)})

    def _create(self):
        """ Creates the Table """

        # situating the host on the master
        self.host.grid(column=0, row=0, sticky='NSE')

        # situating the title_pane on the host/container
        self.title_pane.grid(column=0, row=0)
        cols = len(self.titles)
        self.col_span = (cols * 2) + 2

        # adding a separator at the top of the title pane
        titles_top = ttk.Separator(self.title_pane, orient='horizontal')
        titles_top.grid(column=0, row=0, sticky='WE', columnspan=self.col_span)

        # working on the titles
        self._titles_works()

        # adding 2 separators at the bottom of the title pane
        for i in range(2, 4):
            t_btm = ttk.Separator(self.title_pane, orient='horizontal')
            t_btm.grid(column=0, row=i, sticky='WE', columnspan=self.col_span)

        # scroll bars for te vertical and horizontal
        v_scr = tk.Scrollbar(self.host, orient='vertical')

        # situating the canvas and setting it up to be scrollable
        self.list_canvas.grid(column=0, row=1, sticky='WENS',
                              columnspan=(self.col_span - 1))
        self.list_canvas.configure(yscrollcommand=v_scr.set,
                                   width=self._width,
                                   height=self._height)

        v_scr.grid(column=(self.col_span - 1), row=1, sticky='NS', rowspan=3)

        v_scr['command'] = self.list_canvas.yview
        self._mouse_wheel([self.list_canvas, self.host])

    def _mouse_wheel(self, widgets):
        """ Performing the scrolling using the Mouse Wheel
        :type widgets: list
        :param widgets: list of widgets that make up the row
        :return: None
        """

        def _wheel(event):
            """ Movement of the wheel """
            move = int(event.delta / 60)
            self.list_canvas.yview_scroll(move, tk.UNITS)

        for widget in widgets:
            widget.bind('<MouseWheel>', _wheel, True)

    def _titles_works(self):
        """ Positions the titles as column headers and sets the
        column widths
        :return: None
        """
        lb_list = [ttk.Label(self.title_pane, text='S/N', width=5)]

        for title in self.titles:
            _lb = title['text']
            _lb = ttk.Label(self.title_pane, text=title['text'],
                            width=title['width'])
            lb_list.append(_lb)

        _sep_work(cont=self.title_pane, lb_list=lb_list)
        return True

    def add_rows(self, rows_list=None):
        """ Add given rows on to the canvas of the table
        :type rows_list: list
        :param rows_list: list of rows[dictionaries] to be placed on
            the canvas
        :return: None
        """
        self.rows_list = rows_list
        if self.rows_list is None:
            self.rows_list = self.mock_rows

        self.selected_row = None
        self.selected_w = None

        def des():
            for _w in self.list_canvas.winfo_children():
                _w.destroy()
                del _w
        Thread(target=des(), daemon=True).start()

        num_rows = len(self.rows_list)
        scr_v = num_rows * 26

        self.list_canvas['scrollregion'] = (0, 0, 0, scr_v)

        def works():

            y_cord = 0
            for i in range(len(self.rows_list)):
                _llb = 'frame' + str(i)
                _llb = ttk.Frame(self.list_canvas)

                lb_list = []
                lb_sn = ttk.Label(_llb, text=str(i + 1), width=5)
                lb_list.append(lb_sn)
                self._make_row_widgets(_llb, lb_list, i)

                _sep_work(_llb, lb_list)

                sep11 = ttk.Separator(_llb, orient='horizontal')
                sep11.grid(column=0, row=2, sticky='WE', columnspan=self.col_span)

                if i > 0:
                    y_cord = y_cord + 26

                self.list_canvas.create_window(-2, y_cord, window=_llb,
                                               anchor=tk.NW)

                for _ww in _llb.winfo_children():
                    _ww.bind('<ButtonRelease-1>', self._click, True)
                    self._mouse_wheel([_ww])
                self.selected_w = None

        Thread(target=works(), daemon=True).start()

    def _make_row_widgets(self, _llb, lb_list, _i):
        """ Make the widgets for the row. This is done using the keys
        list and the titles dictionaries
        :tyoe _llb: Label
        :param _llb: label, the row main widget
        :type lb_list: list
        :param lb_list: list of widgets. This is where the manufactured
            widgets are put
        :type _i: int
        :param _i: integer for the position or row number being worked
            upon
        :return: None
        """
        for key in self._keys_:
            _text = self.rows_list[_i][key]
            _type = self.titles[self._keys_.index(key)]['type']
            _width = self.titles[self._keys_.index(key)]['width']
            _w = None
            if self.titles[self._keys_.index(key)]['type'] == 'l':
                _w = ttk.Label(_llb, text=_text, width=_width)
            elif _type == 'c':
                _w = ttk.Combobox(_llb, values=_text, width=(_width - 3),
                                  state='readonly')
                if len(_text) > 0:
                    _w.current(0)
            elif _type == 'e':
                _v = tk.StringVar(value=_text)
                _w = ttk.Entry(_llb, textvariable=_v, width=_width,
                               state='readonly')

            lb_list.append(_w)

    def _click(self, event=None):
        """ Performing the Clicking event on a given row
        :type event: event
        :param event: event of button clicking
        :return: None
        """
        parent_name = event.widget.winfo_parent().split('.')

        self.sel_ind = None
        self.selected_row = None

        counts = 0
        _children = self.list_canvas.winfo_children()
        if self.selected_w is not None:
            try:
                self.selected_w.configure(relief='', borderwidth=0)
                _shade(self.selected_w.winfo_children())
                self.selected_w = None
            except Exception:
                pass

        for win_ in _children:
            w_name = win_.winfo_name()
            if parent_name[len(parent_name)-1] == w_name:
                self._select(win_)
                self.sel_ind = counts

            else:
                if counts == len(_children):
                    self.selected_w = None
            counts = counts + 1

    def _select(self, widget):
        """ Selecting the entire row of widgets that make up the row
        of the table. This is the row that has been clicked.
        This is also aimed at deselecting the previous row before
        before the new one is selected
        :type widget: Frame
        :param widget: frame containing the row widgets. The parent
            for the row
        :return: None
        """

        _wch = widget.winfo_children()
        selected_txt = _wch[1]['text']
        if selected_txt != 'Nothing is Found!':
            self.selected_w = widget
            self.selected_w.configure(relief='sunken', borderwidth=1)
            for row in self.rows_list:
                if selected_txt == row[self._keys_[0]]:
                    self.selected_row = row
            _shade(_wch, 'grey')
        else:
            self.selected_row = None
            self.selected_w = None

    def delete_row(self):
        """ Delete a selected row
        :return: None or dict - Previously Selected row
        """
        if self.selected_row is not None and \
            msg.askquestion('Itory: Deletion Confirmation',
                            'Confirm Deletion?') == u'yes':
                self.selected_w.destroy()
                self.rows_list.remove(self.selected_row)
                prev_selected = self.selected_row
                self.add_rows(check_rows(self.rows_list, self.titles,
                                         self._keys_))
                self._select_new_after_delete()
                return prev_selected
        return None

    def _select_new_after_delete(self):
        """ Perform the selection after the deleting action
        :return: None
        """
        counts = 0
        list_ = self.list_canvas.winfo_children()
        for win_ in list_:
            if counts == len(list_):
                self.selected_w = None
                self.selected_row = None
                self.sel_ind = None
                break
            if counts == self.sel_ind:
                self._select(win_)
                self.sel_ind = counts
                break
            counts = counts + 1

    def get_selected(self):
        """ Get the the text on the first widget of the selected row
        :return: dict row
        """
        return self.selected_row


if __name__ == '__main__':
    root = tk.Tk()
    table = Table(root)
    table.add_rows()

    root.mainloop()
