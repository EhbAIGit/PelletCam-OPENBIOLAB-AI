#!/usr/bin/python

# author: Lode 2021

from pathlib import Path
import statistics
import requests

from PIL import ImageTk, Image, ImageDraw  # pip3 install Pillow
# from tkinter import * # pip3 install tk
from tkinter import Scrollbar, Frame, Canvas, Tk, SUNKEN, N, S, E, W, HORIZONTAL, VERTICAL, BOTH, NW, SW, SE, NE, ALL # pip3 install tk
from tkinter.filedialog import askopenfilename
import time

CURRENT_DIRECTORY = Path.cwd()

########### DEFAULT VALUES ###########
DEFAULT_PICTURES_PATH = CURRENT_DIRECTORY
DEFAULT_OUTPUT_PATH = Path(CURRENT_DIRECTORY, "output")
COLOR_PICKER_SIZE = 3
IMAGE_TAKEOUT_SIZE = 300
#######################################

clicked_coords = None
event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))

reference_R = 0
reference_G = 0
reference_B = 0

def get_files(folder_path, extensions = ["jpg", "JPEG", "PNG", "png", "jpeg", "JPG", "GIF", "gif"]):

    files = set([])
    for ext in extensions:
        files_with_extension = sorted(Path(folder_path).glob('*.{}'.format(ext)))
        files.update(set(files_with_extension))
    
    return list(files)

def process_picture(picture_path, output_folder, color_pick_area_size=3, picture_outtake_size=100):
    global reference_R, reference_G, reference_B
    p = Path(picture_path)

    obtain_mouse_coordinate(picture_path)

    pixel_coordinate = clicked_coords  # use a global variable to deal with tkinter
    
    # CREATE PICTURES 

    # save picture outtake

    # one_pixel_wide = (0,0,1,1)
    # two_pixels_wide = (1,1,1,1)
    # three_pixels_wide = (1,1,2,2)
    # four_pixels_wide = (2,2,2,2)
    # five_pixels_wide = (2,2,3,3)
    # six_pixels_wide = (3,3,3,3)

    s= color_pick_area_size
    if (s%2 == 1):
        colour_picker_box = (s//2, s//2, s//2 + 1, s//2 + 1)
    else:
        colour_picker_box = (s//2, s//2, s//2, s//2)
    # print(colour_picker_box)


    image_colour_pick_region = get_picture_region_by_box_offset(picture_path, pixel_coordinate, colour_picker_box)
    colour_info_dict = get_median_rgb(image_colour_pick_region)

    box_offset = (
        picture_outtake_size//2,
        picture_outtake_size//2,
        picture_outtake_size//2,
        picture_outtake_size//2)

    image_region_of_interest_large = get_picture_region_by_box_offset(picture_path, pixel_coordinate, box_offset)
    image_region_of_interest_large.save(Path(output_folder, "{}_detail.jpg".format(p.stem)))

    # save picture outtake with box
    box_image = ImageDraw.Draw(image_region_of_interest_large)
    shape = (
        picture_outtake_size//2 - colour_picker_box[0] - 1,
        picture_outtake_size//2 - colour_picker_box[1] - 1,
        picture_outtake_size//2 + colour_picker_box[2] ,
        picture_outtake_size//2 + colour_picker_box[3] ,
        )
    box_image.rectangle(shape, outline = "black")
    image_region_of_interest_large.save(Path(output_folder, "{}_detail_with_box.jpg".format(p.stem)))

    # save median colour image
    median_colour_tuple = (
        colour_info_dict["median_R"],
        colour_info_dict["median_G"],
        colour_info_dict["median_B"],
    )
    median_colour_swatch = Image.new('RGB', (picture_outtake_size, picture_outtake_size), median_colour_tuple)
    median_colour_swatch.save(Path(output_folder, "{}_median_colour.jpg".format(p.stem)))

    # CSV LINE
    sampleID = p.stem
    
    date = 666

    if (picture_path == "reference.jpg") :
        reference_R =  colour_info_dict["median_R"]
        reference_G = colour_info_dict["median_G"]
        reference_B = colour_info_dict["median_B"]
    
    csv_line = "{0},{1},{2},{3},{4},{5},{6},{7},{8}".format(
        sampleID,
        picture_path,
        date,
        colour_info_dict["median_R"],
        colour_info_dict["median_G"],
        colour_info_dict["median_B"],
        reference_R,
        reference_G,
        reference_B,
    )

    return csv_line

def add_to_results_csv(filepath, csv_line):

    if not Path(filepath).is_file():
        # create
        with open(filepath, "w") as f:
            f.write("ID, Unic_number, Date, Red, Green, Blue, Ref. Red,Ref. Green,Ref. Blue"+ "\n")
    
    with open(filepath, "a") as f:
            f.write(csv_line + "\n")

def obtain_mouse_coordinate(picture_path):
    # coordinates are stored in a global variable as TKinter does not return values.

    root = Tk()
    root.state("zoomed")  # maximise window

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    img = ImageTk.PhotoImage(Image.open(picture_path))  # PIL solution
    canvas.create_image(0, 0, anchor=NW, image=img)

    canvas.config(scrollregion=canvas.bbox(ALL))

    #function to be called when mouse is clicked
    def printcoords(event):
        #outputting x and y coords to console

        cx, cy = event2canvas(event, canvas)
        # print ("(%d, %d) / (%d, %d)" % (event.x,event.y,cx,cy))
        global clicked_coords 
        clicked_coords = (cx,cy)
        root.destroy()
        
    #mouseclick event
    canvas.bind("<ButtonPress-1>",printcoords)

    root.mainloop()

def obtain_mouse_coordinate_independent():


    root = Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    picture = askopenfilename(parent=root, initialdir="M:/",title='Choose an image.')
    print("opening %s" % picture)

    img = ImageTk.PhotoImage(Image.open(picture))  # PIL solution
    canvas.create_image(0, 0, anchor=NW, image=img)

    # img = PhotoImage(file=File)
    # canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    #function to be called when mouse is clicked
    def printcoords(event):
        #outputting x and y coords to console
        cx, cy = event2canvas(event, canvas)
        # print ("(%d, %d) / (%d, %d)" % (event.x,event.y,cx,cy))
        global clicked_coords 
        clicked_coords = (cx,cy)
        root.destroy()
        
    #mouseclick event
    canvas.bind("<ButtonPress-1>",printcoords)
    # canvas.bind("<ButtonRelease-1>",printcoords)

    root.mainloop()

def get_picture_region_by_radius(picture_path, pixel_coordinate, region_radius=1):
    
    if (region_radius < 1):
        print("Region size must be an integer bigger than zero. Will set to 1 (one pixel")
        region_radius = 1

    x,y = pixel_coordinate
    box = (
        x - region_radius + 1, 
        y - region_radius + 1,
        x + region_radius,
        y + region_radius)

    return get_picture_region(picture_path, box)

def get_picture_region_by_box_offset(picture_path, pixel_coordinate, box_offset=(0,0,0,0)):
    # box: (left,upper,right,lower)
    x,y = pixel_coordinate
    box = (
        x - box_offset[0], 
        y - box_offset[1],
        x + box_offset[2],
        y + box_offset[3],
        )

    return get_picture_region(picture_path, box)

def get_picture_region(picture_path, box):
    img = Image.open(picture_path)
    region = img.crop(box)
    # region.show()
    return region

def get_median_rgb(image):
    R_list = []
    G_list = []
    B_list = []

    pix_val = list(image.getdata())

    #Store every RGB value in there corresponding list 
    for x in range(len(pix_val)):
        R = pix_val[x][0]
        R_list.append(R)
        G = pix_val[x][1]
        G_list.append(G)
        B = pix_val[x][2]
        B_list.append(B)

    #Get median of the RGB lists 
    R_list.sort()
    G_list.sort()
    B_list.sort()
    median_R = int(statistics.median(R_list))
    median_G = int(statistics.median(G_list))
    median_B = int(statistics.median(B_list))

    colour_info_dict = {
        "median_R":median_R,
        "median_G":median_G,
        "median_B":median_B,
    }
    return colour_info_dict

def get_user_path(default_folder, use_default_path=False): 
    if use_default_path:
        user_path = default_folder
    else:
        user_path = input("provide path [ENTER for: {}]: ".format(default_folder)) or default_folder
    p = Path(user_path)
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
    

    return user_path

if __name__ == "__main__":

    pictures_folder = get_user_path(DEFAULT_PICTURES_PATH, False)
    output_folder = get_user_path(DEFAULT_OUTPUT_PATH, False)

    csv_path = Path(output_folder, "results.csv")

    if csv_path.is_file():
        user_input = input("A .csv file ({}) already exists. [d] to delete, [enter] to keep and add: ".format(csv_path)) or "mohowvint"
        if user_input == "d":
            csv_path.unlink()

    urlCapture = 'http://192.168.4.1/capture'
    urlGetPicture = 'http://192.168.4.1/saved-photo'

    user_input = input("Please enter the reference pellet and press enter") or ""
    r = requests.get(urlCapture, allow_redirects=True)
    time.sleep(5)
    r = requests.get(urlGetPicture, allow_redirects=True)

    picture_path = 'reference.jpg'

    fileLocation = picture_path
    open(fileLocation, 'wb').write(r.content)
    p = Path(fileLocation)
    process_picture(picture_path, output_folder, COLOR_PICKER_SIZE, IMAGE_TAKEOUT_SIZE)

    while True:
        user_input = input("Please provide an image tag or 'r' for a new reference pellet: ") or ""

        picture_path = user_input + '.jpg'

        r = requests.get(urlCapture, allow_redirects=True)
        time.sleep(5)
        r = requests.get(urlGetPicture, allow_redirects=True)
        fileLocation = picture_path

        open(fileLocation, 'wb').write(r.content)

        p = Path(fileLocation)
        csv_line = process_picture(picture_path, output_folder, COLOR_PICKER_SIZE, IMAGE_TAKEOUT_SIZE)
        add_to_results_csv(csv_path, csv_line)


    print("Finished.")