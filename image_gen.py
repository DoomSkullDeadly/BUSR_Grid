from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from math import ceil, floor
import json
import os


def load_driver_data():
    """Loads driver data"""
    with open(r"resources/driver_data.json", 'r') as f:
        ff = json.loads(f.read())
    return ff


def save_driver_data(data: dict):
    """Saves driver data"""
    with open(r"resources/driver_data.json", 'w') as f:
        f.write(json.dumps(data, indent=4))


def load_paths():
    """Loads resource paths"""
    with open(r"resources/paths.json", 'r') as f:
        ff = json.loads(f.read())
        return ff


def save_paths(data: dict):
    """Saves resource paths"""
    with open(r"resources/paths.json", 'w') as f:
        f.write(json.dumps(data, indent=4))


def load_settings():
    """Loads image settings"""
    with open(r"resources/image_settings.json", 'r') as f:
        ff = json.loads(f.read())
        return ff


def save_settings(data: dict):
    """Saves image settings"""
    with open(r"resources/image_settings.json", 'w') as f:
        f.write(json.dumps(data, indent=4))


def write_text(text: str, colour, size: int):  # TODO make all this work in pygame instead
    """Writes text centered at position given, in colour and size"""
    lines = text.split('\n')  # splits multiline text into lines
    font = ImageFont.truetype("resources/Akira Expanded Demo.otf", size * 4)  # sets up font for work, 4x size for AA
    text_h = sum([ImageFont.truetype("resources/Akira Expanded Demo.otf", size).getsize(line)[1] for line in lines])
    text_w = max([ImageFont.truetype("resources/Akira Expanded Demo.otf", size).getsize(line)[0] for line in lines])
    text_image = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_image)

    text_size = text_image.size
    y_pos = 0
    for line in lines:
        line_size = ImageFont.truetype("resources/Akira Expanded Demo.otf", size).getsize(line)
        x_pos = 0
        for char in line:
            w, h = draw.textsize(text=char, font=font)  # gets size of text
            img = Image.new("RGBA", (w, h), (0, 0, 0, 0))  # makes new image in text size to write text
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), char, tuple(colour), font=font)
            resized_img = img.resize((int(w / 4), int(h / 4)), Image.ANTIALIAS)  # resizes image to antialiase text
            char_pos = (int((text_size[0] / 2) - (line_size[0] / 2) + x_pos), int(y_pos))
            text_image.paste(resized_img, box=char_pos)
            x_pos += ImageFont.truetype("resources/Akira Expanded Demo.otf", size).getsize(char)[0]
        y_pos += line_size[1]

    if len(lines) > 1:
        return text_image, ImageFont.truetype("resources/Akira Expanded Demo.otf", size).getsize(lines[0])[1]

    else:
        return text_image


def get_short_name(name: str):  # it is stupid but it works maybe lol
    name_splits = len(name.split(" "))
    if len(name.split(" ")[1]) > 2 and name_splits == 2:
        if name.split(" ")[1].isalpha():
            short_name = name.split(" ")[1][:3]
            return short_name.upper()
        else:
            short_name = ""
            for i in name.split(" ")[1]:
                if len(short_name) < 3:
                    if i.isalpha():
                        short_name += i
                else:
                    return short_name.upper()
            if name_splits == 2 and len(short_name) < 3:
                return short_name.upper()

    else:
        short_name = ""
        if name_splits > 2:
            for i in [split for splits in name.split(" ")[1:] for split in splits]:  # took a while to work out how work
                if len(short_name) < 3:
                    if i.isalpha():
                        short_name += i
                else:
                    return short_name.upper()
            return short_name.upper()
        else:
            for i in name.split(" ")[1]:
                if i.isalpha():
                    short_name += i
            return short_name.upper()


def create_image(background: bool = True, round_num: int = None, game: str = None, driver_l: str = None,
                 driver_r: str = None, grid: bool = True, fullgrid: list = None, drivers: bool = True,
                 drivers_only: bool = False):
    """Creates image, using what is given"""

    global driver_data  # makes loaded settings global
    global settings
    global paths

    img = Image.new("RGBA", (2560, 1440))  # makes image to work on

    """BACKGROUND"""

    if background:  # puts background in if needed
        img_back = Image.open(paths[game]["background"])
        img.paste(img_back)
        if round_num:  # adds round number if given
            name_txt = write_text(str(f"round {round_num}"), colour=settings["Round Num"]["colour"],
                                  size=settings["Round Num"]["font size"])
            txt_center = settings["Round Num"]["center"]
            w, h = name_txt.size
            txt_pos = int(txt_center[0] - (w / 2)), int(txt_center[1] - (h / 2))
            img.paste(name_txt, box=txt_pos)

    """GRID"""

    if grid and fullgrid and not drivers_only:  # creates grid, if needed
        l_pos, r_pos = 0, 0
        if driver_l:
            l_pos = fullgrid.index(driver_l) + 1
        if driver_r:
            r_pos = fullgrid.index(driver_r) + 1
        grid_max = max(l_pos, r_pos)  # gets the highest grid position
        if grid_max % 8 != 0:  # chooses which method to use to calculate grid range
            range_min = floor(grid_max / 8) * 8 + 1  # finds minimum grid position
            range_max = ceil(grid_max / 8) * 8  # finds maximum grid position
        else:
            range_min = grid_max - 7
            range_max = grid_max

        if len(fullgrid) < range_max:  # makes sure grid does not extend past last place
            range_max = len(fullgrid)
        grid_range = [i for i in range(range_min, range_max + 1)]  # creates range to be used

        with Image.open(paths["starting grid"]) as im:  # pastes starting grid text
            img.paste(im)

        with Image.open(paths["bracket"]) as im:  # creates grid
            bw, bh = im.size  # gets size of bracket image
            for pos in grid_range:
                if pos % 8 != 0:
                    bracket_pos = settings["Grid"][f"bracket pos {pos % 8}"]  # gets the correct bracket from pos
                else:
                    bracket_pos = settings["Grid"][f"bracket pos {8}"]
                num_txt = write_text(text=str(pos), colour=settings["Grid"]["num colour"],
                                     size=settings["Grid"]["num font size"])
                nw, nh = num_txt.size  # gets size of text image
                num_pos = (int(bracket_pos[0] + (bw / 2) - (nw / 2)),  # gets top left position of number text
                           int(bracket_pos[1] + settings["Grid"]["num y offset"] - nh))

                short_name = get_short_name(fullgrid[pos - 1])
                name_text = write_text(text=short_name, colour=settings["Grid"]["name colour"],
                                       size=settings["Grid"]["name font size"])
                nnw, nnh = name_text.size
                name_pos = (int(bracket_pos[0] + (bw / 2) - (nnw / 2)),  # gets top left position of name text
                            int(bracket_pos[1] + settings["Grid"]["name y offset"]))

                img.paste(im, box=bracket_pos)  # pastes bracket, number, and name
                img.paste(num_txt, box=num_pos)
                img.paste(name_text, box=name_pos)

    """DRIVERS"""

    if (driver_l or driver_r) and drivers:
        if driver_l and driver_r:  # if both drivers given, does them in one loop by switching acting side
            drivers = driver_l, driver_r
            lr = 'left'
        else:  # if only one driver given, decides which side to act on, must still go through loop but only once
            if driver_l:
                drivers = [driver_l]
                lr = 'left'
            else:
                drivers = [driver_r]
                lr = 'right'

        for driver in drivers:  # main loop
            uni = driver_data[driver]["uni"]  # gets uni information
            uni_logo_center = settings["Logos"]["Uni"][f"{lr} center"]
            uni_topline_center = settings["Drivers"]["Uni"][f"{lr} topline center"]

            if "Alumni" in driver_data[driver]:
                uni += " (Alumni)"

            if (len(uni.split(" ")) > 1 and len(uni) > 10) or "(Alumni)" in uni:  # painful things, wraps uni text
                if len(uni.split(" ")) > 1 and len(uni) > 10:
                    uni_ = uni.replace(" ", '\n', 1)
                else:
                    uni_ = uni
                uni_text, sep = write_text(text=uni_.replace(" (Alumni)", '\n(Alumni)'),
                                           colour=settings["Drivers"]["Uni"]["colour"],
                                           size=settings["Drivers"]["Uni"]["font size"])
                text_pos_y = int(uni_topline_center[1] - sep/2)
                text_pos_x = int(uni_topline_center[0] - (uni_text.size[0] / 2))
                pos = text_pos_x, text_pos_y
                img.paste(uni_text, box=pos)

            else:  # nice(r) things.
                uni_text = write_text(text=uni, colour=settings["Drivers"]["Uni"]["colour"],
                                      size=settings["Drivers"]["Uni"]["font size"])
                pos = (int(uni_topline_center[0] - (uni_text.size[0] / 2)),
                       int(uni_topline_center[1] - (uni_text.size[1] / 2)))
                img.paste(uni_text, box=pos)

            if "(Alumni)" in uni and driver in [f.replace('.png', '') for f in os.listdir(paths["Alumni"])]:
                uni_logo = Image.open(paths["Alumni"] + driver + ".png")  # gets personal logo if available
            else:
                uni = uni.replace(" (Alumni)", "")  # gets uni logo if not Alumni or personal is not available
                uni_logo = Image.open(paths["Universities"][uni])
            w, h = uni_logo.size
            uni_logo_pos = (int(uni_logo_center[0] - (w / 2)), int(uni_logo_center[1] - (h / 2)))
            img.paste(uni_logo, box=uni_logo_pos)

            car = driver_data[driver][game]["car"]
            car_logo_center = settings["Logos"]["Car"][f"{lr} center"]
            car_logo = Image.open(paths[game]["cars"] + car + '.png')  # I hate this line
            w, h = car_logo.size
            car_logo_pos = (int(car_logo_center[0] - (w / 2)), int(car_logo_center[1] - (h / 2)))
            img.paste(car_logo, box=car_logo_pos)

            driver_text, sep = write_text(text=driver.replace(" ", '\n', 1).replace("-", '\n'),  # splits names
                                          colour=settings["Drivers"]["Name"]["colour"],
                                          size=settings["Drivers"]["Name"]["font size"])
            driver_topline_center = settings["Drivers"]["Name"][f"{lr} topline center"]
            text_pos_y = int(driver_topline_center[1] - sep/2)
            text_pos_x = int(driver_topline_center[0] - (driver_text.size[0] / 2))
            pos = text_pos_x, text_pos_y
            img.paste(driver_text, box=pos)

            q_pos = str(fullgrid.index(driver) + 1)  # finds driver's qualifying position
            q_end = ''
            if int(q_pos[-1]) in range(1, 4) and ((len(q_pos) == 2 and q_pos[-2] != '1') or len(q_pos) != 2):
                if q_pos[-1] == '1':  # only gives st, nd, rd if not in the teens
                    q_end = 'st'
                elif q_pos[-1] == '2':
                    q_end = 'nd'
                elif q_pos[-1] == '3':
                    q_end = 'rd'
            else:
                q_end = 'th'
            q_text = write_text(text=q_pos + q_end, colour=settings["Drivers"]["Grid Position"]["colour"],
                                size=settings["Drivers"]["Grid Position"]["font size"])
            q_text_center = settings["Drivers"]["Grid Position"][f"{lr} topline center"]
            q_text_pos = (int(q_text_center[0] - (q_text.size[0] / 2)), int(q_text_center[1] - (q_text.size[1] / 2)))
            img.paste(q_text, box=q_text_pos)

            lr = 'right'

    return img


driver_data = load_driver_data()
settings = load_settings()
paths = load_paths()
# create_image()
