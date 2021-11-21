import sys
sys.path.append('../src')
from beadify import *

def get_configuration():
    """
    Get program configuration, including
    path to the image file, pegboard dimension
    and available bead colors.
    """

    with open("../run/beads.config", 'r') as f:
        for num, line in enumerate(f, start=1):

            if line[:10] == "image_path":
                a = line.find("\"")+1
                b = line[a:].find("\"")+a
                image_path = line[a:b]
            elif line[:18] == "pegboard_dimension":
                a = line.find("(")
                pegboard_dimension = eval(line[a:])
            elif line[:11] == "bead_colors":
                a = line.find("[")
                b = line[a:].find("]")+a+1
                bead_colors = eval(line[a:b])
            elif line[:13] == "update_colors":
                a = line.find("=")+1
                update_colors = eval(line[a:])

    return image_path, pegboard_dimension, bead_colors, update_colors

if __name__ == "__main__":

    image_path, pegboard_dimension, available_colors, update = get_configuration()

    if update:
        update_colors(available_colors)

    image_resized = change_resolution(image_path, pegboard_dimension)
    image_resized.save('../out/image_resized.png')

    image_recolored, beads_needed = change_colors(image_resized, pegboard_dimension)
    image_recolored.save('../out/image_recolored.png')

    image_color_switch, beads_needed = switch_colors(image_recolored, beads_needed, 'H76', 'H75')
    image_color_switch.save('../out/image_color_switch.png')

    print(beads_needed[['name','code','quantity']].sort_values(by='quantity', ascending=False))
