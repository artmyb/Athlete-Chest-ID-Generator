"""
Title: AthleteID
Author: Murat Yaşar Baskın
Purpose: Generates chest IDs for sports events in custom size, in custom or metric size PDF format.
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
    interval_start_entry.bind("<Return>",preview)

    interval_end_label = tk.Label(frame, text="End:")
    interval_end_label.pack(side=tk.LEFT)
    interval_end_entry = tk.Entry(frame, width=10)
    interval_end_entry.pack(side=tk.LEFT)
    interval_end_entry.insert(0, "105")
    interval_end_entry.bind("<Return>", preview)

    interval = [interval_no, frame, interval_start_label, interval_start_entry,
                interval_end_label, interval_end_entry, True]
    intervals.append(interval)

    def delete(interval_no):
        if interval_no == 0:
            return
        intervals[interval_no][1].pack_forget()
        intervals[interval_no][-1] = False

    delete_button = tk.Button(frame, text="Delete", command=partial(delete, interval_no))
    delete_button.pack(side=tk.LEFT, padx=20)
    interval_no += 1
    return


def create_pdf(numbers, background_image, filename="output.pdf", font_size = 100):
    print(layout_var)
    if background_image:

        image = Image.open(background_image)
    else:
        image = None

    try:
        margin = float(margin_box.get())
    except:
        margin = 0.64
        margin_box.set("0.64")

    if layout_var.get() == False:
        width, height = 28.35 * float(width_entry.get()), 28.35 * float(height_entry.get())
        print(width, height)
        c = pdfcanvas.Canvas(filename, pagesize=(width, height))
        section_width = width
        section_height = height

        num_pages = ceil(len(numbers))

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
    else:
        if orientation_var.get() == False:
            pdf_width = 28.35*100*(2**(-1/4))*2**(-0.5*int(layout_combobox.get()[-1]))
            pdf_height = 28.35*100*(2**(1/4))* 2 ** (-0.5 * int(layout_combobox.get()[-1]))
        else:
            pdf_width = 28.35*100*(2**(1/4))* 2 ** (-0.5 * int(layout_combobox.get()[-1]))
            pdf_height = 28.35*100*(2**(-1/4))*2**(-0.5*int(layout_combobox.get()[-1]))
        c = pdfcanvas.Canvas(filename, pagesize=(pdf_width, pdf_height))
        width, height = 28.35 * float(width_entry.get()), 28.35 * float(height_entry.get())
        columns = (pdf_width - 2*28.35*float(layout_margin_combobox.get()))//width -1
        rows = (pdf_height - 2 * 28.35 * float(layout_margin_combobox.get())) // height -1
        section_width = width
        section_height = height
        page = 0
        row = 0
        column = 0
        for i in numbers:
            layout_offset_x = 28.35 * float(layout_margin_combobox.get()) + column * section_width
            layout_offset_y = 28.35 * float(layout_margin_combobox.get()) + row * section_height
            if image:

                if aspect_var.get() == 0:
                    c.drawImage(background_image,28.35*margin+ layout_offset_x, 28.35*margin+layout_offset_y, width=section_width - 2*28.35*margin, height=section_height - 2*28.35*margin)
                else:
                    imgwidth, imgheight = image.size
                    if imgwidth / imgheight > section_width / section_height:
                        c.drawImage(background_image, 28.35*margin+layout_offset_x, 0.5*section_height - 0.5*(section_width - 2*28.35*margin)*imgheight/imgwidth+layout_offset_y,
                                    width=section_width - 2*28.35*margin, height=(section_width - 2*28.35*margin)*imgheight/imgwidth)
                    else:
                        c.drawImage(background_image, 0.5*section_width - 0.5*(section_height - 2*28.35*margin)*imgwidth/imgheight+layout_offset_x, 28.35*margin+layout_offset_y,
                                    width=(section_height - 2*28.35*margin)*imgwidth/imgheight, height=section_height - 2*28.35*margin)
                    print(image.size)
            c.setFont("Helvetica-Bold", font_size)
            text_width = c.stringWidth(str(i), "Helvetica-Bold", font_size)
            if grid_var.get() == 1:
                c.setDash(3, 6)
                c.line(layout_offset_x,layout_offset_y, layout_offset_x + section_width, layout_offset_y)
                c.line(layout_offset_x, layout_offset_y, layout_offset_x, layout_offset_y+ section_height)
                c.line(layout_offset_x, layout_offset_y+ section_height, layout_offset_x+ section_width, layout_offset_y + section_height)
                c.line(layout_offset_x+ section_width, layout_offset_y + section_height, layout_offset_x + section_width,
                       layout_offset_y + section_height)
            try:
                x_offset, y_offset = float(x_offset_entry.get()), float(y_offset_entry.get())
            except:
                x_offset, y_offset = 0, 0
            c.drawString((0.5 * section_width - 0.5 * text_width) + x_offset*28.35+layout_offset_x, (0.5 * section_height - 0.36 * font_size)+y_offset*28.35+layout_offset_y, str(i))
            if column == columns and row == rows:
                c.showPage()
                row = 0
                column = 0
            elif column == columns:
                row += 1
                column = 0
            else:
                column += 1
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
    try:
        doc = fitz.open(file_path)
    except:
        return
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
    value = int(float(width_entry.get())+0.5)
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
    value = int(float(height_entry.get())+0.5)
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
aspect_tick = tk.Checkbutton(bottomframe, text = "Maintain background image aspect ratio", variable=aspect_var, command = preview)
aspect_tick.pack(side=tk.LEFT)


font_label = tk.Label(bottomframe, text="   Font Size:")
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


x_offset_label = tk.Label(bottom2frame, text= "X-position offset (cm):")
x_offset_label.pack(side = tk.LEFT)
x_offset_entry = tk.Entry(bottom2frame, width=5)
x_offset_entry.pack(side=tk.LEFT)
x_offset_entry.insert(0,"0.0")
x_offset_entry.bind("<Return>", preview)
x_offset_entry.bind("<MouseWheel>", change_x_offset)

y_offset_label = tk.Label(bottom2frame, text= "        Y-position offset (cm):")
y_offset_label.pack(side = tk.LEFT)
y_offset_entry = tk.Entry(bottom2frame, width=5)
y_offset_entry.pack(side=tk.LEFT)
y_offset_entry.insert(0,"0.0")
y_offset_entry.bind("<Return>", preview)
y_offset_entry.bind("<MouseWheel>", change_y_offset)

layout_frame = tk.Frame(root, height=50, width = 400)
layout_frame.pack(side = "top")

def layout_false():
    layout_combobox.config(state="disabled")
    layout_margin_combobox.config(state="disabled")
    orientation_radio_0.config(state="disabled")
    orientation_radio_1.config(state="disabled")
    grid_tick.config(state="disabled")
    global layout_var
    layout_var.set(False)
    preview()
    return

def layout_true():
    layout_combobox.config(state="normal")
    layout_margin_combobox.config(state="normal")
    orientation_radio_0.config(state="normal")
    orientation_radio_1.config(state="normal")
    layout_combobox.state(["readonly"])
    grid_tick.config(state="normal")
    global layout_var
    layout_var.set(True)
    preview()
    return

layout_var = tk.BooleanVar(value = False)
layout_radio_0 = tk.Radiobutton(layout_frame, text = "One ID/page", variable = layout_var, value = False, command= layout_false)
layout_radio_0.pack(side = tk.LEFT)
layout_radio_1 = tk.Radiobutton(layout_frame, text = "Fit into:", variable = layout_var, value = True, command= layout_true)
layout_radio_1.pack(side = tk.LEFT)
layout_var.set(False)

layout_combobox = ttk.Combobox(layout_frame, values= ["A0","A1","A2","A3","A4","A5"], width= 3, state = "readonly")
layout_combobox.state(["readonly"])
layout_combobox.set("A3")
layout_combobox.pack(side=tk.LEFT)
layout_combobox.bind("<<ComboboxSelected>>",preview)

tk.Label(layout_frame, text = "   Margins (cm):").pack(side = tk.LEFT)

layout_margin_combobox = ttk.Combobox(layout_frame, values= ["0.63","1.27","2.54"], width= 5)
layout_margin_combobox.set("1.27")
layout_margin_combobox.pack(side=tk.LEFT)
layout_margin_combobox.bind("<<ComboboxSelected>>",preview)

layout_combobox.config(state="disabled")
layout_margin_combobox.config(state="disabled")


layout2_frame = tk.Frame(root, height=50, width = 400)
layout2_frame.pack(side = "top")
orientation_var = tk.BooleanVar(value = False)
orientation_radio_0 = tk.Radiobutton(layout2_frame, text = "Portrait", variable = orientation_var, value = False, command = preview)
orientation_radio_0.pack(side = tk.LEFT)
orientation_radio_1 = tk.Radiobutton(layout2_frame, text = "Landscape:", variable = orientation_var, value = True, command = preview)
orientation_radio_1.pack(side = tk.LEFT)

grid_var = tk.BooleanVar(value = False)
grid_tick = tk.Checkbutton(layout2_frame, var = grid_var, text = "Grid", command = preview)
grid_tick.pack(side = tk.LEFT)

orientation_radio_0.config(state="disabled")
orientation_radio_1.config(state="disabled")
grid_tick.config(state="disabled")


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
