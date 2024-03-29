import sys
sys.path.append('C:/Beadify/src')
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


    #image_recolored, beads_needed = switch_colors(image_recolored, beads_needed, 'H12', 'H18', 17,40)
    image_recolored.save('../out/image_recolored.png')
    
    colors = pd.read_csv('../src/colors.csv')
    #print(colors.head())
    
    
    for i in range(29*4):
        print("\nR"+str(i+1)+"|  ", end=' ')
        
        # First pixel in row 
        r,g,b = image_recolored.getpixel((i, 0))
        r_prev, g_prev, b_prev = r,g,b 
        count = 1        
    
        for j in range(1, 29*4-1):
            r,g,b = image_recolored.getpixel((i, j))

            if (r,g,b) == (r_prev, g_prev, b_prev):
                count += 1
            else:
                color = colors[(colors['R'] == r_prev) & (colors['G'] == g_prev) & (colors['B'] == b_prev)]["name"].values[0]
                print(str(count) + "-" + color + " ", end=' ')
                
                count = 1
    
            #if (j+1) % 29 == 0:
             #   print(" || ",end="")
        
                
            r_prev, g_prev, b_prev = r,g,b 
            
        # Edge 
        r,g,b = image_recolored.getpixel((i,29-1))
        
        if (r,g,b) == (r_prev, g_prev, b_prev):
            count += 1
            color = colors[(colors['R'] == r) & (colors['G'] == g) & (colors['B'] == b)]["name"].values[0]
            print(str(count) + "-" + color + " ", end=' ')
            
        else:
            color = colors[(colors['R'] == r_prev) & (colors['G'] == g_prev) & (colors['B'] == b_prev)]["name"].values[0]
            print(str(count) + "-" + color + " ", end=' ')
            color = colors[(colors['R'] == r) & (colors['G'] == g) & (colors['B'] == b)]["name"].values[0]
            count = 1
            print(str(count) + "-" + color + " ", end=' ')

    print(beads_needed[['name','code','quantity']].sort_values(by='quantity', ascending=False))
