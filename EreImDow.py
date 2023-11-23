import os
from tkinter import Tk, Label, Entry, Button, filedialog, DISABLED, Frame, StringVar
from PIL import Image, ImageTk
from requests import get


class ImageDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.style = {
            "bg_color": "#303030",
            "text_color": "#d6d6d6",
            "entry_bg": "#272727",
            "entry_fg": "#d6d6d6",
            "cursor_color": "white",
            "button_bg": "#228e5d",
            "button_fg": "#f5f5f5",
            "highlight_bg": "#272727",
        }
        self.root.configure(bg=self.style["bg_color"])
        self.root.resizable(False, False)
        self.url_var = StringVar()
        self.name_var = StringVar()
        self.current_sid = 0  # Для ВКонтакте

        # Новые атрибуты
        self.title_label = None
        self.github_link = None
        self.entry_frame = None
        self.url_label = None
        self.url_entry = None
        self.directory_label = None
        self.directory_entry = None
        self.browse_button = None
        self.get_image_button = None
        self.image_label = None
        self.name_label = None
        self.name_entry = None
        self.save_button = None
        self.dark_photo = None  # Добавлено для избежания ошибки

        self.create_widgets()

    def create_widgets(self):
        dark_image = Image.new("RGB", (390, 150), color="#272727")
        self.dark_photo = ImageTk.PhotoImage(dark_image)

        self.title_label = Label(
            root,
            text="EreImDow",
            font=("Helvetica", 20),
            bg=self.style["button_bg"],
            fg="white",
        )
        self.title_label.pack(pady=(10, 0))

        self.github_link = Label(
            root,
            text="https://github.com/eremeyko/",
            font=("Helvetica", 10),
            fg=self.style["button_bg"],
            bg=self.style["bg_color"],
            cursor="hand2",
        )
        self.github_link.pack(pady="0 10")
        self.github_link.bind("<Button-1>", lambda event: self.open_github_link())

        self.entry_frame = Frame(self.root, bg=self.style["highlight_bg"])
        self.entry_frame.pack(pady="10 10", padx=5)

        self.url_label = Label(
            self.entry_frame,
            text="Введите URL картинки:",
            font=("Helvetica", 12),
            bg=self.style["highlight_bg"],
            fg=self.style["text_color"],
        )
        self.url_label.grid(row=0, column=0, padx="10 0", pady="10 10")

        self.url_entry = Entry(
            self.entry_frame,
            textvariable=self.url_var,
            width=30,
            bd=3,
            bg=self.style["entry_bg"],
            fg=self.style["entry_fg"],
            font=("Helvetica", 12),
            insertbackground=self.style["cursor_color"],
        )
        self.url_entry.grid(row=0, column=1, padx="0 10", pady="10 10")
        self.url_entry.bind(
            "<KeyRelease>", lambda event: self.enable_get_image_button()
        )

        self.directory_label = Label(
            self.entry_frame,
            text="Выберите директорию для сохранения:",
            font=("Helvetica", 12),
            bg=self.style["highlight_bg"],
            fg=self.style["text_color"],
        )
        self.directory_label.grid(row=1, column=0, padx="10 0", pady="0 10")

        self.directory_entry = Entry(
            self.entry_frame,
            width=30,
            bd=3,
            bg=self.style["entry_bg"],
            fg=self.style["entry_fg"],
            font=("Helvetica", 12),
            insertbackground=self.style["cursor_color"],
        )
        self.directory_entry.grid(row=1, column=1, padx="0 10", pady="0 10")

        self.browse_button = Button(
            self.entry_frame,
            text="Обзор",
            command=self.browse_directory,
            bg=self.style["button_bg"],
            fg=self.style["button_fg"],
            font=("Helvetica", 12),
        )
        self.browse_button.grid(row=1, column=2, pady="0 10")

        self.get_image_button = Button(
            self.root,
            text="Получить картинку",
            command=self.show_image,
            bg=self.style["button_bg"],
            fg=self.style["button_fg"],
            font=("Helvetica", 12),
        )
        self.get_image_button.pack(pady="0 10")
        self.get_image_button["state"] = DISABLED

        self.image_label = Label(
            self.root,
            text="Просмотр картинки:",
            font=("Helvetica", 12),
            bg=self.style["bg_color"],
            fg=self.style["text_color"],
        )
        self.image_label.pack()
        self.image_label.config(image=self.dark_photo)

        self.name_label = Label(
            self.root,
            text="Введите имя файла:",
            font=("Helvetica", 12),
            bg=self.style["bg_color"],
            fg=self.style["text_color"],
        )
        self.name_label.pack()

        self.name_entry = Entry(
            self.root,
            width=30,
            bd=3,
            bg=self.style["entry_bg"],
            fg=self.style["entry_fg"],
            font=("Helvetica", 12),
            insertbackground=self.style["cursor_color"],
        )
        self.name_entry.pack()
        self.name_entry.bind("<Key>", lambda event: self.enable_save_button())

        self.save_button = Button(
            self.root,
            text="Сохранить и Показать следующую",
            command=self.save_and_show_next_image,
            bg=self.style["button_bg"],
            fg=self.style["button_fg"],
            font=("Helvetica", 12),
        )
        self.name_entry.bind(
            "<Return>", lambda event: self.save_and_show_next_image(event)
        )
        self.save_button.pack(pady="10 0")
        self.save_button["state"] = DISABLED

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.directory_entry.delete(0, "end")
        self.directory_entry.insert(0, directory)

    def show_image(self):
        url = self.url_entry.get()
        params = self.extract_params(url)

        response = get(url, params=params)
        image_data = response.content

        image_name = "temp.jpg"
        image_path = os.path.join(self.directory_entry.get(), image_name)

        if not self.directory_entry.get() or not os.path.exists(
            self.directory_entry.get()
        ):
            return

        with open(image_path, "wb") as image_file:
            image_file.write(image_data)

        self.show_image_in_app(image_path)

    def show_image_in_app(self, image_path):
        self.name_var.set("")
        try:
            image = Image.open(image_path)
            image = image.resize((390, 150), Image.BICUBIC)
            photo = ImageTk.PhotoImage(image)
            self.image_loaded = True
        except Exception as e:
            photo = self.dark_photo
            self.image_loaded = False

        self.image_label.config(image=photo)
        self.image_label.image = photo

    def extract_params(self, url):
        params = {}
        query_string = url.split("?")[1]
        pairs = query_string.split("&")

        for pair in pairs:
            key, value = pair.split("=")
            params[key] = value

        self.current_sid = params['sid']  # Задаем сид для обновления
        return params

    def save_and_show_next_image(self, event=None):
        user_defined_name = self.get_user_defined_name()

        temp_image_name = "temp.jpg"
        temp_image_path = os.path.join(self.directory_entry.get(), temp_image_name)

        new_image_name = f"{user_defined_name}.jpg"
        new_image_path = os.path.join(self.directory_entry.get(), new_image_name)

        try:
            os.rename(temp_image_path, new_image_path)
        except FileNotFoundError:
            pass

        self.show_image()

        self.current_sid += 1

        self.save_button["state"] = DISABLED

    def get_user_defined_name(self):
        return self.name_var.get()

    def open_github_link(self):
        os.system("start https://github.com/eremeyko/")

    def enable_get_image_button(self):
        if self.url_var.get():
            self.get_image_button["state"] = "normal"
        else:
            self.get_image_button["state"] = DISABLED

    def enable_save_button(self):
        if self.name_entry.get():
            self.save_button["state"] = "normal"
        else:
            self.save_button["state"] = DISABLED


if __name__ == "__main__":
    root = Tk()
    app = ImageDownloaderApp(root)
    root.mainloop()
