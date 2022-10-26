import image_gen_pygame as image_gen
import pygame

display = pygame.display.set_mode((10, 10), pygame.SRCALPHA, 32)

drivers = []
from_file = True
drivers_only = True
oneatatime = True
background = True
round_num = 1
game = 'F1'

if from_file:
    with open("grid.txt", 'r') as f:
        ff = iter(f.readlines())

while True:
    if from_file:
        driver = next(ff, '-1').replace("\n", "")
    else:
        driver = input("Enter driver name or IGN: ")
    if driver == '-1':
        break
    if driver in image_gen.driver_data:
        drivers.append(driver)
    else:
        got = False
        for key, values in image_gen.driver_data.items():
            if values["F1"]["ign"].lower() == driver.lower():
                drivers.append(key)
                got = True
                break
        if not got:
            print(f"Could not find {driver}, please try again")

if drivers_only:
    img = image_gen.create_image(background=True, round_num=round_num, game=game, grid=False, drivers=False)
    pygame.image.save(img, "output/background.png")
    background = False
    round_num = None
    grid = False
    for j in [i for i in list(range(1, len(drivers)+1))[::8]]:  # gets lowest pos in grid sequences, enough for grid
        img = image_gen.create_image(background=background, round_num=round_num, game=game, driver_l=drivers[j-1],
                                     grid=True, fullgrid=drivers, drivers=False)
        pygame.image.save(img, f"output/grid {j}-.png")

driver_l, driver_r = None, None
lr = 'left'
first = True
for i in range(len(drivers)-1):  # I fucking hate how all this works but shit happens
    if not first:
        if lr == 'left':
            driver_l = drivers[i+1]
        elif lr == 'right':
            driver_r = drivers[i+1]

    else:
        driver_l = drivers[i]
        driver_r = drivers[i+1]

    if not oneatatime:
        img = image_gen.create_image(background=background, round_num=round_num, game=game, driver_l=driver_l,
                                     driver_r=driver_r, fullgrid=drivers, drivers_only=drivers_only)
        pygame.image.save(img, f"output/{i+1}-{i+2}.png")

    else:
        if first:
            img = image_gen.create_image(background=background, round_num=round_num, game=game, driver_l=driver_l,
                                         driver_r=None, fullgrid=drivers, drivers_only=drivers_only)
            pygame.image.save(img, f"output/{i+1}.png")
            img = image_gen.create_image(background=background, round_num=round_num, game=game, driver_l=None,
                                         driver_r=driver_r, fullgrid=drivers, drivers_only=drivers_only)
            pygame.image.save(img, f"output/{i+2}.png")

        else:
            if lr == 'left':
                img = image_gen.create_image(background=background, round_num=round_num, game=game, driver_l=driver_l,
                                             driver_r=None, fullgrid=drivers, drivers_only=drivers_only)
                pygame.image.save(img, f"output/{i+2}.png")

            elif lr == 'right':
                img = image_gen.create_image(background=background, round_num=round_num, game=game, driver_l=None,
                                             driver_r=driver_r, fullgrid=drivers, drivers_only=drivers_only)
                pygame.image.save(img, f"output/{i+2}.png")

    if not first:
        if lr == 'left':
            lr = 'right'
        elif lr == 'right':
            lr = 'left'

    first = False
