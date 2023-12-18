from PIL import Image
import numpy as np
import pandas as pd
from tqdm import tqdm

def update_colors(available_colors, all=False):
    """
    Update the availble status of colors
    based on input from the config file.
    """

    colors = pd.read_csv('../src/colors.csv')

    if all:
        available = np.ones(len(colors), dtype=np.int8)

    else:
        available = np.zeros(len(colors), dtype=np.int8)
        possible_colors = colors['code']

        for i, color in enumerate(possible_colors):
            if color in available_colors:
                available[i] = 1


    colors['available'] = available
    colors.to_csv('../src/colors.csv', index=False)

    return None

def change_resolution(image_path, pegboard_dimension):
    """
    Change resolution of photo according to
    pegboard dimension, and convert to RGB values.
    """
    image = Image.open(image_path)
    image = image.resize(pegboard_dimension, Image.BILINEAR)
    image.convert("RGB")
    return image

def change_colors(image, pegboard_dimension, method='perception'):
    """
    Change RGB values to closest available bead colors.
    """

    colors = pd.read_csv('../src/colors.csv')
    colors = colors[colors['available'] == 1].reset_index()
    R = colors['R']
    G = colors['G']
    B = colors['B']

    number_needed = np.zeros(len(colors))

    nx, ny = pegboard_dimension
    new_RGB = []

    for i in tqdm(range(nx)):
        for j in range(ny):

            pixel = np.asarray(image.getpixel((i,j)))

            min = float('inf')
            closest_RGB = None
            cc = None

            for c in range(len(colors)):

                if method == 'euclidean':
                    dist = (R[c] - pixel[0])**2 +\
                           (G[c] - pixel[1])**2 +\
                           (B[c] - pixel[2])**2

                elif method == 'perception':
                    dist = ((R[c] - pixel[0])*0.30)**2 +\
                           ((G[c] - pixel[1])*0.59)**2 +\
                           ((B[c] - pixel[2])*0.11)**2

                if dist < min:
                    min = dist
                    closest_RGB = (R[c], G[c], B[c])
                    cc = c

            new_RGB.append(closest_RGB)
            number_needed[cc] += 1

    beads_needed = colors
    beads_needed['quantity'] = number_needed

    image_recolored = Image.new(image.mode,image.size)
    image_recolored.putdata(new_RGB)
    image_recolored = image_recolored.rotate(-90)
	
	
    return image_recolored, beads_needed

def switch_colors(image, beads_needed, col, new_col):

    colors = pd.read_csv('../src/colors.csv')
    color = colors[colors['code'] == col].reset_index()
    new_color = colors[colors['code'] == new_col].reset_index()

    q = beads_needed[beads_needed['code']==col]['quantity'].values[0]
    q2 = beads_needed[beads_needed['code']==new_col]['quantity'].values[0]

    beads_needed.loc[beads_needed['code']==col, 'quantity'] = 0
    beads_needed.loc[beads_needed['code']==new_col, 'quantity'] = q + q2

    data = np.array(image)
    red, green, blue = data.T
    
    area = (red == color['R'][0]) & (green == color['G'][0]) & (blue == color['B'][0])

    #print(data.shape); exit()
    data[area.T] = (new_color['R'][0], new_color['G'][0], new_color['B'][0]) # Transpose back needed

    image = Image.fromarray(data)
    return image, beads_needed
