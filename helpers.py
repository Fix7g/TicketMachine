try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError as err:
    tk = tk or None
    messagebox = messagebox or None
    print('Couldn\'t load module. %s' % err)
    exit(1)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ListHelper:
    def __init__(self):
            pass

    @staticmethod
    def list_sub(first, second):
        result = [item for item in first if item not in second]
        return result


def btn_with_img(parent, _path, callback):
    img = tk.PhotoImage()
    img["file"] = _path
    button = tk.Button(parent)
    button["image"] = img
    button["bd"] = 0
    button["command"] = callback
    button.img = img
    return button


def load_image(path):
    img = tk.PhotoImage()
    img["file"] = path
    return img


def coin_val(name):
    return int(name.split('.', 1)[0])/100


def bill_val(name):
    return int(name.split('z', 1)[0])


def show_error(self, exc, val, tab):
    messagebox.showerror('Error occured', str(val))


def show_info(text):
    messagebox.showinfo('Information', text)


def entry(parent, column, row):
    var_for_text = tk.StringVar()
    _input = tk.Entry(parent, textvariable=var_for_text)
    _input.grid(column=column, row=row)
    return _input


def new_label(parent, text):
    lab = tk.Label(parent, text=text)
    return lab


def is_int(value):
    try:
        if not isinstance(value, int):
            _fl = float(value)
            _in = int(value)
            if _fl != _in:
                return False
        return True
    except ValueError:
        print("Value cannot be parsed to number")
        return False
