""" main view for FEBS """
import os

from tkinter import (
    ACTIVE,
    BOTH,
    E,
    END,
    Frame,
    LEFT,
    Listbox,
    Menu,
    N,
    RIGHT,
    S,
    Tk,
    W,
)
from tkinter import filedialog
from tkinter import messagebox

from core.exceptions import ConfigNotProvided
from models.models import MainModel


class MainView(Tk):
    """ class to create main view """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.list1 = None
        self.list2 = None
        self.frame1 = None


def load_config_file():
    """ load config file in JSON format """
    config_file = filedialog.askopenfilename(
        filetypes=(("JSON files", "*.json"),)
    )
    config_dict = MAIN_MODEL.get_config(config_file)
    MAIN_MODEL.get_bucket(config_dict)
    refresh_right_column()


def refresh_right_column():
    """ refresh right column in UI with bucket contents """
    WINDOW.list2.delete(0, END)
    for index, value in enumerate(MAIN_MODEL.list_files()):
        WINDOW.list2.insert(index, value.key)


def refresh_left_column(my_path):
    """ refresh left column with files from my_path """
    WINDOW.list1.delete(0, END)
    for index, value in enumerate(sorted([
            f for f in os.listdir(my_path)
            if os.path.isfile(os.path.join(my_path, f))
    ])):
        WINDOW.list1.insert(index, value)


def double_click_from_local_to_remote(event):
    """ function to upload file """
    try:
        MAIN_MODEL.get_config()
    except ConfigNotProvided:
        load_config_file()
    local_file = WINDOW.list1.get(ACTIVE)
    print(WINDOW.list1.get(ACTIVE))
    MAIN_MODEL.upload(PATH + "/" + local_file, local_file)

    refresh_right_column()
    messagebox.showinfo(
        'File uploaded successfully',
        f'File {local_file} uploaded successfully'
    )


def double_click_from_remote_to_local(event):
    """ function to download file """
    try:
        MAIN_MODEL.get_config()
    except ConfigNotProvided:
        load_config_file()
    remote_file = WINDOW.list2.get(ACTIVE)
    print(WINDOW.list2.get(ACTIVE))
    MAIN_MODEL.download(remote_file, PATH + "/" + remote_file)

    refresh_left_column(PATH)
    messagebox.showinfo(
        'File downloaded successfully',
        f'File {remote_file} downloaded successfully'
    )


WINDOW = MainView()
WINDOW.title('File Explorer for Bucket S3')
WINDOW.geometry('800x600')
MENU = Menu(WINDOW)

NEW_ITEM = Menu(MENU, tearoff=0)  # disable dashed line
NEW_ITEM.add_command(label='Load config file', command=load_config_file)
NEW_ITEM.add_command(label='Quit', command=WINDOW.quit)

MENU.add_cascade(label='File', menu=NEW_ITEM)

WINDOW.config(menu=MENU)

# frame
FRAME1 = Frame(WINDOW)
WINDOW.frame1 = FRAME1
FRAME1.grid(row=0, column=0, sticky=N+S+E+W)

# list
PATH = "/home/lonclegr"
LIST1 = Listbox(FRAME1)

LIST1.bind('<Double-Button-1>', double_click_from_local_to_remote)
LIST1.pack(fill=BOTH, expand=True, side=LEFT)
WINDOW.list1 = LIST1
refresh_left_column(PATH)

LIST2 = Listbox(FRAME1)
LIST2.bind('<Double-Button-1>', double_click_from_remote_to_local)
LIST2.pack(fill=BOTH, expand=True, side=RIGHT)
WINDOW.list2 = LIST2

FRAME1.pack(fill=BOTH, expand=True)

MAIN_MODEL = MainModel()
