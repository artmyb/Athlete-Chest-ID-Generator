#pyinstaller main.py --onefile --windowed --icon "icon.ico" --name "AthleteID"

import tkinter as tk
from functools import partial
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from math import ceil
from PIL import Image, ImageTk
from tkinter import filedialog
from icon import image_data as main_icon
import base64
from io import BytesIO


root = tk.Tk()
root.wm_geometry("370x100")
root.title("AthleteID")
root.resizable(False, True)
decoded_data = base64.b64decode(main_icon)

image = Image.open(BytesIO(decoded_data))

app_icon = ImageTk.PhotoImage(image)

root.wm_iconphoto(False, app_icon)
root.icon_ref = app_icon


intervals = []
interval_no = 0
background_image = None

def add_interval():
    frame = tk.Frame(root, height = 50)
    frame.pack(fill = "x")

    interval_start_label = tk.Label(frame,text = "Start:")
    interval_start_label.pack(side= tk.LEFT)
    interval_start_entry = tk.Entry(frame, width = 10)
    interval_start_entry.pack(side = tk.LEFT)

    interval_end_label = tk.Label(frame,text = "   End:")
    interval_end_label.pack(side= tk.LEFT)
    interval_end_entry = tk.Entry(frame, width = 10)
    interval_end_entry.pack(side = tk.LEFT)

    increment_label = tk.Label(frame,text = "   Increment:")
    increment_label.pack(side= tk.LEFT)
    increment_entry = tk.Entry(frame, width = 5)
    increment_entry.pack(side = tk.LEFT)
    increment_entry.insert(0,"1")


    global interval_no

    interval = [interval_no, frame, interval_start_label, interval_start_entry,
                interval_end_label, interval_end_entry,
                increment_label,
                increment_entry,
                True]

    intervals.append(interval)


    def delete(interval_no):
        intervals[interval_no][1].pack_forget()
        intervals[interval_no][-1] = False


    delete_button = tk.Button(frame,text = "Delete", command = partial(delete,interval_no))
    delete_button.pack(side = tk.LEFT, padx = 5)
    interval_no += 1


def create_pdf(numbers, image_path, filename="output.pdf", font_size=300):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    section_width = width
    section_height = height / 2

    num_pages = ceil(len(numbers) / 2)

    if background_image:
        try:
            image = Image.open(background_image)
            image = image.resize((int(section_width), int(section_height)))  # Resize image to fit the section
        except Exception as e:
            print(f"Error loading image: {e}")
            image = None
    else:
        image = None
    for page in range(num_pages):
        if 2 * page < len(numbers):
            if image:
                c.drawImage(image_path, 0.05 * width, height / 2 + 0.05 * height, width=section_width * 0.9, height=section_height * 0.9)

            c.setFont("Helvetica", font_size)
            text_width = c.stringWidth(str(numbers[2 * page]), "Helvetica", font_size)
            c.drawString((width - text_width) / 2, height / 2 + (section_height - 0.5 * font_size) / 2, str(numbers[2 * page]))

        if 2 * page + 1 < len(numbers):
            if image:
                c.drawImage(image_path, 0.05 * width, 0.05 * height, width=0.9 * section_width, height=0.9 * section_height)

            c.setFont("Helvetica", font_size)
            text_width = c.stringWidth(str(numbers[2 * page + 1]), "Helvetica", font_size)
            c.drawString((width - text_width) / 2, (section_height - 0.5 * font_size) / 2, str(numbers[2 * page + 1]))

        c.setDash(6, 3)
        c.setStrokeColorRGB(0, 0, 0)
        center_y = height / 2
        c.line(0, center_y, width, center_y)

        c.showPage()

    c.save()


def generate():
    numbers = []
    for i in intervals:
        if i[-1] == True:
            if not i[7].get():
                increment = 1
            else:
                increment = int(i[7].get())
            if i[3].get() and i[5].get():
                for j in np.arange(int(i[3].get()),  int(i[5].get())+increment,  increment):
                    numbers.append(int(j))

    file_name = filedialog.asksaveasfile(title = "Save file as", defaultextension=".pdf", filetypes=(("PDF files", "*.pdf"), ("All Files", "*.*")))
    file_name = file_name.name
    if not "pdf" in file_name:
        file_name += ".pdf"
    create_pdf(numbers,background_image, file_name, font_size = int(font_entry.get()))
    tk.messagebox.showinfo(title="File Saved!",
                           message="The Printable Document File has successfully been created and saved.")
    return

topframe = tk.Frame(root, height  =50)
topframe.pack()

def import_image():
    global background_image
    background_image = filedialog.askopenfilename(title = "Import Image")
    global image_button
    config_text = background_image.split("/")[-1]
    if len(config_text) > 15:
        config_text = config_text[:7]+"...."+config_text.split(".")[-1]
    image_button.config(text = config_text)

image_button = tk.Button(topframe, text = "Import Image", command = import_image)
image_button.pack(padx = 5, pady = 10, side = tk.LEFT)

add_button = tk.Button(topframe, text = "Add interval", command = add_interval)
add_button.pack(padx = 5, pady = 10, side = tk.LEFT)

font_label = tk.Label(topframe, text="   Font Size:")
font_label.pack(side=tk.LEFT)
font_entry = tk.Entry(topframe, width=5)
font_entry.pack(side=tk.LEFT)
font_entry.insert(0, "250")

generate_button = tk.Button(topframe, text = "Generate", command = generate)
generate_button.pack(padx = 5, pady = 10, side = tk.LEFT)
add_interval()

tk.mainloop()
