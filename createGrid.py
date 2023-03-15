import math, itertools, sys
import pandas as pd
import ezdxf




def help():
    print("Text file format:  id,x,y,H")
    print("e.g:\n1,500650.590,4204238.460,351.234\n2,500650.920,4204252.530,350.582")
    print("\nFor scale e.g 1/200 use 200 as scale")
    print("\nExecution:\npython createGrid.py scale coords_filename")
    print("e.g:\npython createGrid.py 200 coords.txt")


def add_crosshair(df, block, crosshair, min_x, min_y, max_x, max_y):

    if df['x'] == min_x and df['y'] == min_y:
        block.add_text(df['x'], dxfattribs= {
            "layer": "grid",
            "style": "Arial",
            "height": 0.3 }).set_pos((df['x'] - 0.2, df['y'] - 0.6), align= "LEFT")
        
        block.add_text(df['y'], dxfattribs= {
            "layer": "grid",
            "style": "Arial",
            "rotation": 90,
            "height": 0.3 }).set_pos((df['x'] - 0.3, df['y'] - 0.2), align= "LEFT")

    elif df['x'] == max_x and df['y'] == min_y:
        block.add_text(df['x'], dxfattribs= {
            "layer": "grid",
            "style": "Arial",
            "height": 0.3 }).set_pos((df['x'] + 0.2, df['y'] - 0.6), align= "RIGHT")
        
        block.add_text(df['y'], dxfattribs= {
            "layer": "grid",
            "style": "Arial",
            "rotation": -90,
            "height": 0.3 }).set_pos((df['x'] + 0.3, df['y'] - 0.2), align= "RIGHT")
    
    elif df['x'] == max_x and df['y'] == max_y:
        block.add_text(df['x'], dxfattribs= {
            "layer": "grid",
            "style": "Arial",
            "height": 0.3 }).set_pos((df['x'] + 0.2, df['y'] + 0.3), align= "RIGHT")
        
        block.add_text(df['y'], dxfattribs= {
            "layer": "grid",
            "style": "Arial",
            "rotation": -90,
            "height": 0.3 }).set_pos((df['x'] + 0.3, df['y'] + 0.2), align= "LEFT")
    
    elif df['x'] == min_x and df['y'] == max_y:
        block.add_text(df['x'], dxfattribs= {
            "layer": "grid",
            "style": "Arial",
            "height": 0.3 }).set_pos((df['x'] - 0.2, df['y'] + 0.3), align= "LEFT")
        
        block.add_text(df['y'], dxfattribs= {
            "layer": "grid",
            "style": "Arial",
            "rotation": 90,
            "height": 0.3 }).set_pos((df['x'] - 0.3, df['y'] + 0.2), align= "RIGHT")
    
    elif df['y'] == min_y:
        block.add_text(df['x'], dxfattribs= {
            "layer": "grid",
            "style": "Arial",
            "height": 0.3 }).set_pos((df['x'], df['y'] - 0.6), align= "CENTER")
        
        block.add_lwpolyline([(df['x'], df['y']), (df['x'], df['y'] + crosshair/2)])
    
    elif df['y'] == max_y:
        block.add_text(df['x'], dxfattribs= {
            "layer": "grid",
            "style": "Arial",
            "height": 0.3 }).set_pos((df['x'], df['y'] + 0.3), align= "CENTER")
        
        block.add_lwpolyline([(df['x'], df['y']), (df['x'], df['y'] - crosshair/2)])
    
    elif df['x'] == min_x:
        block.add_text(df['y'], dxfattribs= {
            "layer": "grid",
            "style": "Arial",
            "rotation": 90,
            "height": 0.3 }).set_pos((df['x'] - 0.3, df['y']), align= "CENTER")
        
        block.add_lwpolyline([(df['x'], df['y']), (df['x'] + crosshair/2, df['y'])])
    
    elif df['x'] == max_x:
        block.add_text(df['y'], dxfattribs= {
            "layer": "grid",
            "style": "Arial",
            "rotation": -90,
            "height": 0.3 }).set_pos((df['x'] + 0.3, df['y']), align= "CENTER")
        
        block.add_lwpolyline([(df['x'], df['y']), (df['x'] - crosshair/2, df['y'])])

    else:
        block.add_lwpolyline([(df['x']-crosshair/2, df['y']), (df['x'], df['y']), (df['x'], df['y'] - crosshair/2),
                            (df['x'], df['y'] + crosshair/2), (df['x'], df['y']), (df['x'] + crosshair/2, df['y'])])





def create_grid(input_filename, scale):
    factor = 10 # grid 10cm x 10 cm
    pace = int(scale / factor) # 20m
    # crosshair = 2 * scale / 1000
    crosshair = 4 * scale / 1000

    data = pd.read_csv(input_filename, header= None, names= ["id", "x", "y", "h"])

    # min_x = data['x'].min() - pace
    # min_y = data['y'].min() - pace
    # max_x = data['x'].max() + pace
    # max_y = data['y'].max() + pace

    # min_x = int(math.floor(min_x / pace)) * pace
    # min_y = int(math.floor(min_y / pace)) * pace
    # max_x = int(math.ceil(max_x / pace)) * pace
    # max_y = int(math.ceil(max_y / pace)) * pace

    min_x = data['x'].min()
    min_y = data['y'].min()
    max_x = data['x'].max()
    max_y = data['y'].max()

    half_pace = int(0.5 * pace)

    min_x = int(math.floor(min_x / pace)) * pace - half_pace
    min_y = int(math.floor(min_y / pace)) * pace - half_pace
    max_x = int(math.ceil(max_x / pace)) * pace + half_pace
    max_y = int(math.ceil(max_y / pace)) * pace + half_pace

    # grid_points = list(itertools.product(range(min_x, max_x + pace, pace), range(min_y, max_y + pace, pace)))
    grid_points = list(itertools.product(range(min_x, max_x + half_pace, pace), range(min_y, max_y + half_pace, pace)))
    grid_points_dict = {"x": [point[0] for point in grid_points], "y": [point[1] for point in grid_points]}
    grid_df = pd.DataFrame(grid_points_dict)

    corners = [(min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y), (min_x, min_y)]
    # corners_outer = [(min_x - 1, min_y - 1), (min_x - 1, max_y + 1), (max_x + 1, max_y + 1), (max_x + 1, min_y - 1), (min_x - 1, min_y - 1)]
    corners_outer = [(min_x - 0.8, min_y - 0.8), (min_x - 0.8, max_y + 0.8), (max_x + 0.8, max_y + 0.8), (max_x + 0.8, min_y - 0.8), (min_x - 0.8, min_y - 0.8)]

    doc = ezdxf.new(dxfversion= "R2010")  
    doc.styles.new("Arial", dxfattribs={"font": "arial.ttf"})
    msp = doc.modelspace()
    doc.layers.new("grid", dxfattribs= {"color": 7}) 

    blockname = "grid_block"
    block = doc.blocks.new(name= blockname, base_point= (min_x, min_y))
    msp.add_blockref(blockname, (min_x, min_y), dxfattribs= {"layer": "grid"})

    block.add_lwpolyline(corners)
    block.add_lwpolyline(corners_outer)

    grid_df.apply(add_crosshair, axis= 1, args= [block, crosshair, min_x, min_y, max_x, max_y])

    doc.saveas(f"grid_{scale}.dxf", encoding="utf-8")
    print("Grid done!")


def main():
    arg1 = sys.argv[1]
    
    if arg1 == "help" or arg1 == "--h" or arg1 == "-h":
        help()
    else:
        scale = int(arg1)
        input_filename = sys.argv[2]
        create_grid(input_filename, scale)

if __name__ == "__main__":
    main()

