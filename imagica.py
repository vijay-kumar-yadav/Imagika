from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile
from PIL import Image, ImageTk
import cv2
import sketch_generator
import fileHandler
import datetime as Time
import os

# defining color
white = "#fff"


###################
###  Functions ####
###################

# Function to switch window #size_tkey->key value to change size of window #1 for 1st
def switch_window(switch_frame, size_key):
    if len(fileHandler.getRecentGPImages()) == 0 and size_key == 4:
        messagebox.showinfo(
            "Info",
            "Please convert at least one image to see recently converted images",
        )
        return
    else:
        switch_frame.tkraise()
    if size_key == 1:
        window_geometry(500, 600)
        window.config(bg=white)
    elif size_key == 2:
        window_geometry(800, 700)
        window.configure(bg="#D7DFF4")
        hide_upload_btn()
    elif size_key == 3:
        window_geometry(800, 700)
        window.configure(bg="#D7DFF4")
        display_pencil_img()
    else:
        window_geometry(800, 700)
        window.configure(bg="#D7DFF4")
        recent_images()


# Center The Window #window geometry function
def window_geometry(w_width, w_height):
    s_width, s_height = window.winfo_screenwidth(), window.winfo_screenheight()
    x, y = (s_width / 2) - (w_width / 2), (s_height / 2) - (w_height / 2)
    window.geometry("%dx%d+%d+%d" % (w_width, w_height, x, y))
    window.minsize(width=w_width, height=w_height)  # minimum window size
    window.maxsize(width=w_width, height=w_height)  # maximum window size


# Func for Loading image and making it compatible return image
def image_loader(path, height, width):
    img = Image.open(path).resize((width, height))
    image = ImageTk.PhotoImage(image=img)
    return image


# function for event handling changing play icon color
def on_enter_1(enter):
    win1_btn.config(image=win1_btn_active)


def on_leave_1(leave):
    win1_btn.config(image=win1_btn_inactive)


# function for event handling changing back icon color
def on_enter_2(enter):
    if enter == 1:
        win3_back_btn.config(image=win3_btn_active_back)
    else:
        win4_back_btn.config(image=win3_btn_active_back)


def on_leave_2(leave):
    if leave == 1:
        win3_back_btn.config(image=win3_btn_inactive_back)
    else:
        win4_back_btn.config(image=win3_btn_inactive_back)


# function for event handling changing home icon color
def on_enter_3(enter):
    home_btn.config(image=btn_active_home)


def on_leave_3(leave):
    home_btn.config(image=btn_inactive_home)


# function for event handling changing recent icon color
def on_enter_4(enter):
    if enter == 1:
        win2_recent_history_btn.config(image=recent_active_btn)
    else:
        win3_recent_history_btn.config(image=recent_active_btn)


def on_leave_4(leave):
    if leave == 1:
        win2_recent_history_btn.config(image=recent_inactive_btn)
    else:
        win3_recent_history_btn.config(image=recent_inactive_btn)


# function to display when images were converted
def on_enter_5(time_date, colour):
    date, time = time_date[1], time_date[0]
    created_time_label.config(
        text="Created On:  %s\n\nCreated At:  %s" % (date, time),
        justify="left",
        fg=colour,
        bg="#E4E9F7",
        font=("Helvetica BOLD", 12),
    )
    created_time_label.place(relx=0.38, rely=0.52, width=180, height=80)


def on_leave_5(leave):
    created_time_label.place_forget()


# defining function to hide upload button
def hide_upload_btn():
    win2_btn_2.pack_forget()


##defining func to display choosen image
def display_img(image):
    image.confg = image
    label_org.configure(image=image)


##defining func to display choosen image
def display_pencil_img():
    path = call_sketch_generator()
    image = image_loader(path, 510, 500)
    image.confg = image
    label_pencil.configure(image=image)


##defining function to get path of origional image
def get_path():
    global img_path
    img_path = askopenfilename(
        title="Open",
        filetypes=(("IMAGE FILES", "*.jpg *.png *.jpeg"), ("ALL FILES", "*.*")),
    )
    # Assigning extension of image selected by user
    extension = img_path[::-1].split(".")[0][::-1]
    # Checking If user selected correct image path
    if extension in ["jpg", "png", "jpeg", "jfef"]:
        img = image_loader(img_path, 510, 500)
        # place here because when user upload image convert>>> button will show up
        win2_btn_2.pack(side=RIGHT, padx=(120, 0), ipadx=10, ipady=5)
        display_img(img)
    else:
        messagebox.showinfo("Info", "Please select an image file")


##defining a call func to sketch_generator
def call_sketch_generator():
    global pencil_img_path
    pencil_img_path = sketch_generator.convertImg(img_path)
    return pencil_img_path


##Defining func to save file
def save_image():
    edge = Image.open(pencil_img_path)
    usr_file_name = os.path.basename(
        img_path
    )  # getting name of image as in user computer
    # removing extension
    usr_file_name = usr_file_name.rpartition(".")
    usr_file_name = usr_file_name[0]
    filename = asksaveasfile(
        mode="w",
        initialfile="%s_sketch" % usr_file_name,
        filetypes=(("jpg", "*.jpg"), ("png", "*.png"), ("jpeg", "*.jpeg")),
        defaultextension=".jpg",
    )
    if not filename:
        return
    extension = filename.name[-3:].lower()
    if extension == "png":
        cv2.imwrite(filename.name, cv2.imread(pencil_img_path))
    else:
        edge.save(filename)


# defining func to fetch date and time
def fetch_time(image_path):
    time_img = int(image_path[15:-4])  # getting time from path at which image converted
    time = Time.datetime.fromtimestamp(time_img).strftime("%H:%M:%S")
    date = Time.datetime.fromtimestamp(time_img).strftime("%d-%m-%Y")
    time_date = [time, date]
    return time_date


# defining func to display image in opencv image read window
def windows_viewer(image_path, index):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (550, 600))
    cv2.imshow("Image_%d" % (index), img)


# defining func to display recent images
def recent_images():
    recent_image_tup = []
    files = fileHandler.getRecentGPImages()

    time_date_list = []
    for e in files:
        time_date = fetch_time(e)
        time_date_list.append(time_date)

    for i in range(len(files)):
        img = image_loader(files[i], 200, 220)
        img.tk = img
        recent_image_tup.append(img)
    if len(files) >= 1:
        win4_btn_1.configure(
            image=recent_image_tup[0], command=lambda: windows_viewer(files[0], 1)
        )

        win4_btn_1.pack()
        win4_label_1.grid(row=0, column=0, padx=8, pady=(40, 0))

        win4_btn_1.bind("<Enter>", lambda time: on_enter_5(time_date_list[0], "red"))
        win4_btn_1.bind("<Leave>", on_leave_5)

    if len(files) >= 2:
        win4_btn_2.configure(
            image=recent_image_tup[1], command=lambda: windows_viewer(files[1], 2)
        )

        win4_btn_2.pack()
        win4_label_2.grid(row=0, column=1, padx=8, pady=(40, 30))

        win4_btn_2.bind("<Enter>", lambda time: on_enter_5(time_date_list[1], "green"))
        win4_btn_2.bind("<Leave>", on_leave_5)

    if len(files) >= 3:
        win4_btn_3.configure(
            image=recent_image_tup[2], command=lambda: windows_viewer(files[2], 3)
        )

        win4_btn_3.pack()
        win4_label_3.grid(row=0, column=2, padx=8, pady=(40, 0))

        win4_btn_3.bind("<Enter>", lambda time: on_enter_5(time_date_list[2], "blue"))
        win4_btn_3.bind("<Leave>", on_leave_5)

    if len(files) >= 4:
        win4_btn_4.configure(
            image=recent_image_tup[3], command=lambda: windows_viewer(files[3], 4)
        )

        win4_btn_4.pack()
        win4_label_4.grid(row=1, column=0, padx=8, pady=(0, 0))

        win4_btn_4.bind("<Enter>", lambda time: on_enter_5(time_date_list[3], "purple"))
        win4_btn_4.bind("<Leave>", on_leave_5)

    if len(files) >= 5:
        win4_btn_5.configure(
            image=recent_image_tup[4], command=lambda: windows_viewer(files[4], 5)
        )

        win4_btn_5.pack()
        win4_label_5.grid(row=1, column=1, padx=8, pady=(70, 0))

        win4_btn_5.bind("<Enter>", lambda time: on_enter_5(time_date_list[4], "brown"))
        win4_btn_5.bind("<Leave>", on_leave_5)

    if len(files) == 6:
        win4_btn_6.configure(
            image=recent_image_tup[5], command=lambda: windows_viewer(files[5], 6)
        )

        win4_btn_6.pack()
        win4_label_6.grid(row=1, column=2, padx=8, pady=(0, 0))

        win4_btn_6.bind("<Enter>", lambda time: on_enter_5(time_date_list[5], "black"))
        win4_btn_6.bind("<Leave>", on_leave_5)


## defining function to ask if he really want to close window you press enter to exit after popup
def on_close():
    resp = messagebox.askquestion("Exit", "Are you sure you want to exit?")
    if resp == "yes":
        window.destroy()
    else:
        return


if __name__ == "__main__":
    # Parent Window
    window = Tk()
    window.title(" Iɱαɠιƙα")
    window.iconphoto(TRUE, PhotoImage(file="image/parrot_sketch.png"))
    window.configure(bg=white)
    # disabling maximize button
    window.resizable(0, 0)

    # permission
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    # Frame defined for MultiWindow display
    frame_1 = Frame(window, bg=white)
    frame_2 = Frame(window, bg="#E4E9F7")
    frame_3 = Frame(window, bg="#E4E9F7")
    frame_4 = Frame(window, bg="#E4E9F7")

    # loop to stick window
    for e in (frame_1, frame_2, frame_3, frame_4):
        e.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    #######################
    ##     1st Window    ##
    #######################
    # creating label for background photo
    kyrie_pencil_sketch = image_loader("image/wally_start_page.png", 600, 500)

    # label start background
    start_label = Label(frame_1, image=kyrie_pencil_sketch)
    start_label.pack()

    # importing btn_inactive,btn_active images for play icon
    win1_btn_inactive = image_loader("image/start_inactive.png", 95, 95)
    win1_btn_active = image_loader("image/start_active.png", 95, 95)

    win1_btn = Button(
        frame_1,
        image=win1_btn_inactive,
        borderwidth=0,
        command=lambda: switch_window(frame_2, 2),
        bg=white,
        activebackground=white,
    )
    win1_btn.place(relx=0.742, rely=0.795)

    ##binding button to an event
    win1_btn.bind("<Enter>", on_enter_1)
    win1_btn.bind("<Leave>", on_leave_1)

    #######################
    ##     2nd   Window  ##
    #######################
    # frame for title of upload window
    win2_title_frame = Frame(frame_2, bg="#E4E9F7")
    win2_title_frame.pack(side=TOP)
    # frame for upload image
    win2_orgimg_frame = Frame(frame_2, bg="#E4E9F7")
    win2_orgimg_frame.pack(pady=8)
    # frame for bottom button to solve side by side placing button issue
    win2_btn_frame = Frame(frame_2, bg="#E4E9F7")
    win2_btn_frame.pack(side=BOTTOM)

    # title label for converted image page
    title_label = Label(
        win2_title_frame,
        text="Transform Your Image to Pencil Sketch",
        font=("Times new roman BOLD", 23),
        bg="#E4E9F7",
        fg="#22A75A",
    )
    title_label.pack(anchor=N)

    # defining button to see recent_historys
    recent_active_btn = image_loader("image/recent_active.png", 50, 50)
    recent_inactive_btn = image_loader("image/recent_inactive.png", 50, 50)
    win2_recent_history_btn = Button(
        frame_2,
        image=recent_inactive_btn,
        command=lambda: switch_window(frame_4, 4),
        bg="#E4E9F7",
        activebackground="#E4E9F7",
        bd=0,
        relief=RAISED,
    )
    win2_recent_history_btn.place(x=700, y=35)
    ##binding btn to an event
    win2_recent_history_btn.bind("<Enter>", lambda key: on_enter_4(1))
    win2_recent_history_btn.bind("<Leave>", lambda key: on_leave_4(1))

    # defining button to go back to convert window
    btn_active_home = image_loader("image/home_button_filled.png", 45, 45)
    btn_inactive_home = image_loader("image/home_button_outlined.png", 45, 45)
    home_btn = Button(
        frame_2,
        image=btn_inactive_home,
        command=lambda: switch_window(frame_1, 1),
        bg="#E4E9F7",
        activebackground="#E4E9F7",
        bd=0,
        relief=RAISED,
    )
    home_btn.place(x=22, y=40)

    ##binding btn to an event
    home_btn.bind("<Enter>", on_enter_3)
    home_btn.bind("<Leave>", on_leave_3)

    # defining button to upload image
    win2_btn_1 = Button(
        win2_btn_frame,
        text="Upload Image",
        command=get_path,
        relief="flat",
        bg="#197DFF",
        fg=white,
        font=("Arial Bold", 15),
        activebackground="#197DFF",
        activeforeground=white,
    )
    win2_btn_1.pack(side=LEFT, ipadx=10, ipady=5)

    # defining button to convert image to pencil sketch
    win2_btn_2 = Button(
        win2_btn_frame,
        text="Convert >>>",
        command=lambda: switch_window(frame_3, 3),
        relief="flat",
        bg="#47D182",
        fg=white,
        font=("Arial Bold", 15),
        activebackground="#47D182",
        activeforeground=white,
    )

    # defining Label frame for origional image
    """frame_org_label=LabelFrame(frame_2,text="Your Image Here",font='Helvetic',labelanchor='s',fg='magenta',bd=3,relief='raise')
    frame_org_label.pack(pady=30)"""

    # Global label to show origional image by user
    default_image = image_loader("image/default.png", 510, 500)
    label_org = Label(win2_orgimg_frame, bd=0, image=default_image, bg="#E4E9F7")
    label_org.pack(pady=30)

    #######################
    ##     3rd   Window  ##
    #######################

    # frame for title of converted image window
    win3_title_frame = Frame(frame_3, bg="#E4E9F7")
    win3_title_frame.pack(side=TOP)

    # frame to display coverted image
    win3_pencilimg_frame = Frame(frame_3, bg="#E4E9F7")
    win3_pencilimg_frame.pack(pady=8)

    # frame for bottom button to solve side by side placing button issue
    win3_btn_frame = Frame(frame_3, bg="#E4E9F7")
    win3_btn_frame.pack(side=BOTTOM)

    # title label for converted image page
    title_label = Label(
        win3_title_frame,
        text="Pencil Sketch",
        font=("times new roman BOLD", 25),
        bg="#E4E9F7",
        fg="#A9230E",
    )
    title_label.pack(side=TOP)

    # defining button to see recent_historys

    win3_recent_history_btn = Button(
        frame_3,
        image=recent_inactive_btn,
        command=lambda: switch_window(frame_4, 4),
        bg="#E4E9F7",
        activebackground="#E4E9F7",
        bd=0,
        relief=RAISED,
    )
    win3_recent_history_btn.place(x=700, y=35)
    ##binding btn to an event
    win3_recent_history_btn.bind("<Enter>", lambda key: on_enter_4(2))
    win3_recent_history_btn.bind("<Leave>", lambda key: on_leave_4(2))

    # label to display converted image
    label_pencil = Label(win3_pencilimg_frame, bd=0)
    label_pencil.pack(pady=30)

    # defining button to go back to convert window
    win3_btn_active_back = image_loader("image/back_button_filled.png", 50, 55)
    win3_btn_inactive_back = image_loader("image/back_button_outlined.png", 50, 55)
    win3_back_btn = Button(
        frame_3,
        image=win3_btn_inactive_back,
        command=lambda: switch_window(frame_2, 2),
        bg="#E4E9F7",
        activebackground="#E4E9F7",
        bd=0,
        relief=RAISED,
    )
    win3_back_btn.place(x=22, y=40)

    ##binding frame to an event
    win3_back_btn.bind("<Enter>", lambda key: on_enter_2(1))
    win3_back_btn.bind("<Leave>", lambda key: on_leave_2(1))

    # defining button to save image
    win3_btn_3 = Button(
        win3_btn_frame,
        text="Save Image ⤓",
        command=save_image,
        relief="flat",
        bg="#00B4CF",
        fg=white,
        font=("Arial Bold", 15),
        activebackground="#00B4CF",
        activeforeground="#E4E9F7",
    )
    win3_btn_3.pack(ipadx=10, ipady=5)

    #######################
    ##     4th  Window   ##
    #######################

    win4_title_frame = Frame(frame_4, bg="#E4E9F7")
    win4_title_frame.pack(side=TOP)

    # frame to upload image in grid
    win4_recentimgs_frame = Frame(frame_4, bg="#E4E9F7")
    win4_recentimgs_frame.pack(pady=8)

    # title label
    history_title_label = Label(
        win4_title_frame,
        text="Recently Converted Images",
        font=("Times new roman Bold", 24),
        bg="#E4E9F7",
        fg="#0F3BFF",
    )
    history_title_label.pack(side=TOP, padx=(0, 10))
    history_titleinfo_label = Label(
        win4_title_frame,
        text="Click on image to view in separate window",
        font=("Calibri light", 16),
        bg="#E4E9F7",
    )
    history_titleinfo_label.pack(side=TOP, padx=(0, 10))

    # defining button to go back to convert window
    win4_back_btn = Button(
        frame_4,
        image=win3_btn_inactive_back,
        command=lambda: switch_window(frame_2, 2),
        bg="#E4E9F7",
        activebackground="#E4E9F7",
        bd=0,
        relief=RAISED,
    )
    win4_back_btn.place(x=22, y=40)

    ##binding frame to an event
    win4_back_btn.bind("<Enter>", lambda key: on_enter_2(2))
    win4_back_btn.bind("<Leave>", lambda key: on_leave_2(2))

    # assigning labels
    win4_label_1 = LabelFrame(
        win4_recentimgs_frame,
        text="1",
        labelanchor=S,
        font=("times new roman BOLD", 13),
        bg="#E4E9F7",
        fg="red",
    )
    win4_label_2 = LabelFrame(
        win4_recentimgs_frame,
        text="2",
        labelanchor=S,
        font=("times new roman BOLD", 13),
        bg="#E4E9F7",
        fg="green",
    )
    win4_label_3 = LabelFrame(
        win4_recentimgs_frame,
        text="3",
        labelanchor=S,
        font=("times new roman BOLD", 13),
        bg="#E4E9F7",
        fg="blue",
    )
    win4_label_4 = LabelFrame(
        win4_recentimgs_frame,
        text="4",
        labelanchor=S,
        font=("times new roman BOLD", 13),
        bg="#E4E9F7",
        fg="purple",
    )
    win4_label_5 = LabelFrame(
        win4_recentimgs_frame,
        text="5",
        labelanchor=S,
        font=("times new roman BOLD", 13),
        bg="#E4E9F7",
        fg="brown",
    )
    win4_label_6 = LabelFrame(
        win4_recentimgs_frame,
        text="6",
        labelanchor=S,
        font=("times new roman BOLD", 13),
        bg="#E4E9F7",
        fg="black",
    )

    # assigning btns
    win4_btn_1 = Button(win4_label_1, bd=0)
    win4_btn_2 = Button(win4_label_2, bd=0)
    win4_btn_3 = Button(win4_label_3, bd=0)
    win4_btn_4 = Button(win4_label_4, bd=0)
    win4_btn_5 = Button(win4_label_5, bd=0)
    win4_btn_6 = Button(win4_label_6, bd=0)

    # Label for date and time when image created
    created_time_label = Label(frame_4)

    # asking if user want to close window
    window.protocol("WM_DELETE_WINDOW", on_close)
    window.protocol("WM_MINIMIZE_WINDOW", lambda: print("good"))
    switch_window(frame_1, 1)
    window.mainloop()
