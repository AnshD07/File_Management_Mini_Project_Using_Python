import os
import shutil
import string
from tkinter import *
from tkinter import filedialog


def file_types():
    file_type = {
        'PDF': ['.pdf'],
        'Documents': ['.docx', '.xlsx', '.pptx', '.doc', '.xls', '.ppt'],
        'Images': ['.jpg', '.png', '.gif', '.jpeg', '.bmp', ],
        'Audio': ['.mp3', '.mpeg', '.m4a', '.wav', '.flac'],
        'Video': ['.mp4', '.mkv'],
        'Compressed': ['.zip', '.rar'],
        'Software': ['.exe'],
        'Web': ['.html', '.css', '.js', '.json', '.xml'],
        'Adobe': ['.psd', '.ai'],
        'Application': ['.apk', '.iso', '.torrent'],
        'Python_Note_Book': ['.ipynb', '.py', '.pyc', '.pyo']
    }
    return file_type


def get_extension(files, path):
    dic = {}
    for file in files:

        full_path = os.path.join(path, file)  # for getting full path
        extension = os.path.splitext(file)[1].lower()

        if os.path.isdir(full_path) or extension == "":  # for checking, it is not folder na
            continue
        else:
            if extension in dic:
                dic[extension].append(file)
            else:
                dic[extension] = [file]
    return dic


def create_folder(file_types_extension, dictionary, path2, folder_list):
    extension_list = []
    for i in dictionary.keys():
        extension_list.append(i)

    for file, types in file_types_extension.items():
        for ex in extension_list:
            if ex in types:
                # print(file)
                if os.path.isdir(os.path.join(path2, file)):
                    continue
                else:
                    # if file in os.listdir(path2):
                    #     continue
                    # else:
                    folder_list.append(file)
                    os.mkdir(os.path.join(path2, file))


def move_files(file_types, dictionary, path2, path):
    for x, y in file_types.items():
        for key, value in dictionary.items():
            if key in y:
                for i in value:
                    old_path = os.path.join(path, i)
                    new_path = os.path.join(path2, x, i)
                    shutil.move(old_path, new_path)


def move_folder(file_list, paste_path, copy_path):
    for i in file_list:
        if os.path.isdir(os.path.join(copy_path, i)):
            copy = os.path.join(copy_path, i)
            paste = os.path.join(paste_path, i)
            shutil.move(copy, paste)


def abcd_format(folder_list, path):
    for folder in folder_list:
        full_path = os.path.join(path, folder)
        # print(full_path)
        file_list = os.listdir(full_path)
        # print(file_list)
        character_list = []
        for file in file_list:
            if file[0] in character_list:
                continue
            elif os.path.isdir(os.path.join(full_path, file)):
                continue
            else:
                if file[0] in string.ascii_letters:
                    character_list.append(file[0])
        # making folder of alphabets name
        for c in character_list:
            os.mkdir(os.path.join(full_path, c.upper()))

        # now let's move all file

        for f in file_list:
            if f[0] in character_list:
                old = os.path.join(full_path, f)
                new = os.path.join(full_path, f[0].upper())
                shutil.move(old, new)
        print(character_list)


# This is part of GUI of file management
def browse_source():
    source_folder = filedialog.askdirectory()
    if source_folder:
        source_path.set(source_folder)


def browse_destination():
    dest_folder = filedialog.askdirectory()
    if dest_folder:
        dest_path.set(dest_folder)


# Here is mapping of backend code and frontend code
def start_processing():
    # source_folder = source_path.get()
    # dest_folder = dest_path.get()

    sort_option = "ABCD Format" if sort_option_var.get() == 1 else "Normal Sort"
    # print(f"Source Folder: {source_folder}\nDestination Folder: {dest_folder}\nSorting Option: {sort_option}")

    # curr_path = os.getcwd()
    curr_path = source_path.get()
    browse_path = dest_path.get()
    files = os.listdir(browse_path)

    files = [i for i in files if i != 'main.py']  # for remove main.py file from list
    dictionary = get_extension(files, browse_path)  # get all extension of file

    # for getting extension dictionary
    file_extension = file_types()

    # get all extra folder list
    folder_list = []

    # making extra folder with extension wise
    create_folder(file_extension, dictionary, curr_path, folder_list)

    print(folder_list)

    move_files(file_extension, dictionary, curr_path, browse_path)
    move_folder(files, curr_path, browse_path)  # if folder there move folder also

    # Alphabets Sorting
    if sort_option_var.get() == 1:
        abcd_format(folder_list, browse_path)


def making_gui():
    root = Tk()
    root.title("File Management")
    root.geometry("800x500")
    root.resizable(False, False)

    # Custom Fonts
    title_font = ("Helvetica", 24, "bold")
    label_font = ("Helvetica", 12)
    button_font = ("Helvetica", 12, "bold")

    # Background Colors
    bg_color = "#a3d2ca"
    btn_color = "#e77f67"
    btn_hover_color = "#d1543f"
    btn_text_color = "white"

    left_frame = Frame(root, bg=bg_color)
    left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    right_frame = Frame(root, bg=bg_color)
    right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    # Title
    title_label = Label(left_frame, text="File Management", font=title_font, bg=bg_color)
    title_label.pack(pady=20)

    # Browse Buttons and Paths
    source_label = Label(left_frame, text="Source Folder", font=label_font, bg=bg_color)
    source_label.pack()
    global source_path
    source_path = StringVar()
    source_entry = Entry(left_frame, textvariable=source_path, width=50)
    source_entry.pack()
    browse_button = Button(left_frame, text="Browse", font=button_font, bg=btn_color, fg=btn_text_color,
                           activebackground=btn_hover_color, activeforeground=btn_text_color, command=browse_source)
    browse_button.pack(pady=10)

    dest_label = Label(left_frame, text="Destination Folder", font=label_font, bg=bg_color)
    dest_label.pack()
    global dest_path
    dest_path = StringVar()
    dest_entry = Entry(left_frame, textvariable=dest_path, width=50)
    dest_entry.pack()
    dest_button = Button(left_frame, text="Browse", font=button_font, bg=btn_color, fg=btn_text_color,
                         activebackground=btn_hover_color, activeforeground=btn_text_color, command=browse_destination)
    dest_button.pack(pady=10)

    # Sorting Options
    sort_label = Label(right_frame, text="Sorting Options", font=title_font, bg=bg_color)
    sort_label.pack(pady=20)
    global sort_option_var
    sort_option_var = IntVar()  # Define the variable
    sort_option_var.set(1)  # Set default value
    abcd_radio = Radiobutton(right_frame, text="Sort in ABCD Format", font=label_font, bg=bg_color,
                             variable=sort_option_var,
                             value=1)
    abcd_radio.pack(anchor="w", padx=20, pady=5)
    normal_radio = Radiobutton(right_frame, text="Normal Sort", font=label_font, bg=bg_color, variable=sort_option_var,
                               value=2)
    normal_radio.pack(anchor="w", padx=20, pady=5)

    # Start Button
    start_button = Button(root, text="Start Processing", font=button_font, bg=btn_color, fg=btn_text_color,
                          activebackground=btn_hover_color, activeforeground=btn_text_color, command=start_processing)
    start_button.place(relx=0.5, rely=0.95, anchor="s")

    root.mainloop()


making_gui()

