"""
Title: AthleteID
Author: Murat Yaşar Baskın
Purpose: Generates chest IDs for sports events in A5 size, in A4 PDF format, two IDs in each page
"""
import tkinter as tk
from tkinter import ttk
from functools import partial
import numpy as np
from reportlab.pdfgen import canvas as pdfcanvas
from math import ceil
from PIL import Image, ImageTk
from tkinter import filedialog
from icon import image_data as main_icon
import base64
from io import BytesIO
import fitz


root = tk.Tk()
root.wm_geometry("800x400")
root.title("AthleteID")
root.resizable(False, False)

decoded_data = base64.b64decode(main_icon)
image = Image.open(BytesIO(decoded_data))
app_icon = ImageTk.PhotoImage(image)
root.wm_iconphoto(False, app_icon)
root.icon_ref = app_icon

intervals = []
interval_no = 0
background_image = None

def add_interval():
    global interval_no
    frame = tk.Frame(scrollable, height=50)
    frame.pack(fill="x", pady=5)

    interval_start_label = tk.Label(frame, text="                       Start:")
    interval_start_label.pack(side=tk.LEFT)
    interval_start_entry = tk.Entry(frame, width=10)
    interval_start_entry.pack(side=tk.LEFT)
    interval_start_entry.insert(0,"100")

    interval_end_label = tk.Label(frame, text="End:")
    interval_end_label.pack(side=tk.LEFT)
    interval_end_entry = tk.Entry(frame, width=10)
    interval_end_entry.pack(side=tk.LEFT)
    interval_end_entry.insert(0, "105")

    interval = [interval_no, frame, interval_start_label, interval_start_entry,
                interval_end_label, interval_end_entry, True]
    intervals.append(interval)

    def delete(interval_no):
        intervals[interval_no][1].pack_forget()
        intervals[interval_no][-1] = False

    delete_button = tk.Button(frame, text="Delete", command=partial(delete, interval_no))
    delete_button.pack(side=tk.LEFT, padx=20)
    interval_no += 1
    return


def create_pdf(numbers, background_image, filename="output.pdf", font_size = 10):
    width, height = 28.35 * float(width_entry.get()), 28.35 * float(height_entry.get())
    print(width, height)
    c = pdfcanvas.Canvas(filename, pagesize=(width, height))
    section_width = width
    section_height = height

    num_pages = ceil(len(numbers))

    if background_image:

        image = Image.open(background_image)
    else:
        image = None

    try:
        margin = float(margin_box.get())
    except:
        margin = 0.64
        margin_box.set("0.64")

    for page in range(num_pages):
        if image:
            if aspect_var.get() == 0:
                c.drawImage(background_image,28.35*margin, 28.35*margin, width=section_width - 2*28.35*margin, height=section_height - 2*28.35*margin)
            else:
                imgwidth, imgheight = image.size
                if imgwidth / imgheight > section_width / section_height:
                    c.drawImage(background_image, 28.35*margin, 0.5*section_height - 0.5*(section_width - 2*28.35*margin)*imgheight/imgwidth,
                                width=section_width - 2*28.35*margin, height=(section_width - 2*28.35*margin)*imgheight/imgwidth)
                else:
                    c.drawImage(background_image, 0.5*section_width - 0.5*(section_height - 2*28.35*margin)*imgwidth/imgheight, 28.35*margin,
                                width=(section_height - 2*28.35*margin)*imgwidth/imgheight, height=section_height - 2*28.35*margin)
                print(image.size)
        c.setFont("Helvetica-Bold", font_size)
        text_width = c.stringWidth(str(numbers[page]), "Helvetica-Bold", font_size)

        try:
            x_offset, y_offset = float(x_offset_entry.get()), float(y_offset_entry.get())
        except:
            x_offset, y_offset = 0, 0
        c.drawString((0.5 * section_width - 0.5 * text_width) + x_offset*28.35, (0.5 * section_height - 0.36 * font_size)+y_offset*28.35, str(numbers[page]))

        c.showPage()

    c.save()


def generate(mode=0):
    numbers = []
    if mode == 0:
        for i in intervals:
            if i[-1] == True:
                increment = 1
                if i[3].get() and i[5].get():
                    for j in np.arange(int(i[3].get()), int(i[5].get()) + increment, increment):
                        numbers.append(int(j))

    if mode == 1:
        i = intervals[0]
        if i[-1] == True:
            increment = 1
            if i[3].get() and i[5].get():
                for j in np.arange(int(i[3].get()), int(i[5].get()) + increment, increment):
                    numbers.append(int(j))
        create_pdf(numbers, background_image, "temp.pdf", font_size=int(font_entry.get()))
    else:
        file_name = filedialog.asksaveasfile(title="Save file as", defaultextension=".pdf", filetypes=(("PDF files", "*.pdf"), ("All Files", "*.*")))
        file_name = file_name.name
        if not "pdf" in file_name:
            file_name += ".pdf"
        create_pdf(numbers, background_image, file_name, font_size=int(font_entry.get()))
        tk.messagebox.showinfo(title="File Saved!",
                               message="The Portable Document File has successfully been created and saved.")
    return


def import_image():
    global background_image
    background_image = filedialog.askopenfilename(title="Import Image")
    global image_button
    config_text = background_image.split("/")[-1]
    if len(config_text) > 15:
        config_text = config_text[:7] + "...." + config_text.split(".")[-1]
    image_button.config(text=config_text)
    preview()


def preview(event=0):
    preview_canvas.delete("all")

    generate(mode=1)
    file_path = "temp.pdf"
    if not file_path:
        return

    doc = fitz.open(file_path)
    page = doc[0]

    zoom_x = 1
    zoom_y = 1
    mat = fitz.Matrix(zoom_x, zoom_y)
    pix = page.get_pixmap(matrix=mat, alpha=False)

    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    if pix.height < pix.width:
        new_width = 400
        new_height = int(400 * pix.height / pix.width)
    else:
        new_height = 400
        new_width = int(400 * pix.width / pix.height)

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    img_tk = ImageTk.PhotoImage(img)

    preview_canvas.img_tk = img_tk

    preview_canvas.create_image(203, 203, anchor="center", image=img_tk)

def change_fontsize(event):
    value = int(font_entry.get())
    if not value:
        value = 200
    if event.delta > 0:
        value += 5
        font_entry.delete(0,tk.END)
        font_entry.insert(0,str(value))
    else:
        value -= 5
        font_entry.delete(0,tk.END)
        font_entry.insert(0,str(value))
    preview()

def change_width(event):
    value = int(width_entry.get())
    if not value:
        value = 18
    if event.delta > 0:
        value += 1
        width_entry.delete(0,tk.END)
        width_entry.insert(0,str(value))
    else:
        value -= 1
        width_entry.delete(0,tk.END)
        width_entry.insert(0,str(value))
    preview()

def change_height(event):
    value = int(height_entry.get())
    if not value:
        value = 14
    if event.delta > 0:
        value += 1
        height_entry.delete(0,tk.END)
        height_entry.insert(0,str(value))
    else:
        value -= 1
        height_entry.delete(0,tk.END)
        height_entry.insert(0,str(value))
    preview()


preview_canvas = tk.Canvas(root, height = 402, width = 402, bg="black")
preview_canvas.pack(side = tk.LEFT)

topframe = tk.Frame(root, height=50, width = 400)
topframe.pack(side = "top")

add_button = tk.Button(topframe, text="  Add interval", command=add_interval)
add_button.pack(padx=0, pady=0, side=tk.LEFT)

image_button = tk.Button(topframe, text="Import Image     ", command=import_image)
image_button.pack(padx=0, pady=0, side=tk.LEFT)

generate_button = tk.Button(topframe, text="Generate     ", command=generate)
generate_button.pack(padx=0, pady=0, side=tk.LEFT)

midframe = tk.Frame(root, height=50, width = 400)
midframe.pack(side = "top")



width_label = tk.Label(midframe, text="Width (cm):")
width_label.pack(side=tk.LEFT)
width_entry = tk.Entry(midframe, width=5)
width_entry.pack(side=tk.LEFT)
width_entry.insert(0, "18")
width_entry.bind("<Return>", preview)
width_entry.bind("<MouseWheel>",change_width)

height_label = tk.Label(midframe, text="Height (cm):")
height_label.pack(side=tk.LEFT)
height_entry = tk.Entry(midframe, width=5)
height_entry.pack(side=tk.LEFT)
height_entry.insert(0, "14")
height_entry.bind("<Return>", preview)
height_entry.bind("<MouseWheel>",change_height)

margin_label = tk.Label(midframe, text="Margins (cm):")
margin_label.pack(side = tk.LEFT)
margin_box = ttk.Combobox(midframe, values = ["0.00","0.64","1.27","2.54"], width = 5)
margin_box.pack(side = tk.LEFT)
margin_box.bind("<<ComboboxSelected>>", preview)


bottomframe = tk.Frame(root, height=50, width = 400)
bottomframe.pack(side = "top")


aspect_var = tk.BooleanVar()
aspect_tick = tk.Checkbutton(bottomframe, text = "Maintain image aspect ratio", variable=aspect_var, command = preview)
aspect_tick.pack(side=tk.LEFT)


font_label = tk.Label(bottomframe, text="                                 Font:")
font_label.pack(side=tk.LEFT)
font_entry = tk.Entry(bottomframe, width=5)
font_entry.pack(side=tk.LEFT)
font_entry.insert(0, "200")
font_entry.bind("<Return>", preview)
font_entry.bind("<MouseWheel>",change_fontsize)

bottom2frame = tk.Frame(root, height=50, width = 400)
bottom2frame.pack(side = "top")

def change_x_offset(event = 0):
    value = float(x_offset_entry.get())
    if not value:
        value = 0
    if event.delta > 0:
        value += 0.1
        x_offset_entry.delete(0,tk.END)
        x_offset_entry.insert(0,str(value)[:4])
    else:
        value -= 0.1
        x_offset_entry.delete(0,tk.END)
        x_offset_entry.insert(0,str(value)[:4])
    preview()

def change_y_offset(event = 0):
    value = float(y_offset_entry.get())
    if not value:
        value = 0
    if event.delta > 0:
        value += 0.1
        y_offset_entry.delete(0,tk.END)
        y_offset_entry.insert(0,str(value)[:4])
    else:
        value -= 0.1
        y_offset_entry.delete(0,tk.END)
        y_offset_entry.insert(0,str(value)[:4])
    preview()


x_offset_label = tk.Label(bottom2frame, text= "X-offset (cm):   ")
x_offset_label.pack(side = tk.LEFT)
x_offset_entry = tk.Entry(bottom2frame, width=5)
x_offset_entry.pack(side=tk.LEFT)
x_offset_entry.insert(0,"0.0")
x_offset_entry.bind("<Return>", preview)
x_offset_entry.bind("<MouseWheel>", change_x_offset)

y_offset_label = tk.Label(bottom2frame, text= "                                Y-offset (cm):   ")
y_offset_label.pack(side = tk.LEFT)
y_offset_entry = tk.Entry(bottom2frame, width=5)
y_offset_entry.pack(side=tk.LEFT)
y_offset_entry.insert(0,"0.0")
y_offset_entry.bind("<Return>", preview)
y_offset_entry.bind("<MouseWheel>", change_y_offset)

scroll_frame_parent = tk.Frame(root, width = 400)
scroll_frame_parent.pack(side = "top", fill="y")

canvas = tk.Canvas(scroll_frame_parent, borderwidth=0, highlightthickness=0)
scrollbar = tk.Scrollbar(scroll_frame_parent, orient="vertical", command=canvas.yview)

scrollable = tk.Frame(canvas)

scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=scrollable, anchor="n")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

add_interval()
preview()
root.mainloop()
