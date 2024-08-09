"""
Name : Rishi Patel
Student ID : 10330771
Group : Rishi Patel, Bhavya Solanki, Lakshya Dubey
"""

"""
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokemon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""
from tkinter import *
from tkinter import ttk
import os
from poke_api import get_all_pokemon_names, download_pokemon_artwork
from image_lib import set_desktop_background_image

# Get the script and images directory
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')

# Create the images directory if it does not exist
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Create the main window
root = Tk()
root.title("Pokemon Viewer")
root.geometry("500x500")

# Set the icon
root.iconbitmap(os.path.join(script_dir, 'poke_ball.ico'))

# Create frames
top_frame = Frame(root)
top_frame.pack(pady=10)
mid_frame = Frame(root)
mid_frame.pack(pady=10)
bottom_frame = Frame(root)
bottom_frame.pack(pady=10)

# Populate frames with widgets
# Top frame: Label and Combobox for selecting a Pokemon
pokemon_label = Label(top_frame, text="Select a Pokemon:")
pokemon_label.pack(side=LEFT)

pokemon_names = get_all_pokemon_names()
pokemon_combo = ttk.Combobox(top_frame, values=pokemon_names, state="readonly")
pokemon_combo.set("Choose a Pokemon")
pokemon_combo.pack(side=LEFT, padx=10)

# Middle frame: Canvas for displaying Pokemon artwork
canvas = Canvas(mid_frame, width=400, height=400, bg="white")
canvas.pack()

# Bottom frame: Button for setting the desktop background
set_bg_button = Button(bottom_frame, text="Set as Desktop Image", state=DISABLED)
set_bg_button.pack()

# Define event handler functions
def on_pokemon_select(event):
    pokemon = pokemon_combo.get()
    if pokemon:
        image_path = os.path.join(images_dir, f"{pokemon.lower()}.png")
        if download_pokemon_artwork(pokemon, images_dir):
            display_image(image_path)
            set_bg_button.config(state=NORMAL)
        else:
            canvas.delete("all")
            set_bg_button.config(state=DISABLED)

def display_image(image_path):
    image = PhotoImage(file=image_path)
    canvas.image = image  # Keep a reference to avoid garbage collection
    canvas.create_image(200, 200, image=image)

def on_set_bg_button_click():
    pokemon = pokemon_combo.get()
    image_path = os.path.join(images_dir, f"{pokemon.lower()}.png")
    set_desktop_background_image(image_path)

# Bind events
pokemon_combo.bind("<<ComboboxSelected>>", on_pokemon_select)
set_bg_button.config(command=on_set_bg_button_click)

root.mainloop()
