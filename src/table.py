"""
This module creates a table form according to the specifications
from the designing developer
"""

import tkinter as tk  # importing tkinter as tk for easy reference
from threading import Thread
from tkinter import messagebox as msg, ttk  # importing the themed tkinter module


def _shade(wl_, color=None):
    """
    Shading a given row when selection occurs
    :type wl_: list
    :type color: str
    :param wl_: list of widgets on the row
    :param color: color to be used
    :return: None
    """
    if color is None:
        color = ''
    for _w in wl_:
        if isinstance(_w, type(ttk.Label())):
            _w['background'] = color


def _sep_work(cont, lb_list):
    """
    Create and Situate separators on a given container between
    widgets
    :type lb_list: list
    :type cont: any
    :param cont: container widget
    :param lb_list: list of widgets to be separated using the
    separators
    :return: None
    """
    _col = 0
    for _c in range(len(lb_list) + 1):
        if _c > 0:
            _col = _col + 2
        sep = ttk.Separator(cont, orient='vertical')
        sep.grid(column=_col, row=1, sticky='NS')

        if _c < len(lb_list):
            lb_list[_c].grid(column=(_col + 1), row=1, sticky='WE',
                             padx=2, pady=2)


def check_rows(rows_list: list, titles: list, _keys_: list):
    """
    Checking the rows to see if they are okay
    :return:
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
    """
    This class creates the table form as specified by the one
    designing the table. A master of any kind is passed in at
    initialization. Then a method called create is called to
    create the table. This method takes arguments: list of
    dictionaries for the titles with their text, width and type
    of the widget for each row cell. e.g
    {'text': 'Name of something', 'width': 30, 'type': 'l'}
    'l' is for ttk.Label(), 'c' is for ttk.Combobox(), 'e' is
    for ttk.Entry()
    """

    def __init__(self, master, _keys_=None, titles=None, width=None,
                 height=None):
        """
        Initializes the Table creation
        :type master: any
        :param master: the container to hold the table structure
        """
        self.host = ttk.Frame(master=master)
        self.title_pane = ttk.Frame(self.host)
        # the main canvas that is scrollable
        self.list_canvas = tk.Canvas(self.host)
        self._keys_ = _keys_
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
        self.work_on_mock()
        self.rows = []

        # self._make_rows(50)
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

        v_scr.grid(column=(self.col_span - 1), row=1, sticky='NS',
                   rowspan=3)

        v_scr['command'] = self.list_canvas.yview
        self._mouse_wheel([self.list_canvas, self.host])

    def _mouse_wheel(self, widgets):

        def _wheel(event):
            move = int(event.delta / 60)
            self.list_canvas.yview_scroll(move, tk.UNITS)

        for widget in widgets:
            widget.bind('<MouseWheel>', _wheel, True)

    def _titles_works(self):
        """
        This method works on the titles. Positions the and sets the
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
        """
        Add given rows on to the canvas of the table
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
                sep11.grid(column=0, row=2, sticky='WE',
                           columnspan=self.col_span)

                if i > 0:
                    y_cord = y_cord + 26

                self.list_canvas.create_window(-2, y_cord, window=_llb,
                                               anchor=tk.NW)

                for _ww in _llb.winfo_children():
                    _ww.bind('<ButtonRelease-1>', self._click, True)
                    self._mouse_wheel([_ww])

        Thread(target=works(), daemon=True).start()

    def _make_row_widgets(self, _llb, lb_list, _i):
        """
        Make the widgets for the row
        :param _llb: label, the row main widget
        :param lb_list: list of widgets. This is where the widgets are
        put
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
        """
        Work on the clicking event on a given row
        :param event: event of button
        :return: None
        """

        self._selection(event.widget.winfo_parent())

    def _selection(self, parent_name):
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
            if str(w_name) in str(parent_name):
                self._select(win_)
                self.sel_ind = counts

            else:
                if counts == len(_children):
                    self.selected_w = None
            counts = counts + 1

    def _select(self, widget):
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

    def _select_new_after_delete(self):
        """
        Perform the selection after the deleting action
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

    def delete_row(self):
        """
        Delete a selected row
        :return: None
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

    def get_selected(self):
        """
        Get the the text on the first widget of the selected row
        :return: dict row
        """
        return self.selected_row


if __name__ == '__main__':
    root = tk.Tk()
    table = Table(root)
    table.add_rows()

    root.mainloop()
