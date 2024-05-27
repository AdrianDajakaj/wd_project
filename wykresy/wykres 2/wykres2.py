import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Folder z obrazkami
image_folder = r'E:\wizualizacja\static'

# Funkcja zwracająca ścieżkę do obrazka na podstawie roku
def get_image_path(year):
    filename = f"{int(year) - 2000}.png"
    return os.path.join(image_folder, filename)

# Funkcja aktualizująca wyświetlany obrazek
def update_image(event):
    global image_label
    year = year_slider.get()
    image_path = get_image_path(year)
    if os.path.exists(image_path):
        image = Image.open(image_path)
        image = image.resize((400, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo
    else:
        image_label.config(image='')

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Image Viewer")

# Tworzenie suwaka do wyboru roku
year_slider = ttk.Scale(root, from_=2010, to=2023, orient='horizontal', command=update_image)
year_slider.set(2010)
year_slider.pack()

# Etykieta do wyświetlania obrazka
image_label = tk.Label(root)
image_label.pack()

# Inicjalizacja pierwszego obrazka
update_image(None)

# Uruchomienie pętli głównej
root.mainloop()
